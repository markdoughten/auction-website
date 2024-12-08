import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { Router } from "@angular/router";
import { HttpClient } from "@angular/common/http";
import { SERVER_URLS, RESPONSE_STATUS } from "@core/constants";

@Component({
  selector: "app-admin-dashboard",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./modify.component.html",
  styleUrl: "../admin.component.css",
})
export class ModifyComponent implements OnInit {
  users: any;

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {}
  ngOnInit(): void {
    const self = this;
    this.http
      .get(SERVER_URLS.get_accounts, { responseType: "json" })
      .subscribe((response: any) => {
        if (response.status == RESPONSE_STATUS.SUCCESS) {
          self.users = response.data;
        } else {
          alert(response.message);
        }
      });
  }

  modifyUser(userData: any) {
    console.log(userData);
    this.router.navigate(["/admin/register"], {
      queryParams: userData,
    });
  }
}
