def user_model_to_api_resp(user):
    resp = user.to_dict()
    del resp["password"]
    return resp