import random
import math
import os
import re

class User():
   """
   This is the generic User class that is the parent class 
      for any user. It has the fields common to all its child 
      classes, i.e.:
         1. ID
         2. Username
         3. Password
   It has a constructor that sets value to these fields.
   It has the following methods:
      1. generate_user_id() to generate a unique user ID
      2. encryption() to encrypt a plain-text password
      3. login() to authenticate a user trying to log in
   It also has other methods which are to be overridden by 
      its child classes only when they have the permission e.g.,
      only an Admin class object can view users or extract/remove
      data. Hence, if not ovverridden, it means the corresponding 
      class does not have the permission to perform the action 
      e.g., an instructor can not remove data. 
   Hence, this class defines these methods as printing a 
      message that says operation not allowed.
   Lastly, it overrides the dunder __str__ method and returns 
      a string that stores user id, username, and password 
      separated by ";;;"
   """

   # Constructor
   def __init__(self, id = -1, username = "", password = ""):
      self.id = id
      self.username = username
      self.password = password
   
   def generate_user_id(self):
      """
      This method generates and returns a unique user ID that is
         not present anywhere across the user_admin, user_student, 
         and user_instructor files.
      It progresses as follows:
         1. Generate a 10-digit numeric string using random library
         2. Open the 3 user files as stated above, and scan each line
            of these files to search for a match of ID with the 
            generated id string.
         3. Keep repeating steps 1 and 2 until a match is not found.
         4. Now we have a unique user ID, return it.
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
         # Open all 3 user files
         with open("user_admin.txt", "r", encoding="utf-8") as adminFile:
            with open("user_instructor.txt", "a+", encoding="utf-8") as itrFile:
               with open("user_student.txt", "a+", encoding="utf-8") as studFile:
                  # Locate cursor at beginning of file
                  itrFile.seek(0, 0)
                  studFile.seek(0, 0)
                  # Scan the admin users file
                  for line in adminFile:
                     line_id = line.split(";;;")[0]
                     if user_id == line_id: # not unique, stop 
                        flag = 1
                        break
                  if flag == 0:   # Match not found
                     # Scan the instructor users file
                     for line in itrFile:
                        line_id = line.split(";;;")[0]
                        if user_id == line_id: # not unique, stop 
                           flag = 1
                           break
                  if flag == 0:   # Match not found
                     # Scan the student users file
                     for line in studFile:
                        line_id = line.split(";;;")[0]
                        if user_id == line_id: # not unique, stop 
                           flag = 1
                           break
                  if flag == 0:   # Match not found
                        # print("Unique ==> added")
                        break
      return user_id
   
   def encryption(self, input_password):
      """
      This function is used to encrypt the user password to enhance data security.
      It has one parameter which is the password in plain text.
      The function encrypts this argument string using the given logic and returns 
         it.
      This enrypted password string is returned.
      """
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
      iter = 1
      output_str = ""
      for ch in input_password:
         """Multiple the code character by its index iter and 
         append this string before and after the password 
         character ch
         """
         ch = encodingList[iter-1]*iter + ch + encodingList[iter-1]*iter
         output_str += ch
         # Update index i in encodingList, reset to 0 if end of list reached
         iter = (iter+1) % 4
         if iter == 0:
               iter = 1
      # Add the final head and tail strings to the encrypted password
      output_str = "^^^" + output_str + "$$$"
      # print(output_str)
      return output_str
   
   def login(self):
      """
      This method authenticates the user based on the username and password 
         credentials provided, and returns the login result as a tuple.
      It progresses the following way:
         1. Open all the user files.
         2. Scan each user line and compare the usernames and encrypted 
            passwords.
         3. Keep scanning until a match is found.
         4. If a match is found, set login result as successful, assign the 
            user a login role, set the user ID, and set the login user info 
            as a list of the form [id, un, pw, role].
         5.If a match is not found, display a wrong credentials message. 
      Return a tuple of the form (login_result, role, login_user_info)
      """
      login_result = False
      login_user_role = ''
      login_user_info = []
      # Open all 3 user files
      with open("user_admin.txt", "a+", encoding="utf-8") as adminFile:
         with open("user_instructor.txt", "a+", encoding="utf-8") as itrFile:
            with open("user_student.txt", "a+", encoding="utf-8") as studFile:
               # Relocate cursors to beginning of files
               adminFile.seek(0, 0)
               studFile.seek(0, 0)
               itrFile.seek(0, 0)
               # Scan each user file
               for line in adminFile:
                  entry = line.split(";;;")
                  if(self.username == entry[1] and self.encryption(self.password) == entry[2].strip("\n")):
                     # Match found, update values of fields/variables
                     self.id = entry[0]
                     login_result = True
                     login_user_role = 'Admin'
                     login_user_info = [str(self.id), str(self.username), 
                                             str(self.password), str(login_user_role)]
                     break                      
               if not login_result:   # Match not found yet
                  for line in itrFile:
                     entry = line.split(";;;")
                     if(self.username == entry[1] and self.encryption(self.password) == entry[2].strip("\n")):
                        # Match found, update values of fields/variables
                        self.id = entry[0]
                        login_result = True
                        login_user_role = 'Instructor'
                        login_user_info = [str(self.id), str(self.username), 
                                                str(self.password), str(login_user_role)]
                        break
               if not login_result:   # Match not found yet
                  for line in studFile:
                     entry = line.split(";;;")
                     if(self.username == entry[1] and self.encryption(self.password) == entry[2].strip("\n")):
                        # Match found, update values of fields/variables
                        self.id = entry[0]
                        login_result = True
                        login_user_role = 'Student'
                        login_user_info = [str(self.id), str(self.username), 
                                                str(self.password), str(login_user_role)]
                        break
      if not login_result:   # Match not found yet
         login_user_role = 'INVALID'
         login_user_info = "USER_NOT_FOUND"
      return (login_result, login_user_role, login_user_info)
      
   def extract_info(self):
      """
      Generic user action method that is to be ovverridden by the child 
      classes that have the permission to perform this action.
      """
      print("You have no permission to extract information.")
      return None
   
   def view_courses(self, args=[]):
      """
      Generic user action method that is to be ovverridden by the child 
      classes that have the permission to perform this action.
      """
      print("You have no permission to view courses.")
      return None
   
   def view_users(self):
      """
      Generic user action method that is to be ovverridden by the child 
      classes that have the permission to perform this action.
      """
      print("You have no permission to view users.")
      return None
   
   def view_reviews(self, args=[]):
      """
      Generic user action method that is to be ovverridden by the child 
      classes that have the permission to perform this action.
      """
      print("You have no permission to view reviews.")
      return None
   
   def remove_data(self):
      """
      Generic user action method that is to be ovverridden by the child 
      classes that have the permission to perform this action.
      """
      print("You have no permission to remove data.")
      return None

   def __str__(self):
      """
      Overridden dunder method that returns the user id, username, 
      and password as a string delimited by ";;;" 
      """
      return (str(self.id) + ";;;" + str(self.username)\
                  + ";;;" + str(self.password))

# print(a.__str__())