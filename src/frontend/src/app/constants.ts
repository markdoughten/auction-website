import { API_URL } from "./env";

export const SERVER_URLS = {
  signup: API_URL + "/signup",
  login: API_URL + "/login",
  c_account: API_URL + "/c_account",
};

export const RESPONSE_STATUS = {
  SUCCESS: 0,
  FAILURE: 1,
  MISSING_TOKEN: 2,
};

export const IS_REQUIRED = "This is required";
export const NOT_EMAIL = "This is not an email";
export const MIN_LEN = "Minimum Length is 5";
export const JWT_TOKEN = "JWT_TOKEN";
