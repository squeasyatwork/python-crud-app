from User import User

class Instructor(User):
    def __init__(self, id = -1, un = "", pw = "", dname = "", job = "",
                    img100 = "", cidlist = []):
        super().__init__(id, un, pw)
        self.display_name = dname
        self.job_title = job
        self.image_100x100 = img100
        self.course_id_list = cidlist
    
    def view_courses(self, args=[]):
        return None
    
    def view_reviews(self, args=[]):
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