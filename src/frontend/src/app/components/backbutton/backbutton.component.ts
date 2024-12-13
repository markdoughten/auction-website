import { NgIf } from "@angular/common";
import { Component, EventEmitter, Input, Output } from "@angular/core";
import { RouterLink, RouterLinkActive } from "@angular/router";

@Component({
  selector: "app-back",
  standalone: true,
  imports: [RouterLink, RouterLinkActive, NgIf],
  templateUrl: "./backbutton.component.html",
})
export class BackButtonComponent {
  @Input() href: string = "/";
  @Input() message: string = "Home";
  @Output() trigger = new EventEmitter<any>();
  @Input() linkDisabled: boolean = false;

  triggerEvent() {
    this.trigger.emit();
  }
}
