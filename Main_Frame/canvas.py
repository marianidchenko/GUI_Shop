import ast
from tkinter import *
import json
from PIL import Image, ImageTk
from tkinter import messagebox
import re
password_requirements = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
name_requirements = r'(?:[A-Z][a-z]+([ ])*){2,}'

global current_user


def clear_view():
    for slave in window.grid_slaves():
        slave.destroy()


def login_or_register():
    clear_view()
    login = Button(window, text='Login', bg="gray32", fg="white", font=('impact', 13),
                   command=lambda: render_login_view())
    login.config(height=2, width=10)
    login.grid(column=1, row=1, padx=10, pady=10)
    register = Button(window, text='Register', bg="gray32", fg="white", font=('impact', 13),
                      command=lambda: render_register_view())
    register.configure(height=2, width=10)
    register.grid(column=2, row=1, padx=10, pady=10)


def render_login_view():
    clear_view()
    # Username Entry
    Label(window, text="Username:", bg="dark grey", fg="black", font=('impact', 11)).grid(column=0, row=0,
                                                                                          padx=5, pady=5)
    username = Entry(window, width=30, font='Arial, 12')
    username.grid(column=1, row=0, padx=5, pady=5)
    # Password Entry
    Label(window, text='Password:', bg="dark grey", fg="black", font=('impact', 11)).grid(column=0, row=1,
                                                                                          padx=5, pady=5)
    password = Entry(window, width=30, show='*', font='Arial, 12')
    password.grid(column=1, row=1, padx=5, pady=5)
    # Login Button
    login_button = Button(window, text='Login', bg="gray32", fg="white", font=('impact', 11),
                          command=lambda: log_in(username.get(), password.get()))
    login_button.configure(height=1, width=8)
    login_button.grid(column=1, row=2, padx=5, pady=5)
    back_button = Button(window, text='Back', bg="gray32", fg="white", font=('impact', 11),
                         command=lambda: login_or_register())
    back_button.configure(height=1, width=8)
    back_button.grid(column=0, row=2, padx=5, pady=5)

    Label(window, text='Try the admin powers:\n'
                       'Username: admin\n'
                       'Password: adminpass1', background='grey56', font='Arial, 12').grid(column=2, row=3, padx=140, pady=320)


