from User import User
from Course import Course
from Review import Review

class Instructor(User):
    def __init__(self, id = -1, un = "", pw = "", dname = "", job = "",
                    img100 = "", cidlist = []):
        super().__init__(id, un, pw)
        self.display_name = dname
        self.job_title = job
        self.image_100x100 = img100
        self.course_id_list = cidlist
        with open("user_instructor.txt", "r", encoding="utf-8") as itrFile:
            for line in itrFile:
                entry = line.split(";;;")
                if (entry[1] == un and entry[2] == self.encryption(pw)):
                    self.id = entry[0]
                    self.display_name = entry[3]
                    self.job_title = entry[4]
                    self.image_100x100 = entry[5]
                    self.course_id_list = entry[6].strip("\n").split("-")
                    break
    
    def view_courses(self, args=[]):
        print()
        coursesList = Course().find_course_by_instructor_id(self.id)
        iter = 0
        while iter < min(len(coursesList), 10):
            print (iter+1, ":", coursesList[iter].course_title)
            iter += 1
        return None
    
    def view_reviews(self, args=[]):
        print()
        coursesList = Course().find_course_by_instructor_id(self.id)
        iter1 = 0
        for iter1 in range(len(coursesList)):
            print (coursesList[iter1].course_title, ":", end = "\n\t")
            reviewsList = Review().find_review_by_course_id\
                                        (coursesList[iter1].course_id)
            iter2 = 0
            while iter2 < min(len(reviewsList), 10):
                print (iter2+1, ":", 
                        reviewsList[iter2].content, end = "\n\t")
                iter2 += 1
            iter1 += 1
        return None
    
    def __str__(self):
        user_string = super().__str__()
        courses_string = ''
        for item in self.course_id_list:
            if len(courses_string) == 0:
                courses_string += str(item)
            else:
                courses_string += '-' + str(item)
        return (user_string + ";;;" + self.display_name + ";;;" 
                    + self.job_title + ";;;" + self.image_100x100 + ";;;" 
                    + courses_string)

# i = Instructor('123', 'user1', 'pass1', 'Rajesh', 'Engineer', 'https://url',
#                     [1111, 2222, 3333, 0000])

# print(i.__str__())