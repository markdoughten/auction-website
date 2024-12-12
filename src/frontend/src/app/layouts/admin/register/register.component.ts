import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RegisterComponent } from "@components/register/register.component";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule, RegisterComponent],
  templateUrl: "./register.component.html",
})
export class RegisterUserComponent implements OnInit {
  readonly isAdmin: boolean = true;
  constructor() {}
  ngOnInit(): void {}

  userAdd() {
    alert("User has been added successfully!");
  }
}
