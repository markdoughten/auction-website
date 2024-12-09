import { Routes } from "@angular/router";
import { DashboardComponent } from "./layouts/dashboard/dashboard.component";
import { CanDeactivateGuard } from "./guards/can-deactivate.guard";

export const routes: Routes = [
  {
    path: "dashboard",
    component: DashboardComponent,
    canDeactivate: [CanDeactivateGuard], // Attach the guard here
  },
  {
    path: "",
    redirectTo: "dashboard",
    pathMatch: "full",
  },
];
