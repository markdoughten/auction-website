import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormControl, FormGroup } from "@angular/forms";
import { ReactiveFormsModule, Validators } from "@angular/forms";
import { ElementRef } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import {
  SERVER_URLS,
  RESPONSE_STATUS,
  IS_REQUIRED,
  MIN_LEN,
  NOT_EMAIL,
} from "../constants";

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

  constructor(
    private elRef: ElementRef<HTMLElement>,
    private http: HttpClient,
  ) {}

  signUp = new FormGroup(
    {
      uname: new FormControl("", [
        Validators.required,
        Validators.minLength(5),
      ]),
      email: new FormControl("", [Validators.required, Validators.email]),
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
    email: new FormControl("", [Validators.required, Validators.email]),
    password: new FormControl("", Validators.required),
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
    const self = this;
    this.http
      .post(SERVER_URLS.login, this.login.value, { responseType: "json" })
      .subscribe((response: any) => {
        if (response.status === RESPONSE_STATUS.SUCCESS) {
          console.log(response);
          // } else {
          // // handle this better...
          //   self.login.controls["email"].setErrors({ incorrect: true });
        }
      });
    // perform some more oprs...
  }

  signupUsr() {
    const signUp = this.signUp;
    if (
      signUp.get("uname")?.errors != null ||
      signUp.get("email")?.errors != null ||
      signUp.get("password")?.errors != null ||
      signUp.get("passwordConfirm")?.errors != null
    ) {
      return;
    }
    // const self = this;
    this.http
      .post(SERVER_URLS.signup, signUp.value, { responseType: "json" })
      .subscribe((response: any) => {
        if (response.status === RESPONSE_STATUS.SUCCESS) {
          let element: HTMLElement = document.getElementById(
            "login_now",
          ) as HTMLElement;
          element.click();
          // } else {
          // // handle validation better...
          //   signUp.controls["uname"].setErrors({ incorrect: true });
          //   signUp.controls["email"].setErrors({ incorrect: true });
        }
      });
  }
}
