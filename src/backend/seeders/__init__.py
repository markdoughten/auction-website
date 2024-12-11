from .seed_item_meta import seed_item_meta
from .seed_items import seed_items
from .seed_users import seed_users
from .seed_auctions import seed_auctions
from .seed_bids import seed_bids
from .seed_qa import seed_qa
from .seed_alerts import seed_alerts
from ..utils.db import db_delete_all
from ..models import Alert, Notification, Auctions, Bids, MetaItemAttribute, MetaItemCategory, MetaItemSubCategory, \
Item, ItemAttribute, UserQuestion, UserAnswer, User



def seed_all():
    print("Seeding users")
    seed_users()

    print("Seeding item metadata")
    seed_item_meta()

    print("Seeding items")
    seed_items()

    print("Seeding auctions")
    seed_auctions()

    print("Seeding bids")
    seed_bids()

    print("Seeding Q&A")
    seed_qa()

    print("Seeding alerts")
    seed_alerts()



def delete_all_data():
    print("Deleting all data")
    db_delete_all(Notification)
    db_delete_all(Alert)
    db_delete_all(UserAnswer)
    db_delete_all(UserQuestion)
    db_delete_all(Bids)
    db_delete_all(Auctions)
    db_delete_all(ItemAttribute)
    db_delete_all(Item)
    db_delete_all(MetaItemAttribute)
    db_delete_all(MetaItemSubCategory)
    db_delete_all(MetaItemCategory)
    db_delete_all(User)
