import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { timer } from "rxjs";
import { AuthService } from "@core/auth.service";
import { IS_REQUIRED, NOT_EMAIL, RESPONSE_STATUS } from "@core/constants";
import { check_duplicate } from "@core/form_validator";
import { LoadingService } from "@core/loading.service";
import { Router } from "@angular/router";

@Component({
  selector: "app-login",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./login.component.html",
})
export class LoginComponent implements OnInit {
  readonly IS_REQUIRED = IS_REQUIRED;
  readonly NOT_EMAIL = NOT_EMAIL;
  INCORRECT_TRY_AGAIN = "Incorrect email/password";
  duplicate: number = 0;
  login: FormGroup;

  ngOnInit(): void {}

  constructor(
    private authSerice: AuthService,
    private loading: LoadingService,
    private router: Router,
  ) {
    this.login = new FormGroup({
      email: new FormControl("", [
        Validators.required,
        Validators.email,
        check_duplicate(this),
      ]),
      password: new FormControl("", [
        Validators.required,
        check_duplicate(this),
      ]),
    });
  }

  handle_duplicate(form: FormGroup) {
    this.duplicate = 1;
    this.login.get("password")?.updateValueAndValidity();
    this.login.get("email")?.updateValueAndValidity();
  }

  async loginUser() {
    const login = this.login;
    let is_invalid = false;
    Object.keys(login.controls).forEach((field) => {
      if (login.get(field)?.errors != null) {
        is_invalid = true;
        return;
      }
    });

    if (is_invalid) {
      login.markAllAsTouched();
      return;
    }

    this.loading.show();
    this.authSerice.login(login).subscribe({
      next: (response) => {
        if (response.status === RESPONSE_STATUS.SUCCESS) {
          timer(100).subscribe(() => {
            this.loading.hide();
            window.location.href = "/dashboard";
          });
        } else {
          this.handle_duplicate(login);
          this.loading.hide();
        }
      },
      error: (error) => {
        this.loading.hide();
        this.handle_duplicate(login);
      },
    });
  }
}
