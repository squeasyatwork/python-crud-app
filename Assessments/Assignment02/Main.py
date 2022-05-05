from User import User
from Admin import Admin
from Instructor import Instructor
from Student import Student

def show_menu(role):
    print("\nPlease enter", role, "command for further service:")
    print("1. EXTRACT_DATA\n2. VIEW_COURSES\n3. VIEW_USERS")
    print("4. VIEW_REVIEWS\n5. REMOVE_DATA")
    return None
def process_operations(user_object):
    flag = 0
    # flag = int(input("(PROCESSOR) Enter flag value: "))
    input_string = input().split()
    if len(input_string) > 0:
        if(input_string[0]) == "logout":
            flag = 1
        else:
            if (len(input_string) <= 3 and len(input_string)>0):
                if type(user_object).__name__ == 'Admin':
                    # print("YOU ARE ADMIN")
                    if input_string[0] == '1':
                        if len(input_string) == 1:
                            user_object.extract_info()
                        else:
                            print("\nNo additional arguments allowed")
                    elif input_string[0] == '2':
                        if len(input_string) == 1:
                            print("Number of courses:", end = " ")
                            user_object.view_courses()
                        elif len(input_string) == 3:
                            user_object.view_courses\
                                ([input_string[1], input_string[2]])
                        else:
                            print("\nInvalid options! Enter 0 or 2 search options.")
                    elif input_string[0] == '3':
                        if (len(input_string) == 1):
                            print("Number of users:", end = " ")
                            user_object.view_users()
                        else:
                            print("\nNo additional arguments allowed")
                    elif input_string[0] == '4':
                        if len(input_string) == 1:
                            print("Number of reviews:", end = " ")
                            user_object.view_reviews()
                        elif len(input_string) == 3:
                            user_object.view_reviews\
                                ([input_string[1], input_string[2]])
                        else:
                            print("\nInvalid options! Enter 0 or 2 search options.")
                    elif input_string[0] == '5':
                        if (len(input_string) == 1):
                            user_object.remove_data()
                        else:
                            print("\nNo additional arguments allowed")
                    else:
                        print("\nInvalid command! Choose between 1-5")
                else:
                    # print("YOU ARE", type(user_object).__name__)
                    if input_string[0] == '1':
                        user_object.extract_info()
                    elif input_string[0] == '2':
                        if len(input_string) == 1:
                            user_object.view_courses()
                        else:
                            print("\nOptions not allowed!")
                    elif input_string[0] == '3':
                        user_object.view_users()
                    elif input_string[0] == '4':
                        if len(input_string) == 1:
                            user_object.view_reviews()
                        else:
                            print("\nOptions not allowed!")
                    elif input_string[0] == '5':
                        user_object.remove_data()
                    else:
                        print("\nInvalid command! Choose between 1-5")
            else:
                print("\nInvalid command/options!")
    else:
        print("\nChoose an option!")
    return flag

def main():
    while True:
        print("Please enter username and password", end = " ")
        print("to login:(format username password)")
        input_string = input().split(" ")
        if len(input_string) == 2 and input_string[0].replace("_", "X").isalpha():
            temp_user = User(-1, input_string[0], input_string[1])
            login_value = temp_user.login()
            if login_value[0]:
                userObj = None
                if login_value[1] == 'Admin':
                    userObj = Admin(login_value[2][0], 
                                        temp_user.username,
                                        temp_user.password)
                elif login_value[1] == 'Instructor':
                    userObj = Instructor(login_value[2][0], 
                                            temp_user.username,
                                            temp_user.password)
                elif login_value[1] == 'Student':
                    userObj = Student(login_value[2][0], 
                                        temp_user.username,
                                        temp_user.password)
                print("Login successful\nWelcome", 
                        temp_user.username, end = " ")
                print("Your role is {}.".format(login_value[1]))
                flag = 0
                show_menu(login_value[1])
                flag = process_operations(userObj)
                print()
                while flag == 0:
                    show_menu(login_value[1])
                    flag = process_operations(userObj)
                    print()
                if flag == 1:
                    print("Thank you for using our system")
                else:
                    print("SHUTDOWN: Thank you for using our system")
                    break
            else:
                print("username or password incorrect.")
        elif len(input_string) == 1 and input_string[0] == 'exit':
                print("SHUTDOWN: Thank you for using our system")
                break
        else:
            print("WRONG FORMAT for username/password: ", end = "\n\t")
            print("Username can have letters and _'s only,", end = "\n\t")
            print("password cannot have spaces.")
    return None


if __name__ == "__main__":
    # print a welcome message
    print("Welcome to our system")
    # manually register admin
    a = Admin(999, "admin", "admin")
    a.register_admin()
    # a.extract_info()
    main()