from .user import user_model_to_api_resp
from .item import item_match_by_attr, zip_item_attrs

def auction_model_to_api_resp(auction):
    resp = auction.to_dict(True,True)
    del resp["seller"]["password"]

    resp["categoryName"] = resp["item"]["meta"]["category"]["categoryName"]
    resp["subcategoryName"] = resp["item"]["meta"]["subcategoryName"]
    resp["item"]["attributes"] = zip_item_attrs(resp["item"]["meta"]["attributes"], resp["item"]["attributes"])
    del resp["item"]["meta"]


    return resp


def filter_auctions_by_attr(auctions, attr_id, attr_value):
    out = []
    for auction in auctions:
        item = auction["item"]
        if item_match_by_attr(item, attr_id, attr_value):
            out.append(auction)
    return out