import { Component, input } from "@angular/core";
import { CommonModule } from "@angular/common";

@Component({
  selector: "app-auction",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./auction.component.html",
  styleUrl: "./auction.component.css",
})
export class AuctionComponent {
  message = input<string>("");
  auctionItems = input<any[]>([]);
}
