import { Injectable, Inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AbstractControl } from "@angular/forms";
import { BehaviorSubject, catchError, tap, throwError } from "rxjs";
import { DOCUMENT } from "@angular/common";
import { UserModel } from "@model/usermodel";
import { SERVER_URLS, RESPONSE_STATUS, JWT_TOKEN } from "./constants";
import { R_ADMIN } from "@model/usermodel";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private _isLoggedIn = new BehaviorSubject<boolean>(false);
  private _isAdmin = new BehaviorSubject<boolean>(false);
  isLoggedIn = this._isLoggedIn.asObservable();
  isAdmin = this._isAdmin.asObservable();
  user!: UserModel;

  token(): string {
    const sessionStorage = this.document.defaultView?.sessionStorage;
    if (sessionStorage) {
      let token = sessionStorage.getItem(JWT_TOKEN);
      return token == null ? "" : token;
    }
    return "";
  }

  constructor(
    @Inject(DOCUMENT) protected document: Document,
    private http: HttpClient,
  ) {
    const token = this.token();
    this._isLoggedIn.next(!!token);
    this.user = this.getUser(token);
    this._isAdmin.next(this.user?.role === R_ADMIN);
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
        catchError((error) => {
          return throwError(error);
        }),
      );
  }

  addUpUsr(
    data: AbstractControl,
    url: { url: string; request: string; id: number },
  ) {
    let req_url = url.id != -1 ? url.url + url.id.toString() : url.url;
    return this.http
      .request(url.request, req_url, { body: data.value, responseType: "json" })
      .pipe(
        tap((response: any) => {
          // perform opers if any
        }),
        catchError((error) => {
          return throwError(error);
        }),
      );
  }

  delUser(id: number) {
    let req_url = SERVER_URLS.delete_user + id;
    const self = this;
    console.log(req_url);
    return this.http.delete(req_url, { responseType: "json" }).pipe(
      tap((response: any) => {
        if (id == self.user.id) {
          sessionStorage.clear();
          location.reload();
        }
      }),
      catchError((error) => {
        return throwError(error);
      }),
    );
  }

  private getUser(token: string): UserModel {
    if (token !== "") {
      return JSON.parse(atob(token.split(".")[1])).sub as UserModel;
    } else {
      return { id: -1, username: "", role: "", email: "" };
    }
  }
}
