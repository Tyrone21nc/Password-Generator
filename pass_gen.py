"""
Author: Romain Dzeinse
Date: 06/7/24
Objective: Create an algorithm that validates passwords on making sure it includes all the requirments
filename: password_checker.py
Modified: 12/4 and 12/5/25
"""
import random
from pymongo import MongoClient
from bson.objectid import ObjectId
import os   # I use this for clearing the terminal


def generate_password(f_name):
    """
    This is the pseudocode:
    - First create the function with the appropriate parameters
    - create a variable named password to store all the password components
    - have random characters from first name
        - Then create a list with letters of the first name
        - Then get a set of 3, representing the number of characters in the f_name string;
            this is after the first round
        - The number of rounds is random from (2-4) between 2 and 3, not including 4
    - have random numbers (0-9)
        - Then randomly get 2 numbers from a numbers list
    - have random spec chars (!@#$%^&*())
        - Then randomly get 2 special characters from a spec char list
    - Then add all the random string characters from f_name, and then
        add the numbers, then ass the spec characters. That should be at least 10 characters

    :param f_name: the first name
    :return: this will return the generated password
    """
    password = ""
    random_set = random.choice(range(2, 4))
    for the_set in range(random_set):
        counter_for_upper_case = 0
        for i in range(3):
            random_fname = random.choice(f_name)
            if counter_for_upper_case == 0:
                random_fname = random_fname.upper()
            password += random_fname
            counter_for_upper_case += 1

    numbers = "1234567890"
    for i in range(2):
        random_num = random.choice(numbers)
        password += random_num

    special_characters = "!@#$%^&*()"
    for i in range(2):
        random_spec_char = random.choice(special_characters)
        password += random_spec_char

    return password

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["passwordManager"]
collection = db["savedPasswords"]

def save_password(password, nameF="First", nameL="Last"):
    # Ensure you are using consistent field names with dashes
    collection.insert_one({"password": password, "first-name": nameF, "last-name": nameL})
    print("\033[32mPassword saved!\033[0m")

def display_passwords():
    users = collection.find({}, {"_id": 1, "first-name": 1, "last-name": 1, "password": 1})
    print("\n\n\033[44mDISPLAYING PASSWORDS\033[0m")
    for user in users:
        # print("\033[32m________________________\033[0m")
        print("\033[41mUserID: " + str(user["_id"]) + "\033[0m")
        print("First Name: " + user["first-name"])
        print("Last Name: " + user["last-name"])
        print("Password: " + user["password"])
        print()
        # print("\033[32m¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\033[0m\n")

def delete_by_ID(id):
    passwords = collection
    print(f"\033[31mDELETING: {id}\033[0m")
    try:
        obj_id = ObjectId(id)
    except:
        print("invalid id or id format")
        return
    result = passwords.delete_one({"_id": obj_id})
    if result.deleted_count > 0:
        print("\033[32mDelete successful\033[0m")
    else:
        print("Invalid id, can't delete")

def create_password():
    """
    Allows us to create and return a "randomly" generated password
    """
    print("\t\t\033[7m*****Password generator*****\033[0m\nIt's not completely random, the program generates the password based\non characters found in your name\n")
    fname = input("Please enter your first name: ").lower()
    gene_pass = ""
    password_good = False
    while not password_good:
        if not fname:
            fname = "abcde"
        gene_pass = generate_password(fname)
        print(f"\033[32m{gene_pass}\033[0m")
        like_password = input("Do you like your password (y/n): ").lower()
        if like_password == "y":
            password_good = True
            print("I'm glad you like it")
    return gene_pass    # we return the generated password

def save_password1(created_pass=""):
    """
    Docstring for save_password1
        Save the created password passed as a parameter

    :param created_pass: this is the actual created password
    """
    if created_pass != "":
        print("We need your credentials to save your password")
        fname = input("Enter first name: ")
        lname = input("Enter last name: ")
        if(not fname):
            fname = "Tyrone"
        if(not lname):
            lname = "Brown"
        save_password(created_pass, fname, lname)
    else:
        print("There is no created password")

def save_password2():
    """
    Docstring for save_password1
        the user will save their own password, that they already created
    """
    user_pass = input("Enter your password: ")  # I will assume the password is valid
    print("We need your credentials to save your password")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    if(not fname):
        fname = "Tyrone"
    if(not lname):
        lname = "Brown"
    save_password(user_pass, fname, lname)

def valid_input(user_i=""):
    if user_i == "":
        print("\033[33m\033[7mEnter an option\033[0m", end="")
    while user_i.isnumeric() == False:
        user_i = input("""
1. Display current saved Passwords
2. Create a password
3. Save a password
4. Delete Password
5. Clear Terminal
6. Quit  
>>> """)
    return user_i

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')    # if the OS type is not WINDOWS, we use clear, if it is we use cls. "nt" = Windows NT, NT = "New Technology"



def options():
    """
    This will provide some options for the user to select from
    """
    print("\033[33m\033[7mEnter an option\033[0m", end="")
    user_input = input("""
    1. Display current saved Passwords
    2. Create a password
    3. Save a password
    4. Delete Password
    5. Clear Terminal
    6. Quit
    >>> """)
    valid_value = [1, 2, 3, 4, 5]
    save_password_values = [1, 2]
    saved_password = ""
    user_input = valid_input(user_input)
    
    user_input = int(user_input)
    while user_input != 6:
        if user_input in valid_value:
            if user_input == 1:  # if it's 1, we display the currently saved passwords
                display_passwords()
            elif user_input == 2:    # create a password
                saved_password = create_password()
            elif user_input == 3:   # save a password
                save_type = input("""\t1. Save the created password\n\t2. Save your own password\n\t>>> """)
                if save_type.isnumeric:
                    save_type = int(save_type)
                    if save_type in save_password_values:
                        if save_type == 1:
                            # print("There is no saved password")
                            save_password1(saved_password)
                        elif save_type == 2:
                            save_password2()
            elif user_input == 4:
                print("You can delete passwords by ID")
                delete_id = input("Enter ID: ")
                delete_by_ID(delete_id)
            elif user_input == 5:   # then clear the terminal
                clear_terminal()
        else:
            print("invalid option")
        print()
        user_input = valid_input()   # when it get's here, it has to be a number
        user_input = int(user_input)
            

if __name__ == "__main__":
    options()
    

