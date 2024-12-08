import { Injectable, Inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AbstractControl } from "@angular/forms";
import { UserModel } from "./model/usermodel";
import { BehaviorSubject, tap } from "rxjs";
import { SERVER_URLS, RESPONSE_STATUS, JWT_TOKEN } from "./constants";
import { DOCUMENT } from "@angular/common";
import { R_ADMIN } from "./model/usermodel";
import { switchMap } from "rxjs/operators";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private _isLoggedIn = new BehaviorSubject<boolean>(false);
  private _isAdmin = new BehaviorSubject<boolean>(false);
  isLoggedIn = this._isLoggedIn.asObservable();
  isAdmin = this._isAdmin.asObservable();
  user!: UserModel;

  constructor(
    @Inject(DOCUMENT) protected document: Document,
    private http: HttpClient,
  ) {
    const sessionStorage = this.document.defaultView?.sessionStorage;
    if (sessionStorage) {
      let token = sessionStorage.getItem(JWT_TOKEN);
      this._isLoggedIn.next(!!token);
      this.user = this.getUser(token === null ? "" : token);
      this._isAdmin.next(this.user?.role === R_ADMIN);
    }
  }

  async fetchData() {
    // Simulate fetching data from an API
    return new Promise((resolve) => {
      setTimeout(() => {
        return resolve;
      }, 1000);
    });
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

  signup(data: AbstractControl, url: string) {
    return this.http.post(url, data.value, { responseType: "json" }).pipe(
      tap((response: any) => {
        // perform opers if any
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
