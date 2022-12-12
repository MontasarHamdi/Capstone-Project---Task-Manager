# Import required module
import datetime
import os, time
import stat


def username_check():  # Function to create dictionary of matching usernames and passwords
    # Declare local variables
    users = {}
    # Access "user.txt" file in read mode
    with open("user.txt", "r") as f:  # Run through "user.txt" file to check for matching usernames/passwords.
        for line in f:
            user_check = line.strip("\n")  # Prevent range out of bound errors as caused by empty lines
            if user_check != "":
                user_check = user_check.split(", ")
                users.update({user_check[0]: user_check[1]})
    return users


# Function to create a list of tasks
def task_check():  # Function to create a list of tasks
    tasks = []  # Declare local variables
    count = 1

    # Access "tasks.txt" file in read mode
    with open("tasks.txt", "r") as f:
        for line in f:  # Run through "tasks.txt" file to check for matching combination
            task_check = line.strip("\n")  # Prevent range out of bound errors as caused by empty lines
            if task_check != "":
                task_check = [task_check.split(", ") + [count]]
                tasks.extend(task_check)
                count += 1
    return tasks


# Function to log onto task manager program by matching username/password combination
def login():
    username = input("Please enter your username:\n")  # Get username and password combination from user
    password = input("Please enter your password:\n")
    print()

    # Call username_check() function to compare login details to dictionary storage
    user_list = username_check()
    if username in user_list and user_list.get(username) == password:
        return username

    else:
        print("Your username and/or password is incorrect, please ensure your caps lock is off and try again.\n")
        return "loop"


# Function to display appropriate menu
def menu():  # Declare local variables
    carry_on = True

    # While loop to continue returning to menu until user selects exit
    while carry_on:
        print('''\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
e - Exit''')
        if admin_rights:  # Only show the display statistics option if admin is logged in
            print("d - display statistics\n")
        print()
        selection = input()
        print()

        # if-elif-else statement to call function module based on user selection
        if selection.lower() == "r":
            reg_user()
        elif selection.lower() == "a":
            add_task()
        elif selection.lower() == "va":
            view_all()
        elif selection.lower() == "vm":
            view_mine()
        elif selection.lower() == "d":
            display_statistics()
        elif selection.lower() == "e":
            carry_on = False
            print("Thank you for using Task Manager. Goodbye!")
        elif selection.lower() == "gr":
            generate_reports()
        else:
            print("Your selection did not meet a menu item. Please try again.\n")


# Function to register a new user to "user.txt" file

def reg_user():
    carry_on = True  # Declare local variables
    user_list = username_check()
    if admin_rights == False:  # check that user has admin rights
        print("You do not have permission to perform this action.\n")
    else:
        while carry_on:  # While loop to ensure correct details are added
            with open("user.txt", "a") as f:  # Access "user.txt" file using 'a' modifier
                # Get username to be added from admin
                new_username = input("Please enter the username you would like to add, or 'e' to exit:\n")
                print()
                if new_username in user_list:   # check that username does not exist
                    print("This username already exists, please try a different username.\n")
                else:
                    password = input(f"Please enter a password for {new_username}:\n")
                    print()
                    confirmation = input("Please confirm the password entered:\n")
                    if password == confirmation:  # check if password and confirmation are the same
                        f.write(f"\n{new_username}, {password}\n")  # write new details in user text
                        print(f"new user {new_username} has been added!")
                        print()
                        carry_on = False
                    else:  # If password is not same as confirmation print error message and try again.
                        print("Your password and confirmation do not match, please try again.\n")


# Function to add a task to "tasks.txt" file

