import { API_URL } from "../env";

export const SERVER_URLS = {
  login: API_URL + "/user/login",
  get_accounts: API_URL + "/users",
  signup: { url: API_URL + "/users", request: "post", id: -1 },
  create_account: { url: API_URL + "/staff", request: "post", id: -1 },
  get_account: { url: API_URL + "/users/", request: "post", id: -1 },
  update_user: { url: API_URL + "/users/", request: "put", id: -1 },
  delete_user: API_URL + "/users/",
  user_items: API_URL + "/users/auctions/",
  user_bids: API_URL + "/users/bids/",
  auctions: API_URL + "/auctions",
  get_meta_items: API_URL + "/item_meta/categories",
  items: API_URL + "/items",
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
export const TOKEN_EXPIRED = "User token expired, please sign in again";
