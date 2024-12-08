import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { NavbarComponent } from "@components/navbar/navbar.component";

@Component({
  selector: "app-profile",
  standalone: true,
  imports: [CommonModule, NavbarComponent],
  templateUrl: "./profile.component.html",
  styleUrl: "./profile.component.css",
})
export class ProfileComponent implements OnInit {
  productId: string = "";
  auctionItems: any = undefined;
  bidItems: any = undefined;
  showBid: boolean = false;

  constructor(private route: ActivatedRoute) {
    const productId = this.route.snapshot.paramMap.get("id");
    this.productId = productId ? productId : "";
    console.log(this.productId);
  }

  sample() {}
  ngOnInit() {}
}
