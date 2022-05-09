class Course:
    """
    This class stores the details of a course:
        1. Course ID
        2. Course title
        3. Course image URL
        4. Course headline
        5. Course number of subscribers
        6. Course average rating
        7. Course content length
    The constructor initialises and sets the value of each field.
    It has the following methods that serve the the same end goal of finding a course
    or a list of courses corresponding to a specific criterion:
        1. Find course by course ID
        2. Find course by title keyword
        3. Find course by instructor ID
        4. Overview of courses
    It also has an overridden definition of the dunder method __str__ .
    """
    # Constructor
    def __init__(self, id = -1, title = "", image100 = "",  
                    headline = "", subs = -1, rating = -1.0, length = -1):
        self.course_id = id
        self.course_title = title
        self.course_image_100x100 = image100
        self.course_headline = headline
        self.course_num_subscribers = subs
        self.course_avg_rating = rating
        self.course_content_length = length

    """
    This method takes an argument called keyword and does the following:
        1. Opens the course.txt file that contains details of all the courses
        2. Reads it line by line
        3. If the line contains the keyword in its course title, make a new Course 
            object corresponding to the course in the current line, and add it 
            to the list of courses to be returned.
        4. After reaching the end of file, return the result list.
    """
    def find_course_by_title_keyword(self, keyword):
        result_list = []   # The result list of courses to be returned 
        with open('data/result/course.txt', 'r', encoding='utf-8') as courseReader:
            for line in courseReader:   # Scan each line of course
                if keyword in line.split(';;;')[1]:   # If keyword found in title
                    result_list.append(Course(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3],
                                                line.split(';;;')[4],
                                                line.split(';;;')[5],
                                                line.split(';;;')[6]))
        return result_list
    
    """
    This method takes an argument called course_id and does the following:
        1. Opens the course.txt file that contains details of all the courses
        2. Reads it line by line
        3. If the line contains the course_id in its course id field, make a new 
            Course object corresponding to the course in the current line, and 
            return it.
    """
    def find_course_by_id(self, course_id):
        course = None   # The Course object to be returned
        with open('data/result/course.txt', 'r', encoding='utf-8') as courseReader:
            for line in courseReader:   # Scan each line of course
                if line.split(';;;')[0] == str(course_id):   # If course ID's match
                    course = Course(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3],
                                                line.split(';;;')[4],
                                                line.split(';;;')[5],
                                                line.split(';;;')[6])
                    break
        return course
    
    """
    This method takes an argument called instructor_id and does the following:
        1. Opens the user_instrcutor.txt file that contains details of instructors
        2. Reads it line by line
        3. If the instructor ID's match, it makes a list of all courses taught by 
            this instructor.
        4. Calls the find_course_by_id() method on each course present in this list.
        5. Appends all the courses returned to a result list, and returns it.
    """
    def find_course_by_instructor_id(self, instructor_id):
        result_list = []   # The result list of courses to be returned 
        with open('user_instructor.txt', 'r', encoding='utf-8') as itrReader:
            for line in itrReader:   # Scan each line of instructor
                if line.split(';;;')[0] == str(instructor_id):   # instructor found
                    # Make a list from the ID's of all the courses taught by this
                    #   instructor 
                    id_list = line.split(';;;')[6].split('-')
                    # print(id_list)
                    # For each course ID, append the course to the result list
                    for course in id_list:
                        result_list.append(self.find_course_by_id(course.strip()))
                    break
        return result_list
    
    """
    This method takes no arguments. It returns the number of courses in the course.txt file
    1. It initialises a counter to 0
    2. Scans the course.txt file
    3. Increases the counter for each new scanned line
    Returns the counter.
    """
    def courses_overview(self):
        courseCount = 0   # Initialise the counter
        with open('data/result/course.txt', 'r', encoding='utf-8') as courseReader:
            for line in courseReader:   # Scan each line of course
                courseCount += 1
        return (str(courseCount)) 

    """
    Override the dunder __str__ method to return a string that is identical to the 
    entry of course found in the course.txt file
    """
    def __str__(self):
        return (str(self.course_id) + ";;;" + self.course_title + ";;;" 
                        + self.course_image_100x100 + ";;;" + self.course_headline 
                        + ";;;" + str(self.course_num_subscribers) + ";;;" 
                        + str(self.course_avg_rating) + ";;;" 
                        + str(self.course_content_length))
                
# c = Course(900434, "VueJS V1 Introduction to VueJS JavaScript Framework", 
#             "https://img-c.udemycdn.com/course/100x100/900434_5203.jpg", 
#             "Complete guide to getting started with VueJS easy to learn JavaScript \
#             Framework for data binding and dynamic web content", 3.55, 22993, 2)

# print("\n",c.__str__())
# print("\n",c.find_course_by_title_keyword("HTML5"))
# print("\n",c.find_course_by_id(c.course_id))
# print("\n",c.find_course_by_instructor_id(61671222))
# print("\n",c.courses_overview())