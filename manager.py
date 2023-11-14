# Not encrypted password manager by @intosins

import os
import hashlib
import json
import pyperclip
from tkinter import *
from tkinter import messagebox, simpledialog

data = {}

print('Made by @intosins')

def is_valid_account_website(website):
    valid_domains = ['.com', '.net', '.xyz', '.vip', '.lol', '.org', '.cn', '.de', '.ru', '.рф', '.ua', '.ukr', '.nl', '.store', '.uk', '.br', '.io', '.us']
    for domain in valid_domains:
        if website.endswith(domain):
            return True
    return False

def is_valid_account_email(email):
    valid_domains = ['@gmail.com', '@ukr.net', '@mail.ru', '@outlook.com', '@hotmail.com', '@proton.me', '@protonmail.com', '@yahoo.com']
    for domain in valid_domains:
        if email.endswith(domain):
            return True
    return False

def save_account():
    global data

    website = simpledialog.askstring('Message', 'Enter website:')
    if website is None:
        return
    elif not is_valid_account_website(website):
        messagebox.showerror('Message', 'Invalid or unsupported website domain.')
        return
    
    email = simpledialog.askstring('Message', 'Enter email:')
    if email is None:
        return
    elif not is_valid_account_email(email):
        messagebox.showerror('Message', 'Invalid or unsupported email domain.')
        return
    
    username = simpledialog.askstring('Message', 'Enter username:')
    if username is None:
        username = 'No Username'

    password = simpledialog.askstring('Message', 'Enter password:')
    if password is None:
        return
    
    hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()

    data[website] = {
        'email': email,
        'username': username,
        'password': password,
        'hashed': hashed,
        'secure': False # security features not added yet
    }

    with open('data', 'w') as file:
        json.dump(data, file, indent=4)

    display_accounts()

def load_accounts():
    global data
    try:
        with open('data', 'r') as file:
            content = file.read()
            if content:
                data = json.loads(content)
            else:
                data = {}
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}

def remove_account():
    global listbox, data
    selected_index = listbox.curselection()

    if not selected_index:
        messagebox.showinfo('Info', 'Please select an account to remove.')
        return

    selected_website = listbox.get(selected_index)
    selected_website = selected_website.split(':')[0]

    if selected_website in data:
        del data[selected_website]

        with open('data', 'w') as file:
            json.dump(data, file, indent=4)

        display_accounts()

def display_accounts():
    listbox.delete(0, END)

    for website, account_info in data.items():
        listbox.insert(END, f'{website}') # Email: {account_info["email"]} Username: {account_info['username']} Password: {account_info['password']}

def show_account_details(event):
    selected_index = listbox.curselection()

    if not selected_index:
        return

    selected_website = listbox.get(selected_index)
    selected_website = selected_website.split(':')[0]

    if selected_website in data:
        email_label.config(text=f'Email: {data[selected_website]['email']}')
        username_label.config(text=f'Username: {data[selected_website]['username']}')
        password_label.config(text=f'Password: {data[selected_website]['password']}')

def copy_account_password():
    selected_index = listbox.curselection()

    if not selected_index:
        messagebox.showinfo('Info', 'Please select an account to copy the password.')
        return

    selected_website = listbox.get(selected_index)
    selected_website = selected_website.split(':')[0]

    if selected_website in data:
        password = data[selected_website]['password']
        pyperclip.copy(password)

def create_data_file():
    if not os.path.exists('data'):
        with open('data', 'w') as file:
            json.dump({}, file)

def application():
    global listbox, email_label, username_label, password_label
    window = Tk()

    window.title('Password Manager')
    window.geometry('650x500')
    window.resizable(False, False)

    create_data_file()
    load_accounts()

    header_label = Label(window, text='Password Manager', font=('Arial', 20, 'bold'), bg='#4CAF50', fg='white', pady=10)
    header_label.pack(fill='x')

    listbox_frame = Frame(window)
    listbox_frame.pack(pady=10, side='left')

    listbox = Listbox(listbox_frame, width=35, height=15, selectmode=SINGLE, bd=0, font=('Arial', 12))
    listbox.pack(side='left', fill='both', expand=True)

    scrollbar = Scrollbar(listbox_frame, orient='vertical', command=listbox.yview)
    scrollbar.pack(side='right', fill='y')

    listbox.config(yscrollcommand=scrollbar.set)

    listbox.bind('<<ListboxSelect>>', show_account_details)

    display_accounts()

    accounts_frame = Frame(window)
    accounts_frame.pack(pady=(0, 10), side='left', padx=10)

    email_label = Label(accounts_frame, text='Email:', font=('Arial', 12))
    email_label.grid(row=0, column=0, padx=10, sticky='w')

    username_label = Label(accounts_frame, text='Username:', font=('Arial', 12))
    username_label.grid(row=1, column=0, padx=10, sticky='w')

    password_label = Label(accounts_frame, text='Password:', font=('Arial', 12))
    password_label.grid(row=2, column=0, padx=10, sticky='w')

    buttons_frame = Frame(window)
    buttons_frame.place(relx=0.5, rely=0.96, anchor='s')

    add_button = Button(buttons_frame, text='Add Account', font=('Arial', 14), command=save_account)
    add_button.grid(row=0, column=0, padx=10)

    remove_button = Button(buttons_frame, text='Remove Account', font=('Arial', 14), command=remove_account)
    remove_button.grid(row=0, column=1, padx=10)

    copy_button = Button(buttons_frame, text='Copy Password to Clipboard', font=('Arial', 14), command=copy_account_password)
    copy_button.grid(row=0, column=2, padx=10)

    window.mainloop()

if __name__ == '__main__':
    application()
