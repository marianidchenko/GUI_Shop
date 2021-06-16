from tkinter import *
from Users.authentication import *


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


if __name__ == '__main__':
    window = Tk()
    window.title('GUI Shop')
    window.geometry("800x600")  # window size
    login_or_register()
    window.mainloop()

