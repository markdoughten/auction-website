import { Component, EventEmitter, OnInit, Output } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  Validators,
  FormControl,
  FormsModule,
  ReactiveFormsModule,
} from "@angular/forms";
import { NgIf, NgFor } from "@angular/common";
import { IS_REQUIRED, SERVER_URLS } from "@core/constants";
import { HttpClient } from "@angular/common/http";
import { LoadingService } from "@core/loading.service";
import { check_duplicate } from "@core/form_validator";

@Component({
  selector: "app-item-form",
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, NgIf, NgFor],
  templateUrl: "./itemform.component.html",
})
export class ItemFormComponent implements OnInit {
  readonly IS_REQUIRED: string = IS_REQUIRED;
  readonly DUPLICATE: string = "Name already found, try again.";
  itemForm: FormGroup;
  response: any = {};
  meta_items: any = undefined;
  categories: string[] = [];
  subcategories: string[] = [];
  attributes: string[] = [];
  duplicate: number = 0;
  @Output() success = new EventEmitter<any>();

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private loading: LoadingService,
  ) {
    this.itemForm = this.fb.group({
      name: ["", [Validators.required, check_duplicate(this)]],
      category: ["", Validators.required],
      subcategory: ["", Validators.required],
      attributes: this.fb.group({
        attribute: new FormControl("", Validators.required),
      }),
    });
    this.get_meta();
  }

  get_meta() {
    this.http.get(SERVER_URLS.get_meta_items).subscribe({
      next: (response: any) => {
        this.response = response;
        this.meta_items = {};
        for (let categIndex in response) {
          const categName = response[categIndex].categoryName;
          this.categories = [...this.categories, categName];
          let categories: { [key: string]: any } = {};
          const subCategs = response[categIndex].subcategories;
          let subcategories = [];
          for (let subIndex in subCategs) {
            const subCateg = subCategs[subIndex].subcategoryName;
            subcategories.push(subCateg);
            const attrs = subCategs[subIndex].attributes;
            let attributes = [];
            for (let attrIndex in attrs) {
              attributes.push(attrs[attrIndex].attributeName);
            }
            categories[subCateg] = attributes;
          }
          categories["subcategories"] = subcategories;
          this.meta_items[categName] = categories;
        }
        this.itemForm.get("category")?.setValue(this.categories[0]);
        this.onCategoryChange();
      },
      error: (error) => {
        alert(`Some error occurred!! ${error.error.message}`);
      },
    });
  }

  ngOnInit(): void {}

  onCategoryChange(): void {
    const category = this.itemForm.get("category")?.value;
    this.subcategories = this.meta_items[category]["subcategories"] || [];
    this.itemForm.get("subcategory")?.setValue(this.subcategories[0]);
    this.onSubcategoryChange();
  }

  onSubcategoryChange(): void {
    const category = this.itemForm.get("category")?.value;
    const subcategory = this.itemForm.get("subcategory")?.value;
    this.attributes = subcategory ? this.meta_items[category][subcategory] : [];
    const attributesGroup: any = {};
    this.attributes.forEach((attr, index) => {
      attributesGroup[attr] = new FormControl("", Validators.required);
    });
    this.itemForm.setControl("attributes", this.fb.group(attributesGroup));
  }

  processForm() {
    const category = this.itemForm.get("category")?.value;
    const subcategory = this.itemForm.get("subcategory")?.value;
    let output: { [key: string]: any } = {};
    for (let ci in this.response) {
      if (this.response[ci].categoryName !== category) {
        continue;
      }
      output["categoryId"] = this.response[ci].id;
      const subcategs = this.response[ci].subcategories;
      for (let sci in subcategs) {
        if (subcategs[sci].subcategoryName !== subcategory) {
          continue;
        }
        output["subcategoryId"] = subcategs[sci].id;
        const attrs = subcategs[sci].attributes;
        let out_attrs = [];
        for (let ai in attrs) {
          let id = attrs[ai].id;
          let value = this.itemForm
            .get("attributes")
            ?.get(attrs[ai].attributeName)?.value;
          let curr_attr = {
            attributeId: id,
            attributeValue: value,
          };
          out_attrs.push(curr_attr);
        }
        output["attributes"] = out_attrs;
        output["name"] = this.itemForm.get("name")?.value;
        break;
      }
      break;
    }
    return output;
  }

  onSubmit(): void {
    const iFrm = this.itemForm;
    let is_invalid = false;
    Object.keys(iFrm.controls).forEach((field) => {
      if (iFrm.get(field)?.errors != null) {
        is_invalid = true;
        return;
      }
    });

    if (is_invalid) {
      iFrm.markAllAsTouched();
      return;
    }

    const data = this.processForm();
    if (Object.keys(data).length < 4) {
      iFrm.markAllAsTouched();
      return;
    }
    this.loading.show();
    this.http.post(SERVER_URLS.items, data).subscribe({
      next: (response: any) => {
        this.loading.hide();
        this.success.emit(response);
      },
      error: (error) => {
        this.duplicate = 1;
        iFrm.markAllAsTouched();
        iFrm.get("name")?.updateValueAndValidity();
        this.loading.hide();
        console.log();
      },
    });
  }
}
