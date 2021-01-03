import tkinter as tk
import tksheet
import DBconnect as db
from functools import partial
from tkcalendar import DateEntry

class AdminPanel(tk.Tk):

    emp = db.Employers()
    def __init__(self, fname, lname):
        tk.Tk.__init__(self)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.emp.deleteEmployer(3)
        self.emp.deleteEmployer(4)
        self.sheet = tksheet.Sheet(self.frame)
        self.title('MedLab Admin Panel (%s %s)' % (fname, lname))
        self.form()

    def addEmployer(self):
        x = addEmp()

    def refreshData(self):
        self.sheet.set_sheet_data( [list(x) for x in self.emp.showEmployers()])
        self.after(500,self.refreshData)

    def form(self):

        self.button = tk.Button(self, text='Add Employer', command=self.addEmployer).grid(row=2, column=1)
        self.sheet = tksheet.Sheet(self)
        self.sheet.grid()
        self.sheetHeaderList = ['ID', 'Employer First Name', 'Employer Last Name']
        self.sheet.headers([f'{c}' for c in self.sheetHeaderList])
        self.sheet.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                    "drag_select",  # enables shift click selection as well
                                    "column_drag_and_drop",
                                    "row_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                     "row_width_resize",
                                     "column_height_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row",
                                    "hide_columns",
                                    "copy",
                                    "cut",
                                    "paste",
                                    "delete",
                                    "undo",
                                    "edit_cell"))
        self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])
        self.refreshData()


class addEmp(AdminPanel):

    def __init__(self):
        self.master = tk.Tk()
        self.frame = tk.Frame(self.master)
        self.emp = super().emp
        self.form_()
        self.frame.pack()

    def form_(self):
        self.master.title('MedLab Admin Panel (Add new employer)')
        lName = tk.StringVar(self.frame)
        fName = tk.StringVar(self.frame)
        self.fnameLabel = tk.Label(self.frame, text='First name').grid(row=0, column=0)
        fnameEntry = tk.Entry(self.frame, textvariable = fName).grid(row=0, column=1)

        self.lnameLabel = tk.Label(self.frame, text='Last name').grid(row=1, column=0)
        lnameEntry = tk.Entry(self.frame, textvariable = lName).grid(row=1, column=1)
        self.DateLabel = tk.Label(self.frame, text='Birth date').grid(row=2, column=0)
        dateEntry = DateEntry(self.frame).grid(row=2, column=1)
        def confirm(emp_name, emp_last):
            self.emp.addEmployer(emp_name.get(),emp_last.get())
            self.master.destroy()

        validate = partial(confirm, fName, lName)
        self.button = tk.Button(self.frame, text='Add', command=validate).grid(row=4, column=0, columnspan = 2, rowspan = 1)