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
import {
  _ATTR,
  _ID,
  MetaAttributes,
  MetaCategory,
  MetaItems,
  MetaSubCategory,
} from "@model/items";

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
  meta_items: MetaItems = {};
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
        for (let cIdx in response) {
          let category: MetaCategory = {};
          let subcategories = [];
          const categ = response[cIdx];
          const subCategs = categ.subcategories;
          this.categories.push(categ.categoryName);
          category[_ID] = categ.id;
          for (let sIdx in subCategs) {
            let subCategory: MetaSubCategory = {};
            let attributes = [];
            const subCateg = subCategs[sIdx];
            subCategory[_ID] = subCateg.id;
            subcategories.push(subCateg.subcategoryName);
            const attrs = subCateg.attributes;
            for (let aIdx in attrs) {
              let attrName = attrs[aIdx].attributeName;
              let attrId = attrs[aIdx].id;
              attributes.push(attrName);
              let metaAttr: MetaAttributes = {};
              metaAttr[_ID] = attrId;
              subCategory[attrName] = metaAttr;
            }
            subCategory[_ATTR] = attributes;
            category[subCateg.subcategoryName] = subCategory;
          }
          category[_ATTR] = subcategories;
          this.meta_items[categ.categoryName] = category;
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

  getCateg(): any {
    const categ = this.itemForm.get("category")?.value;
    if (categ === null) {
      return null;
    }

    return this.meta_items[categ] || null;
  }

  getSubCateg(metaCateg: any): any {
    const sub = this.itemForm.get("subcategory")?.value;
    if (sub === null) {
      return null;
    }

    return metaCateg[sub] || null;
  }

  onCategoryChange(): void {
    const metaCateg: any = this.getCateg();
    this.subcategories = metaCateg[_ATTR] || [];
    this.itemForm.get("subcategory")?.setValue(this.subcategories[0]);
    this.onSubcategoryChange();
  }

  onSubcategoryChange(): void {
    const metaSub: any = this.getSubCateg(this.getCateg());
    this.attributes = metaSub[_ATTR] || [];
    const attributesGroup: any = {};
    this.attributes.forEach((attr, index) => {
      attributesGroup[attr] = new FormControl("", Validators.required);
    });
    this.itemForm.setControl("attributes", this.fb.group(attributesGroup));
  }

  processForm(metaCateg: any, metaSub: any): any {
    let out_attrs = [];
    for (let attr of metaSub[_ATTR]) {
      const value = this.itemForm.get("attributes")?.get(attr)?.value;
      if (value) {
        out_attrs.push({
          attributeId: metaSub[attr][_ID],
          attributeValue: this.itemForm.get("attributes")?.get(attr)?.value,
        });
      }
    }
    return {
      categoryId: metaCateg[_ID],
      subcategoryId: metaSub[_ID],
      attributes: out_attrs,
      name: this.itemForm.get("name")?.value,
    };
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

    const metaCateg: any = this.getCateg();
    const metaSub: any = this.getSubCateg(metaCateg);
    const data = this.processForm(metaCateg, metaSub);
    if (
      Object.keys(data).length < 4 ||
      data.attributes.length < metaSub[_ATTR].length
    ) {
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
