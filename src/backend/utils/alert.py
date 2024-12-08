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