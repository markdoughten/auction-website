from ..utils import constants
from ..models.auction import Auctions
from flask import request, jsonify
from flask import current_app as app
from flask_jwt_extended import jwt_required

@app.route('/get_items', methods=["POST"])
@jwt_required()
def get_items():
    output = {}
    if request.method == 'POST':
        Auctions.query.filter()
        return jsonify(output)

    output[constants.STATUS] = constants.STATUS_RESPONSE.FAILURE.value
    output[constants.MESSAGE] = constants.FAILURE_MSG
    return jsonify(output)

@app.route('/add_items', methods=["POST"])
def add_items():
    print("Entered add_items")
    failed = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'dict/meta_items.json')) as f:
        m_itm = json.load(f)
        for item in m_itm:
            categs = m_itm[item]
            for categ in categs:
                attrs = categs[categ]
                for attr in attrs:
                    sub_item, retval = item_meta.add_item_attr(item, categ, attr)
                    if sub_item is None:
                        failed.append((item, categ, attr))
                        print(failed[-1], "add failed")
                    elif not retval:
                        failed.append((item, categ, attr))
                        print(failed[-1], "item already added")

    response = {}
    response[constants.STATUS] = len(failed)
    response[constants.MESSAGE] = failed if len(failed) else "items added successfully"
    return response