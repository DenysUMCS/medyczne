import tkinter as tkimport DBconnect as dbfrom functools import partialimport calendarclass addEmp:    def __init__(self):        self.root = tk.Tk()        self.root.title('MedLab Admin Panel (Add new employer)')        self.form()        self.root.mainloop()    def form(self):        self.fnameLabel = tk.Label(self.root, text='First name').grid(row=0, column=0)        fName = tk.StringVar()        fnameEntry = tk.Entry(self.root, textvariable=fName).grid(row=0, column=1)        self.lnameLabel = tk.Label(self.root, text='Last name').grid(row=1, column=0)        lname = tk.StringVar()        lnameEntry = tk.Entry(self.root, textvariable=lname).grid(row=1, column=1)class AdminPanel:    def __init__(self, fname, lname):        self.root = tk.Tk()        self.root.title('MedLab Admin Panel (%s %s)' % (fname, lname))        self.form()        self.root.mainloop()    def addEmployer(self):        x = addEmp()        pass    def form(self):        self.button = tk.Button(self.root, text='Add Employer', command=self.addEmployer).grid(row=2, column=1)