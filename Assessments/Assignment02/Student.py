from User import User

class Student(User):
    """
    This class stores details of an student. It inherits the User class.
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
    def __init__(self, id = -1, un = "", pw = "", title = "", img50 = "",
                    inits = "", rev_id = -1):
        super().__init__(id, un, pw)   # Call the parent class constructor
        self.user_title = title
        self.image_50x50 = img50
        self.user_initials = inits
        self.review_id = rev_id
        """
        Locate the student in the user_student.txt file and map the
        details to this object.
        """
        with open("user_student.txt", "r", encoding="utf-8") as studFile:
            for line in studFile:
                entry = line.split(";;;")
                if (entry[1] == un and entry[2] == self.encryption(pw)):
                    # Student found
                    self.id = entry[0]
                    self.user_title = entry[3]
                    self.image_50x50 = entry[4]
                    self.user_initials = entry[5]
                    self.review_id = entry[6].strip()
                    break
    
    """
    This method prints the course ID of the course this student is enrolled in.
    It scans the review file line by line for the review ID of the student.
    Once a match is found, it displays the course ID in the corresponding 
    review line.
    """
    def view_courses(self, args=[]):
        print()
        with open('data/result/review.txt', 'r', encoding='utf-8') as revreader:
            for line in revreader:   # Scan each review line
                if line.split(';;;')[0] == str(self.review_id):
                    # Review ID's match
                    print("Enrolled course id: ", line.split(';;;')[3])
                    break
        return None
    
    """
    This method prints the course ID of the course this student is enrolled in.
    It scans the review file line by line for the review ID of the student.
    Once a match is found, it displays the review content in the corresponding 
    review line.
    """
    def view_reviews(self, args=[]):
        print()
        with open('data/result/review.txt', 'r', encoding='utf-8') as revreader:
            for line in revreader:   # Scan each review line
                if line.split(';;;')[0].strip() == str(self.review_id):
                    # Review ID's match
                    print(line.split(';;;')[1])
                    break
        return None
    
    """
    Override the dunder __str__ method to return a string that is identical to the 
    entry of student found in the user_student.txt file
    """
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