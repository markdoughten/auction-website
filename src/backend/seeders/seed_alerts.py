from ..models.alert import Alert
from ..utils.db import db_create_one


alerts = [
    {
        "userId": 1,
        "categoryId": 1,
        "subcategoryId": 1,
        "attributeId": 1,
        "attributeValue": "xl"
    },
    {
        "userId": 10,
        "categoryId": 1,
        "subcategoryId": 1,
        "attributeId": 1,
        "attributeValue": "xl"
    },
    {
        "userId": 20,
        "categoryId": 1,
        "subcategoryId": 1,
        "attributeId": 1,
        "attributeValue": "xl"
    },
        {
        "userId": 2,
        "categoryId": 1,
        "subcategoryId": 3,
        "attributeId": 11,
        "attributeValue": "red"
    },
    {
        "userId": 11,
        "categoryId": 1,
        "subcategoryId": 3,
        "attributeId": 11,
        "attributeValue": "red"
    },
    {
        "userId": 21,
        "categoryId": 1,
        "subcategoryId": 3,
        "attributeId": 11,
        "attributeValue": "red"
    },
]




def seed_alerts():
    for a in alerts:
        alert = Alert(
            user_id = a["userId"],
            category_id = a["categoryId"],
            subcategory_id = a["subcategoryId"],
            attribute_id = a["attributeId"],
            attribute_value = a["attributeValue"]
        )
        db_create_one(alert)

