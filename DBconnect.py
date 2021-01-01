import psycopg2

class ConnectDB:

    def __init__(self):
        try :
            self.connection = psycopg2.connect(user = 'postgres',
                                          password = 'Prosto12',
                                          host = '127.0.0.1',
                                          port = '5432',
                                          database = 'postgres')
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def __del__(self):
        if self.connection:
             self.cursor.close()
             self.connection.close()
             print("PostgreSQL connection is closed")

    def Cursor(self):
        return self.cursor

    def Connection(self):
        return self.connection

class admins(ConnectDB):

    def showAdmins(self):
        super().Cursor().execute('''SELECT * FROM public."Admins"''')
        print(super().Cursor().fetchall())

    def addAdmin(self,fname,lname,login,password):
        addQuery = '''
                   Insert into public."Admins" 
                   (username, password,first_name, last_name) 
                   values (\'%s\',\'%s\',\'%s\',\'%s\');
               ''' % (login,password,fname,lname)
        super().Cursor().execute(addQuery)
        super().Connection().commit()

    def Login(self, login, password):
        super().Cursor().execute('''SELECT * FROM public."Admins" where username = \'%s\' and password = \'%s\';'''
                                 %(login,password))
        res = super().Cursor().fetchall()
        if res != []:
            return res[0][2:]
        else : return []

class Employers(ConnectDB):
    def showEmployers(self):
        super().Cursor().execute('''SELECT * FROM public."Employers"''')
        print(super().Cursor().fetchall())

    def count(self):
        countQuery = '''select count(*) from public."Employers"'''
        self.cursor.execute(countQuery)
        x = self.cursor.fetchall()
        return int(x[0][0]) + 1

    def addEmployer(self,fn, ln):
        InsertQuery = '''
            Insert into public."Employers" (id,first_name, last_name) values (%s,\'%s\',\'%s\');
        '''%(self.count(),fn, ln)
        self.cursor.execute(InsertQuery)
        self.connection.commit()

    def updateEmployer(self,id,fn, ln):
        updateQuery = '''
            update public."Employers" set first_name = \'%s\', last_name = \'%s\' where id = %s;
        '''%(fn, ln, id)
        self.cursor.execute(updateQuery)
        self.connection.commit()

    def deleteEmployer(self, id):
        deleteQuery = '''
            delete from public."Employers" where id = %s
        '''%(id)
        self.cursor.execute(deleteQuery)
        self.connection.commit()