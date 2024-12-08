import { Injectable } from "@angular/core";
import {
  ActivatedRouteSnapshot,
  CanActivate,
  GuardResult,
  MaybeAsync,
  Router,
  RouterStateSnapshot,
} from "@angular/router";
import { AuthService } from "./auth.service";

@Injectable({
  providedIn: "root",
})
export class HasRoleGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): MaybeAsync<GuardResult> {
    let result = false;
    this.authService.isLoggedIn.subscribe((isLoggedIn) => {
      if (
        !isLoggedIn ||
        !route.data["role"].includes(this.authService.user.role)
      ) {
        result = false;
        this.router.navigate([""]);
      } else {
        result = true;
      }
    });
    return result;
  }
}
