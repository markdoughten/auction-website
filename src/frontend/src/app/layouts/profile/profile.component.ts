import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { NavbarComponent } from "@components/navbar/navbar.component";
import { AuctionComponent } from "@components/auction/auction.component";
import { BidsComponent } from "@components/bids/bids.component";
import { LoadingService } from "@core/loading.service";
import { AuthService } from "@core/auth.service";
import { staff_access } from "@model/usermodel";
import { SERVER_URLS } from "@core/constants";

@Component({
  selector: "app-profile",
  standalone: true,
  imports: [CommonModule, NavbarComponent, AuctionComponent, BidsComponent],
  templateUrl: "./profile.component.html",
})
export class ProfileComponent implements OnInit {
  profileId: number = -1;
  readonly showBid: boolean = true;
  protected profileDetails: any = undefined;
  protected auctionDetails: any = {
    data: undefined,
    page: 0,
    morePages: false,
  };
  protected bidDetails: any = {
    data: undefined,
    page: 0,
    morePages: false,
  };
  protected auctionMessage: any = { success: "", error: "" };
  protected bidMessage: any = { success: "", error: "" };
  readonly pageLimit: number = 20;
  readonly showAdd: boolean = false;

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
    private auth: AuthService,
    private loading: LoadingService,
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
    this.showAdd = this.auth.user.id == this.profileId;
    this.loading.show();
    this.get_init_data();
    this.loading.hide();
  }

  async get_init_data() {
    this.profileDetails = await this.get_items(SERVER_URLS.get_account.url);
    if (this.profileDetails && this.profileDetails?.username) {
      this.auctionMessage.success = `Items auctioned by ${this.profileDetails.username}.`;
      this.auctionMessage.error = `${this.profileDetails.username} has not put up any item for auction.`;
      this.bidMessage.success = `Items bid by ${this.profileDetails.username}.`;
      this.bidMessage.error = `${this.profileDetails.username} has not bid on any item yet.`;
    }
    this.update_auction(1);

    // bids made by a user are only shown for that user or staff & admin users
    if (
      this.auth.user.id == this.profileId ||
      staff_access.includes(this.auth.user.role)
    ) {
      this.update_bid(1);
    }
  }

  async update_auction(page: number) {
    this.get_items(SERVER_URLS.user_items, page, this.auctionDetails).then(
      (response) => {
        this.auctionDetails = response;
      },
    );
  }

  async update_bid(page: number) {
    this.get_items(SERVER_URLS.user_bids, page, this.bidDetails).then(
      (response) => {
        this.bidDetails = response;
      },
    );
  }

  async get_items(
    server_url: string,
    page: number = 0,
    old_item: any = undefined,
  ) {
    const url = server_url + this.profileId;
    let body = {};
    if (page) {
      body = {
        page: page,
      };
    }
    try {
      const response: any = await this.http
        .get(url, { responseType: "json", params: body })
        .toPromise();
      if (response) {
        return page
          ? {
              data: response,
              page: page,
              morePages: response.length < this.pageLimit ? false : true,
            }
          : response;
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      if (page) {
        old_item.morePages = false;
      }
    }
    return old_item;
  }
  sample() {}
  ngOnInit() {}
}
