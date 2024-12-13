import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterLink } from "@angular/router";
import { PageComponent } from "@components/page/page.component";

@Component({
  selector: "app-bids",
  standalone: true,
  imports: [CommonModule, RouterLink, PageComponent],
  templateUrl: "./bids.component.html",
})
export class BidsComponent implements OnInit {
  @Input() succMsg: string = "Items that were bid";
  @Input() errMsg: string =
    "There are no bids to display at the moment. Please check back later.";
  @Input() bidItems: any = [];
  @Input() showBid: boolean = false;
  @Input() currentPage = 1;
  @Input() hasMorePages: boolean = true;
  @Output() updatePage = new EventEmitter<number>();

  constructor() {}

  ngOnInit(): void {}

  changePage(page: number) {
    this.updatePage.emit(page);
  }
}
