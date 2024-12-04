import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";
import { LandingComponent } from "./landing/landing.component";
import { AuthService } from "./auth.service";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { NavbarComponent } from "./navbar/navbar.component";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    LandingComponent,
    DashboardComponent,
    NavbarComponent,
  ],
  templateUrl: "./app.component.html",
  styleUrl: "./app.component.css",
})
export class AppComponent {
  title = "frontend";
  constructor(public authService: AuthService) {}
}
