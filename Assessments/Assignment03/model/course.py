import os
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np


class Course:

    def __init__(self, category_title="", subcategory_id=-1, subcategory_title="", subcategory_description="",
                 subcategory_url="", course_id=-1, course_title="", course_url="", num_of_subscribers=0,
                 avg_rating=0.0, num_of_reviews=0):
        self.category_title = category_title
        self.subcategory_id = subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews

    def __str__(self):
        return (self.category_title + ";;;" + self.subcategory_id + ";;;" + self.subcategory_title + ";;;" + self.subcategory_description + ";;;"
                    + self.subcategory_url + ";;;" + self.course_id + ";;;" + self.course_title + ";;;"
                     + self.course_url + ";;;" + self.num_of_subscribers + ";;;" + self.avg_rating + ";;;" + self.num_of_reviews)

    def get_courses(self):
        for dirpath, dirs, files in os.walk("data\\source_course_files"):
            for filename in files:
                fname = os.path.join(dirpath, filename)
                with open(fname, "r", errors="ignore") as myfile:
                #     print(myfile.read())
                    values = json.load(myfile)
                    str_one = values["unitinfo"]["category"] if \
                        values["unitinfo"]["category"] is not None else "null"
                    str_two = str(values["unitinfo"]["source_objects"][0]["id"]) if \
                        values["unitinfo"]["source_objects"][0]["id"] is not None else "null"
                    str_three = values["unitinfo"]["source_objects"][0]["title"] if \
                        values["unitinfo"]["source_objects"][0]["title"] is not None else "null"
                    str_four = values["unitinfo"]["source_objects"][0]["description"] if \
                        values["unitinfo"]["source_objects"][0]["description"] is not None else "null"
                    str_five = values["unitinfo"]["source_objects"][0]["url"] if \
                        values["unitinfo"]["source_objects"][0]["url"] is not None else "null"
                    for course in values["unitinfo"]["items"]:
                        str_six = str(course["id"]) if course["id"] is not None else "null"
                        str_seven = course["title"] if course["title"] is not None else "null"
                        str_eight = course["url"] if course["url"] is not None else "null"
                        str_nine = str(course["num_subscribers"]) if course["num_subscribers"] is not None else "null"
                        str_ten = str(course["avg_rating"]) if course["avg_rating"] is not None else "null"
                        str_eleven = str(course["num_reviews"]) if course["num_reviews"] is not None else "null"
                        course_str = ";;;".join([str_one, str_two, str_three, str_four, str_five, str_six,
                                                 str_seven, str_eight, str_nine, str_ten, str_eleven])
                        with open("..\\data\\course.txt", "a", encoding="utf-8") as course_file:
                            course_file.write(course_str + "\n")
                        # cnt += 1
        # print(cnt)
        return None

    def clear_course_data(self):
        with open("data\\course.txt", "w") as course_file:
            pass
        return None

    def generate_page_num_list(self, page, total_pages):
        page_num_list = [x+1 for x in range(9)]
        if 5 < page < total_pages - 4:
            page_num_list = [x for x in range(page-4, page+5)]
        elif page >= total_pages - 4:
            page_num_list = [x for x in range(total_pages - 8, total_pages+1)]
        return page_num_list

    def get_courses_by_page(self, page):
        pass

    def delete_course_by_id(self, temp_course_id):
        pass

    def get_course_by_course_id(self, temp_course_id):
        pass

    def get_course_by_instructor_id(self, instructor_id):
        pass

    def generate_course_figure1(self):
        pass

    def generate_course_figure2(self):
        pass

    def generate_course_figure3(self):
        pass

    def generate_course_figure4(self):
        pass

    def generate_course_figure5(self):
        pass

    def generate_course_figure6(self):
        pass


# print(Course().generate_page_num_list(17,20))