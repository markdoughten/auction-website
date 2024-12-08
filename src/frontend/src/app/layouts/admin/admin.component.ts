import { Component, OnInit } from "@angular/core";
import { RouterOutlet } from "@angular/router";
import { NavbarComponent } from "@components/navbar/navbar.component";

@Component({
  selector: "app-admin",
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: "./admin.component.html",
  styleUrl: "./admin.component.css",
})
export class AdminComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}
}
