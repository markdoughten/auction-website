import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";
import { NavigationEnd, Router } from "@angular/router";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: "./app.component.html",
  styleUrl: "./app.component.css",
})
export class AppComponent {
  constructor(private router: Router) {
    this.router.events.subscribe((event) => {
      // console.log(event);
      // if (event instanceof NavigationEnd) {
      //   if (event.url === this.router.url) {
      //     this.router
      //       .navigateByUrl("/", { skipLocationChange: true })
      //       .then(() => {
      //         this.router.navigate([event.url]);
      //       });
      //   }
      // }
    });
  }
}
