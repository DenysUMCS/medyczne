import tkinter as tk
import tksheet
import DBconnect as db
from functools import partial
from tkcalendar import DateEntry
from tkinter import messagebox
import base64
from PIL import Image
import pathlib
from tkinter import filedialog as fd
import string



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

    def __init__(self, fname, lname):
        self.emp = db.Employers()
        self.pat = db.Patient()
        self.prev = []
        self.idx = -1
        self.frame = tk.Tk()  # tk.Frame(self.root)
        self.sheet = tksheet.Sheet(self.frame)
        self.sheet.hide("row_index")
        self.frame.title('MedLab Admin Panel (%s %s)' % (fname, lname))
        self.form()
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.lam = lambda x: [x[0], x[1], x[2].strftime('%d-%b-%Y'),
                              '%s - %s' % (x[3].lower.strftime('%H:%M'), x[3].upper.strftime('%H:%M')), x[4]]
        self.frame.mainloop()

    def on_closing(self):
        MsgBox = tk.messagebox.askquestion('Close program',
                                           'Are you sure you want to exit',
                                           icon='question')
        if MsgBox == 'yes':
            del self.emp
            self.frame.quit()

    def addEmployer(self):
        app = addEmp(None, self.emp)
        app.title = "Add employer"
        app.mainloop()
        self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])
        self.frame.update()

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
                    self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])
                    self.frame.update()
        else :
            messagebox.showerror("Error", "Select Employer to delete")

    def refreshData(self):
        #self.sheet.set_sheet_data( [list(x) for x in self.emp.showEmployers()])
        self.showEmployer()
        self.frame.after(500,self.refreshData)

    def showEmployer(self):

        selected = list(self.sheet.get_selected_cells())
        if (selected != [] and self.prev == []) or (selected != [] and self.prev[0][0] != selected[0][0]) :
            self.idx = int(self.sheet.get_row_data(selected[0][0])[0])
            self.emp_data = self.emp.getEmployerData(self.idx)
            self.img_['data'] = base64.b64decode(self.emp_data[5].translate({ord(c): None for c in string.whitespace}))
            self.lnameEntry.delete(0, tk.END)
            self.lnameEntry.insert(0, self.emp_data[2])
            self.fnameEntry.delete(0, tk.END)
            self.fnameEntry.insert(0, self.emp_data[1])
            self.bdateEntry.set_date(self.emp_data[3])
            self.SdateEntry.set_date(self.emp_data[4])
            self.pattients = [self.lam(x) for x in self.pat.showDoctorPatients(self.idx)]
            for i in self.pattients:
                i.insert(2,self.emp_data[1] + ' ' + self.emp_data[2])
            self.sheet_pattient.set_sheet_data(self.pattients)
            self.frame.update()
        self.prev = selected

    def getPhoto(self):
        file_name = fd.askopenfilenames()
        self.img_['data'] = convertToPNG(file_name[0])
        print(self.img_['data'])
        return convertToPNG(file_name[0])

    def confirm(self, id, emp_name, emp_last, bdateEntry, sdateEntry):
        try:
            self.id = int(self.sheet.get_row_data( list(self.sheet.get_selected_cells())[0][0])[0])
        except TypeError:
            messagebox.showerror("Error", "Select Employer to show")
            return
        self.emp.updateEmployer( self.id,
                             emp_name.get(),  # imie
                             emp_last.get(),  # nazwisko
                             bdateEntry.get_date().strftime('%Y-%m-%d'),  # urodziny
                             sdateEntry.get_date().strftime('%Y-%m-%d'), # data zatrudnienia
                             self.img_["data"].decode('utf-8')
                             )
        self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])
        self.frame.update()

    def editEmployerForm(self):
        self.emp_photo = tk.LabelFrame(self.f_emp)
        self.img_ = tk.PhotoImage(master=self.emp_photo)
        self.avatar = tk.Canvas(self.emp_photo, width=200, height=270, bg='white')
        self.avatar.create_image(0, 0, image=self.img_, anchor="nw")
        self.avatar.pack(side = tk.TOP)
        self.emp_edit_confirm = tk.Button(self.emp_photo, text='Download new photo', command = self.getPhoto).pack(side=tk.BOTTOM)
        self.emp_photo.grid(row = 0, column = 0)

        self.edit_info = tk.LabelFrame(self.f_emp)
        self.lName = tk.StringVar(self.edit_info)
        self.fName = tk.StringVar(self.edit_info)
        self.fnameLabel = tk.Label(self.edit_info, text='First name').grid(row=0, column=0, ipadx=10, ipady=2)
        self.fnameEntry = tk.Entry(self.edit_info, textvariable=self.fName)
        self.fnameEntry.grid(row=0, column=1, ipadx=10, ipady=2)

        self.lnameLabel = tk.Label(self.edit_info, text='Last name').grid(row=1, column=0)
        self.lnameEntry = tk.Entry(self.edit_info, textvariable=self.lName)
        self.lnameEntry.grid(row=1, column=1)

        self.BDateLabel = tk.Label(self.edit_info, text='Birth date').grid(row=2, column=0)
        self.bdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.bdateEntry.grid(row=2, column=1)
        self.SDateLabel = tk.Label(self.edit_info, text='Start date').grid(row=3, column=0)
        self.SdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.SdateEntry.grid(row=3, column=1)
        self.edit_info.grid(row = 1, column = 0)

        self.validate = partial(self.confirm, self.idx, self.fName, self.lName, self.bdateEntry, self.SdateEntry)

        self.emp_edit_confirm = tk.Button(self.f_emp, text='Confirm change', command=self.validate).grid(row = 2, column = 0)

    def addPatient(self):
        pass

    def form(self):

        self.f_bot = tk.LabelFrame(self.frame,text="Acttion")
        self.button = tk.Button(self.f_bot, text='Add Employer', command=self.addEmployer).pack(side = tk.LEFT)
        self.delete_button = tk.Button(self.f_bot, text='Delete Employer', command=self.deleteEmployer).pack(side = tk.RIGHT)#.grid(row=0, column=1)
        self.add_patient_button = tk.Button(self.f_bot, text='Add Patient', command=self.addPatient()).pack(
            side=tk.BOTTOM)
        self.f_bot.pack(side = tk.BOTTOM, fill="both")

        self.f_top = tk.LabelFrame(self.frame, width =1300)
        self.sheet_frame = tk.LabelFrame(self.f_top)
        self.sheet, self.sheet_pattient = tksheet.Sheet(self.sheet_frame, width =700), tksheet.Sheet(self.sheet_frame, width =700)
        self.sheet.pack(side = tk.TOP,fill="both", expand="yes")
        self.sheet_pattient.pack(side = tk.BOTTOM, fill="both", expand="yes")


        self.sheet_frame.pack(side = tk.LEFT,fill="both", expand="yes")

        self.f_emp = tk.LabelFrame(self.f_top, text = "Employer ediit form", width = 300)
        self.editEmployerForm()
        self.f_emp.pack(side=tk.RIGHT, fill="both")

        self.f_top.pack(side=tk.TOP, fill="both", expand="yes")
        self.sheetEmpHeaderList = ['ID', 'Employer First Name', 'Employer Last Name', 'Birth date', 'Start date']
        self.sheetPattientHeaderList = ['First Name', 'Last Name', 'Doctor', 'Visit date', 'Time', 'Phone']
        self.sheet.headers([f'{c}' for c in self.sheetEmpHeaderList])
        self.sheet_pattient.headers([f'{c}' for c in self.sheetPattientHeaderList])
        self.sheet_bind_tuple = ("single_select",  # "single_select" or "toggle_select"
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
                                    "edit_cell")
        self.sheet.enable_bindings(self.sheet_bind_tuple)
        self.sheet_pattient.enable_bindings(self.sheet_bind_tuple)
        self.sheet.set_sheet_data([list(x) for x in self.emp.showEmployers()])
        self.refreshData()


