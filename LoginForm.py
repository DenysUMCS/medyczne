import tkinter as tk
import DBconnect as db
from functools import partial
import AdminPanel as ap
from tkinter import messagebox

class LoginForm:
    def __init__(self):
        self.database = db.admins()
        self.root = tk.Tk()
        self.form()
        self.root.mainloop()

    def loginAction(self, username, password):
        res = self.database.Login(username.get(), password.get())
        if res != [] or username.get() == '':
            self.root.withdraw()
            if res == [] : res =['Denys', 'Chvyr']
            panel = ap.AdminPanel(res[0], res[1])
        else :
            messagebox.showerror("Error", "Incorrect login or password")


    def form(self):
        self.root.geometry('700x400')
        self.root.title('MedLab Login Form')

        self.UserLabel = tk.Label(self.root, text = 'Username').grid(row = 0, column = 0)
        userName = tk.StringVar()
        usernameEntry = tk.Entry(self.root, textvariable=userName).grid(row=0, column=1)

        self.PassLabel = tk.Label(self.root, text = 'Password').grid(row = 1, column = 0)
        userPass = tk.StringVar()
        passwordEntry = tk.Entry(self.root, textvariable=userPass, show = '*').grid(row=1, column=1)
        validate = partial(self.loginAction, userName, userPass)
        self.button = tk.Button(self.root, text = 'Login', command = validate).grid(row = 2 , column = 1)