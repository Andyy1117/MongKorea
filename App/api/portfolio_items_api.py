from flask import g, request, jsonify, Blueprint
from models.portfolio_item import PortfolioItem, PortfolioItemDB

portfolio_api_blueprint = Blueprint("portfolio_api_blueprint", __name__)


@portfolio_api_blueprint.route('/api/v1/portfolio_items/', defaults={'item_id': None}, methods=["GET"])
@portfolio_api_blueprint.route('/api/v1/portfolio_items/<int:item_id>/', methods=["GET"])
def get_portfolio_items(item_id):
    """
    get_portfolio_items can take urls in a variety of forms:
        * /api/v1/portfolio_items/ - get all portfolio items
        * /api/v1/portfolio_items/1 - get the portfolio item with id 1 (or any other valid id)
        * /api/v1/portfolio_items/?type="web" - find all portfolio items of type "web"
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional
    """

    args = request.args

    portfolio_item_db = PortfolioItemDB(g.mysql_db, g.mysql_cursor)

    result = None

    if item_id is None:
        if not 'type' in args:
            result = portfolio_item_db.select_all_portfolio_items()
        else:
            result = portfolio_item_db.select_portfolio_items_by_type(args['type'])

    else:
        result = portfolio_item_db.select_portfolio_item_by_id(item_id)

    return jsonify({"status": "success", "portfolio_items": result}), 200


@portfolio_api_blueprint.route('/api/v1/portfolio_items/', methods=["POST"])
def add_portfolio_item():
    portfolio_item_db = PortfolioItemDB(g.mysql_db, g.mysql_cursor)

    portfolio_item = PortfolioItem(
        request.json['portfolio_id'],
        request.json['title'],
        request.json['description'],
        request.json['type']
    )
    result = portfolio_item_db.insert_portfolio_item(portfolio_item)

    return jsonify({"status": "success", "id": result['item_id']}), 200


@portfolio_api_blueprint.route('/api/v1/portfolio_items/<int:item_id>/', methods=["PUT"])
def update_portfolio_item(item_id):
    portfolio_item_db = PortfolioItemDB(g.mysql_db, g.mysql_cursor)

    portfolio_item = PortfolioItem(
        request.json['portfolio_id'],
        request.json['title'],
        request.json['description'],
        request.json['type']
    )
    portfolio_item_db.update_portfolio_item(item_id, portfolio_item)

    return jsonify({"status": "success", "id": item_id}), 200


@portfolio_api_blueprint.route('/api/v1/portfolio_items/<int:item_id>/', methods=["DELETE"])
def delete_portfolio_item(item_id):
    portfolio_item_db = PortfolioItemDB(g.mysql_db, g.mysql_cursor)

    portfolio_item_db.delete_portfolio_item_by_id(item_id)

    return jsonify({"status": "success", "id": item_id}), 200