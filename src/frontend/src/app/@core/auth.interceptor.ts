import { HttpErrorResponse, HttpInterceptorFn } from "@angular/common/http";
import { catchError, throwError } from "rxjs";
import { inject } from "@angular/core";
import { AuthService } from "./auth.service";
import { TOKEN_EXPIRED } from "./constants";

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.token();
  if (token) {
    const authReq = req.clone({
      setHeaders: {
        Authorization: token === null ? "" : `Bearer ` + token,
      },
    });
    return next(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          alert(TOKEN_EXPIRED);
          sessionStorage.clear();
          location.reload();
        }
        return throwError(() => error);
      }),
    );
  }
  return next(req);
};
