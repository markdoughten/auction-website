def zip_item_attrs(attrs_meta, attrs_vals):
    attr_id_to_name = {}
    for attr in attrs_meta:
        attr_id_to_name[attr["id"]] = attr["attributeName"]
    
    out = []
    for attr in attrs_vals:
        ret = {}
        ret["attributeId"] = attr["attributeId"]
        ret["attributeName"] = attr_id_to_name[attr["attributeId"]]
        ret["attributeValue"] = attr["attributeValue"]
        out.append(ret)
    
    return out


def item_model_to_api_resp(item):
    resp = item.to_dict(True,True)
    resp["categoryName"] = resp["meta"]["category"]["categoryName"]
    resp["subcategoryName"] = resp["meta"]["subcategoryName"]
    resp["attributes"] = zip_item_attrs(resp["meta"]["attributes"], resp["attributes"])
    del resp["meta"]

    return resp
