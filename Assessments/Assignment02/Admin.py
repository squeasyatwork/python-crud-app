from User import User
import re
import os

class Admin(User):
    def __init__(self, id = -1, username = "", password = ""):
        User.__init__(self, id, username, password)

    def register_admin(self):
        username = input("Enter username:")
        flag = 0
        with open("user_admin.txt", "r") as adminFile:
            pattern = re.compile(r';((\w)+);')
            matches = pattern.finditer(adminFile.read())
            for match in matches:
                if(match.groups('1')[0] == username):
                    flag = 1
                    # print("Match found in the line: ", match.__str__())
            if flag == 0:
                # print("Match NOT found")
                adminId = input("Enter ID: ")
                pw = input("Enter password: ")
                adminFile.seek(0, 2)
                adminFile.write(adminId+";;;"+username+";;;"+self.encryption(pw))
        return None
    
    def extract_course_info(self):
        with open("data/course_data/raw_data.txt", "r", encoding="utf-8") as courseFile:
            course_id_pattern = re.compile(r'"course","id":(\d+),')
            matches = course_id_pattern.finditer(courseFile.read())
            course_id_list = []
            for match in matches:
                course_id_list.append(match.groups('1')[0])
            # print(len(course_id_list))
            # print(type(course_id_list[0]))
            course_title_pattern = re.compile(r'"course","id":[\d]+,"title":"(.*?)"')
            courseFile.seek(0, 0)
            matches = course_title_pattern.finditer(courseFile.read())
            course_title_list = []
            for match in matches:
                course_title_list.append(match.groups('1')[0])
            # print(len(course_title_list))
            # print(course_title_list[0])
            # image_pattern = re.compile(r'(https:\/\/img-c\.udemycdn\.com\/course\/100x100\/[\w_]+?\.jpg)')
            image_pattern  =re.compile(r'(.{13}\.udemycdn\.com\/course\/100(.*?))"')
            courseFile.seek(0, 0)
            matches = image_pattern.finditer(courseFile.read())
            image_list = []
            for match in matches:
                image_list.append(match.groups('1')[0])
            print(len(image_list))
            print(image_list[:100])
            headline_pattern = re.compile(r'","headline":"(.*?)","num')
            courseFile.seek(0, 0)
            matches = headline_pattern.finditer(courseFile.read())
            headline_list = []
            for match in matches:
                headline_list.append(match.groups('1')[0])
            # print(len(headline_list))
            # print(headline_list[0])
            pattern = re.compile(r'ibers":(\d+)')
            courseFile.seek(0, 0)
            matches = pattern.finditer(courseFile.read())
            sub_list = []
            for match in matches:
                sub_list.append(match.groups('1')[0])
            # print(len(sub_list))
            # print(sub_list[0])
            pattern = re.compile(r'"avg_rating":(\d+\.*\d*)')
            courseFile.seek(0, 0)
            matches = pattern.finditer(courseFile.read())
            rating_list = []
            for match in matches:
                rating_list.append(match.groups('1')[0])
            # print(len(rating_list))
            # print(rating_list[0])
            pattern = re.compile(r'"content_info_short":"(\d+\.*\d*) (hour|hours|mins|question|questions)"')
            courseFile.seek(0, 0)
            matches = pattern.finditer(courseFile.read())
            duration_list = []
            temp_list = []
            for match in matches:
                if(match.groups('0')[1] == "mins"):
                    # print(match.groups('0')[0],"-->", end="")
                    temp_list = list(match.groups('0'))
                    temp_list[0] = round(float(match.groups('0')[0])/60, 2)
                    # print("After conversion-->",temp_list[0])
                    duration_list.append(temp_list[0])
                else:
                    duration_list.append(match.groups('0')[0])
                # print(len(match.groups('0')))
                # print("g0-->", match.groups('0')[0], "\t", match.groups('0')[1])
                # print("g1-->", match.groups('1')[0], "\t", match.groups('1')[1])
                # print("g2-->", match.groups('2')[0], "\t", match.groups('2')[1])
            # print(len(match_list))
            # print(type(course_id_list[0]))
            # print(type(course_title_list[0]))
            # print(type(image_list[0]))
            # print(type(headline_list[0]))
            # print(type(sub_list[0]))
            # print(type(rating_list[0]))
            # print(type(duration_list[0]))
        with open("data/result/course.txt", "w", encoding="utf-8") as courseFileWriter:
            for iter in range(len(course_id_list)):
                courseFileWriter.writelines(str(course_id_list[iter])+";;;"
                                                +str(course_title_list[iter])
                                                +";;;"+str(image_list[iter])
                                                +";;;"+str(headline_list[iter])
                                                +";;;"+str(sub_list[iter])
                                                +";;;"+str(rating_list[iter])
                                                +";;;"+str(duration_list[iter])+"\n")
        with open("data/result/course.txt", "r", encoding="utf-8") as courseFileReader:
            print(courseFileReader.read())
        return None

a = Admin()
# a.register_admin()
a.extract_course_info()