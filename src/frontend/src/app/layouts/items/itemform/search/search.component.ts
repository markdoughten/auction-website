import { NgFor, NgIf } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { Component, EventEmitter, OnInit, Output } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { PageComponent } from "@components/page/page.component";
import { SERVER_URLS } from "@core/constants";

@Component({
  selector: "app-item-search",
  standalone: true,
  imports: [FormsModule, NgIf, NgFor, PageComponent],
  templateUrl: "./search.component.html",
})
export class SearchIemComponent implements OnInit {
  searchQuery: string = "";
  items: any = undefined;
  currentPage: number = 1;
  hasMorePages: boolean = true;
  @Output() success = new EventEmitter<any>();

  constructor(private http: HttpClient) {
    this.getItems(1);
  }

  select(itemDetails: any) {
    this.success.emit(itemDetails);
  }

  search() {}

  getItems(page: number) {
    let params = {
      ...(page && { page: page }),
      ...(this.searchQuery !== "" && { name: this.searchQuery }),
    };
    this.http
      .get(SERVER_URLS.items, {
        responseType: "json",
        params: params,
      })
      .subscribe({
        next: (response: any) => {
          this.items = response;
          this.currentPage = page;
          if (response.length < 20) {
            this.hasMorePages = false;
          }
        },
        error: (error) => {
          if (this.currentPage >= 1) {
            this.hasMorePages = false;
          }
          console.log(error, error.error.message);
        },
      });
  }
  ngOnInit(): void {}
}
