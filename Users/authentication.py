import json
from tkinter import messagebox
import re
password_requirements = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
name_requirements = r'(?:[A-Z][a-z]+([ ])*){2,}'


def log_in(username, password):
    with open('../Users/users.txt', 'r') as file:
        usernames = json.loads(file.read())
        if username in usernames:
            with open('../Users/credentials.txt', 'r') as password_file:
                credentials = json.loads(password_file.read())
                if password == credentials[username]:
                    pass # take to application
                else:
                    messagebox.showinfo(' ', 'Password is incorrect!')
                    return
        else:
            messagebox.showinfo(' ', 'Username is not registered. Please try again or create an account.')


def register_user(username, password, password_confirmation, name):

    try:
        with open('../Users/credentials.txt', 'r') as file:
            credentials = json.loads(file.read())
    except:
        credentials = {}

    try:
        with open('../Users/users.txt', 'r') as file:
            users = json.loads(file.read())
    except:
        users = []

    try:
        with open('../Users/names.txt', 'r') as file:
            names = json.loads(file.read())
    except:
        names = {}
    if re.match(name_requirements, name):
        if password_confirmation == password:
            if re.match(password_requirements, password):
                if username not in credentials.keys():
                    credentials[username] = password
                    users.append(username)
                    names[username] = name
                    with open('../Users/credentials.txt', 'w') as file:
                        json.dump(credentials, file)
                    with open('../Users/users.txt', 'w') as file:
                        json.dump(users, file)
                    with open('../Users/names.txt', 'w') as file:
                        json.dump(names, file)
                    messagebox.showinfo(' ', 'Registered successfully!')
                else:
                    messagebox.showinfo(' ', 'Already registered. Please log in.')
            else:
                messagebox.showinfo(' ', 'Password must be at least 8 characters '
                                         'and contain at least one letter and number.')
        else:
            messagebox.showinfo(' ', 'Passwords do not match.')
    else:
        messagebox.showinfo(' ', 'First and last name should not contain digits or '
                                 'special characters and start with a capital letter.')
