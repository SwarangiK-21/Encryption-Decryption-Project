from tkinter import *
from tkinter import messagebox, filedialog
import random
import string
import base64
import smtplib
from email.mime.text import MIMEText
import os
import json

# Encode and Decode Functions
def encode(key, msg):
    enc = []
    for i in range(len(msg)):
        list_key = key[i % len(key)]
        list_enc = chr((ord(msg[i]) + ord(list_key)) % 256)
        enc.append(list_enc)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, code):
    dec = []
    enc = base64.urlsafe_b64decode(code).decode()
    for i in range(len(enc)):
        list_key = key[i % len(key)]
        list_dec = chr((256 + ord(enc[i]) - ord(list_key)) % 256)
        dec.append(list_dec)
    return "".join(dec)

# UI Functions
def login_page():
    for widget in root.winfo_children():
        widget.destroy()

    # Styling the page background
    root.configure(bg="lightblue")

    # Title label
    Label(root, text="Secure Tool Welcomes You! Stay Protected With Us.", font=('Courier', 25, 'bold'), bg="lightblue", fg="navy").pack(pady=90)

    # Username label and entry
    Label(root, text="Username", font=('Courier', 18, 'bold'), bg="lightblue", fg="black").pack(pady=5)
    Entry(root, textvariable=username_var, font=('calibre', 18), bd=2, relief="solid", width=25).pack(pady=5)

    # Password label and entry
    Label(root, text="Password", font=('Courier', 18, 'bold'), bg="lightblue", fg="black").pack(pady=5)
    Entry(root, textvariable=password_var, show='*', font=('calibre', 18), bd=2, relief="solid", width=25).pack(pady=5)

    # Buttons for login and account creation
    Button(root, text="Login", command=login, bg="green", fg="white", font=('calibre', 15, 'bold'), width=15, height=1, bd=2, relief="raised").pack(pady=10)
    Button(root, text="Create Account", command=create_account, bg="blue", fg="white", font=('calibre', 15, 'bold'), width=15, height=1, bd=2, relief="raised").pack(pady=5)

    # Footer label
    Label(root, text="Your Security, Our Priority!", font=('Courier', 15, 'bold'), bg="lightblue", fg="black").pack(side="bottom", pady=10)

def main_interface():
    for widget in root.winfo_children():
        widget.destroy()

    # Styling the page background
    root.configure(bg="white")

    # Title label
    heading_label = Label(root, text="Encryption and Decryption Tool!", fg='navy', bg="white", font=('Courier', 25, 'bold'))
    heading_label.pack(pady=20)

    # Message label and entry
    Label(root, text='Enter the Message', font=('courier', 13, 'bold'), bg="white", fg="black").pack(pady=5)
    Entry(root, textvariable=message_var, width=40, font=('calibre', 13), bd=2, relief="solid").pack(pady=5)

    # Key label and entry
    Label(root, text='Enter the Key', font=('courier', 13, 'bold'), bg="white", fg="black").pack(pady=5)
    Entry(root, textvariable=key_var, show="*", width=40, font=('calibre', 13), bd=2, relief="solid").pack(pady=5)

    # Mode selection label and radio buttons
    Label(root, text='Select Mode (Encrypt/Decrypt)', font=('courier', 13, 'bold'), bg="white", fg="black").pack(pady=10)
    Radiobutton(root, text='Encrypt', variable=mode_var, value=1, bg="white", font=('calibre', 12)).pack()
    Radiobutton(root, text='Decrypt', variable=mode_var, value=2, bg="white", font=('calibre', 12)).pack()

    # Result label and entry
    Label(root, text='Result', font=('Courier', 13, 'bold'), bg="white", fg="darkgreen").pack(pady=5)
    Entry(root, textvariable=output_var, width=40, font=('calibre', 13), bd=2, relief="solid", bg="lightyellow").pack(pady=5)

    # Action buttons
    Button(root, text="Show Result", bg='lightblue', fg='black', font=('calibre', 10, 'bold'), command=calculate_result, width=20).pack(pady=10)
    Button(root, text="View History", bg='lightblue', fg='black', font=('calibre', 10, 'bold'), command=load_message_history, width=20).pack(pady=5)
    Button(root, text="Check Passkey Strength", bg='lightblue', fg='black', font=('calibre', 10, 'bold'), command=check_key_strength, width=20).pack(pady=5)
    Button(root, text="Toggle Dark Mode", bg='lightblue', fg='black', font=('calibre', 10, 'bold'), command=toggle_theme, width=20).pack(pady=5)
    Button(root, text='Reset', bg='lightblue', fg='black', font=('calibre', 10, 'bold'), command=reset, width=20).pack(pady=10)
    Button(root, text='Exit', bg='red', fg='black', font=('calibre', 10, 'bold'), command=login_page, width=20).pack(pady=10)

    # Footer label
    Label(root, text="Secure your data with ease", font=('Courier', 10, 'bold'), bg="white", fg="black").pack(side="bottom", pady=10)


