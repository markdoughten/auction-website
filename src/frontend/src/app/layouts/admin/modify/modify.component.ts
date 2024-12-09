import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Router } from "@angular/router";
import { HttpClient } from "@angular/common/http";
import { AuthService } from "@core/auth.service";
import { SERVER_URLS, RESPONSE_STATUS } from "@core/constants";
import { catchError, throwError } from "rxjs";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./modify.component.html",
  styleUrl: "../admin.component.css",
})
export class ModifyComponent implements OnInit {
  users: any = undefined;

  constructor(
    private http: HttpClient,
    private router: Router,
    private authService: AuthService,
  ) {}
  ngOnInit(): void {
    this.populate_users();
  }

  populate_users() {
    const self = this;
    this.http
      .get(SERVER_URLS.get_accounts, { responseType: "json" })
      .pipe(
        catchError((error) => {
          return throwError(error);
        }),
      )
      .subscribe(
        (response: any) => {
          if (response.status == RESPONSE_STATUS.SUCCESS) {
            self.users = response.data;
          } else {
            alert(response.message);
          }
        },
        (error) => {
          alert(error.error.message);
        },
      );
  }

  modifyUser(userData: any) {
    this.router.navigate(["/admin/register"], {
      queryParams: userData,
    });
  }

  deleteUser(userData: any) {
    if (confirm("Are you sure??")) {
      this.authService.delUser(userData.id).subscribe(
        (response) => {
          if (response.status == RESPONSE_STATUS.SUCCESS) {
            this.populate_users();
            alert(
              response.message +
                "\n" +
                userData.username +
                " deleted successfully",
            );
          } else {
            alert(response.message);
          }
        },
        (error) => {
          alert(error.error.message);
        },
      );
    }
  }
}
