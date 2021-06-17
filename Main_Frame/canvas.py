import ast
import tkinter
from tkinter import *
import json
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import string
password_requirements = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
name_requirements = r'(?:[A-Z][a-z]+([ ])*){2,}'

global current_user


def clear_view():
    for slave in window.grid_slaves():
        slave.destroy()


def login_or_register():
    clear_view()
    login = Button(window, text='Login', command=lambda: render_login_view())
    login.grid(column=0, row=0, padx=5, pady=5)
    register = Button(window, text='Register', command=lambda: render_register_view())
    register.grid(column=1, row=0, padx=5, pady=5)


def render_login_view():
    clear_view()
    # Username Entry
    Label(window, text="Username:").grid(column=0, row=0, padx=5, pady=5)
    username = Entry(window, width=30)
    username.grid(column=1, row=0, padx=5, pady=5)
    # Password Entry
    Label(window, text='Password:').grid(column=0, row=1, padx=5, pady=5)
    password = Entry(window, width=30, show='*')
    password.grid(column=1, row=1, padx=5, pady=5)
    # Login Button
    login_button = Button(window, text='Login', command=lambda: log_in(username.get(), password.get()))
    login_button.grid(column=1, row=2, padx=5, pady=5)
    back_button = Button(window, text='Back', command=lambda: login_or_register())
    back_button.grid(column=0, row=2, padx=5, pady=5)

    Label(window, text='Try the admin powers:\n'
                       'Username: admin\n'
                       'Password: adminpass1').grid(column=2, row=3, padx=250, pady=370)


def render_register_view():
    clear_view()
    # Name
    Label(window, text='First and Last Name:').grid(column=0, row=0, padx=5, pady=5)
    name = Entry(window, width=30)
    name.grid(column=1, row=0, padx=5, pady=5)
    # Username Entry
    Label(window, text="Username:").grid(column=0, row=1, padx=5, pady=5)
    username = Entry(window, width=30)
    username.grid(column=1, row=1, padx=5, pady=5)
    # Password Entry
    Label(window, text='Password:').grid(column=0, row=2, padx=5, pady=5)
    password = Entry(window, width=30, show='*')
    password.grid(column=1, row=2, padx=5, pady=5)
    # Password confirmation
    Label(window, text='Confirm Password:').grid(column=0, row=3, padx=5, pady=5)
    password_confirmation = Entry(window, width=30, show='*')
    password_confirmation.grid(column=1, row=3, padx=5, pady=5)
    # Register Button
    register_button = Button(window, text='Register',
                             command=lambda: register_user(username.get(), password.get(), password_confirmation.get(),
                                                           name.get()))
    register_button.grid(column=1, row=5, padx=5, pady=5)
    # Login Button
    login_button = Button(window, text='Login', command=lambda: render_login_view())
    login_button.grid(column=0, row=5, padx=5, pady=5)


def shop_view():
    clear_view()

    # Purchasing
    def purchase_item(i):
        with open('inventory.py') as items:
            templines = []
            for contents in items.read().splitlines():
                line = ast.literal_eval(contents)
                if line['id'] == i:
                    line['count'] -= 1
                    current_item = line['name']
                templines.append(line)
        with open('inventory.py', 'w'):
            pass
        with open('inventory.py', 'a') as newfile:
            for line in templines:
                newfile.write(str(line) + '\n')
        try:
            with open('../Stored_Data/bought_items.txt', 'r') as record:
                carts = json.loads(record.read())
        except:
            carts = {}
        cart = carts[current_user]
        if current_item not in cart:
            cart[current_item] = 1
        else:
            cart[current_item] += 1
        carts[current_user] = cart
        with open('../Stored_Data/bought_items.txt', 'w') as record:
            json.dump(carts, record)
        messagebox.showinfo(' ', 'Purchased successfully!')
        shop_view()

    # items
    with open('inventory.py') as file:
        for index, contents in enumerate(file.read().splitlines()):
            index += 1
            item = ast.literal_eval(contents)
            Label(window, text=f"{item['name']}").grid(column=index, row=0, padx=5, pady=2)
            image = Image.open(f"{item['image_path']}")
            photo = ImageTk.PhotoImage(image)
            img_label = Label(image=photo)
            img_label.image = photo
            img_label.grid(column=index, row=1, padx=5, pady=2)
            if item['count'] == 0:
                Label(window, text='OUT OF STOCK').grid(column=index, row=2, padx=5, pady=2)
            else:
                num = Button(window, text="Buy")
                num.configure(command=lambda b=index: purchase_item(b))
                num.grid(column=index, row=2, padx=5, pady=2)

    # Admin View:
    if current_user == 'admin':
        Button(window, text='Restock', command=lambda: item_add_view()).grid(row=3, column=1, padx=5, pady=2)


