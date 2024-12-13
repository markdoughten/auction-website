import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BehaviorSubject } from "rxjs";
import { RegisterComponent } from "@components/register/register.component";
import { UserComponent } from "./user_components/user.component";
import { BackButtonComponent } from "@components/backbutton/backbutton.component";
import { AuthService } from "@core/auth.service";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [
    CommonModule,
    RegisterComponent,
    UserComponent,
    BackButtonComponent,
  ],
  templateUrl: "./modify.component.html",
})
export class ModifyComponent implements OnInit {
  readonly isAdmin: boolean = true;
  readonly message: string = "";
  showUsers$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(true);
  userData: any = undefined;
  constructor(protected auth: AuthService) {
    this.message = `Back to ${this.auth.user.role} Dashboard`;
  }
  ngOnInit(): void {}

  updateUser(userData: any) {
    this.userData = userData;
    this.showUsers$.next(false);
  }

  userMod() {
    alert("User has been modified successfully!");
    this.showUsers$.next(true);
  }

  goBack() {
    this.showUsers$.next(true);
  }
}
