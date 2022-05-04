class Review:
    def __init__(self, id = -1, content = "", rating = -1.0, cid = -1):
        self.id = id
        self.content = content
        self.rating = rating
        self.course_id = cid
    
    def find_review_by_id(self, review_id):
        review = None
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:
                if line.split(';;;')[0] == str(review_id):
                    review = Review(line.split(';;;')[0],
                                        line.split(';;;')[1],
                                        line.split(';;;')[2],
                                        line.split(';;;')[3])
                    break
        return review
    
    def find_review_by_keywords(self, keyword):
        result_list = []
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:
                if keyword in line.split(';;;')[1]:
                    result_list.append(Review(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3]))
        return result_list
    
    def find_review_by_course_id(self, course_id):
        result_list = []
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:
                if line.split(';;;')[3].strip() == str(course_id):
                    result_list.append(Review(line.split(';;;')[0],
                                                line.split(';;;')[1],
                                                line.split(';;;')[2],
                                                line.split(';;;')[3]))
        return result_list
    
    def reviews_overview(self):
        reviewCount = 0
        with open('data/result/review.txt', 'r', encoding='utf-8') as reviewReader:
            for line in reviewReader:
                reviewCount += 1
        return (str(reviewCount))
    
    def __str__(self):
        return (str(self.id) + ";;;" + self.content + ";;;" 
                    + str(self.rating) + ";;;" + str(self.course_id))
    
# review = Review(65389432, "Good session", 4.5, 99986)
# print("\n",review.__str__())
# print("\n",review.find_review_by_id(65389432))
# print("\n",len(review.find_review_by_keywords("very bad")))
# print("\n",review.find_review_by_course_id(99986))
# print("\n",review.reviews_overview())
