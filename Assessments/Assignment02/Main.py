"""
This is the main file where the entire program runs.
It controls the flow of direct interaction with the user through the
terminal. It consists of functions for each of the following tasks:
    1. A starting code block that initalises and registers an Admin user who can extract and compile
        data about an education system that consists of several courses 
        taught by various instructors, and have several students that 
        enrol in it and give a review on the courses. 
    2. A main function to drive the program by calling various methods that perform actions such as authenticating and logging in users,
        showing them a list of actions, or asking them for an action to perform such as extract/view/remove data
        about courses/reviews/students/instructors. It also asks if the users want to exit the program.
    3. A menu function to display the actions that users may want to perform.
    4. A function that asks users what action they wish to perform, decides the validity of the requested action, and makes calls to various methods 
        across different classes to achieve the requested action.
Once the file reaches completion of execution, the entire program is complete.
"""

# Importing various class files that are used in the file
from User import User
from Admin import Admin
from Instructor import Instructor
from Student import Student

"""
This function displays the role of the logged in user, along with a complete list of actions that the system can perform for them.\
It accepts exactly 1 parameter:
    1. The role of the logged in user
"""
def show_menu(role):
    print("\nPlease enter", role, "command for further service:")
    print("1. EXTRACT_DATA\n2. VIEW_COURSES\n3. VIEW_USERS")
    print("4. VIEW_REVIEWS\n5. REMOVE_DATA")
    return None

"""
This function asks the user what action they wish to perform.
It makes various validation checks on the input it has taken from users in the order listed below:
    1. It stores all the input parameters entered by the users.
    2. It checks if the user has entered an empty input and displays an appropriate output message accordingly.
    3. It checks if the user has entered logout command.
    4. If not, it checks the role of the logged in user.
    5. If it is Admin, then all actions are checked and executed, otherwise only commands 2 and 4 are checked and executed.
    6. Then, it checks if the commands have been entered in the format specified by the program.
    7. If the format is correct, it checks the command chosen and checks if the correct number and type of input parameters have been entered.
    8. If the number and type of parameters is correct, then the corresponding functions are called; otherwise and appropriate output message is displayed.
After the command validation and execution is complete, it returns an integer value indicating whether the user wants to continue to stay logged in or they want to log out.
return value 0 means the user wants to continue to stay logged in,
return value 1 (or any other value) means the user wants to log out.
"""
def process_operations(user_object):
    flag = 0
    # flag = int(input("(PROCESSOR) Enter flag value: "))
    # Take the command input and store it in a comma-separated list called input_string
    input_string = input().split()
    # Check if user has entered an empty input
    if len(input_string) > 0:
        # Check if user has entered logout command
        if(input_string[0]) == "logout":
            flag = 1
        else:
            # Check if user has entered too many parameters
            if (len(input_string) <= 3):
                # Check if user is an Admin
                if type(user_object).__name__ == 'Admin':
                    # print("YOU ARE ADMIN")
                    # Check which command Admin user has entered
                    if input_string[0] == '1':
                        # Check number of parameters user has entered
                        if len(input_string) == 1:
                            user_object.extract_info()
                        else:   # If user has entered anything after 1
                            print("\nNo additional arguments allowed")
                    elif input_string[0] == '2':
                        if len(input_string) == 1:   # If user enters just 2
                            print("Number of courses:", end = " ")
                            user_object.view_courses()
                        # If user enters 2 parameters after entering 2
                        elif len(input_string) == 3:
                            user_object.view_courses\
                                ([input_string[1], input_string[2]])
                        else:   # If user enters just 1 parameter after entering 2
                            print("\nInvalid options! Enter 0 or 2 search options.")
                    elif input_string[0] == '3':
                        # Check number of parameters user has entered
                        if (len(input_string) == 1):
                            print("Number of users:", end = " ")
                            user_object.view_users()
                        else:   # If user has entered anything after 3
                            print("\nNo additional arguments allowed")
                    elif input_string[0] == '4':
                        if len(input_string) == 1:   # If user enters just 4
                            print("Number of reviews:", end = " ")
                            user_object.view_reviews()
                        # If user enters 2 parameters after entering 4
                        elif len(input_string) == 3:
                            user_object.view_reviews\
                                ([input_string[1], input_string[2]])
                        else:   # If user enters just 1 parameter after entering 4
                            print("\nInvalid options! Enter 0 or 2 search options.")
                    elif input_string[0] == '5':
                        # Check number of parameters user has entered
                        if (len(input_string) == 1):
                            user_object.remove_data()
                        else:   # If user has entered anything after 5
                            print("\nNo additional arguments allowed")
                    else:   # If user has entered any command other than 1/2/3/4/5
                        print("\nInvalid command! Choose between 1-5")
                else:
                    # print("YOU ARE", type(user_object).__name__)
                    if input_string[0] == '1':   # Command diallowed for non-Admins
                        user_object.extract_info()
                    elif input_string[0] == '2':
                        # Check number of parameters non-Admin user has entered
                        if len(input_string) == 1:
                            user_object.view_courses()
                        else:   # If user has entered anything after 2
                            print("\nOptions not allowed!")
                    elif input_string[0] == '3':   # Command diallowed for non-Admins
                        user_object.view_users()
                    elif input_string[0] == '4':
                        # Check number of parameters user has entered
                        if len(input_string) == 1:
                            user_object.view_reviews()
                        else:   # If user has entered anything after 4
                            print("\nOptions not allowed!")
                    elif input_string[0] == '5':   # Command diallowed for non-Admins
                        user_object.remove_data()
                    else:   # If user has entered any command other than 1/2/3/4/5
                        print("\nInvalid command! Choose between 1-5")
            else:
                print("\nInvalid command/options!")
    else:
        print("\nChoose an option!")
    return flag

