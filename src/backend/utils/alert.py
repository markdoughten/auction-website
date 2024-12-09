from .item import zip_item_attrs

def notification_model_to_api_resp(notification):
    resp = notification.to_dict(True,True)
    resp["item"]["categoryName"] = resp["item"]["meta"]["category"]["categoryName"]
    resp["item"]["subcategoryName"] = resp["item"]["meta"]["subcategoryName"]
    resp["item"]["attributes"] = zip_item_attrs(resp["item"]["meta"]["attributes"], resp["item"]["attributes"])
    del resp["item"]["meta"]
    return resp



def find_attr_name(attributeId, attrs):
    for a in attrs:
        if a["id"] == attributeId:
            return a["attributeName"]

def alert_model_to_api_resp(alert):
    resp = alert.to_dict(True,True)
    resp["attributeName"] = find_attr_name(resp["attributeId"], resp["meta"]["attributes"])
    resp["categoryName"] = resp["meta"]["category"]["categoryName"]
    resp["subcategoryName"] = resp["meta"]["subcategoryName"]
    del resp["meta"]
    return resp