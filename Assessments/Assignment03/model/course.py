import os
import json
import math
# import matplotlib
# matplotlib.use('Agg')
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
        self.clear_course_data()
        for dirpath, dirs, files in os.walk("data/source_course_files"):
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
                        with open("data/course.txt", "a", encoding="utf-8") as course_file:
                            course_file.write(course_str + "\n")
                        # cnt += 1
        # print(cnt)
        return None

    def clear_course_data(self):
        with open("data/course.txt", "w") as course_file:
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
        course_list = []
        num_of_pages = 0
        with open("data/course.txt", "r", encoding="utf-8") as course_file:
            for line in course_file:
                course_list.append(Course(line.split(";;;")[0], int(line.split(";;;")[1]), line.split(";;;")[2],
                                             line.split(";;;")[3], line.split(";;;")[4], int(line.split(";;;")[5]),
                                             line.split(";;;")[6], line.split(";;;")[7], int(line.strip().split(";;;")[8]),
                                             float(line.strip().split(";;;")[9]), int(line.strip("\n").split(";;;")[10])))
        max_pages = math.ceil(len(course_list) / 20)
        if page == max_pages:
            selected_course_list = course_list[20 * (page - 1):]
        elif 0 < page < max_pages:
            selected_course_list = course_list[20 * (page - 1): 20 * (page - 1) + 20]
        else:
            selected_course_list = []
        return selected_course_list, max_pages, len(course_list)

    def delete_course_by_id(self, temp_course_id):
        del_result = False
        lines = []
        with open("data/course.txt", "r", encoding="utf-8") as course_file:
            lines = course_file.readlines()
        with open("data/course.txt", "w", encoding="utf-8") as course_file:
            for line in lines:
                if int(line.split(";;;")[5]) != int(temp_course_id):
                    course_file.write(line)
                else:
                    del_result = True
        if del_result:
            with open("data/user.txt", "r", encoding="utf-8") as user_file:
                lines = user_file.readlines()
            with open("data/user.txt", "w", encoding="utf-8") as user_file:
                for line in lines:
                    if line.strip("\n").split(";;;")[4] == "instructor" and str(temp_course_id) in line.strip("\n").split(";;;")[8].split("--"):
                        instr_entry_list = line.strip().split(";;;")[:8]
                        course_ids_list = line.strip("\n").split(";;;")[8].split("--")
                        course_ids_list.remove(str(temp_course_id))
                        course_ids_string = "--".join(course_ids_list) + "\n"
                        user_file.write( ";;;".join(instr_entry_list) + ";;;" + course_ids_string )
                    else:
                        user_file.write(line)
        return del_result

    def get_course_by_course_id(self, temp_course_id):
        course_obj = None
        comment = ""
        with open("data/course.txt", "r", encoding="utf-8") as course_file:
            for line in course_file:
                if int(line.split(";;;")[5]) == int(temp_course_id):
                    course_obj = Course(line.split(";;;")[0], int(line.split(";;;")[1]), line.split(";;;")[2],
                                             line.split(";;;")[3], line.split(";;;")[4], int(line.split(";;;")[5]),
                                             line.split(";;;")[6], line.split(";;;")[7], int(line.strip().split(";;;")[8]),
                                             float(line.strip().split(";;;")[9]), int(line.strip("\n").split(";;;")[10]))
                    if course_obj.num_of_subscribers > 100000 and course_obj.avg_rating > 4.5 and course_obj.num_of_reviews > 10000:
                        comment = "Top Courses"
                    elif course_obj.num_of_subscribers > 50000 and course_obj.avg_rating > 4.0 and course_obj.num_of_reviews > 5000:
                        comment = "Popular Courses"
                    elif course_obj.num_of_subscribers > 10000 and course_obj.avg_rating > 3.5 and course_obj.num_of_reviews > 1000:
                        comment = "Good Courses"
                    else:
                        comment = "General Courses"
        return course_obj, comment

    def get_course_by_instructor_id(self, instructor_id):
        with open("data/user.txt", "r", encoding="utf-8") as user_file:
            num_of_courses = 0
            courses_list = []
            for line in user_file:
                if line.strip("\n").split(";;;")[0] == str(instructor_id) and line.strip("\n").split(";;;")[4] == "instructor":
                    courses_list = line.strip("\n").split(";;;")[8].split("--")
                    num_of_courses = len(courses_list)
                    limit = num_of_courses if num_of_courses <= 20 else 20
                    for iter in range(limit):
                        courses_list[iter] = Course().get_course_by_course_id(courses_list[iter])[0]
                        # print(courses_list[iter].course_id, " ", iter)
        return courses_list, num_of_courses

    def generate_course_figure1(self):
        subcat_dict = {}
        with open("../data/course.txt", "r", encoding="utf-8") as course_file:
            for line in course_file:
                if line.strip("\n").split(";;;")[2] is not None and line.strip("\n").split(";;;")[2] not in subcat_dict:
                    subcat_dict[line.strip("\n").split(";;;")[2]] = 0
            course_file.seek(0, 0)
            for line in course_file:
                if line.strip("\n").split(";;;")[2] is not None:
                    subcat_dict[line.strip("\n").split(";;;")[2]] += int(line.strip("\n").split(";;;")[8])
        subcat_list = list(subcat_dict.items())
        subcat_list.sort(key=lambda x: x[1], reverse=True)
        top_subcat_list = [ ( "\n".join(x[0].split()[:3]), x[1] ) for x in subcat_list[:10] ]
        labels, ys = zip(*top_subcat_list)
        xs = np.arange(len(labels))
        width = 0.7
        plt.rcParams.update({'font.size': 7})
        plt.bar(xs, ys, width, align='center')
        plt.xticks(xs, labels)  # Replace default x-ticks with xs, then replace xs with labels
        # plt.xticks(rotation=75)
        plt.yticks(ys)
        for index, value in enumerate(ys):
            plt.text(index, value, str(value), ha="center", va="bottom")
        plt.title("Top 10 Subcategories Having Most Number of Subscribers")
        plt.xlabel("Subcategory Title")
        plt.ylabel("Number of Subscribers")
        plt.show()
        # return top_instr_list
        plt.savefig("../static/img/instructor_figure1.png")
        plt.clf()
        return "My understanding: This figure shows the top ten subcategory of courses that have the highest number of subscribers that have enroled in it."

    def generate_course_figure2(self):
        courses_list = []
        with open("data/course.txt", "r", encoding="utf-8") as course_file:
            for line in course_file:
                if int(line.strip("\n").split(";;;")[10]) > 50000:
                    courses_list.append([ line.strip("\n").split(";;;")[6],
                                          float(line.strip("\n").split(";;;")[9]).__round__(3)
                                          ])
        courses_list.sort(key=lambda x: x[1])
        bottom_courses_list = [ ( "\n".join(x[0].split()[:3]), x[1] ) for x in courses_list[:10] ]
        labels, ys = zip(*bottom_courses_list)
        xs = np.arange(len(labels))
        width = 0.7
        plt.rcParams.update({'font.size': 7})
        plt.bar(xs, ys, width, align='center')
        plt.xticks(xs, labels)  # Replace default x-ticks with xs, then replace xs with labels
        # plt.xticks(rotation=75)
        plt.yticks(ys)
        for index, value in enumerate(ys):
            plt.text(index, value, str(value), ha="center", va="bottom")
        plt.title("Top 10 Courses With Lowest Avg. Rating Having More Than 50000 Reviews")
        plt.xlabel("Course Title")
        plt.ylabel("Rating")
        # plt.show()
        # return top_instr_list
        plt.savefig("static/img/course_figure2.png")
        plt.clf()
        return "My understanding: This figure shows the top ten courses which have received the lowest rating based on more than 50000 reviews."

    def generate_course_figure3(self):
        pass

    def generate_course_figure4(self):
        pass

    def generate_course_figure5(self):
        pass

    def generate_course_figure6(self):
        pass


print(Course().generate_course_figure1())   # lines 538, 683 in user.txt and 833 in course.txt