import { API_URL } from "../env";

export const SERVER_URLS = {
  signup: { url: API_URL + "/users", request: "post", id: -1 },
  login: API_URL + "/user/login",
  create_account: { url: API_URL + "/c_account", request: "post", id: -1 },
  get_accounts: API_URL + "/users",
  get_account: { url: API_URL + "/users/", request: "post", id: -1 },
  update_user: { url: API_URL + "/users/", request: "put", id: -1 },
  delete_user: API_URL + "/users/",
  get_user_items: API_URL + "/users/items/",
  get_user_bids: API_URL + "/users/bids/",
  get_auction_items: API_URL + "/auctions_all",
  get_auction_item: API_URL + "/auctions/",
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
