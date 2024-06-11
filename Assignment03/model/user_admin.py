from model.user import User


class Admin(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="admin"):
        super().__init__(uid, username, password, register_time, role)
        # Admin does not have email attribute

    def register_admin(self):
        username = "admin_account"
        password = self.encrypt_password("admin_account")
        self.username = username
        self.password = password
        if not self.check_username_exist(username):
            # !Enter register_time
            with open("data/user.txt", "a") as adminFile:
                adminFile.write(self.generate_unique_user_id() + ";;;" + username
                                + ";;;" + password + ";;;" + self.register_time
                                + ";;;" + self.role + "\n")
        return None


# print(Admin(register_time="2022-01-10_13:12:11.123"))