def calculate_result():
    msg_text = message_var.get()
    k = key_var.get()
    i = mode_var.get()

    if not k:
        messagebox.showwarning('Warning', 'Please enter a key.')
        return

    try:
        if i == 1:
            output_var.set(encode(k, msg_text))
        elif i == 2:
            output_var.set(decode(k, msg_text))
        else:
            messagebox.showinfo('Error', 'Please choose either Encrypt or Decrypt.')
    except Exception as e:
        messagebox.showerror('Error', str(e))

def load_message_history():
    try:
        with open('message_history.txt', 'r') as file:
            history = file.read()
            messagebox.showinfo("Message History", history)
    except FileNotFoundError:
        messagebox.showinfo("Message History", "No history found.")        


def save_encrypted_message():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, 'w') as file:
            file.write(output_var.get())

def load_encrypted_message():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, 'r') as file:
            message_var.set(file.read())

def check_key_strength():
    strength = "Weak"
    passkey = key_var.get()
    if len(passkey) > 8 and any(char.isdigit() for char in passkey):
        strength = "Moderate"
    if len(passkey) > 12 and any(char.isupper() for char in passkey) and any(char in string.punctuation for char in passkey):
        strength = "Strong"
    messagebox.showinfo("Passkey Strength", f"Passkey strength: {strength}")


def toggle_theme():
    global headingLabel  # Use global headingLabel here too
    if root["bg"] == "azure2":
        root.configure(bg='gray20')
        headingLabel.configure(bg='gray20', fg='white')
    else:
        root.configure(bg='azure2')
        headingLabel.configure(bg='azure2', fg='black')            


def reset():
    message_var.set("")
    key_var.set("")
    mode_var.set(0)
    output_var.set("")

def create_account():
    username = username_var.get()
    password = password_var.get()

    if not username or not password:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    if len(password) < 8:
        messagebox.showwarning("Warning", "Password must be at least 8 characters long!")
        return

    try:
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
    except FileNotFoundError:
        accounts = {}

    if username in accounts:
        messagebox.showwarning("Warning", "Username already exists!")
        return

    accounts[username] = password

    with open("accounts.json", "w") as file:
        json.dump(accounts, file)

    messagebox.showinfo("Success", "Account created successfully!")
    login_page()

def login():
    username = username_var.get()
    password = password_var.get()

    try:
        with open("accounts.json", "r") as file:
            accounts = json.load(file)
    except FileNotFoundError:
        accounts = {}

    if accounts.get(username) == password:
        main_interface()
    else:
        messagebox.showerror("Error", "Invalid login credentials")


# Initialize Tkinter root
root = Tk()
root.title('Encryption Decryption Tool')
root.geometry('500x600')
root.configure(bg='azure2')

# Declare tkinter variables
username_var = StringVar()
password_var = StringVar()
message_var = StringVar()
key_var = StringVar()
output_var = StringVar()
mode_var = IntVar()

# Load the login page initially
login_page()

root.mainloop()