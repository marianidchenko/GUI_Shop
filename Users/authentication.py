import json
from tkinter import messagebox


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


def register_user(username, password, password_confirmation):
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

    if password_confirmation == password:
        if username not in credentials.keys():
            credentials[username] = password
            users.append(username)
            with open('../Users/credentials.txt', 'w') as file:
                json.dump(credentials, file)
            with open('../Users/users.txt', 'w') as file:
                json.dump(users, file)
            messagebox.showinfo(' ', 'Registered successfully!')
        else:
            messagebox.showinfo(' ', 'Already registered. Please log in.')
    else:
        messagebox.showinfo(' ', 'Passwords do not match.')
