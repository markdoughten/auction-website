import { Routes } from "@angular/router";
import { LandingComponent } from "./landing/landing.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { IsAuthGuard } from "./is-auth.guard";
import { NotIsAuthGuard } from "./not-is-auth.guard";
import { HasRoleGuard } from "./has-role.guard";
import {
  admin_access,
  staff_access,
  all_access,
  R_ADMIN,
} from "./model/usermodel";
import { AdminComponent } from "./admin/admin.component";
import { AuthService } from "./auth.service";
import { inject } from "@angular/core";
import { RegisterComponent } from "./admin/register/register.component";
import { AdminDashboardComponent } from "./admin/dashboard/dashboard.component";
import { ModifyComponent } from "./admin/modify/modify.component";

export const routes: Routes = [
  {
    path: "",
    redirectTo: () => {
      const authService = inject(AuthService);
      let path = "/login";
      authService.isLoggedIn.subscribe((isLoggedIn) => {
        if (isLoggedIn) {
          authService.isAdmin.subscribe((isAdmin) => {
            if (isAdmin) {
              path = "/admin";
            } else {
              path = "/dashboard";
            }
          });
        }
      });
      return path;
    },
    pathMatch: "full",
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
      role: staff_access,
    },
    children: [
      { path: "dashboard", component: AdminDashboardComponent },
      {
        path: "register",
        component: RegisterComponent,
        canActivate: [HasRoleGuard],
        data: { role: admin_access },
      },
      {
        path: "modify",
        component: ModifyComponent,
      },
      { path: "**", redirectTo: "dashboard", pathMatch: "full" },
    ],
  },
  {
    path: "login",
    component: LandingComponent,
    canActivate: [NotIsAuthGuard],
  },
  {
    path: "signup",
    component: LandingComponent,
    canActivate: [NotIsAuthGuard],
  },
  { path: "**", redirectTo: "/", pathMatch: "full" },
];
