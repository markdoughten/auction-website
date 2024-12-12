import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { NavbarComponent } from "@components/navbar/navbar.component";
import { AuctionComponent } from "@components/auction/auction.component";
import { RESPONSE_STATUS, SERVER_URLS } from "@core/constants";

@Component({
  selector: "app-profile",
  standalone: true,
  imports: [CommonModule, NavbarComponent, AuctionComponent],
  templateUrl: "./profile.component.html",
})
export class ProfileComponent implements OnInit {
  profileId: number = -1;
  readonly showBid: boolean = true;
  profileDetails: any = undefined;
  auctionItems: any = undefined;
  bidItems: any = undefined;
  message: string = "";

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    const profileId = this.route.snapshot.paramMap.get("id");
    this.profileId = profileId ? parseInt(profileId) : -1;
    if (
      this.profileId === undefined ||
      this.profileId === null ||
      isNaN(this.profileId) ||
      this.profileId === -1
    ) {
      alert("User not found...");
      this.router.navigate(["/"]);
    }
    this.get_init_data();
  }

  async get_init_data() {
    this.profileDetails = await this.get_items(SERVER_URLS.get_account.url);
    if (this.profileDetails) {
      this.message = "Items auctioned by " + this.profileDetails.username;
    }
    this.auctionItems = await this.get_items(SERVER_URLS.get_user_items);
    this.bidItems = await this.get_items(SERVER_URLS.get_user_bids);
  }

  async get_items(server_url: string) {
    let update_item = undefined;
    const url = server_url + this.profileId;
    try {
      const response: any = await this.http
        .get(url, { responseType: "json" })
        .toPromise();
      if (response) {
        if (response.status == RESPONSE_STATUS.SUCCESS) {
          update_item = response.data;
        } else {
          alert(response.message);
        }
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    return update_item;
  }
  sample() {}
  ngOnInit() {}
}
