from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.user import User
from model.course import Course

import pandas as pd
from flask import render_template, Blueprint

from model.user_instructor import Instructor

instructor_page = Blueprint("instructor_page", __name__)

model_instructor = Instructor()
model_course = Course()

@instructor_page.route("/instructor-list", methods=["GET"])
def instructor_list():
    if User.current_login_user is not None:
        context = {}
        context["current_user_role"] = User.current_login_user.role
        context["one_page_instructor_list"], context["total_pages"], context["total_num"] = Instructor().get_instructors_by_page(1)
        context["current_page"] = int(request.values["page"]) if "page" in request.values and request.values[
            "page"].isnumeric() and int(request.values["page"]) <= int(context["total_pages"]) else 1
        context["one_page_instructor_list"], context["total_pages"], context["total_num"] = Instructor().get_instructors_by_page(
            int(context["current_page"]))
        context["page_num_list"] = [i + 1 for i in range(context["total_pages"])]
        if context["one_page_instructor_list"] is None:
            context["one_page_instructor_list"] = []

        # context['one_page_instructor_list'] = one_page_instructor_list
        # context['total_pages'] = total_pages
        # context['page_num_list'] = page_num_list
        # context['current_page'] = int(page)
        # context['total_num'] = total_num
        # add "current_user_role" to context
    else:
        return redirect(url_for("index_page.index"))
    return render_template("07instructor_list.html", **context)


@instructor_page.route("/teach-courses", methods=["GET"])
def teach_courses():
    context = {}
    if User.current_login_user is not None:
        context["current_user_role"] = User.current_login_user.role
        if context["current_user_role"] in ["admin", "instructor"]:
            if context["current_user_role"] == "admin" and "id" not in request.values:
                return render_err_result(msg="Course information not available: no Instructor chosen!")
            elif context["current_user_role"] == "instructor" and "id" in request.values:
                return render_err_result(msg="Course information not available: you can only view your own courses!")
            else:
                uid = request.values["id"] if "id" in request.values else User.current_login_user.uid
                try:
                    course_list, total_num = model_course.get_course_by_instructor_id(uid)
                    context['course_list'] = course_list
                    context['total_num'] = total_num
                except:
                    return render_err_result(msg="No courses recorded!")
        else:
            return render_err_result(msg="You do not have the permission to view this information!")

    else:
        return redirect(url_for("index_page.index"))
    return render_template("09instructor_courses.html", **context)



@instructor_page.route("/instructor-analysis")
def instructor_analysis():
    # if Instructor.instructor_data.shape[0] == 0:
    #     return render_err_result(msg="no instructor in datafile")
    if User.current_login_user is not None:
        try:
            explain1 = model_instructor.generate_instructor_figure1()
        except:
            return render_err_result(msg="No instructors in database! Process Instructor Data first")
        # print("right below except!")
        context = {}
        context["current_user_role"] = User.current_login_user.role
        context['explain1'] = explain1
    else:
        return redirect(url_for("index_page.index"))
    # print("right below if loop!")
    return render_template("08instructor_analysis.html", **context)


@instructor_page.route("/process-instructor", methods=["POST"])
def process_instructor():
    try:
        model_instructor.get_instructors()
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process instructors")

    return render_result(msg="process instructors finished successfully")