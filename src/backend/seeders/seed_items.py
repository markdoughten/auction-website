from ..models.item import Item,ItemAttribute
from ..utils.db import db_create_one


items = [
    {
    "categoryId": 1,
    "subcategoryId": 1,
    "name": "shirt1",
    "attributes": [
        {
            "attributeId": 1,
            "attributeValue": "xl"
        },
        {
            "attributeId": 2,
            "attributeValue": "red"
        },
        {
            "attributeId": 3,
            "attributeValue": "cotton"
        },
        {
            "attributeId": 4,
            "attributeValue": "long"
        },
        {
            "attributeId": 5,
            "attributeValue": "collar"
        }
    ]
    },
    {
    "categoryId": 1,
    "subcategoryId": 1,
    "name": "tshirt1",
    "attributes": [
        {
            "attributeId": 1,
            "attributeValue": "m"
        },
        {
            "attributeId": 2,
            "attributeValue": "black"
        },
        {
            "attributeId": 3,
            "attributeValue": "cotton"
        },
        {
            "attributeId": 4,
            "attributeValue": "short"
        },
        {
            "attributeId": 5,
            "attributeValue": "crew"
        }
    ]
    },
    {
    "categoryId": 1,
    "subcategoryId": 2,
    "name": "pants1",
    "attributes": [
        {
            "attributeId": 6,
            "attributeValue": "36"
        },
        {
            "attributeId": 7,
            "attributeValue": "l"
        },
        {
            "attributeId": 8,
            "attributeValue": "blue"
        },
        {
            "attributeId": 9,
            "attributeValue": "track"
        }
    ]
    },
    {
    "categoryId": 1,
    "subcategoryId": 2,
    "name": "jeans1",
    "attributes": [
        {
            "attributeId": 6,
            "attributeValue": "42"
        },
        {
            "attributeId": 7,
            "attributeValue": "xl"
        },
        {
            "attributeId": 8,
            "attributeValue": "black"
        },
        {
            "attributeId": 9,
            "attributeValue": "denim"
        }
    ]
    },
    {
    "categoryId": 1,
    "subcategoryId": 3,
    "name": "shoes1",
    "attributes": [
        {
            "attributeId": 10,
            "attributeValue": "8"
        },
        {
            "attributeId": 11,
            "attributeValue": "white"
        },
        {
            "attributeId": 12,
            "attributeValue": "sneakers"
        },
        {
            "attributeId": 13,
            "attributeValue": "lace"
        }
    ]
    },
    {
    "categoryId": 1,
    "subcategoryId": 3,
    "name": "sandals1",
    "attributes": [
        {
            "attributeId": 10,
            "attributeValue": "9.5"
        },
        {
            "attributeId": 11,
            "attributeValue": "green"
        },
        {
            "attributeId": 12,
            "attributeValue": "sandals"
        },
        {
            "attributeId": 13,
            "attributeValue": "strap"
        }
    ]
    }
]


def seed_items():
    for i in items:
        item = Item(
            name = i["name"],
            category_id = i["categoryId"],
            subcategory_id = i["subcategoryId"]
        )
        db_create_one(item)

        for a in i["attributes"]:
            attr = ItemAttribute(
                item_id = item.id,
                attribute_id = a["attributeId"],
                attribute_value = a["attributeValue"]
            )
            db_create_one(attr)
