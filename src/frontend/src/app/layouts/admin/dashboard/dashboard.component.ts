import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AuthService } from "@core/auth.service";
import { RouterLink } from "@angular/router";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: "./dashboard.component.html",
})
export class AdminDashboardComponent implements OnInit {
  constructor(protected authService: AuthService) {}

  ngOnInit() {}
}
