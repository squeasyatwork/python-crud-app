from User import User

class Student(User):
    def __init__(self, id = -1, un = "", pw = "", title = "", img50 = "",
                    inits = "", rev_id = -1):
        super().__init__(id, un, pw)
        self.user_title = title
        self.image_50x50 = img50
        self.user_initials = inits
        self.review_id = rev_id
    
    def view_courses(self, args=[]):
        with open('data/result/review.txt', 'r', encoding='utf-8') as revreader:
            for line in revreader:
                if line.split(';;;')[0] == str(self.review_id):
                    print("Enrolled course id: ", line.split(';;;')[3])
                    break
        return None
    
    def view_reviews(self, args=[]):
        with open('data/result/review.txt', 'r', encoding='utf-8') as revreader:
            for line in revreader:
                if line.split(';;;')[0] == str(self.review_id):
                    print(line.split(';;;')[1])
                    break
        return None
    
    def __str__(self):
        user_string = super().__str__()
        return (user_string + ";;;" + self.user_title + ";;;" 
                    + self.image_50x50 + ";;;" + self.user_initials + ";;;" 
                    + str(self.review_id))
    
# s = Student(1111, 'user1', 'pass1', 'comp student', 'https://url',
#                 'AF', 46010312)
# print(s.__str__())
# s.view_courses()
# s.view_reviews()
# s.view_users()