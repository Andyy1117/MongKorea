from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from models.user import *

portfolio_blueprint = Blueprint('portfolio_api_blueprint', __name__)

@portfolio_blueprint.route('/', methods=["GET"])
def index():
    database = UserDB(g.mysql_db, g.mysql_cursor)
    if request.method == "POST":
        uids = request.form.get("user_name")
        for uid in uids:
            database.delete_user_by_id(id)

    return render_template('index.html')