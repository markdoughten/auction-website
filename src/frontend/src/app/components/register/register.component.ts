import { CommonModule } from "@angular/common";
import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { AuthService } from "@core/auth.service";
import {
  IS_REQUIRED,
  MIN_LEN,
  NOT_EMAIL,
  RESPONSE_STATUS,
  SERVER_URLS,
} from "@core/constants";
import { LoadingService } from "@core/loading.service";
import { check_duplicate } from "@core/form_validator";
import { staff_access, R_STAFF, R_USER } from "@model/usermodel";

@Component({
  selector: "app-register",
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: "./register.component.html",
})
export class RegisterComponent implements OnInit {
  readonly IS_REQUIRED = IS_REQUIRED;
  readonly MIN_LEN = MIN_LEN;
  readonly NOT_EMAIL = NOT_EMAIL;
  NOT_MATCHING = "Passwords don't match";
  DUP_TRY_AGAIN = "Email or User already present";
  duplicate: number = 0;
  signUp: FormGroup;
  roles = staff_access;
  @Input() userDetails: any = undefined;
  @Input() isAdmin: boolean = false;
  @Input() showDelete: boolean = false;
  @Output() success = new EventEmitter<any>();
  constructor(
    private auth: AuthService,
    private loading: LoadingService,
  ) {
    this.signUp = new FormGroup(
      {
        username: new FormControl("", [
          Validators.required,
          Validators.minLength(5),
          check_duplicate(this),
        ]),
        email: new FormControl("", [
          Validators.required,
          Validators.email,
          check_duplicate(this),
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
      { validators: this.verify_password },
    );
  }

  verify_password(formGroup: FormGroup | any) {
    formGroup.controls["passwordConfirm"].setErrors(
      formGroup.get("password").value === formGroup.get("passwordConfirm").value
        ? null
        : { notMatching: true },
    );
    return formGroup;
  }

  set_default_vals(add_email: boolean = false) {
    if (add_email) {
      this.signUp.controls["email"].setValue(this.userDetails.email, {
        onlySelf: true,
      });
    }
    this.signUp.controls["username"].setValue(this.userDetails.username, {
      onlySelf: true,
    });
    this.signUp.controls["role"].setValue(this.userDetails.role, {
      onlySelf: true,
    });
  }

  disable_defaults() {
    this.signUp.controls["username"].disable();
    this.signUp.controls["role"].disable();
  }

  ngOnInit(): void {
    if (this.isAdmin) {
      this.signUp.controls["role"].setValue(R_STAFF, { onlySelf: true });
    }
    if (this.userDetails !== undefined) {
      this.roles = [this.userDetails.role];
      this.set_default_vals(true);
      this.disable_defaults();
    }
  }

  handle_duplicates(form: FormGroup) {
    this.duplicate = 2;
    form.get("username")?.updateValueAndValidity();
    form.get("email")?.updateValueAndValidity();
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

    this.loading.show();
    let url = SERVER_URLS.signup;
    if (this.userDetails !== undefined) {
      this.set_default_vals();
      this.signUp.enable({ emitEvent: true });
      SERVER_URLS.update_user.id = this.auth.user.id;
      url = SERVER_URLS.update_user;
    } else if (this.isAdmin) {
      url = SERVER_URLS.create_account;
    }

    this.auth.add_modify(this.signUp, url).subscribe({
      next: (data) => {
        if (data.status === RESPONSE_STATUS.SUCCESS) {
          this.success.emit();
        } else {
          this.handle_duplicates(signUp);
        }
        this.loading.hide();
      },
      error: (err) => {
        this.handle_duplicates(signUp);
        this.loading.hide();
      },
    });
  }

  deleteUser() {
    if (confirm("Are you sure??")) {
      const self = this;
      this.auth.delUser(this.auth.user.id).subscribe(
        (response) => {
          if (response.status == RESPONSE_STATUS.SUCCESS) {
            alert(
              response.message +
                "\n" +
                self.auth.user.username +
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
