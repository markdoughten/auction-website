import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ValidatorFn,
} from "@angular/forms";
import { ReactiveFormsModule, Validators } from "@angular/forms";
import { RESPONSE_STATUS, IS_REQUIRED, MIN_LEN, NOT_EMAIL } from "../constants";
import { AuthService } from "../auth.service";
import { Router } from "@angular/router";

function dup_entry_found(self: LandingComponent): ValidatorFn {
  return (c: AbstractControl): { [key: string]: boolean } | null => {
    if (self.dup_entry > 0) {
      self.dup_entry--;
      return { incorrect: true };
    }
    return null;
  };
}

@Component({
  selector: "app-landing",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./landing.component.html",
  styleUrl: "./landing.component.css",
})
export class LandingComponent implements OnInit {
  readonly IS_REQUIRED = IS_REQUIRED;
  readonly MIN_LEN = MIN_LEN;
  readonly NOT_EMAIL = NOT_EMAIL;
  NOT_MATCHING = "Passwords don't match";
  DUP_TRY_AGAIN = "Email or User already present";
  INCORRECT_TRY_AGAIN = "Incorrect email/password";
  dup_entry = 0;

  constructor(
    private auth: AuthService,
    private router: Router,
  ) {}

  signUp = new FormGroup(
    {
      uname: new FormControl("", [
        Validators.required,
        Validators.minLength(5),
        dup_entry_found(this),
      ]),
      email: new FormControl("", [
        Validators.required,
        Validators.email,
        dup_entry_found(this),
      ]),
      password: new FormControl("", [
        Validators.required,
        Validators.minLength(5),
      ]),
      passwordConfirm: new FormControl("", [
        Validators.required,
        Validators.minLength(5),
      ]),
    },
    this.passwordMatchValidator,
  );

  login = new FormGroup({
    email: new FormControl("", [
      Validators.required,
      Validators.email,
      dup_entry_found(this),
    ]),
    password: new FormControl("", [Validators.required, dup_entry_found(this)]),
  });

  passwordMatchValidator(g: FormGroup | any) {
    g.controls["passwordConfirm"].setErrors(
      g.get("password").value === g.get("passwordConfirm").value
        ? null
        : { notSame: true },
    );
    return g;
  }

  ngOnInit(): void {}

  loginUsr() {
    this.signUp.reset();
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
    const self = this;

    this.auth.login(this.login).subscribe((response: any) => {
      if (response.status === RESPONSE_STATUS.SUCCESS) {
        this.router.navigate(["login"]);
      } else {
        this.dup_entry = 2;
        self.login.get("email")?.updateValueAndValidity();
        self.login.get("password")?.updateValueAndValidity();
      }
    });
  }

  signupUsr() {
    this.login.reset();
    const signUp = this.signUp;
    let is_invalid = false;
    Object.keys(signUp.controls).forEach((field) => {
      if (signUp.get(field)?.errors != null) {
        is_invalid = true;
        return;
      }
    });
    if (is_invalid) {
      signUp.markAllAsTouched();
      return;
    }

    this.auth.signup(this.signUp).subscribe((response: any) => {
      if (response.status === RESPONSE_STATUS.SUCCESS) {
        let element: HTMLElement = document.getElementById(
          "login_now",
        ) as HTMLElement;
        element.click();
      } else {
        this.dup_entry = 2;
        signUp.get("uname")?.updateValueAndValidity();
        signUp.get("email")?.updateValueAndValidity();
      }
    });
  }
}
