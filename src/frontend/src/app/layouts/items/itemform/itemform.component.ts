import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { IS_REQUIRED } from "@core/constants";

@Component({
  selector: "app-newitem",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./itemform.component.html",
})
export class ItemFormComponent {
  itemForm: FormGroup;
  readonly IS_REQUIRED = IS_REQUIRED;
  MIN_VALUE = "Minimum value should be greater than 0";

  constructor(private fb: FormBuilder) {
    this.itemForm = this.fb.group({
      name: ["", Validators.required],
      description: [""],
      initial_price: [0, Validators.min(0)],
      min_price: [0, Validators.min(0)],
      min_increment: [0, Validators.min(0)],
    });
  }

  onSubmit() {
    console.log(this.itemForm);
    if (this.itemForm.valid) {
      // Process the form data, e.g., send it to a backend service
      console.log(this.itemForm.value);
    }
  }
}
