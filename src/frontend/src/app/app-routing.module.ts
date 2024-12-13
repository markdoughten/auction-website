import { NgModule } from "@angular/core";
import { RouterModule } from "@angular/router";
import { routes } from "./app.routes";

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      urlUpdateStrategy: "deferred",
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
