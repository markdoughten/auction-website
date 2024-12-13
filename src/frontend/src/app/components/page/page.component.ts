import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";

@Component({
  selector: "app-page",
  standalone: true,
  imports: [],
  templateUrl: "./page.component.html",
})
export class PageComponent implements OnInit {
  @Input() currentPage: number = 1;
  @Input() hasMorePages: boolean = true;
  @Output() updatePage = new EventEmitter<number>();
  readonly itemsPerPage: number = 20;
  constructor() {}
  changePage(page: number) {
    if (page >= 1 && (page > this.currentPage || this.hasMorePages)) {
      this.updatePage.emit(page);
    }
  }
  ngOnInit(): void {}
}
