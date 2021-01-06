import tkinter as tk
import tksheet
import DBconnect as db
from functools import partial
from tkcalendar import DateEntry
from tkinter import messagebox


class AdminPanel(tk.Tk):

    emp = db.Employers()
    def __init__(self, fname, lname):
        tk.Tk.__init__(self)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.sheet = tksheet.Sheet(self.frame)
        self.sheet.hide("row_index")
        self.title('MedLab Admin Panel (%s %s)' % (fname, lname))
        self.form()

    def addEmployer(self):
        x = addEmp()

    def deleteEmployer(self):
        row = list(set([x[0] for x in self.sheet.get_selected_cells()]))
        if row != [] :
            for idx in row :
                data = self.sheet.get_row_data(idx)
                MsgBox = tk.messagebox.askquestion('Delete employer',
                                                   'Are you sure you want to delete %s %s'%(data[1], data[2]),
                                                   icon='question')
                if MsgBox == 'yes':
                    self.emp.deleteEmployer(int(data[0]))
        else :
            messagebox.showerror("Error", "Select Employer to delete")

    def refreshData(self):
        self.sheet.set_sheet_data( [list(x) for x in self.emp.showEmployers()])
        self.after(500,self.refreshData)

    def form(self):

        self.f_bot = tk.LabelFrame(self,text="Acttion")
        self.button = tk.Button(self.f_bot, text='Add Employer', command=self.addEmployer).pack(side = tk.LEFT)
        self.delete_button = tk.Button(self.f_bot, text='Delete Employer', command=self.deleteEmployer).pack(side = tk.RIGHT)#.grid(row=0, column=1)
        self.f_bot.pack(side = tk.BOTTOM, fill="both", expand="yes")

        self.sheet = tksheet.Sheet(self)
        self.sheet.pack(side = tk.TOP, fill="both", expand="yes")#.grid(row = 1,column = 1)
        self.sheetHeaderList = ['ID', 'Employer First Name', 'Employer Last Name', 'Birth date', 'Start date']
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
                                    "get_selection_boxes"
                                    "edit_cell"))
        self.sheet.extra_bindings([("cell_select", None),])
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

        self.BDateLabel = tk.Label(self.frame, text='Birth date').grid(row=2, column=0)
        bdateEntry = DateEntry(self.frame, date_pattern='dd/MM/yyyy')
        bdateEntry.grid(row=2, column=1)
        self.BDateLabel = tk.Label(self.frame, text='Start date').grid(row=3, column=0)
        SdateEntry = DateEntry(self.frame, date_pattern='dd/MM/yyyy')
        SdateEntry.grid(row=3, column=1)

        def confirm(emp_name, emp_last, bdateEntry, sdateEntry ):
            self.emp.addEmployer(emp_name.get(), #imie
                                 emp_last.get(), #nazwisko
                                 bdateEntry.get_date().strftime('%Y-%m-%d'), #urodziny
                                 sdateEntry.get_date().strftime('%Y-%m-%d')  #data zatrudnienia
                                 )
            self.master.destroy()

        validate = partial(confirm, fName, lName, bdateEntry, SdateEntry)
        self.confirm_button = tk.Button(self.frame, text='Add', command=validate).grid(row=4, column=0, columnspan = 2, rowspan = 1)