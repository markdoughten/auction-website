import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ValidatorFn,
} from "@angular/forms";
import { Router, ActivatedRoute } from "@angular/router";
import { ReactiveFormsModule, Validators } from "@angular/forms";
import {
  RESPONSE_STATUS,
  IS_REQUIRED,
  MIN_LEN,
  NOT_EMAIL,
  SERVER_URLS,
} from "@core/constants";
import { AuthService } from "@core/auth.service";
import { staff_access, R_STAFF } from "@model/usermodel";

function dup_entry_found(self: RegisterComponent): ValidatorFn {
  return (c: AbstractControl): { [key: string]: boolean } | null => {
    if (self.dup_entry > 0) {
      self.dup_entry--;
      return { incorrect: true };
    }
    return null;
  };
}

@Component({
  selector: "app-register",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./register.component.html",
  styleUrl: "../admin.component.css",
})
export class RegisterComponent {
  dup_entry = 0;
  readonly IS_REQUIRED = IS_REQUIRED;
  readonly MIN_LEN = MIN_LEN;
  readonly NOT_EMAIL = NOT_EMAIL;
  NOT_MATCHING = "Passwords don't match";
  DUP_TRY_AGAIN = "Email or User already present";
  INCORRECT_TRY_AGAIN = "Incorrect email/password";
  userRoles = staff_access;
  signUp: FormGroup;
  modify_user: boolean = false;
  initParams: any;

  constructor(
    private auth: AuthService,
    private router: Router,
    private activator: ActivatedRoute,
  ) {
    this.signUp = new FormGroup(
      {
        username: new FormControl("", [
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
        userRole: new FormControl(null),
      },
      this.passwordMatchValidator,
    );
    this.signUp.controls["userRole"].setValue(R_STAFF, { onlySelf: true });
    const self = this;
    this.activator.queryParams.subscribe((params) => {
      if (Object.keys(params).length === 0) {
        return;
      }
      this.initParams = JSON.parse(JSON.stringify(params));
      if (!this.userRoles.includes(this.initParams.role)) {
        this.userRoles = [this.initParams.role];
      }
      if (
        !(
          self.is_empty(this.initParams.username) ||
          self.is_empty(this.initParams.email) ||
          self.is_empty(this.initParams.role)
        )
      ) {
        self.setDefModSignUp();
        self.disableModSignUp();
        self.modify_user = true;
      }
    });
  }

  setDefModSignUp() {
    this.signUp.controls["username"].setValue(this.initParams.username, {
      onlySelf: true,
    });
    this.signUp.controls["email"].setValue(this.initParams.email, {
      onlySelf: true,
    });
    this.signUp.controls["userRole"].setValue(this.initParams.role, {
      onlySelf: true,
    });
  }

  disableModSignUp() {
    this.signUp.controls["username"].disable();
    this.signUp.controls["email"].disable();
    this.signUp.controls["userRole"].disable();
  }

  is_empty(s: string) {
    if (s === undefined || s === null || s === "") {
      return true;
    }
    return false;
  }

  passwordMatchValidator(g: FormGroup | any) {
    g.controls["passwordConfirm"].setErrors(
      g.get("password").value === g.get("passwordConfirm").value
        ? null
        : { notSame: true },
    );
    return g;
  }

  signupUsr() {
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

    const self = this;
    if (this.modify_user) {
      this.setDefModSignUp();
      signUp.enable({ emitEvent: true });
      this.auth
        .signup(signUp, SERVER_URLS.update_user)
        .subscribe((response: any) => {
          if (response.status === RESPONSE_STATUS.SUCCESS) {
            alert("User updated successfully");
            self.router.navigate(["admin"]);
          } else {
            alert(response.message);
          }
        });

      self.dup_entry = 2;
      self.disableModSignUp();
    } else {
      this.auth
        .signup(this.signUp, SERVER_URLS.create_account)
        .subscribe((response: any) => {
          if (response.status === RESPONSE_STATUS.SUCCESS) {
            alert("Staff registered successfully");
            self.router.navigate(["admin"]);
          } else {
            self.dup_entry = 2;
            signUp.get("username")?.updateValueAndValidity();
            signUp.get("email")?.updateValueAndValidity();
          }
        });
    }
  }
}
