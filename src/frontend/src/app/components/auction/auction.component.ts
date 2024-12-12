import { Component, Input, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";

@Component({
  selector: "app-auction",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./auction.component.html",
})
export class AuctionComponent implements OnInit {
  @Input() message: string = "";
  @Input() auctionItems: any = [];
  @Input() showBid: boolean = false;

  constructor() {}

  ngOnInit(): void {}
}
