import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

# Connecting to SQLite Database
connector = sqlite3.connect('library.db')
cursor = connector.cursor()

# Create table for library books if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS Library (
    BK_NAME TEXT,
    BK_ID TEXT PRIMARY KEY NOT NULL,
    AUTHOR_NAME TEXT,
    BK_STATUS TEXT,
    CARD_ID TEXT
)
''')

# Drop and recreate Users table to ensure ROLE column exists
cursor.execute('DROP TABLE IF EXISTS Users')
cursor.execute('''
CREATE TABLE Users (
    USERNAME TEXT PRIMARY KEY NOT NULL,
    PASSWORD TEXT,
    ROLE TEXT
)
''')

# Function to run the application
def run_application():
    global root
    root = Tk()
    root.title('DBU Library Management System')
    root.geometry('1010x530')
    root.resizable(0, 0)

    Label(root, text='LIBRARY MANAGEMENT SYSTEM  FOR  DBU  UNIVERATIY ', font=("Arial", 15, 'bold'), bg='SteelBlue', fg='White').pack(side=TOP, fill=X)

    show_login_page()

    root.mainloop()

# Initialize GUI elements
def initialize_gui_elements(role):
    global left_frame, RT_frame, RB_frame, tree
    global bk_name_entry, bk_id_entry, author_name_entry, bk_status_option

    # Frames
    left_frame = Frame(root, bg='LightSkyBlue')
    left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

    RT_frame = Frame(root, bg='DeepSkyBlue')
    RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

    RB_frame = Frame(root)
    RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

    # Left Frame
    Label(left_frame, text='Book Name', bg='LightSkyBlue', font=('Georgia', 13)).place(x=98, y=25)
    bk_name_entry = Entry(left_frame, width=25, font=('Times New Roman', 12))
    bk_name_entry.place(x=45, y=55)

    Label(left_frame, text='Book ID', bg='LightSkyBlue', font=('Georgia', 13)).place(x=110, y=105)
    bk_id_entry = Entry(left_frame, width=25, font=('Times New Roman', 12))
    bk_id_entry.place(x=45, y=135)

    Label(left_frame, text='Author Name', bg='LightSkyBlue', font=('Georgia', 13)).place(x=90, y=185)
    author_name_entry = Entry(left_frame, width=25, font=('Times New Roman', 12))
    author_name_entry.place(x=45, y=215)

    Label(left_frame, text='Status of the Book', bg='LightSkyBlue', font=('Georgia', 13)).place(x=75, y=265)
    bk_status_option = ttk.Combobox(left_frame, values=['Available', 'Issued'], font=('Times New Roman', 12), width=12)
    bk_status_option.place(x=75, y=300)

    if role == 'Admin':
        Button(left_frame, text='Add new record', font=('Gill Sans MT', 13), bg='SteelBlue', width=20, command=add_record).place(x=50, y=375)
        Button(left_frame, text='Clear fields', font=('Gill Sans MT', 13), bg='SteelBlue', width=20, command=clear_fields).place(x=50, y=435)
    else:
        bk_name_entry.config(state='disabled')
        bk_id_entry.config(state='disabled')
        author_name_entry.config(state='disabled')
        bk_status_option.config(state='disabled')

    # Right Top Frame
    if role == 'Admin':
        Button(RT_frame, text='Delete book record', font=('Gill Sans MT', 13), bg='SteelBlue', width=17, command=remove_record).place(x=8, y=30)
        Button(RT_frame, text='Delete full inventory', font=('Gill Sans MT', 13), bg='SteelBlue', width=17, command=delete_inventory).place(x=178, y=30)
        Button(RT_frame, text='Update book details', font=('Gill Sans MT', 13), bg='SteelBlue', width=17, command=update_record).place(x=348, y=30)
        Button(RT_frame, text='Change Book Availability', font=('Gill Sans MT', 13), bg='SteelBlue', width=19, command=change_availability).place(x=518, y=30)
        Button(RT_frame, text='Register Librarian', font=('Gill Sans MT', 13), bg='SteelBlue', width=19, command=register_librarian).place(x=688, y=30)

    # Right Bottom Frame
    Label(RB_frame, text='BOOK INVENTORY', bg='DodgerBlue', font=("Arial", 15, 'bold')).pack(side=TOP, fill=X)

    tree = ttk.Treeview(RB_frame, selectmode=BROWSE, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Issuer Card ID'))

    XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
    YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
    XScrollbar.pack(side=BOTTOM, fill=X)
    YScrollbar.pack(side=RIGHT, fill=Y)

    tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

    tree.heading('Book Name', text='Book Name', anchor=CENTER)
    tree.heading('Book ID', text='Book ID', anchor=CENTER)
    tree.heading('Author', text='Author', anchor=CENTER)
    tree.heading('Status', text='Status of the Book', anchor=CENTER)
    tree.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=CENTER)

    tree.column('#0', width=0, stretch=NO)
    tree.column('#1', width=225, stretch=NO)
    tree.column('#2', width=70, stretch=NO)
    tree.column('#3', width=150, stretch=NO)
    tree.column('#4', width=105, stretch=NO)
    tree.column('#5', width=132, stretch=NO)

    tree.place(y=30, x=0, relheight=0.9, relwidth=1)

    clear_and_display()

# Function to display login page
def show_login_page():
    global login_frame, login_username_entry, login_password_entry, login_role_option

    try:
        register_frame.destroy()
    except NameError:
        pass

    login_frame = Frame(root, bg='LightSkyBlue')
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(login_frame, text='Login', font=('Helvetica', 16), bg='LightSkyBlue').pack()

    Label(login_frame, text='Username:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    login_username_entry = Entry(login_frame, font=('Helvetica', 12))
    login_username_entry.pack()

    Label(login_frame, text='Password:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    login_password_entry = Entry(login_frame, font=('Helvetica', 12), show='*')
    login_password_entry.pack()

    Label(login_frame, text='Role:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    login_role_option = ttk.Combobox(login_frame, values=['Admin', 'Librarian'], font=('Times New Roman', 12), width=12)
    login_role_option.pack()

    Button(login_frame, text='Login', font=('Helvetica', 12), bg='SteelBlue', command=login_user).pack(pady=10)

    Button(login_frame, text='Register', font=('Helvetica', 12), bg='SteelBlue', command=show_register_page).pack()

# Function to display register page
def show_register_page():
    global register_frame, register_username_entry, register_password_entry, register_role_option

    try:
        login_frame.destroy()
    except NameError:
        pass

    register_frame = Frame(root, bg='LightSkyBlue')
    register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(register_frame, text='Register', font=('Helvetica', 16), bg='LightSkyBlue').pack()

    Label(register_frame, text='Username:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    register_username_entry = Entry(register_frame, font=('Helvetica', 12))
    register_username_entry.pack()

    Label(register_frame, text='Password:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    register_password_entry = Entry(register_frame, font=('Helvetica', 12), show='*')
    register_password_entry.pack()

    Label(register_frame, text='Role:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    register_role_option = ttk.Combobox(register_frame, values=['Admin', 'Librarian'], font=('Times New Roman', 12), width=12)
    register_role_option.pack()

    Button(register_frame, text='Register', font=('Helvetica', 12), bg='SteelBlue', command=register_user).pack(pady=10)

    Button(register_frame, text='Back', font=('Helvetica', 12), bg='SteelBlue', command=show_login_page).pack()

# Function to authenticate user login
def login_user():
    username = login_username_entry.get().strip().lower()
    password = login_password_entry.get().strip()
    role = login_role_option.get().strip()

    if not username or not password or not role:
        mb.showerror('Invalid Input', 'Username, password, and role cannot be empty.')
        return

    cursor.execute('SELECT * FROM Users WHERE USERNAME=? AND PASSWORD=? AND ROLE=?', (username, password, role))
    user = cursor.fetchone()

    if user:
        mb.showinfo('Login Successful', f'Welcome, {username.capitalize()} ({role})!')
        show_main_application(role)
    else:
        mb.showerror('Login Failed', 'Invalid username, password, or role.')

# Function to register new user
def register_user():
    username = register_username_entry.get().strip().lower()
    password = register_password_entry.get().strip()
    role = register_role_option.get().strip()

    if not username or not password or not role:
        mb.showerror('Invalid Input', 'Username, password, and role cannot be empty.')
        return

    try:
        cursor.execute('INSERT INTO Users (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)', (username, password, role))
        connector.commit()
        mb.showinfo('Registration Successful', 'User registered successfully.')
        show_login_page()
    except sqlite3.IntegrityError:
        mb.showerror('Registration Failed', 'Username already exists. Please choose another username.')

# Function to display main application interface
def show_main_application(role):
    login_frame.destroy()
    initialize_gui_elements(role)

# Function to ask for Issuer's Card ID
def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')

    if not Cid:
        mb.showerror('Issuer ID cannot be zero!', 'Issuer ID cannot be empty.')
    else:
        return Cid

# Function to display records in TreeView
def display_records():
    global tree

    tree.delete(*tree.get_children())

    curr = cursor.execute('SELECT * FROM Library')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

# Function to clear entry fields
def clear_fields():
    bk_name_entry.delete(0, END)
    bk_id_entry.delete(0, END)
    author_name_entry.delete(0, END)
    bk_status_option.set('Available')

# Function to clear fields and display updated records
def clear_and_display():
    clear_fields()
    display_records()

# Function to add a record to the database
def add_record():
    bk_name = bk_name_entry.get().strip()
    bk_id = bk_id_entry.get().strip()
    author_name = author_name_entry.get().strip()
    bk_status = bk_status_option.get()

    if not bk_name or not bk_id or not author_name:
        mb.showerror('Invalid Input', 'Please fill in all fields.')
        return

    if bk_status == 'Issued':
        card_id = issuer_card()
    else:
        card_id = 'N/A'

    surety = mb.askyesno('Are you sure?', 'Are you sure this is the data you want to enter?')

    if surety:
        try:
            cursor.execute(
                'INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                (bk_name, bk_id, author_name, bk_status, card_id))
            connector.commit()

            clear_and_display()

            mb.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            mb.showerror('Book ID already in use!',
                         'The Book ID you are trying to enter is already in the database.')

# Function to update a record in the database
def update_record():
    bk_name = bk_name_entry.get().strip()
    bk_id = bk_id_entry.get().strip()
    author_name = author_name_entry.get().strip()
    bk_status = bk_status_option.get()

    if not bk_name or not bk_id or not author_name:
        mb.showerror('Invalid Input', 'Please select a record to update.')
        return

    if bk_status == 'Issued':
        card_id = issuer_card()
    else:
        card_id = 'N/A'

    cursor.execute('UPDATE Library SET BK_NAME=?, AUTHOR_NAME=?, BK_STATUS=?, CARD_ID=? WHERE BK_ID=?',
                   (bk_name, author_name, bk_status, card_id, bk_id))
    connector.commit()

    clear_and_display()

# Function to delete a record from the database
def remove_record():
    global tree

    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    cursor.execute('DELETE FROM Library WHERE BK_ID=?', (selection[1],))
    connector.commit()

    tree.delete(current_item)

    mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

    clear_and_display()

# Function to delete the entire book inventory from the database
def delete_inventory():
    global tree

    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?'):
        tree.delete(*tree.get_children())

        cursor.execute('DELETE FROM Library')
        connector.commit()

        mb.showinfo('Done', 'The entire inventory was successfully deleted.')

        clear_and_display()

# Function to change book availability status
def change_availability():
    global tree

    if not tree.selection():
        mb.showerror('Error!', 'Please select a book from the database')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    BK_id = values['values'][1]
    BK_status = values["values"][3]

    if BK_status == 'Issued':
        if mb.askyesno('Is return confirmed?', 'Has the book been returned to you?'):
            cursor.execute('UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?', ('Available', 'N/A', BK_id))
            connector.commit()
    else:
        cursor.execute('UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?', ('Issued', issuer_card(), BK_id))
        connector.commit()

    clear_and_display()

# Function to register a librarian (only accessible to Admin)
def register_librarian():
    global register_frame, register_username_entry, register_password_entry, register_role_option

    register_frame = Frame(root, bg='LightSkyBlue')
    register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(register_frame, text='Register Librarian', font=('Helvetica', 16), bg='LightSkyBlue').pack()

    Label(register_frame, text='Username:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    register_username_entry = Entry(register_frame, font=('Helvetica', 12))
    register_username_entry.pack()

    Label(register_frame, text='Password:', font=('Helvetica', 12), bg='LightSkyBlue').pack()
    register_password_entry = Entry(register_frame, font=('Helvetica', 12), show='*')
    register_password_entry.pack()

    register_role_option = 'Librarian'

    Button(register_frame, text='Register', font=('Helvetica', 12), bg='SteelBlue', command=register_user).pack(pady=10)

    Button(register_frame, text='Back', font=('Helvetica', 12), bg='SteelBlue', command=register_frame.destroy).pack()

# Initialize the application
if __name__ == "__main__":
    run_application()
