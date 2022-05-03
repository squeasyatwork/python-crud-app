import random
import math
import os
import re

class User():
   def __init__(self, id = -1, username = "", password = ""):
      self.id = id
      self.username = username
      self.password = password
   
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
         with open("user_admin.txt", "r") as filestreamone:
            with open("user_instructor.txt", "r") as filestreamtwo:
               with open("user_student.txt", "r") as filestreamthree:
                  for line in filestreamone:
                     line_id = line.split(";;;")[0]
                     if user_id == line_id: # not unique, stop 
                        flag = 1
                        break
                  if flag == 0:
                     for line in filestreamtwo:
                        line_id = line.split(";;;")[0]
                        if user_id == line_id: # not unique, stop 
                           flag = 1
                           break
                  if flag == 0:
                     for line in filestreamthree:
                        line_id = line.split(";;;")[0]
                        if user_id == line_id: # not unique, stop 
                           flag = 1
                           break
                  if flag == 0:
                        # print("Unique ==> added")
                        break
      return user_id
   
   def encryption(self, input_str):
    all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    # your answer
    # Obtaining the three encoding characters
    first_character = all_punctuation[len(input_str) % len(all_punctuation)]
    second_character = all_punctuation[len(input_str) % 5]
    third_character = all_punctuation[len(input_str) % 10]
    # making a list of these three characters for use below
    encodingList = [first_character, second_character, third_character]
    # print(second_character)
    # Building the encrypted password
    i = 1
    output_str = ""
    for j in input_str:
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