class addPatient(tk.Tk):
    def __init__(self, parrent, db_):
        tk.Tk.__init__(self, parrent)
        self.parrent = parrent
        self.frame = tk.Frame(self)
        self.emp = db_
        self.form_()

    def __del__(self):
        print('bye')

    def form_(self):
        self.edit_info = tk.LabelFrame(self)
        self.lName = tk.StringVar(self.edit_info)
        self.fName = tk.StringVar(self.edit_info)

        self.fnameLabel = tk.Label(self.edit_info, text='First name').grid(row=0, column=0, ipadx=10, ipady=2)
        self.fnameEntry = tk.Entry(self.edit_info, textvariable=self.fName)
        self.fnameEntry.grid(row=0, column=1, ipadx=10, ipady=2)

        self.lnameLabel = tk.Label(self.edit_info, text='Last name').grid(row=1, column=0)
        self.lnameEntry = tk.Entry(self.edit_info, textvariable=self.lName)
        self.lnameEntry.grid(row=1, column=1)

        self.VisitDateLabel = tk.Label(self.edit_info, text='Visit date').grid(row=2, column=0)
        self.vdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.vdateEntry.grid(row=2, column=1)

        self.edit_info.grid(row=1, column=0)

        self.validate = partial(self.confirm, self.fName, self.lName, self.bdateEntry, self.SdateEntry, self.img_)
        self.emp_edit_confirm = tk.Button(self, text='Confirm change', command=self.validate).grid(row=2, column=0)

