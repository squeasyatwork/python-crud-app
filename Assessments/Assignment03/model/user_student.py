from model.user import User
import math
import matplotlib.pyplot as plt, numpy as np


class Student(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student", email=""):
        super().__init__(uid, username, password, register_time, role)
        self.email = email

    def __str__(self):
        """
          Overridden dunder method that returns the user id, username,
          password, register time, and role as a string delimited by ";;;"
        """
        return (str(self.uid) + ";;;" + str(self.username)
                + ";;;" + self.encrypt_password(self.password) + ";;;" + str(self.register_time)
                + ";;;" + str(self.role) + ";;;" + str(self.email))

    def get_students_by_page(self, page):
        stud_list = []
        num_of_pages = 0
        with open("data\\user.txt", "r", encoding="utf-8") as user_file:
            for line in user_file:
                if line.split(";;;")[4] == "student":
                    stud_list.append(Student(int(line.split(";;;")[0]), line.split(";;;")[1], line.split(";;;")[2],
                                                 line.split(";;;")[3], line.split(";;;")[4], line.split(";;;")[5]))
        max_pages = math.ceil(len(stud_list) / 20)
        page_num_list = [i+1 for i in range(max_pages)]
        if page == max_pages:
            selected_stud_list = stud_list[20 * (page - 1):]
        elif 0 < page < max_pages:
            selected_stud_list = stud_list[20 * (page - 1): 20 * (page - 1) + 20]
        else:
            selected_stud_list = []
        return selected_stud_list, max_pages, len(stud_list)

    def get_student_by_id(self, uid):
        with open("data\\user.txt", "r", encoding="utf-8") as user_file:
            for line in user_file:
                if line.split(";;;")[0] == str(uid):
                    return Student(int(line.split(";;;")[0]), line.split(";;;")[1], line.split(";;;")[2],
                                                 line.split(";;;")[3], line.split(";;;")[4], line.split(";;;")[5])
        return None

    def delete_student_by_id(self, uid):
        with open("data\\user.txt", "r", encoding="utf-8") as user_file:
            lines = user_file.readlines()
        with open("..\\data\\user.txt", "w", encoding="utf-8") as user_file:
            for line in lines:
                if line.split(";;;")[0] != str(uid):
                    user_file.write(line)
            return None


# Student().delete_student_by_id("123881")