import { Component, EventEmitter, OnInit, Output } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { AuthService } from "@core/auth.service";
import { SERVER_URLS, RESPONSE_STATUS } from "@core/constants";

@Component({
  selector: "app-user-comp",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./user.component.html",
})
export class UserComponent implements OnInit {
  users: any = undefined;
  @Output() modifyUser = new EventEmitter<any>();

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) {}
  ngOnInit(): void {
    this.get_users();
  }

  updateUser(userData: any) {
    this.modifyUser.emit(userData);
  }

  get_users() {
    const self = this;
    this.http
      .get(SERVER_URLS.get_accounts, {
        responseType: "json",
        params: { page: 1 },
      })
      .subscribe({
        next: (response: any) => {
          self.users = response;
        },
        error: (error) => {
          alert(error.error.message);
        },
      });
  }

  deleteUser(userData: any) {
    if (confirm("Are you sure??")) {
      this.authService.delUser(userData.id).subscribe({
        next: (response) => {
          if (response.status == RESPONSE_STATUS.SUCCESS) {
            this.get_users();
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
        error: (error) => {
          alert(error.error.message);
        },
      });
    }
  }
}
