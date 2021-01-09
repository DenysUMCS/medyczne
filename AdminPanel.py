import tkinter as tk
import tksheet
import DBconnect as db
from functools import partial
from tkcalendar import DateEntry
from tkinter import messagebox
import base64
from PIL import ImageTk, Image
import pathlib
from tkinter import filedialog as fd



def imgToBase64(path):
    image = open(path, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    return image_64_encode.decode('utf-8')


def convertToPNG(path):
    im_start = Image.open(path)
    im_end = im_start.resize((200,270), Image.ANTIALIAS)
    im_end.save('tmp.png')
    return imgToBase64(str(pathlib.Path(__file__).parent.absolute())+'\\tmp.png')


class AdminPanel:

    emp = db.Employers()

    def __init__(self, fname, lname):
        self.prev = []
        self.frame = tk.Tk()  # tk.Frame(self.root)
        self.sheet = tksheet.Sheet(self.frame)
        self.sheet.hide("row_index")
        self.frame.title('MedLab Admin Panel (%s %s)' % (fname, lname))
        self.form()
        self.frame.mainloop()

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
        self.showEmployer()
        self.frame.after(500,self.refreshData)

    def showEmployer(self):

        selected = list(self.sheet.get_selected_cells())
        if (selected != [] and self.prev == []) or (selected != [] and self.prev[0][0] != selected[0][0]) :
            print(selected)
            self.idx = int(self.sheet.get_row_data(selected[0][0])[0])
            self.emp_data = self.emp.getEmployerData(self.idx)[:5]
            self.img_['data'] = self.emp.getEmployerPhoto(self.idx)

            self.lnameEntry.delete(0, tk.END)
            self.lnameEntry.insert(0, self.emp_data[2])

            self.fnameEntry.delete(0, tk.END)
            self.fnameEntry.insert(0, self.emp_data[1])

            #self.fnameEntry['text'] =
        self.prev = selected

    def getPhoto(self):
        file_name = fd.askopenfilenames()
        self.img_['data'] = convertToPNG(file_name[0])
        print(self.img_['data'])
        return convertToPNG(file_name[0])

    def editEmployerForm(self):
        self.emp_photo = tk.LabelFrame(self.f_emp)
        self.img_ = tk.PhotoImage(master=self.emp_photo)
        self.avatar = tk.Canvas(self.emp_photo, width=200, height=270, bg='white')
        self.avatar.create_image(0, 0, image=self.img_, anchor="nw")
        self.avatar.pack(side = tk.TOP)
        self.emp_edit_confirm = tk.Button(self.emp_photo, text='Download new photo', command = self.getPhoto).pack(side=tk.BOTTOM)
        self.emp_photo.pack(side = tk.TOP)

        self.edit_info = tk.LabelFrame(self.f_emp)
        self.lName = tk.StringVar(self.edit_info)
        self.fName = tk.StringVar(self.edit_info)
        self.fnameLabel = tk.Label(self.edit_info, text='First name').grid(row=1, column=0, ipadx=10, ipady=2)
        self.fnameEntry = tk.Entry(self.edit_info, textvariable=self.fName)
        self.fnameEntry.grid(row=1, column=1, ipadx=10, ipady=2)

        self.lnameLabel = tk.Label(self.edit_info, text='Last name').grid(row=2, column=0)
        self.lnameEntry = tk.Entry(self.edit_info, textvariable=self.lName)
        self.lnameEntry.grid(row=2, column=1)

        self.BDateLabel = tk.Label(self.edit_info, text='Birth date').grid(row=3, column=0)
        self.bdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.bdateEntry.grid(row=3, column=1)
        self.BDateLabel = tk.Label(self.edit_info, text='Start date').grid(row=4, column=0)
        self.SdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.SdateEntry.grid(row=4, column=1)
        self.edit_info.pack(side = tk.BOTTOM)
        #



    def form(self):

        self.f_bot = tk.LabelFrame(self.frame,text="Acttion")
        self.button = tk.Button(self.f_bot, text='Add Employer', command=self.addEmployer).pack(side = tk.LEFT)
        self.delete_button = tk.Button(self.f_bot, text='Delete Employer', command=self.deleteEmployer).pack(side = tk.RIGHT)#.grid(row=0, column=1)
        self.f_bot.pack(side = tk.BOTTOM, fill="both")

        self.f_top = tk.LabelFrame(self.frame, width =1300)
        self.sheet = tksheet.Sheet(self.f_top, width =1000, height = 500,)
        self.sheet.pack(side = tk.LEFT, fill="both", expand="yes")


        self.f_emp = tk.LabelFrame(self.f_top, text = "Employer ediit form", width = 300)
        self.editEmployerForm()
        self.f_emp.pack(side=tk.RIGHT, fill="both")

        self.f_top.pack(side=tk.TOP, fill="both", expand="yes")
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
                                    "hide_columns",
                                    "copy",
                                    "cut",
                                    "paste",
                                    "delete",
                                    "undo",
                                    "get_selection_boxes"
                                    "edit_cell"))
        self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])
        self.refreshData()

class addEmp:

    def __init__(self):
        self.master = tk.Tk()
        self.frame = tk.Frame(self.master)
        self.emp = db.Employers()
        self.form_()
        self.frame.pack()
        self.master.mainloop()

    def form_(self):
        self.master.title('MedLab Admin Panel (Add new employer)')
        lName = tk.StringVar(self.frame)
        fName = tk.StringVar(self.frame)
        self.image = ImageTk.PhotoImage( file = 'medyczne\default.jpg')
        self.img_ = tk.PhotoImage(file = self.image )
        self.avatar = tk.Canvas(self.frame, width=200, height=270, bg='white')
        self.avatar.create_image(0, 0, image=self.img_, anchor="nw")
        self.img_ = tk.PhotoImage(master = self.frame)
        self.avatar.grid(row=5, column=0)

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