import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from "@angular/forms";
import { Router } from "@angular/router";
import { AuthService } from "@core/auth.service";
import {
  IS_REQUIRED,
  MIN_LEN,
  NOT_EMAIL,
  RESPONSE_STATUS,
  SERVER_URLS,
} from "@core/constants";

function dup_entry_found(self: SettingsComponent): ValidatorFn {
  return (c: AbstractControl): { [key: string]: boolean } | null => {
    if (self.dup_entry > 0) {
      self.dup_entry--;
      return { incorrect: true };
    }
    return null;
  };
}

@Component({
  selector: "app-settings",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./settings.component.html",
})
export class SettingsComponent implements OnInit {
  dup_entry = 0;
  readonly IS_REQUIRED = IS_REQUIRED;
  readonly MIN_LEN = MIN_LEN;
  readonly NOT_EMAIL = NOT_EMAIL;
  NOT_MATCHING = "Passwords don't match";
  DUP_TRY_AGAIN = "Email or User already present";
  INCORRECT_TRY_AGAIN = "Incorrect email/password";
  signUp: FormGroup;

  ngOnInit(): void {}

  constructor(
    private authService: AuthService,
    private router: Router,
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
        role: new FormControl(null),
      },
      this.passwordMatchValidator,
    );
    const self = this;
    this.signUp.controls["username"].setValue(this.authService.user.username, {
      onlySelf: true,
    });
    this.signUp.controls["username"].disable();
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

    this.signUp.controls["username"].setValue(this.authService.user.username, {
      onlySelf: true,
    });
    signUp.enable({ emitEvent: true });
    const self = this;
    SERVER_URLS.update_user.id = this.authService.user.id;
    this.authService.add_modify(signUp, SERVER_URLS.update_user).subscribe(
      (response: any) => {
        if (response.status === RESPONSE_STATUS.SUCCESS) {
          alert("User updated successfully");
          self.router.navigate(["admin"]);
          // } else {
          //   alert(response.message);
        }
      },
      (error) => {
        // alert(error.error.message);
      },
    );
    this.dup_entry = 1;
    signUp.get("email")?.updateValueAndValidity();
    this.signUp.controls["username"].setValue(this.authService.user.username, {
      onlySelf: true,
    });
    this.signUp.controls["username"].disable();
  }

  isdelete() {
    if (confirm("Are you sure??")) {
      const self = this;
      this.authService.delUser(this.authService.user.id).subscribe(
        (response) => {
          if (response.status == RESPONSE_STATUS.SUCCESS) {
            alert(
              response.message +
                "\n" +
                self.authService.user.username +
                " deleted successfully",
            );
          } else {
            alert(response.message);
          }
        },
        (error) => {
          alert(error.error.message);
        },
      );
    }
  }
}
