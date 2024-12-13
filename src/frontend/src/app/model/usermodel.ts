export interface UserModel {
  id: number;
  username: string;
  email: string;
  role: string;
}

export const R_ADMIN = "Admin";
export const R_STAFF = "Staff";
export const R_USER = "User";
export const admin_access = [R_ADMIN];
export const staff_access = [...admin_access, R_STAFF];
export const all_access = [...staff_access, R_USER];
