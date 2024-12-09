import { Component, OnInit } from "@angular/core";
import { NavbarComponent } from "@components/navbar/navbar.component";
import { AuctionComponent } from "@components/auction/auction.component";
import { HttpClient } from "@angular/common/http";
import { catchError, interval, Subscription, throwError } from "rxjs";
import { RESPONSE_STATUS, SERVER_URLS } from "@core/constants";

@Component({
  selector: "app-dashboard",
  standalone: true,
  imports: [NavbarComponent, AuctionComponent],
  templateUrl: "./dashboard.component.html",
  styleUrl: "./dashboard.component.css",
})
export class DashboardComponent implements OnInit {
  private subscription?: Subscription;
  message: string = "Items currently being sold";
  auctionItems: any = undefined;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const timer$ = interval(15000);
    this.subscription = timer$.subscribe(() => {
      this.get_items_data();
    });
    this.get_items_data();
  }

  get_items_data() {
    const self = this;
    this.http
      .get(SERVER_URLS.get_auction_items, { responseType: "json" })
      .pipe(
        catchError((error) => {
          return throwError(error);
        }),
      )
      .subscribe(
        (response: any) => {
          if (response.status == RESPONSE_STATUS.SUCCESS) {
            self.auctionItems = response.data;
          } else {
            alert(response.message);
          }
        },
        (err) => {
          alert(err.error.message);
        },
      );
  }

  ngOnDestroy() {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
