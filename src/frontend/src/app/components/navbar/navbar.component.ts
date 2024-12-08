import { Component, input } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { AuthService } from "@core/auth.service";

@Component({
  selector: "app-navbar",
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: "./navbar.component.html",
  styleUrl: "./navbar.component.css",
})
export class NavbarComponent {
  constructor(protected authService: AuthService) {
    this.username = this.authService.user.username;
  }
  showSearch = input<boolean>(true);
  product: string = "";
  username: string = "";

  searchevent() {
    console.log("test...", this.product);
  }

  logout() {
    sessionStorage.clear();
    location.reload();
  }
}
