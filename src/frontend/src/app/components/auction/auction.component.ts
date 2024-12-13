import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { CommonModule, NgClass, NgIf } from "@angular/common";
import { RouterLink } from "@angular/router";
import { PageComponent } from "@components/page/page.component";

@Component({
  selector: "app-auction",
  standalone: true,
  imports: [CommonModule, RouterLink, PageComponent, NgClass, NgIf],
  templateUrl: "./auction.component.html",
})
export class AuctionComponent implements OnInit {
  @Input() succMsg: string = "Items in auction";
  @Input() errMsg: string =
    "There are no items to display at the moment. Please check back later.";
  @Input() auctionItems: any = [];
  @Input() showAdd: boolean = true;
  @Input() currentPage = 1;
  @Input() hasMorePages: boolean = true;
  @Output() updatePage = new EventEmitter<number>();

  constructor() {}

  ngOnInit(): void {}

  changePage(page: number) {
    this.updatePage.emit(page);
  }
}
