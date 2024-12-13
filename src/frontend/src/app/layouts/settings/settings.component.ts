import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { RegisterComponent } from "@components/register/register.component";
import { AuthService } from "@core/auth.service";
import { RESPONSE_STATUS } from "@core/constants";

@Component({
  selector: "app-settings",
  standalone: true,
  imports: [CommonModule, RegisterComponent],
  templateUrl: "./settings.component.html",
})
export class SettingsComponent implements OnInit {
  readonly showDelete: boolean = true;
  ngOnInit(): void {}

  constructor(protected authService: AuthService) {}

  updateUser() {
    alert("User details updated successfully!");
  }
}
