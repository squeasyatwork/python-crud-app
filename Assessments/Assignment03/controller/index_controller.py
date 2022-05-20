
from flask import render_template, Blueprint

from model.user import User
from model.user_admin import Admin


index_page = Blueprint("index_page", __name__)

@index_page.route("/")
def index():
    # check the class variable User.current_login_user

    # manually register an admin account when open index page


    pass


