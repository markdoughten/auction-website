import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";

export function check_duplicate(self: any): ValidatorFn {
  return (c: AbstractControl): { [key: string]: boolean } | null => {
    if (self.duplicate <= 0) {
      return null;
    }
    self.duplicate--;
    return { duplicate: true };
  };
}
