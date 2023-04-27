"""
task_api.py

Routes for the API and logic for managing Tasks.
"""

from flask import g, request, jsonify, Blueprint

from models.portfolio import Portfolio, PortfolioDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
portfolio_api_blueprint = Blueprint("portfolio_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a task to the end of the url
#   so we can retrieve a specific task or the entire list of tasks as a JSON object
@portfolio_api_blueprint.route('/api/v1/portfolio/', defaults={'task_id':None}, methods=["GET"])
@portfolio_api_blueprint.route('/api/v1/portfolio/<int:task_id>/', methods=["GET"])
def get_portfolios(portfolio_id):
    """
    get_tasks can take urls in a variety of forms:
        * /api/v1/task/ - get all tasks
        * /api/v1/task/1 - get the task with id 1 (or any other valid id)
        * /api/v1/task/?search="eggs" - find all tasks with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the TaskDB object with the mysql connection and cursor objects
    portfoliodb = PortfolioDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the task is not supplied then we are either returning all
    #   tasks or any tasks that match the search query string.
    if portfolio_id is None:
        # Logic to find all or multiple tasks

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = portfoliodb.select_all_description()
        # All tasks matching the query string "search"
        else:
            result = portfoliodb.select_all_portfolio_by_description(args['search'])
    
    else:
        # Logic to request a specific task
        # We get a specific tasks based on the provided task ID
        result = portfoliodb.select_all_portfolios(portfolio_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the tasks found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "portfolios": result}), 200


@portfolio_api_blueprint.route('/api/v1/portfolios/', methods=["POST"])
def add_task():
    portfoliodb = PortfolioDB(g.mysql_db, g.mysql_cursor)
        
    portfolio = Portfolio(request.json['description'])
    result = portfoliodb.insert_task(portfolio)
    
    return jsonify({"status": "success", "id": result['portfolio_id']}), 200


@portfolio_api_blueprint.route('/api/v1/portfolios/<int:portfolio_id>/', methods=["PUT"])
def update_portfolio(portfolio_id):
    portfoliodb = PortfolioDB(g.mysql_db, g.mysql_cursor)

    portfolio = Portfolio(request.json['description'])
    portfoliodb.update_portfolio(portfolio_id, portfolio)
    
    return jsonify({"status": "success", "portfolio_id": portfolio_id}), 200


@portfolio_api_blueprint.route('/api/v1/portfolio/<int:portfolio_id>/', methods=["DELETE"])
def delete_portfolio(portfolio_id):
    portfoliodb = PortfolioDB(g.mysql_db, g.mysql_cursor)

    portfoliodb.delete_portfolio_by_id(portfolio_id)
        
    return jsonify({"status": "success", "id": portfolio_id}), 200
