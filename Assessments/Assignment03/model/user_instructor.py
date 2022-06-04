from model.user import User
import os
import json
import math
import matplotlib as mpl, pandas as pd


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
        return ";;;".join([str(self.uid), self.username, self.password, self.register_time, self.role,
                           self.email, self.display_name, self.job_title, "--".join(self.course_id_list)])

    def get_instructors(self):
        # dirs_list = [x[2] for x in os.walk("../data/source_course_files")]
        # # for a_file in dirs_list:
        # #     with open(a_file, "r") as file_reader:
        # #         print(file_reader.read(10))
        # print(dirs_list)

        # for filename in os.listdir("..\\data\\source_course_files"):
        #     os.chmod(os.path.join("..\\data\\source_course_files", filename), 666)
        #     with open(os.path.join("..\\data\\source_course_files", filename), 'r') as f:
        #         text = f.read()
        #         print(text)
        # cnt = 0
        # for root, subdirs, files in os.walk("..\\data\\source_course_files"):
        #     for subdir in subdirs:
        #         for root, subdirs, files in os.walk(os.path.join(root, subdir)):
        #             for subdir in subdirs:
        #                 for a_file in os.listdir(os.path.join(root, subdir)):
        #                     with open(os.path.join(root, subdir, a_file), "r") as file_reader:
        #                         cnt += 1
        #                         # print(file_reader.read())
        with open("data\\user.txt", "a+", encoding="utf-8", errors="ignore") as user_file:
            # user_file.seek(0, 0)
            instr_list = []
            for dirpath, dirs, files in os.walk("data\\source_course_files"):
                for filename in files:
                    fname = os.path.join(dirpath, filename)
                    with open(fname, "r", errors="ignore") as myfile:
                    #     print(myfile.read())
                        values = json.load(myfile)
                        for course in values["unitinfo"]["items"]:
                            for instr in course["visible_instructors"]:
                                if instr["id"] not in instr_list:
                                    instr_list.append(instr["id"])
                                    curr_id = instr["id"]
                                    instr_course_list = []
                                    for dirpath2, dirs2, files2 in os.walk("data\\source_course_files"):
                                        for filename2 in files2:
                                            fname2 = os.path.join(dirpath2, filename2)
                                            with open(fname2, "r", errors="ignore") as myfile2:
                                                #     print(myfile2.read())
                                                values2 = json.load(myfile2)
                                                for course2 in values2["unitinfo"]["items"]:
                                                    for instr2 in course2["visible_instructors"]:
                                                        if instr2["id"] == curr_id:
                                                            instr_course_list.append(str(course2["id"]))
                                    username = instr["display_name"].lower().replace(" ", "_")
                                    user_file.write(";;;".join( [str(instr["id"]), username, self.encrypt_password(str(instr["id"])),
                                                    "yyyy-MM-dd_HH:mm:ss.SSS", "instructor", username+"@gmail.com",
                                                    instr["display_name"], instr["job_title"], "--".join(instr_course_list)] ) + "\n")

                                # print(type(instr["id"]))

            #                     flag = 0
            #                     # user_file.write(instr["display_name"]+"\n")
            #
            #                     user_file.seek(0, 0)
            #                     for line in user_file:
            #
            #                         if line.split(";;;")[0] == str(instr["id"]):
            #                             flag = 1
            #                             break
            #                     if flag == 0:
            #                         username = instr["display_name"].lower().replace(" ", "_")
            #                         user_file.write(";;;".join( [str(instr["id"]), username, self.encrypt_password(str(instr["id"])),
            #                                         "yyyy-MM-dd_HH:mm:ss.SSS", "instructor", username+"@gmail.com",
            #                                         instr["display_name"], instr["job_title"]] ) + ";;;\n")
            #                     # if instr["display_name"]:
            #                     #     cnt += 1
            #                     #     print(instr["display_name"])
            #     # for a_file in filesprint(files)
            # user_file.seek(0, 0)
            # for line in user_file:
            #     if line.split(";;;") == "instructor":
            #         instr_course_list = []
            #         instr_course_list.append(line.split(";;;")[0])
            #         for dirpath, dirs, files in os.walk("..\\data\\source_course_files"):
            #             for filename in files:
            #                 fname = os.path.join(dirpath, filename)
            #                 with open(fname, "r", errors="ignore") as myfile:
            #                     #     print(myfile.read())
            #                     values = json.load(myfile)
            #                     for course in values["unitinfo"]["items"]:
            #                         for instr in course["visible_instructors"]:
            #                             if instr["id"] == instr_course_list[0]:
            #                                 instr_course_list.append(course["id"])
            #         user_file.seek(0, 0)



        # print(cnt)
        return None

    def get_instructors_by_page(self, page):
        instr_list = []
        num_of_pages = 0
        with open("..\\data\\user.txt", "r", encoding="utf-8") as user_file:
            for line in user_file:
                if line.split(";;;")[4] == "instructor":
                    instr_list.append(Instructor(int(line.split(";;;")[0]), line.split(";;;")[1], line.split(";;;")[2], line.split(";;;")[3], line.split(";;;")[4], line.split(";;;")[5], line.split(";;;")[6], line.split(";;;")[7], line.strip().split(";;;")[8]))
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
        with open("..\\data\\user.txt", "r", encoding="utf-8") as user_file:
            for line in user_file:
                if line.split(";;;")[4] == "instructor":
                    instr_list.append(Instructor(int(line.split(";;;")[0]), line.split(";;;")[1], line.split(";;;")[2],
                                                 line.split(";;;")[3], line.split(";;;")[4], line.split(";;;")[5],
                                                 line.split(";;;")[6], line.split(";;;")[7],
                                                 line.strip().split(";;;")[8]))



# print(Instructor(123456, "username_two", "passsword_two", "yyyy-MM-dd_HH:mm:ss.SSS", "instructor", "harry@gmail.com", "harry potter", "magic", ["1a", "2b", "3c", "0z", "6f", "4d", "5e"]).get_instructors_by_page(2))