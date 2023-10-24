from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter.simpledialog import askfloat
import os
from tkinter import messagebox

db_filename = 'simpleshop.sql'

if not os.path.exists(db_filename):
    conn = sqlite3.connect(db_filename)
    db = conn.cursor()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(50) NOT NULL,
            surname varchar(50) NOT NULL,
            login varchar(50) NOT NULL UNIQUE,
            password varchar(50) NOT NULL,
            cash float DEFAULT 1000
        )
    """)
    conn.commit()
else:
    conn = sqlite3.connect(db_filename)
    db = conn.cursor()



class Products:
    def __init__(self, name="", price=0,):
        self.name = name
        self.price = price

class Furniture(Products):
    def __init__(self, name="", price=0, size="",):
        self.size = size
        super().__init__(name, price)

class Food(Products):
    def __init__(self, name="", price=0, expiry="",):
        self.expiry = expiry
        super().__init__(name, price)

class Electronics(Products):
    def __init__(self, name="", price=0, voltage=0,):
        self.voltage = voltage
        super().__init__(name, price)

class Tools(Products):
    def __init__(self, name="", price=0,):
        super().__init__(name, price)

current_category = "All"
basket_contents = {}
total_price = 0
products = [
    Furniture("Desk", 200, "100x200"),
    Food("Apple", 2, "12.05.2023"),
    Electronics("Iphone", 400, 5),
    Tools("Hammer", 15),
    Electronics("Headphones", 150, 4),
    Tools("Screwdriver", 10)
]

def display_products(category="All"):
    for widget in products_frame.winfo_children():
        widget.destroy()

    row = 0
    column = 0

    for product in products:
        if category == "All" or category == product.__class__.__name__:
            frame = Frame(products_frame, width=225, height=225, highlightthickness=3, highlightcolor='black',
                          highlightbackground='blue', bg='#E6E6FA')
            frame.grid(row=row, column=column, pady=10, padx=10)
            frame.grid_propagate(0)
            
            label_name = Label(frame, text=product.name, font=(40), bg="#E6E6FA")
            label_name.grid(row=0, column=0, padx=10)

            label_price = Label(frame, text=f"${product.price}", font=(35), bg="#E6E6FA")
            label_price.grid(row=0, column=1)

            buy_button = Button(frame, text="Add to order", padx=40, pady=10, command=lambda prod=product: add_to_basket(prod), bg = "#ADD8E6")
            buy_button.grid(row=1, column=0, columnspan=2, pady=5)

            column += 1
            if column == 3:
                column = 0
                row += 1

def update_basket_display():
    global basket_frame
    basket_frame.destroy()
    basket_frame = Frame(menu_window, width=300, height=275, highlightthickness=3, highlightcolor='black', highlightbackground='blue', bg='white')
    basket_frame.place(x=30, y=500)
    basket_frame.pack_propagate(0) 

    label_basket = Label(basket_frame, text="Order contents:", font=(15), bg="white")
    label_basket.pack()

    global total_price
    total_price = 0

    for product_name, product_info in basket_contents.items():
        quantity = product_info['quantity']
        if quantity > 0:
            product = product_info['product']
            row_frame = Frame(basket_frame, bg="white")
            row_frame.pack(fill="x")

            label_product = Label(row_frame, text=f"{product.name} x{quantity}", bg="white", width=20)
            label_product.grid(row=0, column=0)

            remove_button = Button(row_frame, text="Remove", padx=10, command=lambda prod=product: remove_from_basket(prod), bg="#ADD8E6")
            remove_button.grid(row=0, column=1)

            total_price += product.price * quantity

    label_price = Label(basket_frame, text=f"Total price: ${total_price}", font=(12), bg="white")
    label_price.pack()




def add_to_basket(product):
    global total_price
    if product.name in basket_contents:
        basket_contents[product.name]['quantity'] += 1
    else:
        basket_contents[product.name] = {'product': product, 'quantity': 1}
    total_price += product.price
    update_basket_display()

def remove_from_basket(product):
    global total_price
    if product.name in basket_contents and basket_contents[product.name]['quantity'] > 0:
        basket_contents[product.name]['quantity'] -= 1
        total_price -= product.price
        update_basket_display()

def filter_category(category):
    global current_category
    current_category = category
    display_products(category)

def clickRegister(newWindow, loginEntry, passwordEntry, nameEntry, surnameEntry):
    login = loginEntry.get()
    password = passwordEntry.get()
    name = nameEntry.get()
    surname = surnameEntry.get()

    db.execute("SELECT * FROM users WHERE login=?", (login,))
    existing_user = db.fetchone()

    if existing_user:
        registrationMessage = Label(newWindow, text="Error! Login already exists.", fg='red')
    elif login == "" or password == "" or name == "" or surname == "":
        registrationMessage = Label(newWindow, text="Error! You need to provide data in each field", fg='red')
    else:
        cash = 1000.0 
        db.execute("INSERT INTO users (name, surname, login, password, cash) VALUES (?, ?, ?, ?, ?)", (name, surname, login, password, cash))
        conn.commit()
        registrationMessage = Label(newWindow, text="Congratulations! Registration completed!", fg='green')
    registrationMessage.place(x=53, y=300)


def clickLogin():
    login = login_entry.get()
    password = password_entry.get()

    db.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    existing_user = db.fetchone()

    if existing_user:
        login_window.withdraw()
        menu_window.deiconify()
        welcome_message.config(text='Welcome ' + login + '! Happy shopping!')
    else:
        wrongLoginMessage = Label(login_window, text="Wrong login or password!", fg="red", bg="white", font=(15))
        wrongLoginMessage.place(x=500, y=420)

def openRegister():
    reg = Toplevel()
    reg.title('Registration')
    reg.geometry('350x450')
    reg_label_title = Label(reg, text = 'Registration', font = (30))
    reg_label_title.pack()
    
    name_reg = Label(reg,text="Name", font=(15) )
    name_reg.place(x=0,y=30)
    name_entry_reg = Entry(reg, width=50)
    name_entry_reg.place(x=0, y = 60)

    surname_reg = Label(reg, text="Surname", font=(15))
    surname_reg.place(x=0,y = 90)
    surname_entry_reg = Entry(reg, width=50)
    surname_entry_reg.place(x=0,y = 120)
    
    login_reg = Label(reg,text="Login", font=(15) )
    login_reg.place(x=0,y=150)
    login_entry_reg = Entry(reg, width=50)
    login_entry_reg.place(x=0, y = 180)

    password_reg = Label(reg, text="Password", font=(15))
    password_reg.place(x=0,y = 220)
    password_entry_reg = Entry(reg, width=50)
    password_entry_reg.place(x=0,y = 250)
    
    reg_button = Button(reg,text="Register", fg='blue', padx=50,pady=30, command= lambda: clickRegister(reg, login_entry_reg, password_entry_reg, name_entry_reg, surname_entry_reg))
    reg_button.place(x=95,y=350)

def makeOrder():
    def reset_payment_window():
        ord.withdraw() 
        makeOrder() 

    ord = Toplevel()
    ord.title('Payment')
    ord.geometry('350x450')
    ord_label_title = Label(ord, text='Make order', font=(30))
    ord_label_title.pack()

    user_login = login_entry.get() 
    db.execute("SELECT cash FROM users WHERE login=?", (user_login,))
    user_balance = db.fetchone()[0]

    balance_label = Label(ord, text=f'Your money: ${user_balance}', font=(15))
    balance_label.place(x=20, y=50)

    add_cash = Button(ord, width=12, height=2, bg='#ADD8E6', text="Add money")
    add_cash.place(x=130, y=85)

    user_balance_label = Label(ord, text=f'Your money: ${user_balance}', font=(15))
    user_balance_label.place(x=20, y=50)

    basket_order_frame = Frame(ord, width=250, height=250, highlightthickness=2, highlightcolor='black', highlightbackground='blue', bg='white')
    basket_order_frame.place(x=50, y=135)
    basket_order_frame.pack_propagate(0)

    total_price = 0 

    for product_name, product_info in basket_contents.items():
        quantity = product_info['quantity']
        if quantity > 0:
            product = product_info['product']
            row_frame = Frame(basket_order_frame, bg="white")
            row_frame.pack(fill="x")
            row_frame.pack_propagate(0)

            label_product = Label(row_frame, text=f"{product.name} x{quantity}", bg="white", width=20)
            label_product.grid(row=0, column=0)
            label_price = Label(row_frame, text=f"${product.price * quantity}", bg="white")
            label_price.grid(row=0, column=1)

           
            total_price += product.price * quantity


    total_label = Label(basket_order_frame, text=f'Total: ${total_price}', font=(15), bg='white')
    total_label.pack(side="bottom")

    def add_money():
        amount = askfloat("Add Money", "Enter the amount of money to add:")
        if amount is not None and amount > 0:
            new_balance = user_balance + amount
            db.execute("UPDATE users SET cash = ? WHERE login = ?", (new_balance, user_login))
            conn.commit()
            user_balance_label.config(text=f'Your money: ${new_balance}')
            reset_payment_window() 

    add_cash.config(command=add_money)

    def process_payment():
        nonlocal user_balance, total_price 

        if not basket_contents:
            messagebox.showinfo("Empty Basket", "Your basket is empty. Please add items to your basket before making a payment.")
        elif user_balance >= total_price:
          
            new_balance = user_balance - total_price
            db.execute("UPDATE users SET cash = ? WHERE login = ?", (new_balance, user_login))
            conn.commit()
            user_balance = new_balance
            user_balance_label.config(text=f'Your money: ${new_balance}')
            total_label.config(text=f'Total: $0') 
            messagebox.showinfo("Payment Successful", "Payment was successful!")

        
            basket_contents.clear()
            update_basket_display()
            ord.withdraw() 
            makeOrder()

        else:
            messagebox.showerror("Insufficient Funds", "You don't have enough money to complete the purchase.")

    pay = Button(ord, width=12, height=2, bg='#ADD8E6', text="Pay", command=process_payment)
    pay.place(x=120, y=400)


    
def logout():
    login_window.deiconify()
    menu_window.withdraw()

login_window = Tk()
login_window.title("Shop")
login_window.geometry('1200x800')

background_login = PhotoImage(file="images/tlo.png")
background_label_login = Label(login_window, image=background_login)
background_label_login.place(x=0, y=0, relwidth=1, relheight=1)

logo = Image.open("images/logo.png")
logo = logo.resize((175, 175))
logo_tk = ImageTk.PhotoImage(logo)
logo_label = Label(login_window, image=logo_tk, bg='white')
logo_label.place(x=500, y=100)

welcome_label = Label(text="SimpleShop", font=("Bangers", 20), bg='white')
welcome_label.place(x=520, y=300)

label_login = Label(text="Login", bg='white')
label_login.place(x=445, y=325)
login_entry = Entry(login_window, width=50)
login_entry.place(x=445, y=350)

password_login = Label(text="Password", bg='white')
password_login.place(x=445, y=375)
password_entry = Entry(login_window, width=50)
password_entry.place(x=445, y=400)

register_button = Button(login_window, text="Register", padx=100, pady=20, font=(20), command=lambda: openRegister(), fg="blue")
register_button.place(x=450, y=550)

login_button = Button(login_window, text="Login", padx=114, pady=20, font=(20), command=lambda: clickLogin(), fg="blue")
login_button.place(x=450, y=450)

menu_window = Tk()
menu_window.title('Shop')
menu_window.geometry('1200x800')

background_menu = PhotoImage(file="images/tlo.png", master=menu_window)
background_label_menu = Label(menu_window, image=background_menu)
background_label_menu.place(x=0, y=0, relwidth=1, relheight=1)

basket_frame = Frame(menu_window, width=300, height=275, highlightthickness=3, highlightcolor='black', highlightbackground='blue', bg='white')
basket_frame.place(x=30, y=500)
basket_frame.grid_propagate(0)

categories_frame = Frame(menu_window, width=300, height=375, highlightthickness=3, highlightcolor='black', highlightbackground='blue', bg='white')
categories_frame.place(x=30, y=100)

products_frame = Frame(menu_window, width=800, height=675, highlightthickness=3, highlightcolor='black', highlightbackground='blue', bg='white')
products_frame.place(x=370, y=100)
products_frame.grid_propagate(0)

logout_frame = Frame(menu_window, width=700, height=70, highlightthickness=3, highlightcolor='black', highlightbackground='blue', bg='white')
logout_frame.place(x=30, y=20)

buy_frame = Frame(menu_window, width=400, height=70, highlightthickness=3, highlightcolor='black', highlightbackground='blue', bg='white')
buy_frame.place(x=770, y=20)

all_category = Button(categories_frame, text='All', font=(10), padx=100, pady=10, bg='#ADD8E6', command=lambda: filter_category('All'))
all_category.place(x=20, y=25)

electorincs_category = Button(categories_frame, text='Electronics', font=(10), padx=70, pady=10, bg='#ADD8E6', command=lambda: filter_category('Electronics'))
electorincs_category.place(x=20, y=100)

furniture_category = Button(categories_frame, text='Furniture', font=(10), padx=80, pady=10, bg='#ADD8E6', command=lambda: filter_category('Furniture'))
furniture_category.place(x=20, y=170)

food_category = Button(categories_frame, text='Food', font=(10), padx=95, pady=10, bg='#ADD8E6', command=lambda: filter_category('Food'))
food_category.place(x=20, y=240)

tools_category = Button(categories_frame, text='Tools', font=(10), padx=95, pady=10, bg='#ADD8E6', command=lambda: filter_category('Tools'))
tools_category.place(x=20, y=305)

logout = Button(logout_frame, text='Log out -->', font=(7), padx=60, pady=8, bg='#ADD8E6', command=logout)
logout.place(x=450, y=5)
welcome_message = Label(logout_frame, text='', font=(20), bg='white')
welcome_message.place(x=20, y=10)

gopay = Button(buy_frame, text='Make order', font=(7), padx=60, pady=8, bg='#ADD8E6', command = lambda: makeOrder())
gopay.place(x=70, y=5)

display_products()
menu_window.withdraw()
login_window.mainloop()
menu_window.mainloop()