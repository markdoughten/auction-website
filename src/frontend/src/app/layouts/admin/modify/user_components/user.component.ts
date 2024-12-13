import { Component, EventEmitter, OnInit, Output } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { RouterLink } from "@angular/router";
import { AuthService } from "@core/auth.service";
import { SERVER_URLS, RESPONSE_STATUS } from "@core/constants";
import { PageComponent } from "@components/page/page.component";
import { FormsModule } from "@angular/forms";

@Component({
  selector: "app-user-comp",
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, PageComponent],
  templateUrl: "./user.component.html",
})
export class UserComponent implements OnInit {
  users: any = undefined;
  currentPage = 1;
  hasMorePages: boolean = true;
  searchQuery: string = "";
  @Output() modifyUser = new EventEmitter<any>();
  readonly itemsPerPage = 20; // default limit in python is 20

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) {}
  ngOnInit(): void {
    this.get_users(this.currentPage);
  }

  updateUser(userData: any) {
    this.modifyUser.emit(userData);
  }

  get_users(page: any) {
    let params = {
      ...(page && { page: page }),
      ...(this.searchQuery !== "" && { username: this.searchQuery }),
    };
    this.http
      .get(SERVER_URLS.get_accounts, {
        responseType: "json",
        params: params,
      })
      .subscribe({
        next: (response: any) => {
          this.users = response;
          this.currentPage = page;
          if (response.length < 20) {
            this.hasMorePages = false;
          }
        },
        error: (error) => {
          if (this.currentPage >= 1) {
            this.hasMorePages = false;
          }
          if (this.users === undefined) {
            alert("No users found!");
          }
        },
      });
  }

  deleteUser(userData: any) {
    if (confirm("Are you sure??")) {
      this.authService.delUser(userData.id).subscribe({
        next: (response) => {
          this.get_users(this.currentPage);
          alert(userData.username + " deleted successfully");
        },
        error: (error) => {
          alert(error.error.message);
        },
      });
    }
  }
}
