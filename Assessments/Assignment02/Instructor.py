from User import User
from Course import Course
from Review import Review

class Instructor(User):
    """
    This class stores details of an instructor. It inherits the User class.
    It has the following fields:
        1. ID
        2. username
        3. password
        4. display name
        5. job title
        6. image URL
        7. course id list
    It has methods to view the courses taught by an instructor, and to 
    view the reviews of these courses.
    It also has an overridden definition of the dunder method __str__ . 
    """

    # Constructor
    def __init__(self, id = -1, un = "", pw = "", dname = "", job = "",
                    img100 = "", cidlist = []):
        super().__init__(id, un, pw)   # Call the parent class constructor
        self.display_name = dname
        self.job_title = job
        self.image_100x100 = img100
        self.course_id_list = cidlist
        """
        Locate the instructor in the user_instructor.txt file and map the
        details to this object.
        """
        with open("user_instructor.txt", "r", encoding="utf-8") as itrFile:
            for line in itrFile:
                entry = line.split(";;;")
                if (entry[1] == un and entry[2] == self.encryption(pw)):
                    # Instructor found
                    self.id = entry[0]
                    self.display_name = entry[3]
                    self.job_title = entry[4]
                    flag = 0
                    if(entry[5].startswith("https:")):
                        self.image_100x100 = entry[5]
                    else:
                        flag = 1
                        self.image_100x100 = ""
                    if flag == 0:
                        self.course_id_list = entry[6].strip("\n").split("-")
                    else:
                        self.course_id_list = entry[5].strip("\n").split("-")
                    break
    
    """
    This method calls the find_course_by_instructor_id() of the Course 
    class with id of the instructor as argument, and stores the list.
    Next it prints details of the first 10 courses from this list.
    """
    def view_courses(self, args=[]):
        print()
        coursesList = Course().find_course_by_instructor_id(self.id)
        iter = 0
        while iter < min(len(coursesList), 10):  # Print only 10 courses
            print (iter+1, ":", coursesList[iter].course_title)
            iter += 1
        return None
    
    """
    This method calls the find_course_by_instructor_id() of the Course 
    class with id of the instructor as argument, and stores the list.
    For each course in this list, it calls the 
        find_review_by_course_id() and build a review list of all the 
        reviews on the course. 
    Next, it prints out the first 10 reviews from this review list.
    """
    def view_reviews(self, args=[]):
        print()
        # Build a list of courses taught by this instructor
        coursesList = Course().find_course_by_instructor_id(self.id)
        iter1 = 0
        # Build a review list for each course in course list
        for iter1 in range(len(coursesList)):
            print (coursesList[iter1].course_title, ":", end = "\n\t")
            reviewsList = Review().find_review_by_course_id\
                                        (coursesList[iter1].course_id)
            iter2 = 0
            # Print only 10 reviews
            while iter2 < min(len(reviewsList), 10):
                print (iter2+1, ":", 
                        reviewsList[iter2].content, end = "\n\t")
                iter2 += 1
            iter1 += 1
        return None
    
    """
    Override the dunder __str__ method to return a string that is identical to the 
    entry of instructor found in the user_instructor.txt file
    """
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