"""
This function is the overall driver function that keeps the program flowing in the correct order, i.e.:
1. Ask user for username and password.
2. Create a temporary User object to store the user's provided credentials.
3. Authenticate the user by calling the login method in User class.
4. If login has been successful, assign the user a new Admin/Instructor/Student class object based on their role stored in the system.
5. Display a welcome message to the user showing them their role.
6. Call the process_operations() function until a non-zero return is received.
7. Log the user out of the system, and ask for a new username and password to log in to the system.
8. If "exit" is entered, stop the program.
9. The username can have letters and underscores only, the password cannot have spaces. Display appropriate output message if this validation fails.
This function returns nothing. 
"""
def main():
    # Keep running till exit is entered
    while True:
        # Input username and password
        print("Please enter username and password", end = " ")
        print("to login:(format username password)")
        input_string = input().split(" ")
        # Check if username and password are in correct format
        if len(input_string) == 2 and input_string[0].replace("_", "X").isalpha():
            temp_user = User(-1, input_string[0], input_string[1])
            # Authenticate user using provided credentials
            login_value = temp_user.login()
            if login_value[0]:   # If login is successful
                userObj = None
                # Check role of user stored in the system
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
                # Keep calling process_operations function until logout is entered
                show_menu(login_value[1])
                flag = process_operations(userObj)
                print()
                while flag == 0:
                    show_menu(login_value[1])
                    flag = process_operations(userObj)
                    print()
                if flag == 1:   # When logout command is input
                    print("Thank you for using our system")
                else:
                    print("SHUTDOWN: Thank you for using our system")
                    break
            else:   # Username password not found in system
                print("username or password incorrect.")
        elif len(input_string) == 1 and input_string[0] == 'exit':
                # User has entered exit command
                print("SHUTDOWN: Thank you for using our system")
                break
        else:
            print("WRONG FORMAT for username/password: ", end = "\n\t")
            print("Username can have letters and _'s only,", end = "\n\t")
            print("password cannot have spaces.")
    return None

"""
This block of code is the starting point of execution of the program. We 
display a welcome message, register an admin, and call the main() function.
"""
if __name__ == "__main__":
    # print a welcome message
    print("Welcome to our system")
    # manually register admin
    a = Admin(999, "admin", "admin")
    a.register_admin()
    # a.extract_info()
    main()