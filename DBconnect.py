import psycopg2
import configparser
import pathlib
from tkinter import messagebox

def readConfig( path = 'config.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    return config[config.sections()[0]]

class ConnectDB:
    def __init__(self):
        self.configData = readConfig()

        try :
            self.connection = psycopg2.connect(user = self.configData['user'],
                                          password = self.configData['password'],
                                          host = self.configData['host'],
                                          port = self.configData['port'],
                                          database = self.configData['database'])
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error while connecting to PostgreSQL", error)

    def __del__(self):
        if self.connection:
             self.cursor.close()
             self.connection.close()
             print("PostgreSQL connection is closed")

    def Cursor(self):
        return self.cursor

    def Connection(self):
        return self.connection

class Patient:

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def showAllPatients(self):
        self.cursor.execute('''SELECT * FROM public."Patients"''')
        return self.cursor.fetchall()

    def showDoctorPatients(self, id):
        self.cursor.execute('''SELECT * FROM public."Patients" where doctor_id = \'%s\'
        '''%(id))
        return self.cursor.fetchall()

    def addPatient(self, first_name, last_name, visit_date, time, doctor_id, phone = '+48576382402'):
        print(visit_date, time,)
        insertquery = '''
            insert into public."Patients" 
            (first_name, last_name, visit_date, time, phone, doctor_id)
            values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s)
        '''%(first_name, last_name, visit_date, time, phone, doctor_id)
        #self.cursor.execute(insertquery)
        #self.connection.commit()



class admins:

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def showAdmins(self):
        self.cursor.execute('''SELECT * FROM public."Admins"''')
        return self.cursor.fetchall()

    def addAdmin(self,fname,lname,login,password):
        addQuery = '''
                   Insert into public."Admins" 
                   (username, password,first_name, last_name) 
                   values (\'%s\',\'%s\',\'%s\',\'%s\');
               ''' % (login,password,fname,lname)
        self.cursor.execute(addQuery)
        self.connection.commit()

    def Login(self, login, password):
        if '--' in login or '--' in password:
            return []
        try:
            self.cursor.execute('''SELECT * FROM public."Admins" where username = \'%s\' and password = \'%s\';'''
                                 %(login,password))
        except Exception as ex:
            return []
        res = self.cursor.fetchall()
        if res != []:
            return res[0][2:]
        else : return []

class Employers(ConnectDB):

    def __init__(self, cursor, conection):
        self.cursor = cursor
        self.connection = conection

    def showEmployers(self):
        self.cursor.execute('''SELECT id, first_name, last_name, birth_date, start_date, salary FROM public."Employers" ORDER BY id''')
        return self.cursor.fetchall()

    def getEmployerPhoto(self, id):
        self.cursor.execute(
            '''SELECT encode(photo::bytea, 'base64') FROM public."Employers" where id = %s''' % (id))
        self.photo = self.cursor.fetchall()[0][0]
        return self.photo

    def getEmployerData(self,id):
        self.cursor.execute(
            '''SELECT id, first_name, last_name, birth_date, start_date, encode(photo::bytea, 'base64'), salary
            FROM public."Employers" where id = %s''' % (id))
        return self.cursor.fetchall()[0]

    def count(self):
        countQuery = '''select id from public."Employers" ORDER BY id DESC LIMIT 1'''
        self.cursor.execute(countQuery)
        x = self.cursor.fetchall()
        return int(x[0][0]) + 1

    def addEmployer(self,fn, ln, bd, sd, photo = ''):
        InsertQuery = '''
            Insert into public."Employers" (id,first_name, last_name, birth_date, start_date, photo) 
            values (%s,\'%s\',\'%s\',\'%s\',\'%s\', \'%s\');
        '''%(self.count(),fn, ln, bd, sd, photo)
        if photo == '':
            InsertQuery = '''
                        Insert into public."Employers" (id,first_name, last_name, birth_date, start_date) 
                        values (%s,\'%s\',\'%s\',\'%s\',\'%s\');
                    ''' % (self.count(), fn, ln, bd, sd)
        self.cursor.execute(InsertQuery)
        self.connection.commit()

    def updateEmployer(self,id,fn, ln, bd, sd, photo, salary):
        updateQuery = '''
            update public."Employers" 
            set first_name = \'%s\', last_name = \'%s\', birth_date = \'%s\', start_date = \'%s\', photo = \'%s\', salary =\'%s\'
            where id = %s;
        '''%(fn, ln, bd, sd, photo, salary, id)
        self.cursor.execute(updateQuery)
        self.connection.commit()

    def deleteEmployer(self, id):
        deleteQuery = '''
            delete from public."Employers" where id = %s
        '''%(id)
        self.cursor.execute(deleteQuery)
        self.connection.commit()
