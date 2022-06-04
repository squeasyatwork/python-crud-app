
from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(login_user_str):
    login_user = None # a User object

    return login_user


# use @user_page.route("") for each page url
@user_page.route("/login", methods=["GET"])
def login():
    return render_template("00login.html")


@user_page.route("/login", methods=["POST"])
def login_post():
    if request.method == "POST":
        req_list = request.values
        username = req_list["username"] if "username" in req_list else "USERNAME NOT FOUND"
        password = req_list["password"] if "password" in req_list else "PASSWORD ISSUE"
        usr = User(username=username, password=password)
        if usr.validate_username(username) and usr.validate_password(password):
            # print("VALID UN PW VALUES!")
            if usr.authenticate_user(username, password)[0]:
                user_info = usr.authenticate_user(username, password)[1]
                usr.role = user_info.split(";;;")[4]
                User.current_login_user = usr
                # print("LOGIN SUCCESS!!", user_info)
                return render_result(msg="Login success!")
            else:
                # print("WRONG CREDENTIALS!!")
                return render_err_result(msg="Login failure! Wrong credentials.")
        else:
            # print("INVALID VALUE FOR USERNAME/PASSWORD!!!!")
            return render_err_result(msg="Login failure! Enter valid values for username, password and email")
        # print("USERNAME IS:\n", username)

@user_page.route("/logout", methods=["GET"])
def logout():
    User.current_login_user = None
    return render_template("01index.html")


# def generate_user():
#


@user_page.route("/register", methods=["GET"])
def register():
    return render_template("00register.html")


@user_page.route("/register", methods=["POST"])
def register_post():
    if request.method == "POST":
        req_list = request.values
        username = req_list["username"] if "username" in req_list else "USERNAME NOT FOUND"
        password = req_list["password"] if "password" in req_list else "PASSWORD ISSUE"
        email = req_list["email"] if "email" in req_list else "EMAIL ISSUE"
        register_time = req_list["register_time"] if "register_time" in req_list else "TIME ISSUE"
        role = req_list["role"] if "role" in req_list else "ROLE ISSUE"
        usr = User(username=username, password=password)
        if usr.validate_username(username) and usr.validate_password(password) and usr.validate_email(email):
            # print("VALID UN PW VALUES!")
            register_result = usr.register_user(username, password, email, register_time, role)
            if register_result:
                print(render_result())
                return render_result(msg="Registration successful! Login to continue.")
                # print("(print)REGISTER SUCCESS!")
            else:
                return render_err_result(msg="Registration failure! Username already taken.")
                # print("(print)REGISTER FAILED! Username already taken.")
        else:
            return render_err_result(msg="Registration failure! Enter valid values for username, password and email.")
        # print("USERNAME IS:", username)
        # print("PASSWORD IS:", password)
        # print("EMAIL IS:", email)
        # print("TIME IS:", register_time)
        # print("ROLE IS:", role)