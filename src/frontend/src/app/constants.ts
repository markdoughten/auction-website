import { API_URL } from "./env";

export const SERVER_URLS = {
  signup: API_URL + "/signup",
  login: API_URL + "/login",
};

export const RESPONSE_STATUS = {
  SUCCESS: "0",
};

export const IS_REQUIRED = "This is required";
export const NOT_EMAIL = "This is not an email";
export const MIN_LEN = "Minimum Length is 5";