def item_add_view():
    clear_view()

    def restock(id, quantity):
        templines = []
        with open('inventory.py', 'r') as file:
            for row in file.read().splitlines():
                item = ast.literal_eval(row)
                if item['id'] == int(id):
                    item['count'] += int(quantity)
                templines.append(item)
            with open('inventory.py', 'w'):
                pass
            with open('inventory.py', 'a') as newfile:
                for line in templines:
                    newfile.write(str(line)+'\n')
    # ID
    Label(window, text='Item ID:').grid(column=0, row=0, padx=5, pady=5)
    id = Entry(window, width=30)
    id.grid(column=1, row=0, padx=5, pady=5)
    # Name
    Label(window, text="Add Quantity:").grid(column=0, row=1, padx=5, pady=5)
    quantity = Entry(window, width=30)
    quantity.grid(column=1, row=1, padx=5, pady=5)
    # add button
    add_button = Button(window, text='Restock', command=lambda: restock(id.get(), quantity.get()))
    add_button.grid(column=1, row=4, padx=5, pady=5)
    back_button = Button(window, text='Back', command=lambda: shop_view())
    back_button.grid(column=0, row=4, padx=5, pady=5)


def log_in(username, password):
    global current_user
    with open('../Stored_Data/names.txt', 'r') as file:
        usernames = json.loads(file.read())
        if username in usernames.keys():
            with open('../Stored_Data/credentials.txt', 'r') as password_file:
                credentials = json.loads(password_file.read())
                if password == credentials[username]:
                    messagebox.showinfo(' ', f"Welcome, {usernames[username]}")
                    current_user = username
                    shop_view()
                else:
                    messagebox.showinfo(' ', 'Password is incorrect!')
                    return
        else:
            messagebox.showinfo(' ', 'Username is not registered. Please try again or create an account.')


def register_user(username, password, password_confirmation, name):

    try:
        with open('../Stored_Data/credentials.txt', 'r') as file:
            credentials = json.loads(file.read())
    except:
        credentials = {}
    try:
        with open('../Stored_Data/names.txt', 'r') as file:
            names = json.loads(file.read())
    except:
        names = {}
    try:
        with open('../Stored_Data/bought_items.txt', 'r') as file:
            items = json.loads(file.read())
    except:
        items = {}
    if re.match(name_requirements, name):
        if password_confirmation == password:
            if re.match(password_requirements, password):
                if username not in names.keys():
                    credentials[username] = password
                    names[username] = name
                    items[username] = {}
                    with open('../Stored_Data/credentials.txt', 'w') as file:
                        json.dump(credentials, file)
                    with open('../Stored_Data/names.txt', 'w') as file:
                        json.dump(names, file)
                    with open('../Stored_Data/bought_items.txt', 'w') as file:
                        json.dump(items, file)
                    messagebox.showinfo(' ', 'Registered successfully!')
                    render_login_view()
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


if __name__ == '__main__':
    window = Tk()
    window.title('GUI Shop')
    window.geometry("800x600")  # window size
    login_or_register()
    window.mainloop()



