import { Routes } from "@angular/router";
import { inject } from "@angular/core";
import { AuthService } from "@core/auth.service";
import { IsAuthGuard } from "@core/is-auth.guard";
import { NotIsAuthGuard } from "@core/not-is-auth.guard";
import { HasRoleGuard } from "@core/has-role.guard";
import { LandingComponent } from "@layouts/landing/landing.component";
import { DashboardComponent } from "@layouts/dashboard/dashboard.component";
import { AdminComponent } from "@layouts/admin/admin.component";
import { AdminDashboardComponent } from "@layouts/admin/dashboard/dashboard.component";
import { RegisterComponent } from "@layouts/admin/register/register.component";
import { ModifyComponent } from "@layouts/admin/modify/modify.component";
import { admin_access, staff_access, all_access } from "@model/usermodel";
import { ProfileComponent } from "@layouts/profile/profile.component";

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
    path: "profile/:id",
    component: ProfileComponent,
    canActivate: [IsAuthGuard],
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
