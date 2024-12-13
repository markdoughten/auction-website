import { Component, Input, OnInit } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  Validators,
  FormsModule,
  ReactiveFormsModule,
} from "@angular/forms";
import { NgIf, NgFor } from "@angular/common";
import { IS_REQUIRED, SERVER_URLS } from "@core/constants";
import { isValidTime, isValidClose } from "@core/form_validator";
import { AuthService } from "@core/auth.service";
import { LoadingService } from "@core/loading.service";
import { HttpClient } from "@angular/common/http";
import { Router } from "@angular/router";

@Component({
  selector: "app-auction-form",
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, NgIf, NgFor],
  templateUrl: "./auctionform.component.html",
})
export class AuctionFormComponent implements OnInit {
  readonly IS_REQUIRED: string = IS_REQUIRED;
  readonly INVALID_PRICE: string = "Minimum value should be above 0";
  readonly today = new Date();
  readonly tzoffset = new Date().getTimezoneOffset() * 60000;
  protected minDate: any = { date: new Date(), str: "" };
  protected maxDate: any = { date: new Date(), str: "" };
  protected openDate: any = undefined;
  itemForm: FormGroup;
  @Input() itemDetails: any = undefined;
  @Input() auctionDetails: any = undefined;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private loading: LoadingService,
    private http: HttpClient,
    private router: Router,
  ) {
    this.itemForm = this.fb.group({
      itemId: ["", Validators.required],
      sellerId: ["", Validators.required],
      itemName: ["", Validators.required],
      openingTime: ["", [Validators.required]],
      closingTime: [
        "",
        [Validators.required, isValidTime(this), isValidClose(this)],
      ],
      initialPrice: ["", [Validators.required, Validators.min(0)]],
      minPrice: ["", [Validators.required, Validators.min(0)]],
      minIncrement: ["", [Validators.required, Validators.min(0)]],
    });
  }

  ngOnInit(): void {
    const minDate = new Date(this.today.getTime() - this.tzoffset);
    this.minDate.date = minDate;
    this.minDate.str = minDate.toISOString().split("T")[0];
    const maxDate = new Date(this.today.getTime() - this.tzoffset);
    maxDate.setDate(maxDate.getDate() + 30);
    this.maxDate.date = maxDate;
    this.maxDate.str = maxDate.toISOString().split("T")[0];
    this.populateForm();
  }

  populateForm() {
    if (this.itemDetails !== undefined) {
      this.itemForm.get("itemName")?.setValue(this.itemDetails.name);
      this.itemForm.get("itemId")?.setValue(this.itemDetails.id);
      this.itemForm.controls["itemName"].disable();
      this.itemForm.get("sellerId")?.setValue(this.auth.user.id);
      this.itemForm
        .get("openingTime")
        ?.setValidators([Validators.required, isValidTime(this)]);
      this.itemForm.get("openingTime")?.updateValueAndValidity();
    } else {
      this.itemForm
        .get("itemName")
        ?.setValue(this.auctionDetails.seller.username);
      this.itemForm.get("itemId")?.setValue(this.auctionDetails.itemId);
      this.itemForm.get("minPrice")?.setValue(this.auctionDetails.minPrice);
      this.itemForm
        .get("minIncrement")
        ?.setValue(this.auctionDetails.minIncrement);
      this.itemForm
        .get("initialPrice")
        ?.setValue(this.auctionDetails.initialPrice);
      let time = new Date(this.auctionDetails.openingTime);
      this.openDate = time.toISOString().split("T")[0];
      this.itemForm.get("openingTime")?.setValue(this.openDate);
      time = new Date(this.auctionDetails.closingTime);
      this.itemForm
        .get("closingTime")
        ?.setValue(time.toISOString().split("T")[0]);
      this.itemForm.get("sellerId")?.setValue(this.auctionDetails.sellerId);
      this.itemForm.controls["itemName"].disable();
      this.itemForm.controls["openingTime"].disable();
    }
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
    this.loading.show();
    if (this.itemDetails === undefined) {
      this.itemForm.controls["openingTime"].enable();
      this.itemForm.get("openingTime")?.setValue(this.openDate);
    }
    this.http
      .request(
        this.itemDetails !== undefined ? "POST" : "PUT",
        SERVER_URLS.auctions,
        { body: iFrm.value, responseType: "json" },
      )
      .subscribe({
        next: (response: any) => {
          alert(
            this.itemDetails === undefined
              ? "Auction Item has been updated successfully!"
              : "Auction Item has been added successfully!",
          );
          this.router.navigate(["/"]);
        },
        error: (error) => {
          if (this.itemDetails === undefined) {
            this.itemForm.controls["openingTime"].disable();
          }
          console.log(error);
          this.loading.hide();
        },
      });
  }
}
