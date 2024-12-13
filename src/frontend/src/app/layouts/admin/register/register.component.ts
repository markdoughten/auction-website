import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RegisterComponent } from "@components/register/register.component";
import { BackButtonComponent } from "@components/backbutton/backbutton.component";
import { AuthService } from "@core/auth.service";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule, RegisterComponent, BackButtonComponent],
  templateUrl: "./register.component.html",
})
export class RegisterUserComponent implements OnInit {
  readonly isAdmin: boolean = true;
  readonly message: string = "";
  constructor(protected auth: AuthService) {
    this.message = `Back to ${this.auth.user.role} Dashboard`;
  }
  ngOnInit(): void {}

  userAdd() {
    alert("User has been added successfully!");
  }
}
