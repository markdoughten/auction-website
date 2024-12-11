from enum import Enum

JWT_TOKEN: str = "JWT_TOKEN"
STATUS: str = "status"
MESSAGE: str = "message"
SUCCESS_MSG: str = "Operation was a success"
FAILURE_MSG: str = "Unknown error occurred"
INVALID_REQ: str = "Invalid Request"
NOT_FOUND: str = "Not found"

class STATUS_RESPONSE(Enum):
    SUCCESS = 0
    FAILURE = 1
    MISSING_TOKEN = 2


class USER_ROLE(Enum):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    USER = 'User'


CREATE_NOTIFS_PROCEDURE = '''
CREATE PROCEDURE IF NOT EXISTS create_notifications (
    IN in_item_id int,
    IN in_attribute_id int,
    IN in_attribute_value varchar(255),
    IN in_category_id int,
    IN in_subcategory_id int
)
BEGIN
    INSERT INTO notifications (user_id,item_id)
    SELECT a.user_id, in_item_id
    from alerts a
    where a.category_id = in_category_id and
          a.subcategory_id = in_subcategory_id and
          a.attribute_id = in_attribute_id and
          a.attribute_value = in_attribute_value;
end;'''

CREATE_NOTIFS_TRIGGER = '''
CREATE TRIGGER IF NOT EXISTS notify_user
AFTER INSERT on item_attributes
FOR EACH ROW
BEGIN
    SELECT
        ia.item_id, ia.attribute_id, ia.attribute_value, i.category_id, i.subcategory_id
        into @p_item_id, @p_attribute_id, @p_attribute_value, @p_category_id, @p_subcategory_id
    FROM item_attributes ia join items i on ia.item_id=i.id
    where ia.item_id=new.item_id and
          ia.attribute_id=new.attribute_id;
    CALL create_notifications(@p_item_id, @p_attribute_id, @p_attribute_value, @p_category_id, @p_subcategory_id);
end;'''