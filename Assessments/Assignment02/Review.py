class Review:
    """
    This class stores the details of a review:
        1. Review ID
        2. Review content
        3. Review rating
        4. Review course ID
    The constructor initialises and sets the value of each field.
    It has the following methods that serve the the same end goal of finding a review
    or a list of review corresponding to a specific criterion:
        1. Find review by review ID
        2. Find review by keyword
        3. Find review by course ID
        4. Overview of reviews
    It also has an overridden definition of the dunder method __str__ .
    """
    # Constructor
    def __init__(self, id = -1, content = "", rating = -1.0, cid = -1):
        self.id = id
        self.content = content
        self.rating = rating
        self.course_id = cid
    
    """
    This method takes an argument called review_id and does the following:
        1. Opens the review.txt file that contains details of all the reviews
        2. Reads it line by line
        3. If the line contains the review_id in its review id field, make a new 
            Review object corresponding to the review in the current line, and 
            return it.
    """
    def find_review_by_id(self, review_id):
        review = None   # The Course object to be returned
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:   # Scan each line of review
                if line.split(';;;')[0] == str(review_id):   # If review ID's match
                    review = Review(line.split(';;;')[0],
                                        line.split(';;;')[1],
                                        line.split(';;;')[2],
                                        line.split(';;;')[3])
                    break
        return review
    
    """
    This method takes an argument called keyword and does the following:
        1. Opens the review.txt file that contains details of all the reviews
        2. Reads it line by line
        3. If the line contains the keyword in its review content, create a Review 
            object corresponding to the review in the current line, and add it 
            to the list of reviews to be returned.
        4. After reaching the end of file, return the result list.
    """
    def find_review_by_keywords(self, keyword):
        result_list = []   # The result list of reviews to be returned 
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:   # Scan each line of review
                if keyword in line.split(';;;')[1]:   # If keyword found in content
                    result_list.append(Review(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3]))
        return result_list
    
    """
    This method takes an argument called course_id and does the following:
        1. Opens the review.txt file that contains details of all the reviews
        2. Reads it line by line
        3. If the line contains the course_id in course_id field, create a Review 
            object corresponding to the review in the current line, and add it 
            to the list of reviews to be returned.
        4. After reaching the end of file, return the result list.
    """
    def find_review_by_course_id(self, course_id):
        result_list = []   # The result list of reviews to be returned 
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:   # Scan each line of review
                if line.split(';;;')[3].strip() == str(course_id):
                    # course ID's match
                    result_list.append(Review(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3]))
        return result_list
    
    """
    This method takes no arguments. It returns the number of reviews in the review.txt file
    1. It initialises a counter to 0
    2. Scans the review.txt file
    3. Increases the counter for each new scanned line
    Returns the counter.
    """
    def reviews_overview(self):
        reviewCount = 0   # Initialise the counter
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:   # Scan each line of review
                reviewCount += 1
        return (str(reviewCount))
    
    """
    Override the dunder __str__ method to return a string that is identical to the 
    entry of review found in the review.txt file
    """
    def __str__(self):
        return (str(self.id) + ";;;" + self.content + ";;;" 
                    + str(self.rating) + ";;;" + str(self.course_id))
    
# review = Review(65389432, "Good session", 4.5, 99986)
# print("\n",review.__str__())
# print("\n",review.find_review_by_id(65389432))
# print("\n",len(review.find_review_by_keywords("very bad")))
# print("\n",review.find_review_by_course_id(99986))
# print("\n",review.reviews_overview())
