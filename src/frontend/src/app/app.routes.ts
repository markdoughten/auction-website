import { Routes } from "@angular/router";
import { LandingComponent } from "./landing/landing.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { IsAuthGuard } from "./is-auth.guard";
import { HasRoleGuard } from "./has-role.guard";
import { admin_access, staff_access, all_access } from "./model/usermodel";
import { AdminComponent } from "./admin/admin.component";
import { AuthService } from "./auth.service";
import { inject } from "@angular/core";
import { R_ADMIN } from "./model/usermodel";

export const routes: Routes = [
  {
    path: "",
    redirectTo: () => {
      const authService = inject(AuthService);
      let path = "/login";
      if (authService.isLoggedIn) {
        switch (authService.user.role) {
          case R_ADMIN:
            path = "/admin";
            break;
          default:
            path = "/dashboard";
        }
      }
      return path;
    },
    pathMatch: "full",
  },
  {
    path: "login",
    component: LandingComponent,
  },
  {
    path: "signup",
    component: LandingComponent,
  },
  {
    path: "dashboard",
    component: DashboardComponent,
    canActivate: [IsAuthGuard, HasRoleGuard],
    data: {
      role: all_access,
    },
  },
  {
    path: "admin",
    component: AdminComponent,
    canActivate: [IsAuthGuard, HasRoleGuard],
    data: {
      role: admin_access,
    },
  },
];
