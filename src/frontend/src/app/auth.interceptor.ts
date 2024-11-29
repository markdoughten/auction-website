import { HTTP_INTERCEPTORS, HttpInterceptorFn } from "@angular/common/http";
import { JWT_TOKEN } from "./constants";

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = sessionStorage.getItem(JWT_TOKEN);
  req = req.clone({
    headers: req.headers.set(
      "Authorization",
      token === null ? "" : `Bearer ${token}`,
    ),
  });
  return next(req);
};
