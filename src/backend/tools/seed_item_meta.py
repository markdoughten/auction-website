from .. import db
from ..models.item_meta import MetaItemCategory, MetaItemSubCategory, MetaItemAttribute
from ..db_ops.common import db_create_one


item_meta = {
    "clothing": {
        "shirts": [
            "size",
            "color",
            "material",
            "sleeve",
            "neck"
        ],
        "pants": [
            "waist",
            "size",
            "color",
            "style"
        ],
        "shoes": [
            "size",
            "color",
            "style",
            "closure",
        ]
    }
}



def seed_item_meta():
    for category_name, subcategories in item_meta.items():
        meta_cat = MetaItemCategory(category_name=category_name)
        db_create_one(meta_cat)

        for subcat_name, attrs in subcategories.items():
            meta_subcat = MetaItemSubCategory(category_id = meta_cat.id, subcategory_name=subcat_name)
            db_create_one(meta_subcat)

            for attr in attrs:
                meta_attr = MetaItemAttribute(subcategory_id = meta_subcat.id, attribute_name=attr)
                db_create_one(meta_attr)