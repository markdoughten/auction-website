import { Injectable, Inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AbstractControl } from "@angular/forms";
import { UserModel } from "./model/usermodel";
import { BehaviorSubject, tap } from "rxjs";
import { SERVER_URLS, RESPONSE_STATUS, JWT_TOKEN } from "./constants";
import { DOCUMENT } from "@angular/common";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private _isLoggedIn = new BehaviorSubject<boolean>(false);
  isLoggedIn = this._isLoggedIn.asObservable();
  user!: UserModel;

  get token(): string {
    const sessionStorage = this.document.defaultView?.sessionStorage;
    const token =
      sessionStorage === undefined ? null : sessionStorage.getItem(JWT_TOKEN);
    return token === null ? "" : token;
  }

  constructor(
    @Inject(DOCUMENT) private document: Document,
    private http: HttpClient,
  ) {
    this._isLoggedIn.next(!!this.token);
    this.user = this.getUser(this.token);
  }

  login(data: AbstractControl) {
    return this.http
      .post(SERVER_URLS.login, data.value, { responseType: "json" })
      .pipe(
        tap((response: any) => {
          if (response.status === RESPONSE_STATUS.SUCCESS) {
            sessionStorage.setItem(JWT_TOKEN, response.JWT_TOKEN);
            this._isLoggedIn.next(true);
            this.user = this.getUser(response.JWT_TOKEN);
          }
        }),
      );
  }

  signup(data: AbstractControl) {
    return this.http
      .post(SERVER_URLS.signup, data.value, { responseType: "json" })
      .pipe(
        tap((response: any) => {
          console.log(response);
        }),
      );
  }

  private getUser(token: string): UserModel {
    if (token !== "") {
      return JSON.parse(atob(token.split(".")[1])).sub as UserModel;
    } else {
      return { username: "", role: "" };
    }
  }
}
