import { Component } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { AuctionComponent } from "@components/auction/auction.component";

@Component({
  selector: "app-search",
  standalone: true,
  imports: [AuctionComponent, FormsModule],
  templateUrl: "./search.component.html",
})
export class SearchComponent {
  searchQuery: string = "";
  constructor() {}
  search() {}
}
