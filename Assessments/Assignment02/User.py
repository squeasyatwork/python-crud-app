import random
import math
import os
import re

class User():
   def __init__(self, id = -1, username = "", password = ""):
      self.id = id
      self.username = username
      self.password = password
      # self.login_user_info = ''
   
   def generate_user_id(self):
      """
      Keep generating a new id until a unique id is 
      obtained
      """
      while True:
         user_id = ""
         # Generate a random id string
         for i in range(10):
               user_id += str(random.randint(0,9))
               # print("-")
               # user_id = "443322"
         # Check if generated id is unique
         flag = 0
         with open("user_admin.txt", "r", encoding="utf-8") as adminFile:
            with open("user_instructor.txt", "a+", encoding="utf-8") as itrFile:
               with open("user_student.txt", "a+", encoding="utf-8") as studFile:
                  itrFile.seek(0, 0)
                  studFile.seek(0, 0)
                  for line in adminFile:
                     line_id = line.split(";;;")[0]
                     if user_id == line_id: # not unique, stop 
                        flag = 1
                        break
                  if flag == 0:
                     for line in itrFile:
                        line_id = line.split(";;;")[0]
                        if user_id == line_id: # not unique, stop 
                           flag = 1
                           break
                  if flag == 0:
                     for line in studFile:
                        line_id = line.split(";;;")[0]
                        if user_id == line_id: # not unique, stop 
                           flag = 1
                           break
                  if flag == 0:
                        # print("Unique ==> added")
                        break
      return user_id
   
   def encryption(self, input_password):
    all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    # your answer
    # Obtaining the three encoding characters
    first_character = all_punctuation[len(input_password) % len(all_punctuation)]
    second_character = all_punctuation[len(input_password) % 5]
    third_character = all_punctuation[len(input_password) % 10]
    # making a list of these three characters for use below
    encodingList = [first_character, second_character, third_character]
    # print(second_character)
    # Building the encrypted password
    i = 1
    output_str = ""
    for j in input_password:
        """Multiple the code character by its index i and 
        append this string before and after the password 
        character "j"
        """
        j = encodingList[i-1]*i + j + encodingList[i-1]*i
        output_str += j
        # Update index i in encodingList, reset to 0 if end of list reached
        i = (i+1) % 4
        if i == 0:
            i = 1
    # Add the final head and tail strings to the encrypted password
    output_str = "^^^" + output_str + "$$$"
    # print(output_str)
    return output_str
   
   def login(self):
      login_result = False
      login_user_role = ''
      login_user_info = []
      with open("user_admin.txt", "a+", encoding="utf-8") as adminFile:
         with open("user_instructor.txt", "a+", encoding="utf-8") as itrFile:
            with open("user_student.txt", "a+", encoding="utf-8") as studFile:
               adminFile.seek(0, 0)
               studFile.seek(0, 0)
               itrFile.seek(0, 0)
               for line in adminFile:
                  entry = line.split(";;;")
                  if(self.username == entry[1] and self.encryption(self.password) == entry[2].strip("\n")):
                     self.id = entry[0]
                     login_result = True
                     login_user_role = 'Admin'
                     login_user_info = [str(self.id), str(self.username), 
                                             str(self.password), str(login_user_role)]
                     break                      
               if not login_result:
                  for line in itrFile:
                     entry = line.split(";;;")
                     if(self.username == entry[1] and self.encryption(self.password) == entry[2].strip("\n")):
                        self.id = entry[0]
                        login_result = True
                        login_user_role = 'Instructor'
                        login_user_info = [str(self.id), str(self.username), 
                                                str(self.password), str(login_user_role)]
                        break
               if not login_result:
                  for line in studFile:
                     entry = line.split(";;;")
                     if(self.username == entry[1] and self.encryption(self.password) == entry[2].strip("\n")):
                        self.id = entry[0]
                        login_result = True
                        login_user_role = 'Student'
                        login_user_info = [str(self.id), str(self.username), 
                                                str(self.password), str(login_user_role)]
                        break
      if not login_result:
         login_user_role = 'INVALID'
         login_user_info = "USER_NOT_FOUND"
      return (login_result, login_user_role, login_user_info)
      
   def extract_info(self):
      print("You have no permission to extract information.")
      return None
   
   def view_courses(self, args=[]):
      print("You have no permission to view courses.")
      return None
   
   def view_users(self):
      print("You have no permission to view users.")
      return None
   
   def view_reviews(self, args=[]):
      print("You have no permission to view reviews.")
      return None
   
   def remove_data(self):
      print("You have no permission to remove data.")
      return None

   def __str__(self):
      return (str(self.id) + ";;;" + str(self.username)\
                  + ";;;" + str(self.password))

# print(a.__str__())