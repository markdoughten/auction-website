import { Component, input } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AuthService } from "@core/auth.service";

@Component({
  selector: "app-navbar",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./navbar.component.html",
  styleUrl: "./navbar.component.css",
})
export class NavbarComponent {
  constructor(protected authService: AuthService) {
    this.id = this.authService.user.id;
  }
  id: number = -1;

  logout() {
    sessionStorage.clear();
    location.reload();
  }
}