def add_task():
    on_user_list = True  # Declare local variables
    users_list = username_check()  # Call user_check to validate user_list

    with open("tasks.txt", "a") as f:  # Access the "tasks.txt" file and set modifier to append 'a'
        while on_user_list:  # while loop to get task information from user
            assigned_user = input("Who is the owner for this task?\n")
            if assigned_user in users_list:  # Make sure that assigned user is in the "user.txt" file.
                on_user_list = False
            else:
                print("The given user does not exist, please try again.\n")  # Improvement from previous project.
        title = input("Please enter title of task?\n")
        description = input("Please describe the task:\n")
        today = datetime.date.today()  # Get today's date
        today = today.strftime("%d %b %Y")  # Format date to be in dd mmm yyyy format
        date_due = input("Please enter when the task is due in dd mmm yyyy format (e.g. 30 May 1992):\n")
        complete = "No"
        # write all input data and time data into task file.
        f.write(f"\n{assigned_user}, {title}, {description}, {today}, {date_due}, {complete}\n")


# Function to view all tasks within the "tasks.txt" file

def view_all():
    tasks = task_check()  # Get list of tasks
    for i in range(0, len(tasks)):  # for loop to go through each task and print
        print("-" * 50)  # print tasks in a user-friendly manner. Improvement from previous project.
        print(f"Task:\t\t\t{tasks[i][1]}")
        print(f"Assigned to:\t\t{tasks[i][0]}")
        print(f"Date assigned:\t\t{tasks[i][3]}")
        print(f"Due date:\t\t{tasks[i][4]}")
        print(f"Task complete?\t\t{tasks[i][5]}")
        print(f"Task description:\n{tasks[i][2]}")
    print("-" * 50)
    print()


# Function to view all tasks assigned to only logged-in user in the tasks.txt file

def view_mine():
    tasks = task_check()  # Get list of tasks
    for i in range(0, len(tasks)):  # Use for loop to go through each task and print
        if user == tasks[i][0]:  # if user and assigned user match, print task.
            print("-" * 50)
            print(f"Task reference:\t\t{tasks[i][6]}")
            print(f"Task:\t\t\t{tasks[i][1]}")
            print(f"Assigned to:\t\t{tasks[i][0]}")
            print(f"Date assigned:\t\t{tasks[i][3]}")
            print(f"Due date:\t\t{tasks[i][4]}")
            print(f"Task complete?\t\t{tasks[i][5]}")
            print(f"Task description:\n{tasks[i][2]}")
    print("-" * 50)
    print()
    select_task()  # Run previously defined function select_task to edit or mark complete


# Function that print "task_overview.txt" and "user_overview.txt" files to the screen
# If files do not exist, first generate files

def display_statistics():
    old_file = True  # Declare local variables
    # Check that files have been generated. Learned about os.path.exists from ref links below.
    # https://docs.python.org/3/library/os.path.html
    # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
    if (os.path.exists('./task_overview.txt') == False) or (os.path.exists('./user_overview.txt') == False):
        generate_reports()
    else:
        # Check when files were generated and ask user if they would like to update them
        # Learned about os.stat here from this link: https://www.tutorialspoint.com/python/os_stat.htm
        # Learned about stat.ST_MTIME from this link: https://docs.python.org/3/library/stat.html
        task_time = os.stat('task_overview.txt')
        task_time = time.ctime(task_time[stat.ST_MTIME])  # convert format to a human_readable form
        user_time = os.stat('user_overview.txt')
        user_time = time.ctime(user_time[stat.ST_MTIME])   # stat.ST_MTIME gives last modification
        print(f"task_overview.txt was last modified {task_time} and user_overview.txt was last modified {user_time}")

        while old_file:
            regenerate = input("Would you like to update the files before proceeding? (yes or no)\n")
            print()

            if regenerate.lower() == "yes":
                generate_reports()
                print()
                old_file = False

            elif regenerate.lower() == "no":
                old_file = False

            else:
                print("invalid input\n")

    with open('task_overview.txt', 'r') as f:  # Print both files to output
        for line in f:
            print(line, end='')
    print()

    with open('user_overview.txt', 'r') as g:
        for line in g:
            print(line, end='')
    print()


# Function to select a task

