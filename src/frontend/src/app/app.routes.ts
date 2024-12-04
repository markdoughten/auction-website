import { Routes } from "@angular/router";
import { LandingComponent } from "./landing/landing.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { IsAuthGuard } from "./is-auth.guard";
import { HasRoleGuard } from "./has-role.guard";
import { all_access } from "./model/usermodel";

export const routes: Routes = [
  {
    path: "login",
    component: LandingComponent,
    canActivate: [!IsAuthGuard],
  },
  {
    path: "signup",
    component: LandingComponent,
    canActivate: [!IsAuthGuard],
  },
  {
    path: "dashboard",
    component: DashboardComponent,
    canActivate: [IsAuthGuard, HasRoleGuard],
    data: {
      role: all_access,
    },
  },
];
