from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.user import User
from model.course import Course
from model.user_instructor import Instructor
#
# import pandas as pd
#

course_page = Blueprint("course_page", __name__)

model_course = Course()
model_instructor = Instructor()
model_user = User()



@course_page.route("/reset-database", methods=["POST"])
def reset_database():
    try:
        model_user.clear_user_data()
        model_course.clear_course_data()
    except:
        return render_err_result(msg="exception happened")
    return render_result(), redirect(url_for("index_page.index"))


@course_page.route("/course-list", methods=["GET"])
def course_list():
    context = {}
    if User.current_login_user is not None:
        req = request.values
        page = req['page'] if "page" in req else 1

        # get values for one_page_course_list, total_pages, total_num

        # check one_page_course_list, make sure this variable not be None, if None, assign it to []

        # get values for page_num_list
        context["total_pages"] = model_course.get_courses_by_page(1)[1]
        context["current_page"] = int(request.values["page"]) if "page" in request.values and request.values[
            "page"].isnumeric() and int(request.values["page"]) <= int(context["total_pages"]) else 1
        context["one_page_course_list"], context["total_pages"], context[
            "total_num"] = model_course.get_courses_by_page(
            int(context["current_page"]))
        context["page_num_list"] = model_course.generate_page_num_list(int(context["current_page"]),
                                                                       int(context["total_pages"]))
        if context["one_page_course_list"] is None:
            context["one_page_course_list"] = []

        # context['one_page_course_list'] = one_page_course_list
        # context['total_pages'] = total_pages
        # context['page_num_list'] = page_num_list
        # context['current_page'] = int(page)
        # context['total_num'] = total_num

        # add "current_user_role" to context
        context["current_user_role"] = User.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))
    return render_template("02course_list.html", **context)


@course_page.route("/process-course", methods=["POST"])
def process_course():
    try:
        model_course.get_courses()
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process course")

    return render_result(msg="process course finished successfully")


@course_page.route("/course-details")
def course_details():
    context = {}
    if User.current_login_user:
        req = request.values
        course_id = req['id'] if "id" in req and req["id"].isnumeric() and Course().get_course_by_course_id(int(req["id"])) is not None else -1

        if course_id == -1:
            course = None
        else:
            course, overall_comment = model_course.get_course_by_course_id(int(course_id))

        if not course:
            context["course_error_msg"] = "Error, cannot find course"
        else:
            context['course'] = course
            context['overall_comment'] = overall_comment
        context['current_user_role'] = User.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))
    return render_template("03course_details.html", **context)


@course_page.route("/course-delete")
def course_delete():
    req = request.values
    course_id = req['id'] if "id" in req else -1
    print("course to delete:", course_id)
    if course_id == -1:
        return render_err_result(msg="course cannot find")
    result = model_course.delete_course_by_id(int(course_id))
    print("course deletion successful?", result)
    if result:
        return redirect(url_for("course_page.course_list"))
    else:
        return render_err_result(msg="course delete error")


@course_page.route("/course-analysis")
def course_analysis():
    context = {}
    if User.current_login_user:
        try:
            explain1 = model_course.generate_course_figure1()
            explain2 = model_course.generate_course_figure2()
            explain3 = model_course.generate_course_figure3()
            explain4 = model_course.generate_course_figure4()
            explain5 = model_course.generate_course_figure5()
            explain6 = model_course.generate_course_figure6()
        except:
            return render_err_result(msg="No courses in database! Process Course Data first")
        context['explain1'] = explain1
        context['explain2'] = explain2
        context['explain3'] = explain3
        context['explain4'] = explain4
        context['explain5'] = explain5
        context['explain6'] = explain6
        context['current_user_role'] = User.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))


    return render_template("04course_analysis.html", **context)