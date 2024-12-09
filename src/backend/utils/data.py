from datetime import datetime, timedelta
from .. import db
from ..models.auction import Auctions, Bids
from ..models.item import Item, ItemAttribute
from ..models.item_meta import create_new_item, add_item_categ, add_item_attr, MetaItemCategory, MetaItemSubCategory, MetaItemAttribute
from ..models.user import User
from ..utils import constants
from ..utils.hash import get_hash
from sqlalchemy import text

def populate_data():
    try:
        # Delete all existing entries
        print("Deleting all existing entries...")
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=0;'))  # Disable foreign key checks
        MetaItemAttribute.query.delete()
        MetaItemSubCategory.query.delete()
        MetaItemCategory.query.delete()
        ItemAttribute.query.delete()
        Item.query.delete()
        Bids.query.delete()
        Auctions.query.delete()
        User.query.delete()
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=1;'))  # Re-enable foreign key checks
        db.session.commit()
        print("All entries deleted successfully.")

        # Adding Categories, Subcategories, and Attributes
        print("Adding Categories, Subcategories, and Attributes...")

        # Add a clothing category and related subcategories and attributes
        _, category_created = create_new_item("Clothing")
        print(f"Clothing category created: {category_created}")
        _, tshirts_created = add_item_categ("Clothing", "T-Shirts")
        print(f"T-Shirts subcategory created: {tshirts_created}")
        _, jeans_created = add_item_categ("Clothing", "Jeans")
        print(f"Jeans subcategory created: {jeans_created}")
        _, size_attr_created = add_item_attr("Clothing", "T-Shirts", "Size")
        print(f"T-Shirts size attribute created: {size_attr_created}")
        _, material_attr_created = add_item_attr("Clothing", "T-Shirts", "Material")
        print(f"T-Shirts material attribute created: {material_attr_created}")
        _, color_attr_created = add_item_attr("Clothing", "Jeans", "Color")
        print(f"Jeans color attribute created: {color_attr_created}")

        # Adding Items
        print("Adding Items...")
        tshirt_item = Item(name="Graphic T-Shirt", category_id=MetaItemCategory.query.filter_by(category_name="Clothing").first().id,
                           subcategory_id=MetaItemSubCategory.query.filter_by(subcategory_name="T-Shirts").first().id)
        jeans_item = Item(name="Skinny Jeans", category_id=MetaItemCategory.query.filter_by(category_name="Clothing").first().id,
                          subcategory_id=MetaItemSubCategory.query.filter_by(subcategory_name="Jeans").first().id)
        db.session.add_all([tshirt_item, jeans_item])
        db.session.commit()
        print(f"Items added: {tshirt_item}, {jeans_item}")

        # Adding Users
        print("Adding Users...")
        seller = User(username="clothing_seller", email="seller@example.com", password=get_hash("password123"), role=constants.USER_ROLE.USER)
        buyer = User(username="clothing_buyer", email="buyer@example.com", password=get_hash("password123"), role=constants.USER_ROLE.USER)
        db.session.add_all([seller, buyer])
        db.session.commit()
        print("Users added successfully.")

        # Adding Auctions
        print("Adding Auctions...")
        tshirt_auction = Auctions(
            item_id=tshirt_item.id,
            seller_id=seller.id,
            initial_price=20.0,
            min_increment=2.0,
            min_price=15.0,
            opening_time=datetime.now(),
            closing_time=datetime.now() + timedelta(days=7),
            status="Open"
        )
        jeans_auction = Auctions(
            item_id=jeans_item.id,
            seller_id=seller.id,
            initial_price=50.0,
            min_increment=5.0,
            min_price=40.0,
            opening_time=datetime.now(),
            closing_time=datetime.now() + timedelta(days=7),
            status="Open"
        )
        db.session.add_all([tshirt_auction, jeans_auction])
        db.session.commit()
        print("Auctions added successfully.")

        # Adding Bids
        print("Adding Bids...")
        tshirt_bid = Bids(
            auction_id=tshirt_auction.id,
            users_id=buyer.id,
            bid_value=22.0,
            bid_active=True
        )
        jeans_bid = Bids(
            auction_id=jeans_auction.id,
            users_id=buyer.id,
            bid_value=55.0,
            bid_active=True
        )
        db.session.add_all([tshirt_bid, jeans_bid])
        db.session.commit()
        print("Bids added successfully.")
        print("Dummy data populated successfully.")
    except Exception as e:
        print(f"Error populating data: {e}")
        db.session.rollback()