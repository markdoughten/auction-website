import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AuthService } from "@core/auth.service";
import { RouterLink } from "@angular/router";
import { R_USER } from "@model/usermodel";

@Component({
  selector: "app-navbar",
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: "./navbar.component.html",
})
export class NavbarComponent implements OnInit {
  constructor(protected authService: AuthService) {
    this.id = this.authService.user.id;
    this.role = this.authService.user.role;
    this.isUser = this.role === R_USER;
  }
  readonly id: number = -1;
  readonly role: string = "";
  readonly isUser: boolean = true;

  ngOnInit(): void {}

  isNavbarOpen = false;

  toggleNavbar(): void {
    this.isNavbarOpen = !this.isNavbarOpen;
  }

  onNavItemClick(): void {
    if (this.isNavbarOpen) {
      this.isNavbarOpen = false;
    }
  }

  logout() {
    sessionStorage.clear();
    window.alert("user logged out successfully!");
    location.reload();
  }
}
