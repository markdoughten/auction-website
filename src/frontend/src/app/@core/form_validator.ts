import { AbstractControl, ValidatorFn } from "@angular/forms";

export function check_duplicate(self: any): ValidatorFn {
  return (c: AbstractControl): { [key: string]: boolean } | null => {
    if (self.duplicate <= 0) {
      return null;
    }
    self.duplicate--;
    return { duplicate: true };
  };
}

export function isValidTime(self: any): ValidatorFn {
  return (control: AbstractControl): { [key: string]: boolean } | null => {
    if (control.value) {
      const date = new Date(control.value - self.tzoffset);
      return date < self.minDate.date || date > self.maxDate.date
        ? { invalidDate: true }
        : null;
    }
    return null;
  };
}

export function isValidClose(self: any): ValidatorFn {
  return (control: AbstractControl): { [key: string]: boolean } | null => {
    const value = control.value;
    const openingDate = self.itemForm?.get("openingTime")?.value;
    if (value && openingDate && new Date(value) < new Date(openingDate)) {
      return { invalidDate: true };
    }
    return null;
  };
}
