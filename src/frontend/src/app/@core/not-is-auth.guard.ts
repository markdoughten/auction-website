import { Injectable } from "@angular/core";
import { CanLoad, Route, UrlSegment, Router } from "@angular/router";
import { Observable, of } from "rxjs";
import { AuthService } from "./auth.service";

@Injectable()
export class NotIsAuthGuard implements CanLoad {
  constructor(
    private router: Router,
    private authService: AuthService,
  ) {}

  canLoad(
    route: Route,
    segments: UrlSegment[],
  ): Observable<boolean> | Promise<boolean> | boolean {
    let result = false;
    this.authService.isLoggedIn.subscribe((isLoggedIn) => {
      if (isLoggedIn) {
        this.router.navigateByUrl("/");
      }
      result = isLoggedIn;
    });
    return !result;
  }
}
