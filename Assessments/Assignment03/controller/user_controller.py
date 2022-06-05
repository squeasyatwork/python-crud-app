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
    field_list = [x for x in login_user_str.split(";;;")]
    if field_list[4].strip() == "admin":
        return Admin(int(field_list[0]), field_list[1], field_list[2], field_list[3], field_list[4].strip())
    elif field_list[4] == "student":
        return Student(int(field_list[0]), field_list[1], field_list[2], field_list[3], field_list[4], field_list[5].strip())
    elif field_list[4] == "instructor":
        return Instructor(int(field_list[0]), field_list[1], field_list[2], field_list[3], field_list[4],
                          field_list[5], field_list[6], field_list[7], field_list[8].strip().split("--"))


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
                usr.uid = int(user_info.split(";;;")[0])
                usr.role = user_info.split(";;;")[4]
                usr = generate_user(user_info)
                User.current_login_user = usr
                # print("LOGIN SUCCESS!!", user_info)
                print(User.current_login_user.role)
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
    return redirect(url_for("index_page.index"))


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
                print(register_time)
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


@user_page.route("/student-list", methods=["GET"])
def student_list():
    if User.current_login_user is not None:
        context = {}
        context["current_user_role"] = User.current_login_user.role
        context["one_page_user_list"], context["total_pages"], context["total_num"] = Student().get_students_by_page(1)
        context["current_page"] = int(request.values["page"]) if "page" in request.values and request.values["page"].isnumeric() and int(request.values["page"]) <= int(context["total_pages"]) else 1
        context["one_page_user_list"], context["total_pages"], context["total_num"] = Student().get_students_by_page(int(context["current_page"]))
        context["page_num_list"] = [i + 1 for i in range(context["total_pages"])]
        if context["one_page_user_list"] is None:
            context["one_page_user_list"] = []
    else:
        return redirect(url_for("index_page.index"))
    return render_template("10student_list.html", **context)


@user_page.route("/student-info", methods=["GET"])
def student_info():
    if User.current_login_user is not None:
        context = {}
        context["current_user_role"] = User.current_login_user.role
        if context["current_user_role"] == "admin":
            context["student"] = Student().get_student_by_id(int(request.values["id"])) if "id" in request.values and Student().get_student_by_id(int(request.values["id"])) is not None else Student()
        elif context["current_user_role"] == "student":
            context["student"] = Student().get_student_by_id(User.current_login_user.uid)
    else:
        return redirect(url_for("index_page.index"))
    return render_template("11student_info.html", **context)


@user_page.route("/student-delete", methods=["GET"])
def student_delete():
    if User.current_login_user is not None:
        context = {}
        context["current_user_role"] = User.current_login_user.role
        Student().delete_student_by_id(int(request.values["id"]))
    else:
        return redirect(url_for("index_page.index"))
    return redirect(url_for("user_page.student_list"))