class addEmp(tk.Tk):
    def __init__(self, parrent, db_):
        tk.Tk.__init__(self, parrent)
        self.parrent = parrent
        self.frame = tk.Frame(self)
        self.emp = db_
        self.form_()


    def __del__(self):
        print('bye')

    def getPhoto(self):
        file_name = fd.askopenfilenames()
        self.img_['data'] = convertToPNG(file_name[0])
        print(self.img_['data'])
        return convertToPNG(file_name[0])

    def confirm(self, emp_name, emp_last, bdateEntry, sdateEntry, img_):
        if self.img_["data"] != '':

            self.emp.addEmployer(
                                 emp_name.get(),  # imie
                                 emp_last.get(),  # nazwisko
                                 bdateEntry.get_date().strftime('%Y-%m-%d'),  # urodziny
                                 sdateEntry.get_date().strftime('%Y-%m-%d'), # data zatrudnienia
                                  self.img_["data"].decode('utf-8')
                                 )
        else:
            self.emp.addEmployer(emp_name.get(),  # imie
                                 emp_last.get(),  # nazwisko
                                 bdateEntry.get_date().strftime('%Y-%m-%d'),  # urodziny
                                 sdateEntry.get_date().strftime('%Y-%m-%d')
                                 )
        self.quit()
        self.destroy()

    def form_(self):
        self.emp_photo = tk.LabelFrame(self)###
        self.img_ = tk.PhotoImage(master=self.emp_photo)
        self.avatar = tk.Canvas(self.emp_photo, width=200, height=270, bg='white')
        self.avatar.create_image(0, 0, image=self.img_, anchor="nw")
        self.avatar.pack(side=tk.TOP)
        self.emp_edit_confirm = tk.Button(self.emp_photo, text='Download new photo', command=self.getPhoto).pack(
            side=tk.BOTTOM)
        self.emp_photo.grid(row=0, column=0)

        self.edit_info = tk.LabelFrame(self) ###########

        self.lName = tk.StringVar(self.edit_info)
        self.fName = tk.StringVar(self.edit_info)
        self.fnameLabel = tk.Label(self.edit_info, text='First name').grid(row=0, column=0, ipadx=10, ipady=2)
        self.fnameEntry = tk.Entry(self.edit_info, textvariable=self.fName)
        self.fnameEntry.grid(row=0, column=1, ipadx=10, ipady=2)

        self.lnameLabel = tk.Label(self.edit_info, text='Last name').grid(row=1, column=0)
        self.lnameEntry = tk.Entry(self.edit_info, textvariable=self.lName)
        self.lnameEntry.grid(row=1, column=1)

        self.BDateLabel = tk.Label(self.edit_info, text='Birth date').grid(row=2, column=0)
        self.bdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.bdateEntry.grid(row=2, column=1)
        self.SDateLabel = tk.Label(self.edit_info, text='Start date').grid(row=3, column=0)
        self.SdateEntry = DateEntry(self.edit_info, date_pattern='dd/MM/yyyy')
        self.SdateEntry.grid(row=3, column=1)
        self.edit_info.grid(row=1, column=0)

        self.validate = partial(self.confirm, self.fName, self.lName, self.bdateEntry, self.SdateEntry, self.img_)
        self.emp_edit_confirm = tk.Button(self, text='Confirm change', command=self.validate).grid(row=2, column=0)
