from model.user import User
import os
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np



class Instructor(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="instructor", email="", display_name="", job_title="", course_id_list=[]):
        super().__init__(uid, username, password, register_time, role)
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    def __str__(self):
        # return (str(self.uid) + ";;;" + str(self.username)
        #         + ";;;" + str(self.password) + ";;;" + str(self.register_time)
        #         + ";;;" + str(self.role) + ";;;" + str(self.email) + ";;;" + str(self.display_name)
        #         + ";;;" + str(self.job_title) + ";;;" + "--".join(self.course_id_list))
        return ";;;".join([str(self.uid), self.username, self.encrypt_password(self.password), self.register_time, self.role,
                           self.email, self.display_name, self.job_title, "--".join(self.course_id_list)])

    def get_instructors(self):
        """
        START OF OLD WORKING CODE
        # with open("data/user.txt", "a+", encoding="utf-8", errors="ignore") as user_file:
        #     # user_file.seek(0, 0)
        #     instr_list = []
        #     for dirpath, dirs, files in os.walk("data\\source_course_files"):
        #         for filename in files:
        #             fname = os.path.join(dirpath, filename)
        #             with open(fname, "r", errors="ignore") as myfile:
        #             #     print(myfile.read())
        #                 values = json.load(myfile)
        #                 for course in values["unitinfo"]["items"]:
        #                     for instr in course["visible_instructors"]:
        #                         user_file.seek(0, 0)
        #                         for line in user_file:
        #                             if line.split(";;;")[0] == str(instr["id"]):
        #                                 instr_list.append(instr["id"])
        #                                 break
        #                         if instr["id"] not in instr_list:
        #                             instr_list.append(instr["id"])
        #                             curr_id = instr["id"]
        #                             instr_course_list = []
        #                             for dirpath2, dirs2, files2 in os.walk("data\\source_course_files"):
        #                                 for filename2 in files2:
        #                                     fname2 = os.path.join(dirpath2, filename2)
        #                                     with open(fname2, "r", errors="ignore") as myfile2:
        #                                         #     print(myfile2.read())
        #                                         values2 = json.load(myfile2)
        #                                         for course2 in values2["unitinfo"]["items"]:
        #                                             for instr2 in course2["visible_instructors"]:
        #                                                 if instr2["id"] == curr_id:
        #                                                     instr_course_list.append(str(course2["id"]))
        #                             username = instr["display_name"].lower().replace(" ", "_")
        #                             user_file.write(";;;".join( [str(instr["id"]), username, self.encrypt_password(str(instr["id"])),
        #                                             "yyyy-MM-dd_HH:mm:ss.SSS", "instructor", username+"@gmail.com",
        #                                             instr["display_name"], instr["job_title"], "--".join(instr_course_list)] ) + "\n")
        END OF OLD WORKING CODE
        """

        """
        NEW LOGIC UNDER CURRENT USE
        1. Read all the instructors from all json files, and store them in a dict(instr_dict) of dict items of the format 
            {instr["id"]: [instr["display_name"], instr["job_title"], [course["id"],]]}
        2. Read all instructors from data/user.txt and store their id's in a list of integers(id_list)
        3. Open the data/user.txt in append mode
        4. for each instr in instr_list, if instr["id"] not in id_list, write this as a new instructor string
        """

        instr_dict = {}
        for dirpath, dirs, files in os.walk("data/source_course_files"):
            for filename in files:
                fname = os.path.join(dirpath, filename)
                with open(fname, "r", errors="ignore") as myfile:
                #     print(myfile.read())
                    values = json.load(myfile)
                    for course in values["unitinfo"]["items"]:
                        for instr in course["visible_instructors"]:
                            if instr["id"] not in instr_dict:
                                instr_dict[instr["id"]] = [instr["display_name"], instr["job_title"], [str(course["id"])]]
                            else:
                                instr_dict[instr["id"]][2].append(str(course["id"]))
        id_list = []
        with open("data/user.txt", "a+", encoding="utf-8") as user_file:
            user_file.seek(0, 0)
            for line in user_file:
                id_list.append(int(line.split(";;;")[0]))
            for item in instr_dict:
                if item not in id_list:
                    username = instr_dict[item][0].lower().replace(" ", "_")
                    user_file.write(";;;".join( [ str(item), username, self.encrypt_password(str(item)),
                                    "yyyy-MM-dd_HH:mm:ss.SSS", "instructor", username+"@gmail.com",
                                    instr_dict[item][0], instr_dict[item][1], "--".join(instr_dict[item][2])] ) + "\n"
                                   )
        return None

    def get_instructors_by_page(self, page):
        instr_list = []
        num_of_pages = 0
        with open("data/user.txt", "r", encoding="utf-8") as user_file:
            for line in user_file:
                if line.split(";;;")[4] == "instructor":
                    instr_list.append(Instructor(int(line.split(";;;")[0]), line.split(";;;")[1],
                                                 line.split(";;;")[2], line.split(";;;")[3], line.split(";;;")[4],
                                                 line.split(";;;")[5], line.split(";;;")[6], line.split(";;;")[7],
                                                 line.strip().split(";;;")[8].split("--")
                                                 )
                                      )
        max_pages = math.ceil(len(instr_list)/20)
        if page == max_pages:
            selected_instr_list = instr_list[20 * (page-1) :]
        elif 0 < page < max_pages:
            selected_instr_list = instr_list[20 * (page-1) : 20 * (page-1) + 20]
        else:
            selected_instr_list = []
        return selected_instr_list, max_pages, len(instr_list)

    def generate_instructor_figure1(self):
        instr_list = []
        num_of_pages = 0
        with open("data/user.txt", "r", encoding="utf-8") as user_file:
            for line in user_file:
                if line.split(";;;")[4] == "instructor":
                    instr_list.append(Instructor(int(line.split(";;;")[0]), line.split(";;;")[1], line.split(";;;")[2],
                                                 line.split(";;;")[3], line.split(";;;")[4], line.split(";;;")[5],
                                                 line.split(";;;")[6], line.split(";;;")[7],
                                                 line.strip().split(";;;")[8].split("--")
                                                 )
                                      )
        instr_list.sort(key=lambda x: len(x.course_id_list), reverse=True)
        top_instr_list = [ ("\n".join(x.display_name.split()[:3]), len(x.course_id_list))
                           for x in instr_list[:10]
                           ]
        labels, ys = zip(*top_instr_list)
        xs = np.arange(len(labels))
        width = 0.7
        plt.rcParams.update({'font.size': 7})
        plt.rcParams.update({'figure.autolayout': True})
        plt.bar(xs, ys, width, align='center')
        plt.xticks(xs, labels)  # Replace default x-ticks with xs, then replace xs with labels
        # plt.xticks(rotation=75)
        plt.yticks(ys)
        for index, value in enumerate(ys):
            plt.text(index, value, str(value), ha="center", va="bottom")
        plt.rcParams.update({'font.size': 12})
        plt.title("Top 10 Instructors Teaching Most Number of Courses", pad=20)
        plt.xlabel("Instructor Title")
        plt.ylabel("Number of Courses")
        # plt.show()
        # return top_instr_list
        plt.savefig("static/img/instructor_figure1.png", bbox_inches="tight", aspect="auto")
        plt.clf()
        return "My understanding: This figure shows the top ten instructors who teach the highest number of courses."


# li = [ len(x.course_id_list) for x in Instructor(123456, "username_two", "passsword_two", "yyyy-MM-dd_HH:mm:ss.SSS", "instructor", "harry@gmail.com", "harry potter", "magic", ["1a", "2b", "3c", "0z", "6f", "4d", "5e"]).generate_instructor_figure1()[:10] ]
# print(li)
# print(repr(Instructor().generate_instructor_figure1()))
# Instructor().get_instructors()