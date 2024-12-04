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
import { tap } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class IsAuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot,
  ): MaybeAsync<GuardResult> {
    return this.authService.isLoggedIn.pipe(
      tap((isLoggedIn) => {
        if (!isLoggedIn) {
          this.router.navigate(["login"]);
        }
      }),
    );
  }
}
