import { catchError, interval, Subscription, throwError } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AuctionComponent } from "@components/auction/auction.component";
import { SERVER_URLS } from "@core/constants";
import { LoadingService } from "@core/loading.service";

@Component({
  selector: "app-dashboard",
  standalone: true,
  imports: [AuctionComponent, CommonModule],
  templateUrl: "./dashboard.component.html",
})
export class DashboardComponent implements OnInit {
  private subscription?: Subscription;
  protected page: number = 1;
  protected morePages: boolean = false;
  message: string = "Items currently being sold";
  auctionItems: any = undefined;

  constructor(
    private http: HttpClient,
    private loading: LoadingService,
  ) {}

  ngOnInit(): void {
    const timer$ = interval(15000);
    this.subscription = timer$.subscribe(() => {
      this.get_items_data(this.page);
    });
    this.loading.show();
    this.get_items_data(this.page);
    this.loading.hide();
  }

  get_items_data(page: any) {
    this.http.get(SERVER_URLS.auctions, { params: { page: 1 } }).subscribe({
      next: (response: any) => {
        this.auctionItems = response;
        this.page = page;
        if (response.length < 20) {
          this.morePages = false;
        }
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
