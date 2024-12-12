import { catchError, interval, Subscription, throwError } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { NavbarComponent } from "@components/navbar/navbar.component";
import { AuctionComponent } from "@components/auction/auction.component";
import { RESPONSE_STATUS, SERVER_URLS } from "@core/constants";
import { LoadingService } from "@core/loading.service";

@Component({
  selector: "app-dashboard",
  standalone: true,
  imports: [NavbarComponent, AuctionComponent, CommonModule],
  templateUrl: "./dashboard.component.html",
})
export class DashboardComponent implements OnInit {
  private subscription?: Subscription;
  message: string = "Items currently being sold";
  auctionItems: any = undefined;

  constructor(
    private http: HttpClient,
    private loading: LoadingService,
  ) {}

  ngOnInit(): void {
    const timer$ = interval(15000);
    this.subscription = timer$.subscribe(() => {
      this.get_items_data();
    });
    this.loading.show();
    this.get_items_data();
    this.loading.hide();
  }

  get_items_data() {
    const self = this;
    this.http
      .get(SERVER_URLS.get_auction_item, { params: { page: 1 } })
      .subscribe({
        next: (response: any) => {
          self.auctionItems = response;
        },
        error: (err) => {
          // alert(err.error.message);
        },
      });
  }

  ngOnDestroy() {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
