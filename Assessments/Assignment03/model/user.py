import os
import random, re
from lib.helper import get_day_from_timestamp

# print(sys.modules['lib.helper'])


class User:
    current_login_user = None

    # Constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role=""):
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role
        # Ensure constraint chk_role = [admin, instructor, student]

    def __str__(self):
        """
              Overridden dunder method that returns the user id, username,
              password, register time, and role as a string delimited by ";;;"
        """
        return (str(self.uid) + ";;;" + str(self.username)
                + ";;;" + str(self.password) + ";;;" + str(self.register_time)
                + ";;;" + str(self.role))

    def validate_username(self, username):
        if username.replace("_", "").isalpha():
            return True
        else:
            return False

    def validate_password(self, password):
        if len(password) >= 8:
            return True
        else:
            return False

    def validate_email(self, email):
        pattern = r"[a-zA-Z0-9_]+@.*\.com$"
        return bool(re.match(pattern, email) and len(email) > 8)

    def clear_user_data(self):
        with open("data/user.txt", "w") as userFile:
            pass

    def authenticate_user(self, username, password):
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
        # login_user_role = ''
        login_user_info = ""
        # Open all 3 user files
        with open("data\\user.txt", "r", encoding="utf-8") as userFile:
            # # Relocate cursors to beginning of files
            # adminFile.seek(0, 0)
            # studFile.seek(0, 0)
            # itrFile.seek(0, 0)

            # Scan each user file
            for line in userFile:
                entry = line.split(";;;")
                if username == entry[1] and self.encrypt_password(password) == entry[2].strip("\n"):
                    # # Match found, update values of fields/variables
                    # self.id = entry[0]
                    login_result = True
                    # login_user_role = 'Admin'
                    login_user_info = line
                    User.current_login_user = self
                    break

        # if not login_result:  # Match not found yet
        #     login_user_role = 'INVALID'
        #     login_user_info = "USER_NOT_FOUND"
        return login_result, login_user_info

    def check_username_exist(self, username):
        username_exists = False
        # login_user_role = ''
        # Open all 3 user files
        with open("data\\user.txt", "r", encoding="utf-8") as userFile:
            # # Relocate cursors to beginning of files
            # adminFile.seek(0, 0)
            # studFile.seek(0, 0)
            # itrFile.seek(0, 0)

            # Scan each user file
            for line in userFile:
                entry = line.split(";;;")
                if username == entry[1]:
                    # # Match found, update values of fields/variables
                    # self.id = entry[0]
                    username_exists = True
                    # login_user_role = 'Admin'
                    break

        # if not login_result:  # Match not found yet
        #     login_user_role = 'INVALID'
        #     login_user_info = "USER_NOT_FOUND"
        return username_exists

    def generate_unique_user_id(self):
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
            for i in range(6):
                user_id += str(random.randint(0, 9))
                # print("-")
                # user_id = "443322"
            # Check if generated id is unique
            flag = 0
            # Open all 3 user files
            with open("data/user.txt", "r", encoding="utf-8") as userFile:
                # # Locate cursor at beginning of file
                # itrFile.seek(0, 0)
                # studFile.seek(0, 0)
                # Scan the admin users file
                for line in userFile:
                    line_id = line.split(";;;")[0]
                    if user_id == line_id:  # not unique, stop
                        flag = 1
                        break
                if flag == 0:  # Match not found
                    # print("Unique ==> added")
                    break
        return user_id

    def encrypt_password(self, password):
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
        first_character = all_punctuation[len(password) % len(all_punctuation)]
        second_character = all_punctuation[len(password) % 5]
        third_character = all_punctuation[len(password) % 10]
        # making a list of these three characters for use below
        encoding_list = [first_character, second_character, third_character]
        # print(second_character)
        # Building the encrypted password
        itr = 1
        output_str = ""
        for ch in password:
            """Multiple the code character by its index iter and 
            append this string before and after the password 
            character ch
            """
            ch = encoding_list[itr - 1] * itr + ch + encoding_list[itr - 1] * itr
            output_str += ch
            # Update index i in encodingList, reset to 0 if end of list reached
            itr = (itr + 1) % 4
            if itr == 0:
                itr = 1
        # Add the final head and tail strings to the encrypted password
        output_str = "^^^" + output_str + "$$$"
        # print(output_str)
        return output_str

    def register_user(self, username, password, email, register_time, role):
        if self.check_username_exist(username):
            return False
        else:
            uid = self.generate_unique_user_id()
            password = self.encrypt_password(password)
            register_time = self.date_conversion(register_time)
            user_string = ";;;".join([uid, username, password, register_time, role, email])
            if role == "instructor":
                user_string += ";;;;;;;;;"
            with open("data/user.txt", "a") as userFile:
                userFile.write(user_string + "\n")
            return True

    def date_conversion(self, register_time):
        time_string = ""
        register_time = int(register_time)
        original_register_time = register_time
        second = 1000
        minute = second * 60
        hour = minute * 60
        day = hour * 24
        month = day * 30.437
        year = month * 12
        years = int(register_time // year)
        register_time -= (years * year)
        time_string += str(1970+years)
        months = int(register_time // month)
        register_time -= (months * month)
        time_string += "-" + "{:02d}".format(1 + months)
        # days = get_day_from_timestamp(original_register_time/1000) - 1
        days = int((register_time // day) + 1)
        register_time -= ((days-1) * day)
        time_string += "-" + "{:02d}".format(1 + days)
        hours = int(register_time // hour)
        register_time -= (hours * hour)
        time_string += "_" + "{:02d}".format(hours + 7)
        minutes = int(register_time // minute)
        register_time -= (minutes * minute)
        time_string += ":" + "{:02d}".format(minutes-3)
        seconds = int(register_time // second)
        register_time -= (seconds * second)
        time_string += ":" + "{:02d}".format(seconds)
        millis = int(register_time)
        time_string += "." + "{:02d}".format(millis)
        return time_string


# foo = User(username="username", password="12345678")
# # print(foo.validate_email('f9ij@.com'))
# foo.clear_user_data()