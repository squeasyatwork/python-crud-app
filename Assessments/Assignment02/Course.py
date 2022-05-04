class Course:
    def __init__(self, id = -1, title = "", image100 = "",  
                    headline = "", subs = -1, rating = -1.0, length = -1):
        self.course_id = id
        self.course_title = title
        self.course_image_100x100 = image100
        self.course_headline = headline
        self.course_num_subscribers = subs
        self.course_avg_rating = rating
        self.course_content_length = length

    def find_course_by_title_keyword(self, keyword):
        result_list = []
        with open('data/result/course.txt', 'r', encoding='utf-8') as courseReader:
            for line in courseReader:
                if keyword in line.split(';;;')[1]:
                    result_list.append(Course(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3],
                                                line.split(';;;')[4],
                                                line.split(';;;')[5],
                                                line.split(';;;')[6]))
        return result_list
    
    def find_course_by_id(self, course_id):
        course = None
        with open('data/result/course.txt', 'r', encoding='utf-8') as courseReader:
            for line in courseReader:
                if line.split(';;;')[0] == str(course_id):
                    course = Course(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3],
                                                line.split(';;;')[4],
                                                line.split(';;;')[5],
                                                line.split(';;;')[6])
                    break
        return course
    
    def find_course_by_instructor_id(self, instructor_id):
        result_list = []
        with open('user_instructor.txt', 'r', encoding='utf-8') as itrReader:
            for line in itrReader:
                if line.split(';;;')[0] == str(instructor_id):
                    id_list = line.split(';;;')[6].split('-')
                    # print(id_list)
                    for course in id_list:
                        result_list.append(self.find_course_by_id(course.strip()))
                    break
        return result_list
    
    def courses_overview(self):
        courseCount = 0
        with open('data/result/course.txt', 'r', encoding='utf-8') as courseReader:
            for line in courseReader:
                courseCount += 1
        return (str(courseCount)) 

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