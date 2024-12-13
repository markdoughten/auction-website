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
import { ModifyComponent } from "@layouts/admin/modify/modify.component";
import { ProfileComponent } from "@layouts/profile/profile.component";
import { ItemComponent } from "@layouts/items/item/item.component";
import { ItemLandingComponent } from "@layouts/items/itemlanding.component";
import { BaseItemComponent } from "@layouts/items/itemform/base.component";
import { SettingsComponent } from "@layouts/settings/settings.component";
import { admin_access, staff_access, all_access } from "@model/usermodel";
import { RegisterUserComponent } from "@layouts/admin/register/register.component";
import { QuestionsComponent } from "@layouts/admin/questions/questions.component";
import { ReportsComponent } from "@layouts/admin/reports/reports.component";
import { SearchComponent } from "@layouts/search/search.component";

export const routes: Routes = [
  {
    path: "",
    redirectTo: () => {
      const authService = inject(AuthService);
      let path = "/login";
      authService.isLoggedIn.subscribe((isLoggedIn) => {
        if (isLoggedIn) {
          path = "/dashboard";
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
      { path: "modify", component: ModifyComponent },
      {
        path: "register",
        component: RegisterUserComponent,
        canActivate: [HasRoleGuard],
        data: { role: admin_access },
      },
      { path: "questions", component: QuestionsComponent },
      {
        path: "reports",
        component: ReportsComponent,
        canActivate: [HasRoleGuard],
        data: { role: admin_access },
      },
      { path: "**", redirectTo: "dashboard", pathMatch: "full" },
    ],
  },
  {
    path: "search",
    component: SearchComponent,
    canActivate: [IsAuthGuard],
  },
  {
    path: "profile/:id",
    component: ProfileComponent,
    canActivate: [IsAuthGuard],
  },
  {
    path: "item",
    component: ItemLandingComponent,
    canActivate: [IsAuthGuard],
    children: [
      {
        path: "view/:id",
        component: ItemComponent,
        canActivate: [IsAuthGuard],
      },
      {
        path: "",
        component: BaseItemComponent,
        canActivate: [IsAuthGuard],
      },
    ],
  },
  {
    path: "settings",
    component: SettingsComponent,
    canActivate: [IsAuthGuard],
  },
  {
    path: "login",
    component: LandingComponent,
    canLoad: [NotIsAuthGuard],
  },
  {
    path: "signup",
    component: LandingComponent,
    canLoad: [NotIsAuthGuard],
  },
  { path: "**", redirectTo: "/", pathMatch: "full" },
];
