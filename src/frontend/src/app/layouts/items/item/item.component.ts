import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { SERVER_URLS } from "@core/constants";

@Component({
  selector: "app-item",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./item.component.html",
})
export class ItemComponent {
  itemId: number = -1;
  item: any = undefined;

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    const profileId = this.route.snapshot.paramMap.get("id");
    this.itemId = profileId ? parseInt(profileId) : -1;
    if (
      this.itemId === undefined ||
      this.itemId === null ||
      isNaN(this.itemId) ||
      this.itemId === -1
    ) {
      alert("User not found...");
      this.router.navigate(["/"]);
    }
    this.get_item_details();
  }

  async get_item_details() {
    const url = SERVER_URLS.auctions + "/" + this.itemId;
    try {
      const response: any = await this.http
        .get(url, { responseType: "json" })
        .toPromise();
      if (response) {
        this.item = response;
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
}
