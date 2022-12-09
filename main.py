from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]

    password_symbols = [choice(symbols) for char in range(randint(2, 4))]

    password_numbers = [choice(numbers) for char in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_info():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Caution", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                                              f"\nPassword: {password}\n Is it ok to save?")

        if is_ok:
            try:
                with open("data_file.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data_file.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.updata(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
def find_password():
    website = website_input.get()
    with open("data_file.json") as data_file:
        json_file = json.load(data_file)
    if website in json_file:
        email = json_file[website]["email"]
        password = json_file[website]["password"]
        messagebox.showinfo(title=website, message=f"Email/User_name: {email}\n, Password: {password}")

    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} exits.")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
# Website label and Entry
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_label.focus()
website_input = Entry(width=35)
website_input.grid(column=1, row=1)
#
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_input = Entry(width=35)
email_input.insert(0, "lenovo12@gmail.com")
email_input.grid(column=1, row=2)
#
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry(width=21)
password_input.grid(column=1, row=3, columnspan=2)
#
gen_pass_button = Button(text="Generate Password", command=generate_password)
gen_pass_button.grid(column=2, row=3)
#
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1)
#
add_button = Button(text="Add", width=36, command=add_info)
add_button.grid(column=1, row=4)
#
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
image = canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

window.mainloop()
