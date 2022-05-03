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
                courseFileWriter.writelines(str(course_id_list[iter]) + ";;;"
                                                    + str(course_title_list[iter])
                                                    + ";;;" + str(image_list[iter])
                                                    + ";;;" + str(headline_list[iter])
                                                    + ";;;" + str(rating_list[iter])
                                                    + ";;;" + str(sub_list[iter])
                                                    + ";;;" + str(duration_list[iter]) 
                                                    + "\n")
        # with open("data/result/course.txt", "r", encoding="utf-8") as courseFileReader:
        #     print(courseFileReader.read())
        return None
    
    def extract_review_info(self):
        review_id_list = []
        content_list = []
        rating_list = []
        course_id_list = []
        # print(content_list, rating_list, review_id_list, course_id_list)
        for jsonfile in os.listdir(os.getcwd()+"/data/review_data"):
            with open(os.path.join(os.getcwd()+"/data/review_data", jsonfile), 'r', encoding="utf-8") as reviewFile:
                review_id_pattern = re.compile(r'w", "id": (\d+?),')
                matches = review_id_pattern.finditer(reviewFile.read())
                for match in matches:
                    review_id_list.append(match.groups('1')[0])
                reviewFile.seek(0, 0)
                content_pattern = re.compile(r'review", (.+?)t": "(.*?)", "rating')
                matches = content_pattern.finditer(reviewFile.read())
                for match in matches:
                    content_list.append(match.groups()[1])
                    # print(match.groups()[1])
                reviewFile.seek(0, 0)
                rating_pattern = re.compile(r'g": (\d+?\.?\d*?),')
                matches = rating_pattern.finditer(reviewFile.read())
                for match in matches:
                    rating_list.append(match.groups()[0])
                    course_id_list.append(jsonfile.split('.')[0])
        # print(course_id_list[10000:10050])
        # print(len(course_id_list))
        with open("data/result/review.txt", "w", encoding="utf-8") as reviewFileWriter:
            for iter in range(len(review_id_list)):
                reviewFileWriter.writelines(str(review_id_list[iter]) + ";;;"
                                                    + str(content_list[iter])
                                                    + ";;;" + str(rating_list[iter])
                                                    + ";;;" + str(course_id_list[iter]) 
                                                    + "\n")
        # with open("data/result/review.txt", "r", encoding="utf-8") as reviewFileReader:
        #     print(reviewFileReader.read(10000))
        return None

    def extract_students_info(self):
        stud_id_list = []
        un_list = []
        pw_list = []
        title_list = []
        image_list = []
        initials_list = []
        rev_id_list = []
        i = 0
        # First call extract_instructor_info() and generate user_instructor.txt
        """
        Now retrieve all the students who have an id in the json review strings       
        and generate the user_student.txt file.
        Now, retrieve all students wiithout an id in the json review strings
        and generate unique student id's fore them.
        """

        for jsonfile in os.listdir(os.getcwd()+"/data/review_data"):
            with open(os.path.join(os.getcwd()+"/data/review_data", jsonfile), 'r', encoding="utf-8") as reviewFile:
                stud_id_pattern = re.compile(r'"user(.*?)", "user": {"_class": "user", ("id": (\d{0,10}), )?')
                matches = stud_id_pattern.finditer(reviewFile.read())
                for match in matches:
                    # i += 1
                    # print(match.groups())
                    # if(i>100):
                    #     break
                    i+=1
                    if(not(match.groups()[2] is None)): # true if ID exists
                        # print(match.groups()[2], end=" ")
                        stud_id_list.append(match.groups()[2])
                        # i += 1
                reviewFile.seek(0, 0)
                title_pattern = re.compile(r'"user_modified"(.*?)"title": "(.+?)"')
                matches = title_pattern.finditer(reviewFile.read())
                for match in matches:
                    un_list.append(match.groups()[1].lower().replace(" ", "_"))
                    # print(match.groups()[1])
                reviewFile.seek(0, 0)
                pw_pattern = re.compile(r'"initials": "(.{0,10})"}, "response":')
                # pw_pattern = re.compile(r'"user_modified"(.*?)"initials": "(.{0,10})"}')
                matches = pw_pattern.finditer(reviewFile.read())
                i = 0
                for match in matches:
                    if (match.groups()[0] is None):
                        i += 1
                    else:
                        pw_list.append(match.groups()[0].lower())
                        # print(match.groups()[1])
        print(i)
        print(pw_list[140000:160000])
        print("len",len(pw_list))

        # for jsonfile in os.listdir(os.getcwd()+"/data/review_data"):
        #     with open(os.path.join(os.getcwd()+"/data/review_data", jsonfile), 'r', encoding="utf-8") as reviewFile:
        #         stud_id_pattern = re.compile(r'"user(.*?)", "user": {"_class": "user", ("id": (\d{0,10}), )?')
        #         matches = stud_id_pattern.finditer(reviewFile.read())
        #         for match in matches:
        #             # i += 1
        #             # print(match.groups())
        #             # if(i>100):
        #             #     break
        #             i+=1
        #             if(match.groups()[2] is None): # true if ID does not exist
        #                 stud_id_list.append(self.generate_user_id()
        #                 # print(match.groups()[2], end=" ")
        #                 # i += 1
        return None

    def extract_instructor_info(self):
        with open("data/course_data/raw_data.txt", "r", encoding="utf-8") as courseFile:
            itr_pattern = re.compile(r'tors":\[{(.*?)("image_100x100":"(.*?)",|"display_name":"(.*?)",|"job_title":"(.*?)",|"id":(\d*?),)(.*?)("image_100x100":"(.*?)",|"display_name":"(.*?)",|"job_title":"(.*?)",|"id":(.*?),)(.*?)("image_100x100":"(.*?)",|"display_name":"(.*?)",|"job_title":"(.*?)",|"id":(.*?),)(.*?)("image_100x100":"(.*?)"|"display_name":"(.*?)"|"job_title":"(.*?)"|"id":(.*?))(.*?)}\]')
            # itr_id_pattern = re.compile(r'tors":.*?"id":(\d*?),')
            matches = itr_pattern.finditer(courseFile.read())
            itr_entry_list = []
            itr_id_list = []
            itr_string = ''
            itr_dict = {}
            # id displayname jobtitle image courses
            i=0
            for match in matches:
                flag = 0
                i += 1
                # if(i%100)==0:
                #     # print( sorted(list(filter(None, list(match.groups())))) , end="\n\n" )
                #     sorted_entry = sorted(list(filter(None, list(match.groups()))))
                #     # itr_details = [i.split(',')[0].split(':')]
                #     for iter in range(len(sorted_entry)):
                #         sorted_entry[iter] = sorted_entry[iter].rstrip(',')
                #         # print(item.rstrip(","))
                #     print(sorted_entry)
                sorted_entry = sorted(list(filter(None, list(match.groups()))))
                for iter in range(len(sorted_entry)):
                    sorted_entry[iter] = sorted_entry[iter].rstrip(',')
                # Checking if instructor already exists in dictionary itr_dict
                for item in sorted_entry:
                    if item.startswith('"id":'):
                        if (len(item.split(":")[1])>0) and (item.split(":")[1] not in itr_id_list):
                            flag = 1
                            itr_id  = item.split(":")[1]
                        else:
                            flag = 0
                if  flag == 1:
                    itr_name = ''

                    for item in sorted_entry:
                        if item.startswith('"display_name":'):
                            itr_name = item.split(":")[1]
    
                    itr_dict[itr_id] = itr_name
            
                            
                itr_entry_list.append(sorted_entry)
            # print(match.groups())
            print(itr_dict['1364522'])
            # print(itr_id_list[1000:3000])
            
        return None

a = Admin()
# a.register_admin()
# a.extract_course_info()
# a.extract_review_info()
# a.extract_students_info()
a.extract_instructor_info()