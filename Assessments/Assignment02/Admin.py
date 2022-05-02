from User import User
import re
import os

class Admin(User):
    def __init__(self, id = -1, username = "", password = ""):
        User.__init__(self, id, username, password)

    def register_admin(self):
        username = input("Enter username:")
        flag = 0
        with open("user_admin.txt", "r+") as adminFile:
            pattern = re.compile(r';((\w)+);')
            matches = pattern.finditer(adminFile.read())
            for match in matches:
                if(match.groups('1')[0] == username):
                    flag = 1
                    # print("Match found in the line: ", match.__str__())
            if flag == 0:
                # print("Match NOT found")
                adminId = input("Enter ID: ")
                pw = input("Enter password: ")
                adminFile.seek(0, 2)
                adminFile.write(adminId+";;;"+username+";;;"+self.encryption(pw))
        return None
    
    def extract_course_info(self):
        
        return None

a = Admin()
a.register_admin()