def select_task():
    tasks = task_check()  # Get list of tasks
    task_selection = True  # Declare local variables

    while task_selection:  # Use while loop to get task number
        task_number = input("Please enter your task reference or '-1' to return to menu:\n")
        try:
            task_number = int(task_number)
        except:
            print("Invalid input\n")
        if task_number == -1:
            print()
            task_selection = False
            return
        else:
            for i in range(0, len(tasks)):
                if task_number == tasks[i][6] and tasks[i][5].lower() == "yes":  # if loop - conditions are set.
                    print(f"task reference {task_number} is already complete, no further editing is permitted\n")

                elif user == tasks[i][0] and task_number == tasks[i][6]:
                    edit_or_complete = input("Please enter 'mt' to mark task as complete or 'ed' to edit task?\n")
                    print()
                    if edit_or_complete.lower() != 'mt' and edit_or_complete.lower() != 'ed':
                        print("Invalid input.\n")
                    elif edit_or_complete.lower() == 'mt':
                        mark_task(task_number)
                        return

                    else:
                        edit_task(task_number)
                        return


# Function to mark task as complete

def mark_task(task_number):
    tasks = task_check()  # Get list of tasks
    string_task = ""  # Declare local variables
    for i in range(0, len(tasks)):  # for loop to check for task number and 'yes' complete status
        if task_number == tasks[i][6]:
            tasks[i][5] = "Yes"
        tasks[i].pop()  # .pop to remove added number in by task_check() function
        string_task += ", ".join(tasks[i]) + "\n"  # store each task in string_task variable.

    with open("tasks.txt", "w") as f:  # write variable string_task into task.txt file
        f.write(string_task)


# Function to edit assigned user and/or due date

def edit_task(task_number):
    tasks = task_check()  # Get list of tasks and users
    user_list = username_check()
    string_task = ""  # Declare local variables
    editing = True

    while editing:  # while loop to check if user wants to edit due date, or the user, or both.
        user_or_date = input(
            "Please enter 'user' to edit task assignment, 'date' to edit due date or 'both' to edit both:\n")

        if user_or_date.lower() == "user":
            new_user = input("Please enter the username to which this task should be assigned:\n")
            # If user selected, request change in user and check if it's in the user list
            if new_user in user_list:
                for i in range(0, len(tasks)):
                    if task_number == tasks[i][6]:
                        tasks[i][0] = new_user
                    tasks[i].pop()  # Remove number added in from task_check() function
                    string_task += ", ".join(tasks[i]) + "\n"

                editing = False

            else:
                print("Username does not exist\n")

        elif user_or_date.lower() == "date":  # If user selects date, request user to change due date
            new_date = input("Please enter when the task is due in dd mmm yyyy format:\n")
            for i in range(0, len(tasks)):
                if task_number == tasks[i][6]:
                    tasks[i][4] = new_date
                tasks[i].pop()
                string_task += ", ".join(tasks[i]) + "\n"

                editing = False

        elif user_or_date.lower() == "both":  # If user selects both, ask for new user change and change in due date.
            new_user = input("Please enter the username to which this task should be assigned:\n")
            if new_user in user_list:
                new_date = input("Please enter when the task is due in dd mmm yyyy format:\n")

                for i in range(0, len(tasks)):
                    if task_number == tasks[i][6]:
                        tasks[i][0] = new_user
                        tasks[i][4] = new_date
                    tasks[i].pop()
                    string_task += ", ".join(tasks[i]) + "\n"

                    editing = False
            else:
                print("Username does not exist\n")

    with open("tasks.txt", "w") as f:  # open tasks file with 'w' modifier and write string_task variable contents
        f.write(string_task)


