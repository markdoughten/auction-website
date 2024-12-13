import { Component, Input } from "@angular/core";
import { ItemFormComponent } from "./item/itemform.component";
import { AuctionFormComponent } from "./auction/auctionform.component";
import { SearchIemComponent } from "./search/search.component";
import { BackButtonComponent } from "@components/backbutton/backbutton.component";
import { NgIf } from "@angular/common";

@Component({
  selector: "app-items",
  standalone: true,
  imports: [
    ItemFormComponent,
    SearchIemComponent,
    AuctionFormComponent,
    NgIf,
    BackButtonComponent,
  ],
  templateUrl: "./base.component.html",
})
export class BaseItemComponent {
  @Input() auctionDetails: any = undefined;
  readonly searchMsg = "Search for an existing item to add it for auction";
  readonly addMsg = "Add a new item for auction";
  readonly useReload = true;
  searchItem: boolean = false;
  message: string = "";
  itemDetails: any = undefined;

  constructor() {
    this.switchMode();
  }
  switchMode() {
    this.searchItem = !this.searchItem;
    this.message = !this.searchItem ? this.searchMsg : this.addMsg;
  }
  itemAdd(itemDetails: any) {
    this.itemDetails = itemDetails;
  }
}
