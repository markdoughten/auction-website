import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BehaviorSubject } from "rxjs";
import { RegisterComponent } from "@components/register/register.component";
import { UserComponent } from "./user_components/user.component";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule, RegisterComponent, UserComponent],
  templateUrl: "./modify.component.html",
})
export class ModifyComponent implements OnInit {
  readonly isAdmin: boolean = true;
  showUsers$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(true);
  userData: any = undefined;
  constructor() {}
  ngOnInit(): void {}

  updateUser(userData: any) {
    this.userData = userData;
    this.showUsers$.next(false);
  }

  userMod() {
    alert("User has been modified successfully!");
    this.showUsers$.next(true);
  }
}