def render_register_view():
    clear_view()
    # Name
    Label(window, text='First and Last Name:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=0, padx=5, pady=5)
    name = Entry(window, width=30, font='Arial, 12')
    name.grid(column=1, row=0, padx=5, pady=5)
    # Username Entry
    Label(window, text="Username:", bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=1, padx=5, pady=5)
    username = Entry(window, width=30, font='Arial, 12')
    username.grid(column=1, row=1, padx=5, pady=5)
    # Password Entry
    Label(window, text='Password:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=2, padx=5, pady=5)
    password = Entry(window, width=30, show='*', font='Arial, 12')
    password.grid(column=1, row=2, padx=5, pady=5)
    # Password confirmation
    Label(window, text='Confirm Password:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=3, padx=5, pady=5)
    password_confirmation = Entry(window, width=30, show='*', font='Arial, 12')
    password_confirmation.grid(column=1, row=3, padx=5, pady=5)
    # Register Button
    register_button = Button(window, text='Register', bg="gray32", fg="white", font=('impact', 11),
                             command=lambda: register_user(username.get(), password.get(), password_confirmation.get(),
                                                           name.get()))
    register_button.grid(column=1, row=5, padx=5, pady=5)
    register_button.configure(height=1, width=8)
    # Login Button
    login_button = Button(window, text='Login', bg="gray32", fg="white", font=('impact', 11),
                          command=lambda: render_login_view())
    login_button.grid(column=0, row=5, padx=5, pady=5)
    login_button.configure(height=1, width=8)


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
        messagebox.showinfo(' ', 'Added to cart successfully!')
        shop_view()

    # items
    with open('inventory.py') as file:
        for index, contents in enumerate(file.read().splitlines()):
            index += 1
            item = ast.literal_eval(contents)
            Label(window, text=f"{item['name']}", bg="dark grey", fg="black", font=('impact', 11)
                  ).grid(column=index, row=0, padx=5, pady=5)
            image = Image.open(f"{item['image_path']}")
            photo = ImageTk.PhotoImage(image)
            img_label = Label(image=photo)
            img_label.image = photo
            img_label.grid(column=index, row=1, padx=5, pady=5)
            if item['count'] <= 0:
                Label(window, text='OUT OF STOCK', bg="dark grey", fg="black", font=('impact', 11)
                      ).grid(column=index, row=2, padx=5, pady=5)
            else:
                num = Button(window, text="Add to cart", bg="gray32", fg="white", font=('impact', 11))
                num.configure(command=lambda b=index: purchase_item(b), height=1, width=10)
                num.grid(column=index, row=2, padx=5, pady=5)

            if current_user == 'admin':
                restock = Label(window, text=f"Index: {item['id']}", bg="dark grey", fg="black", font=('impact', 11))
                restock.grid(column=index, row=3, padx=5, pady=5)
                restock.configure(height=1, width=8)

    cart = Button(window, text='My Cart', command=lambda: view_cart(), bg="gray32", fg="white",
                    font=('impact', 11))
    cart.grid(row=4, column=3, padx=5, pady=5)
    cart.configure(height=1, width=8)

    logout = Button(window, text='Log Out', command=lambda: login_or_register(), bg="gray32", fg="white",
                     font=('impact', 11))
    logout.grid(row=4, column=4, padx=5, pady=5)
    logout.configure(height=1, width=8)
    # Admin View:
    if current_user == 'admin':
        restock = Button(window, text='Restock', command=lambda: item_restock_view(), bg="gray32", fg="white",
                         font=('impact', 11))
        restock.grid(row=4, column=1, padx=5, pady=5)
        restock.configure(height=1, width=8)

        add = Button(window, text='Add', command=lambda: item_add_view(), bg="gray32", fg="white",
                     font=('impact', 11))
        add.grid(row=4, column=2, padx=5, pady=5)
        add.configure(height=1, width=8)


def item_restock_view():
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
        shop_view()
    # ID
    Label(window, text='Item ID:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=0, padx=5, pady=5)
    id = Entry(window, width=30, font='Arial, 12')
    id.grid(column=1, row=0, padx=5, pady=5)
    # Name
    Label(window, text="Add Quantity:", bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=1, padx=5, pady=5)
    quantity = Entry(window, width=30, font='Arial, 12')
    quantity.grid(column=1, row=1, padx=5, pady=5)
    # add button
    add_button = Button(window, text='Restock', bg="gray32", fg="white", font=('impact', 11),
                        command=lambda: restock(id.get(), quantity.get()))
    add_button.grid(column=1, row=4, padx=5, pady=5)
    add_button.configure(height=1, width=8)
    back_button = Button(window, text='Back', bg="gray32", fg="white", font=('impact', 11),
                         command=lambda: shop_view())
    back_button.grid(column=0, row=4, padx=5, pady=5)
    back_button.configure(height=1, width=8)


def item_add_view():
    clear_view()

    def add_item(id, name, path, count):
        invalid = False
        with open('inventory.py', 'r') as file:
            for raw in file.read().splitlines():
                item = ast.literal_eval(raw)
                if item["id"] == int(id):
                    messagebox.showinfo(' ', 'Item ID exists!')
                    invalid = True
                    break
        if not invalid:
            with open('inventory.py', 'a+') as file:
                line = {"id": int(id), 'name': f"{name}", "image_path": f"{path}", "count": int(count)}
                file.write(str(line) + '\n')
                messagebox.showinfo(' ', 'Added successfully!')

    # ID
    Label(window, text='Item ID:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=0, padx=5, pady=5)
    id = Entry(window, width=30, font='Arial, 12')
    id.grid(column=1, row=0, padx=5, pady=5)
    # Name
    Label(window, text='Name:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=1, padx=5, pady=5)
    name = Entry(window, width=30, font='Arial, 12')
    name.grid(column=1, row=1, padx=5, pady=5)
    # Image Path
    Label(window, text='Image Path:', bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=2, padx=5, pady=5)
    path = Entry(window, width=30, font='Arial, 12')
    path.grid(column=1, row=2, padx=5, pady=5)
    # Quantity
    Label(window, text="Quantity:", bg="dark grey", fg="black", font=('impact', 11)
          ).grid(column=0, row=3, padx=5, pady=5)
    quantity = Entry(window, width=30, font='Arial, 12')
    quantity.grid(column=1, row=3, padx=5, pady=5)
    # add button
    add_button = Button(window, text='Add', bg="gray32", fg="white", font=('impact', 11),
                        command=lambda: add_item(id.get(), name.get(),
                                                 path.get(), quantity.get()))
    add_button.grid(column=1, row=4, padx=5, pady=5)
    add_button.configure(height=1, width=8)
    back_button = Button(window, text='Back', bg="gray32", fg="white", font=('impact', 11),
                         command=lambda: shop_view())
    back_button.grid(column=0, row=4, padx=5, pady=5)
    back_button.configure(height=1, width=8)


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


def view_cart():
    new_count_dict = {}
    clear_view()
    with open('../Stored_Data/bought_items.txt', 'r') as file:
        dictionary = json.loads(file.read())
        files = dictionary[current_user]
    index = 0
    for key, value in files.items():
        Label(window, text=f" {key}:  ", bg="dark grey", fg="black", font=('impact', 13)
              ).grid(row=index, column=0, padx=5, pady=5)
        Label(window, text=f"{value}", bg="dark grey", fg="black", font=('impact', 13)
              ).grid(row=index, column=1, padx=5, pady=5)
        update_add = Button(window, text='+', bg="gray32", fg="white", font=('impact', 11),
                            command=lambda name=key, old_count=files[key]: update_cart_count(name, '+'))
        update_add.grid(row=index, column=3, padx=5, pady=5)
        update_add.configure(height=1, width=8)

        update_remove = Button(window, text='-', bg="gray32", fg="white", font=('impact', 11),
                               command=lambda name=key, old_count=files[key]: update_cart_count(name, '-'))
        update_remove.grid(row=index, column=2, padx=5, pady=5)
        update_remove.configure(height=1, width=8)
        index += 1

    back_button = Button(window, text='Back', bg="gray32", fg="white", font=('impact', 11),
                         command=lambda: shop_view())
    back_button.configure(height=1, width=8)
    back_button.grid(column=0, row=index, padx=5, pady=5)
    with open('../Stored_Data/bought_items.txt', 'r') as file:
        dictionary = json.loads(file.read())
        if not dictionary[current_user] == {}:
            buy = Button(window, text='Place Order', bg="gray32", fg="white", font=('impact', 11),
                         command=lambda: ordered())
            buy.configure(height=1, width=12)
            buy.grid(column=1, row=index, padx=5, pady=5)
        else:
            Label(window, text='Wow, empty. Go buy something.', bg="dark grey", fg="black", font=('impact', 13)
                  ).grid(row=index, column=1, padx=5, pady=5)


def update_cart_count(name, add_or_remove):
    with open('../Stored_Data/bought_items.txt', 'r') as file:
        cart = json.loads(file.read())
        for key, value in cart[current_user].items():
            if key == name:
                if add_or_remove == '+':
                    cart[current_user][key] += 1
                    break
                else:
                    cart[current_user][key] -= 1
                    if cart[current_user][key] == 0:
                        cart[current_user].pop(key)
                    break
    with open('../Stored_Data/bought_items.txt', 'w') as file:
        json.dump(cart, file)
    with open('inventory.py') as items:
        temp = []
        for contents in items.read().splitlines():
            line = ast.literal_eval(contents)
            if line["name"] == name:
                if add_or_remove == '+':
                    line['count'] -= 1
                else:
                    line['count'] += 1
            temp.append(line)
    with open('inventory.py', 'w'):
        pass
    with open('inventory.py', 'a') as newfile:
        for line in temp:
            newfile.write(str(line) + '\n')
    view_cart()


def ordered():
    messagebox.showinfo(' ', 'Ordered successfully. Items will be on their way.')
    with open('../Stored_Data/bought_items.txt', 'r') as file:
        dictionary = json.loads(file.read())
        dictionary[current_user] = {}
    with open('../Stored_Data/bought_items.txt', 'w') as file:
        json.dump(dictionary, file)
    view_cart()


if __name__ == '__main__':
    window = Tk()
    window.title('GUI Shop')
    window.geometry("800x600")  # window size
    window.configure(background='dark gray')
    login_or_register()
    window.mainloop()



