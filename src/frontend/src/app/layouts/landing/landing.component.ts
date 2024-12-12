import { Component, OnInit } from "@angular/core";
import { LoginComponent } from "@components/login/login.component";
import { RegisterComponent } from "@components/register/register.component";

@Component({
  selector: "app-landing",
  standalone: true,
  imports: [LoginComponent, RegisterComponent],
  templateUrl: "./landing.component.html",
  styleUrl: "./landing.component.css",
})
export class LandingComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

  on_signup() {
    alert("User registered successfully");
    let element: HTMLElement = document.getElementById(
      "login_now",
    ) as HTMLElement;
    element.click();
  }
}
