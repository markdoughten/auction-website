import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";
import { NavbarComponent } from "@components/navbar/navbar.component";

@Component({
  selector: "app-items",
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: "./itemlanding.component.html",
})
export class ItemLandingComponent {}
