from User import User
from Instructor import Instructor
from Course import Course
from Review import Review
import re
import os

class Admin(User):
    """
    This class represents an admin user. The admin has all permissions 
    including extract_info, view_users, and remove_data.
    It has the exact same fields as the parent class.
    It has the following methods:
        1. Register admin to register a new admin user.
        2. Extract course info, to extract information about courses from 
            raw_data.txt file and store it in course.txt file
        3. Extract review info, to extract information about reviews from 
            raw_data.txt file and store it in review.txt file
        4. Extract student info, to extract information about students from 
            review_data .json files and store it in user_student.txt file
        5. Extract instructor info, to extract information about 
            instructors from review_data .json files and store it in 
            user_instructor.txt file
        6. Extract info, that calls all four extract methods above.
        7. Remove data, to delete all the extracted data
        8. View courses, that shows the total number of courses, or
            a specific list of course/s that match a provided criterion
        9. View users, that shows the number of users of each type
        10. View reviews, that shows the total number of reviews, or
            a specific list of review/s that match a provided criterion
    """

    # Constructor
    def __init__(self, id = -1, username = "", password = ""):
        User.__init__(self, id, username, password)

    def register_admin(self):
        """
        This method first checks if the current admin object has its 
            credentials stored in the user_admin.txt file.
        If it is stored, it does nothing.
        Otherwise, it generates a unique user ID for the new admin and
            writes the new user credentials to the file.
        """
        flag = 0
        # Open the admins file to search for current admin object
        with open("user_admin.txt", "w+") as adminFile:
            # Define a regex pattern to obtain all admin entries
            pattern = re.compile(r';((\w)+);')
            matches = pattern.finditer(adminFile.read())
            for match in matches:   # Compare each admin entry
                if(match.groups()[0] == self.username):   # Match found
                    flag = 1
                    break
                    # print("Match found in the line: ", match.__str__())
            if flag == 0:   # Match not found
                #  Generate new ID and register the admin
                adminFile.write(self.generate_user_id() + ";;;" + self.username 
                                    + ";;;" + self.encryption(self.password) + "\n")
        return None
    
    def extract_course_info(self):
        """
        This method extracts information of all courses from the raw_data.txt file,
            and stores each course in a separate line in course.txt file.
        It uses a separate regex to capture the fields of information about each 
            course in separate lists, and then appends all these by indices 
            while writing to the course.txt file.
        A similar aproach is used in all extraction methods.
        """
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
            image_pattern  =re.compile(r'(.{13}\.udemycdn\.com\/course\/100(.*?))"')
            courseFile.seek(0, 0)
            matches = image_pattern.finditer(courseFile.read())
            image_list = []
            for match in matches:
                image_list.append(match.groups('1')[0])
            # print(len(image_list))
            # print(image_list[:100])
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
        inits_list = []
        review_list = []
        # First call extract_instructor_info() and generate user_instructor.txt
        for jsonfile in os.listdir(os.getcwd()+"/data/review_data"):
            with open(os.path.join(os.getcwd()+"/data/review_data", jsonfile), 'r', encoding="utf-8") as reviewFile:
                stud_id_pattern = re.compile(r'"user(.*?)", "user": {"_class": "user", ("id": (\d{0,10}), )?')
                matches = stud_id_pattern.finditer(reviewFile.read())
                for match in matches:
                    # print(match.groups())
                    stud_id_list.append(match.groups()[2])
                # generating usernames and adding to un_list, also building title_list in parallel
                reviewFile.seek(0, 0)
                title_pattern = re.compile(r'"user_modified"(.*?)"title": "(.+?)"')
                matches = title_pattern.finditer(reviewFile.read())
                for match in matches:
                    title_list.append(match.groups()[1])
                    un_list.append(match.groups()[1].lower().replace(" ", "_"))
                    # print(match.groups()[1])
                reviewFile.seek(0, 0)
                # Start generating pw_list by extracting and storing the initials
                pw_pattern = re.compile(r'"user_modified".*?"image_50x50":(.*?)"(, "initials": "(.{0,10})"\}|\}), "resp')
                matches = pw_pattern.finditer(reviewFile.read())
                for match in matches:
                    pw_list.append(match.groups()[2])
                # Obtaining user_image and storing it in image_list
                reviewFile.seek(0, 0)
                image_pattern = re.compile(r'"user_modified".*?"image_50x50":(.*?)"(, "initials": "(.{0,10})"\}|\}), "resp')
                matches = pw_pattern.finditer(reviewFile.read())
                i = 0
                for match in matches:
                    i += 1
                    # print(match.groups()[0],end="\n\n")
                    image_list.append(match.groups()[0])
                # print(image_list,end="\n\n")
                # Obtaining review id and storing it in review_id_list
                reviewFile.seek(0, 0)
                review_id_pattern = re.compile(r'w", "id": (\d+?),')
                matches = review_id_pattern.finditer(reviewFile.read())
                for match in matches:
                    review_list.append(match.groups('1')[0])
        """
        By this point, we have lists of all students' id, username, and password
        Now we need to generate the None valued student id's first
        Then we need to build the passwords as <initials + id + initials>
        Next, we can go ahead and obtain user image and their review_id
        Lastly, we can iterate through these lists and build student strings
            to write them in user_student.txt
        """
        # Generate the temporary student id file to search for uniqueness of ID later on
        # with open('user_student.txt', 'r+', encoding='utf-8') as studFile:
        #     for i in stud_id_list:
        #         if i is not None:
        #             studFile.writelines(i+"\n")
        # Now we generate unique student id and update them in the stud_id_list in place 
        iter = 0
        for iter in range(len(stud_id_list)):
            if stud_id_list[iter] is None:
                stud_id_list[iter] = self.generate_user_id()
                # print(iter, "changed to ", stud_id_list[iter], end="\n\n")
        # for i in stud_id_list:
        #         if i is None:
        #             print(i)
        # Now we have the complete None-free stud_id_list
        # Now we build the passwords in the format specified above
        iter = 0
        # generating the final pw_list
        for iter in range(len(stud_id_list)):
            if pw_list[iter] is None:
                pw_list[iter] = ''
            # building inits_list before we lose initials value from pw_list
            inits_list.append(pw_list[iter])
            inits = pw_list[iter].lower()
            ids = stud_id_list[iter].lower()
            real_pw = self.encryption(inits + ids + inits)
            # print(real_pw,end="\n\n")
            pw_list[iter] = real_pw
            # if iter == 1000:
            #     print(pw_list[iter],end="\n\n")
        # print("id_list length: ",len(stud_id_list))
        # print("un_list length: ",len(un_list))
        # print("pw_list length: ",len(pw_list))
        # print("title_list length: ",len(title_list))
        # print("image_list length: ",len(image_list))
        # print("inits_list length: ",len(inits_list))
        # print("review_list length: ",len(review_list))
        # print("review_list length: ",review_list[1000:1100])

        # Building student strings and writing them to user_student.txt file
        with open("user_student.txt", "w", encoding='utf-8') as studWriter:
            for iter in range(len(stud_id_list)):
                studWriter.writelines(stud_id_list[iter] + ";;;"
                                        + un_list[iter] + ";;;"
                                        + pw_list[iter] + ";;;"
                                        + title_list[iter] + ";;;"
                                        + image_list[iter].strip() + ";;;"
                                        + inits_list[iter] + ";;;"
                                        + review_list[iter] + "\n")
        return None

    def extract_instructor_info(self):
        with open("data/course_data/raw_data.txt", "r", encoding="utf-8") as courseFile:
            itr_pattern = re.compile(r'tors":\[{(.*?)("image_100x100":"(.*?)",|"display_name":"(.*?)",|"job_title":"(.*?)",|"id":(\d*?),)(.*?)("image_100x100":"(.*?)",|"display_name":"(.*?)",|"job_title":"(.*?)",|"id":(.*?),)(.*?)("image_100x100":"(.*?)",|"display_name":"(.*?)",|"job_title":"(.*?)",|"id":(.*?),)(.*?)("image_100x100":"(.*?)"|"display_name":"(.*?)"|"job_title":"(.*?)"|"id":(.*?))(.*?)}\]')
            matches = itr_pattern.finditer(courseFile.read())
            itr_entry_list = []
            itr_id_list = []
            itr_string = ''
            itr_dict = {}
            for match in matches:
                flag = 0
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
                if flag == 1:
                    itr_val = ''
                    for item in sorted_entry:
                        if item.startswith('"display_name":'):
                            itr_val += item.split(":")[1].strip('"').lower().replace(" ", "_") + ";;;"
                    
                    itr_val += self.encryption(itr_id) + ";;;"

                    for item in sorted_entry:
                        if item.startswith('"display_name":'):
                            itr_val += item.split(":")[1].strip('"') +";;;"

                    for item in sorted_entry:
                        if item.startswith('"job_title":'):
                            itr_val += item.split(":")[1].strip('"') +";;;"
                    if sorted_entry[len(sorted_entry)-1].startswith("http"):
                        itr_val += sorted_entry[len(sorted_entry)-1] + ";;;"
                    itr_dict[itr_id] = itr_val 
                itr_entry_list.append(sorted_entry)
            # print(match.groups())
            # print(itr_entry_list[1000])
            # print(itr_id_list[1000:3000])

            # adding courses by checking if instructor already exists
            with open("data/course_data/raw_data.txt", "r", encoding="utf-8") as courseFile:
                course_pattern = re.compile(r's":"course","id":(\d*?),(.*?)\[((.*?)"id":(\d*?)[,\}](.*?))\]')
                matches = course_pattern.finditer(courseFile.read())
                i = 0
                for match in matches:
                    # if i%10 == 0:
                    #     print(match.groups()[0]) #course_id at pos 0
                    # accessing each instructor who teaches this course
                    each_itr = re.split(r"\{(.*?)\}" , match.groups()[2])
                    for item in sorted(each_itr):
                        if len(item) > 10:
                            item_id = re.findall(r'"id":(\d*?)[,?]', item)
                            # print("itr_id ",item_id,end="\t")
                            # print(len(item_id))
                            if len(item_id)>0 and item_id[0] in itr_dict:
                                # print(item_id[0]," MATCH WITH ", itr_dict[item_id[0]], end="\t")
                                if itr_dict[item_id[0]].endswith(';'):
                                    itr_dict[item_id[0]] += match.groups()[0]
                                else:
                                    # print(item_id[0])
                                    itr_dict[item_id[0]] += "-" + match.groups()[0]
                                    # print(itr_dict[item_id[0]])
        #         # for i in itr_dict:
                     # print(i)

        with open("user_instructor.txt", "w", encoding="utf-8") as itrFileWriter:
            for item in itr_dict:
                itrFileWriter.writelines(str(item) + ";;;"
                                            + str(itr_dict[item]) 
                                            + "\n")
        return None
    
    def extract_info(self):
        """
        This method simply calls all the four extract methods defined above.
        """
        self.extract_course_info()
        self.extract_students_info()
        self.extract_review_info()
        self.extract_instructor_info()
        return None
    
    def remove_data(self):
        """
        This method opens all files in write mode and truncates all their 
            contents, if any.
        """
        with open('data/result/course.txt', 'w', encoding='utf-8') as deleter:
            pass
        with open('data/result/review.txt', 'w', encoding='utf-8') as deleter:
            pass
        with open('user_student.txt', 'w', encoding='utf-8') as deleter:
            pass
        with open('user_instructor.txt', 'w', encoding='utf-8') as deleter:
            pass
        return None

    def view_courses(self, args=[]):
        """
        This method takes an optional argument, which is a search parameter.
        It progresses in the following way:
            1. It checks the length of args argument 
            2. If no list is passed, it displays the number of courses.
            3. If a list is passed, it validates the elements of it.
            4. If first element is not in ("ID", "TITLE_KEYWORD", 
                "INSTRUCTOR_ID"), then it displays an appropriate incorrect 
                input message.
                Otherwise, it moves on to validate the second element.
            6. If first element is "ID" or "INSTRUCTOR_ID", it can only be 
                numeric otherwise it displays an appropriate incorrect 
                input message.
        """
        print()
        if len(args) == 0:   # No args list passed
            print(Course().courses_overview())
        elif len(args) == 2:   # args list has been passed
            if args[0] == 'TITLE_KEYWORD':
                for course in Course().\
                                find_course_by_title_keyword(args[1]):
                    print(course.course_title)
            elif args[0] == 'ID':
                if args[1].isdigit():   #Check if ID is numeric
                    if Course().find_course_by_id(args[1]) is not None:
                        print(Course().find_course_by_id(args[1]).course_title)
                    else:
                        print("No course found.")
                else:
                    print("Course ID can be numeric only!")
            elif args[0] == 'INSTRUCTOR_ID':
                if args[1].isdigit():   #Check if INSTRUCTOR_ID is numeric
                    coursesList = Course().find_course_by_instructor_id(args[1])
                    for course in coursesList:
                        print(course.course_title)
                else:
                    print("Instructor ID can be numeric only!")
            else:   # first element of args list is invalid
                print("\nINVALID INPUT VALUE TO SEARCH-BY: Enter",end=" ")
                print("one of the following: TITLE_KEYWORD/ID/INSTRUCTOR_ID")
        return None
    
    def view_users(self):
        """
        This method displays the number of users of each type.
        It simply opens each user file and counts the number of users in it.
        At the end of each file, it display the number of users found.
        """
        print()
        # Open admin file and count number of admins
        print("ADMINS:", end=" ")
        with open('user_admin.txt', 'r', encoding='utf-8') as adminReader:
            admincount = 0
            for line in adminReader:
                admincount += 1
            print(admincount, end="\n")
        # Open instructor file and count number of instructors
        print("INSTRUCTORS:", end=" ")
        with open('user_instructor.txt', 'r', encoding='utf-8') as itrReader:
            itrcount = 0
            for line in itrReader:
                itrcount += 1
            print(itrcount, end="\n")
        # Open student file and count number of students
        print("STUDENTS:", end=" ")
        with open('user_student.txt', 'r', encoding='utf-8') as studReader:
            studcount = 0
            for line in studReader:
                studcount += 1
            print(studcount, end="\n")
        return None

    def view_reviews(self, args=[]):
        """
        This method takes an optional argument, which is a search parameter.
        It progresses in the following way:
            1. It checks the length of args argument 
            2. If no list is passed, it displays the number of reviews.
            3. If a list is passed, it validates the elements of it.
            4. If first element is not in ("ID", "KEYWORD", "COURSE_ID"),
                then it displays an appropriate incorrect input message.
                Otherwise, it moves on to validate the second element.
            6. If first element is "ID" or "COURSE_ID", it can only be 
                numeric otherwise it displays an appropriate incorrect 
                input message.
        """
        print()
        if len(args) == 0:   # No args list passed
            print(Review().reviews_overview())
        elif len(args) == 2:   # args list has been passed
            if args[0] == 'ID':
                if args[1].isdigit():   #Check if ID is numeric
                    if Review().find_review_by_id(args[1]) is not None:
                        print(Review().find_review_by_id(args[1]).content)
                    else:
                        print("Review not found.")
                else:
                    print("Review ID can be numeric only!")
            elif args[0] == 'KEYWORD':
                for review in Review().\
                                find_review_by_keywords(args[1]):
                    print(review.content)
            elif args[0] == 'COURSE_ID':
                if args[1].isdigit():   #Check if COURSE_ID is numeric
                    reviewsList = Review().find_review_by_course_id(args[1])
                    for review in reviewsList:
                        print(review.content)
                else:
                    print("Course ID can be numeric only!")
            else:   # first element of args list is invalid
                print("\nINVALID INPUT VALUE TO SEARCH-BY: Enter",end=" ")
                print("one of the following: ID/KEYWORD/COURSE_ID")
        return None
    
    def __str__(self):
        """
        Same as its parent class method definition.
        """
        return super().__str__()

# a = Admin()
# a.register_admin()
# a.extract_course_info()
# a.extract_review_info()
# a.extract_students_info()
# a.extract_instructor_info()
# a.extract_info()
# # a.remove_data() TRY TO TEST THIS ONLY AT THE LAST TESTING STAGE!
# a.view_courses()
# a.view_users()
# a.view_reviews()
# print(a.__str__())
# a = Admin(999, "admin", "admin")
# a.register_admin()