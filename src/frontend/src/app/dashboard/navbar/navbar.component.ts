import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { AuthService } from "../../auth.service";

@Component({
  selector: "app-navbar",
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: "./navbar.component.html",
  styleUrl: "../dashboard.component.css",
})
export class NavbarComponent {
  constructor(protected authService: AuthService) {}
  product: string = "";

  searchevent() {
    console.log("test...", this.product);
  }

  logout() {
    sessionStorage.clear();
    location.reload();
  }
}
