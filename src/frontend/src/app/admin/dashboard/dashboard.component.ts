import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AuthService } from "../../auth.service";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./dashboard.component.html",
  styleUrl: "../admin.component.css",
})
export class AdminDashboardComponent implements OnInit {
  constructor(protected authService: AuthService) {}

  ngOnInit() {}
}
