import tkinter as tk
import tksheet
import DBconnect as db
from functools import partial
import calendar



class AdminPanel:

    root = tk.Tk()
    sheet = tksheet.Sheet(root)
    emp = db.Employers()
    def __init__(self, fname, lname):
        self.root.title('MedLab Admin Panel (%s %s)' % (fname, lname))
        self.form()
        self.root.mainloop()

    def addEmployer(self):
        x = addEmp(self.emp)

    def refreshSheet(self):
        self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])

    def form(self):
        self.button = tk.Button(self.root, text='Add Employer', command=self.addEmployer).grid(row=2, column=1)
        self.sheet = tksheet.Sheet(self.root)
        self.sheet.grid()
        self.sheetHeaderList = ['ID', 'Employer First Name', 'Employer Last Name' ]
        self.sheet.headers([f'{c}' for c in self.sheetHeaderList])
        self.refreshSheet()

class addEmp(AdminPanel):

    def __init__(self, base):
        self.root = tk.Tk()
        self.emp = base
        self.root.title('MedLab Admin Panel (Add new employer)')
        self.form()
        self.root.mainloop()

    def confirm(self, fname, lname):
        print(fname.get(), lname.get())
        #self.emp.addEmployer(fname.get(), lname.get())
        #super().refreshSheet()
        super().sheet.set_sheet_data([list(x) for x in super().emp.showEmployers()])

    def form(self):
        self.fnameLabel = tk.Label(self.root, text='First name').grid(row=0, column=0)
        fName = tk.StringVar()
        fnameEntry = tk.Entry(self.root, textvariable = fName).grid(row=0, column=1)

        self.lnameLabel = tk.Label(self.root, text='Last name').grid(row=1, column=0)
        lname = tk.StringVar()
        lnameEntry = tk.Entry(self.root, textvariable = lname).grid(row=1, column=1)
        validate = partial(self.confirm, fName, lname)
        self.button = tk.Button(self.root, text='Add', command=validate).grid(row=2, column=1)