# Function to generate 2 files: "task_overview.txt" and "user_overview.txt"
# Task_overview and user_overview will generate when user exits (e)
def generate_reports():
    task = task_check()  # Get task list and user list
    users = username_check()
    users = [*users]  # Convert user dictionary to a list of key values

    # Declare local variables
    total = len(task)
    total_users = len(users)
    complete = 0
    incomplete = 0
    overdue = 0
    percent_incomplete = 0
    percent_overdue = 0

    for i in range(0, total):  # Use for loop to find and count all tasks, incomplete tasks and overdue tasks
        if task[i][5].lower() == "yes":
            complete += 1
        elif task[i][5].lower() == "no" and datetime.datetime.strptime(task[i][4],
                                                                       '%d %b %Y') < datetime.datetime.now():
            incomplete += 1
            overdue += 1
            percent_incomplete = (incomplete / total) * 100
            percent_overdue = (overdue / total) * 100

        elif task[i][5].lower() == "no":
            incomplete += 1
            percent_incomplete = (incomplete / total) * 100

    with open("task_overview.txt", "w") as f:  # Create task_overview file and write variables. Make it easily readable.
        f.write(f"Number of tasks\t\t- {total}\n")
        f.write(f"Number completed\t- {complete}\n")
        f.write(f"Number incomplete\t- {incomplete}\n")
        f.write(f"Number overdue\t\t- {overdue}\n")
        f.write(f"Percentage incomplete\t- {percent_incomplete:.2f}%\n")
        f.write(f"Percentage overdue\t- {percent_overdue:.2f}%\n")

    with open("user_overview.txt", "w") as g:  # Create user_overview file and write variables. Make it easy to read.
        g.write(f"Total users\t- {total_users}\n")
        g.write(f"Total tasks\t- {total}\n\n")

        for i in range(0, total_users):  # Use for loop to go through users and separate tasks and their assigned user.
            # To prevent double counting declare local variables within for loop.
            user_tasks = 0
            completed = 0
            not_complete = 0
            user_overdue = 0
            task_percent = 0
            complete_percent = 0
            incomplete_percent = 0
            overdue_percent = 0
            # Use for loop to find completion status, due dates and task count for each specific user
            for j in range(0, total):
                if users[i] == task[j][0] and task[j][5].lower() == "yes":
                    user_tasks += 1
                    completed += 1

                # To allow for time comparisons against current time, use datetime.datetime.strptime(input, format).
                # This converts the string format date into a date object format.
                # Learned about this from link >>> https://www.programiz.com/python-programming/datetime/strptime
                elif users[i] == task[j][0] and task[j][5].lower() == "no" and datetime.datetime.strptime(task[j][4],
                                                                                                          '%d %b %Y') \
                        < datetime.datetime.now():
                    user_tasks += 1
                    not_complete += 1
                    user_overdue += 1

                elif users[i] == task[j][0] and task[j][5].lower() == "no":
                    user_tasks += 1
                    not_complete += 1

                # Calculate user percentages, prevent divide by 0 error but using if user_tasks != 0:
                task_percent = (user_tasks / total) * 100
                if user_tasks != 0:
                    complete_percent = (completed / user_tasks) * 100
                    incomplete_percent = (not_complete / user_tasks) * 100
                    overdue_percent = (user_overdue / user_tasks) * 100

            g.write("-" * 50 + "\n")  # write results to the user_overview file
            g.write(f"User: {users[i]}\n\n")
            g.write(f"Number of user tasks\t\t- {user_tasks}\n")
            g.write(f"Percentage of total tasks\t- {task_percent:.2f}%\n")
            g.write(f"Percentage completed\t\t- {complete_percent:.2f}%\n")
            g.write(f"Percentage incomplete\t\t- {incomplete_percent:.2f}%\n")
            g.write(f"Percentage overdue\t\t- {overdue_percent:.2f}%\n")


# This is the main log in program. Declare global variables.
login_attempt = True
admin_rights = False

while login_attempt:  # Use while loop to log into task manager program.
    user = login()

    if user == "admin":  # If user is admin, allow admin rights.
        admin_rights = True
        login_attempt = False

    elif user != "loop":
        login_attempt = False

menu()
