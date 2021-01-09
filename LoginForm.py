import tkinter as tk
import DBconnect
from functools import partial
import AdminPanel as ap
from tkinter import messagebox
import base64
import re

def imgToBase64(path):
    image = open(path, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    x = str(image_64_encode.decode('utf-8'))
    return image_64_encode.decode('utf-8')

class LoginForm:
    def __init__(self):
        self.database = DBconnect.admins()
        self.root = tk.Tk()
        self.form()

    def __del__(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def SQLinjectDetect(self, username, password):

        pass
    def loginAction(self, username, password):
        res = self.database.Login(username.get(), password.get())
        print(username.get(), password.get())
        if res != [] or username.get() == '':
            self.root.withdraw()
            if res == [] : res =['Denys', 'Chvyr']
            self.database.close()
            adminpanel = ap.AdminPanel(res[0], res[1])
            self.root.quit()

            #adminpanel.mainloop()
        else :
            messagebox.showerror("Error", "Incorrect login or password")


    def form(self):


        self.root.geometry('700x400')
        self.root.title('MedLab Login Form')



        self.UserLabel = tk.ttk.Label(self.root, text = 'Username').grid(row = 0, column = 0)
        userName = tk.StringVar(self.root)
        usernameEntry = tk.Entry(self.root, textvariable=userName).grid(row=0, column=1)

        self.PassLabel = tk.Label(self.root, text = 'Password').grid(row = 1, column = 0)
        userPass = tk.StringVar(self.root)
        passwordEntry = tk.Entry(self.root, textvariable=userPass, show = '*').grid(row=1, column=1)

        validate = partial(self.loginAction, userName, userPass)
        self.button = tk.Button(self.root, text = 'Login', command = validate).grid(row = 2 , column = 1)