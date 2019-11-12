from PyQt5.QtCore import *    # pyqt5 is the cross platform gui interface
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * # getting acces to gui widgets
import sys
import mysql.connector   # creating a database
from PyQt5.uic import loadUiType # used loading ur ui after developing the project
import datetime  # to print current date and time
from xlrd import *  # to write the data into excel folder
from xlsxwriter import *
import os
from login import Ui_Form
from library import Ui_MainWindow
  # intializing login windows


class login(QWidget ,Ui_Form):
    def __init__(self):   # controls functionality of login ui
        QWidget.__init__(self)
        self.setupUi(self)
        self.light_themes()
        self.pushButton.clicked.connect(self.Handel_login)

    def Handel_login(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',  # creating a database connector
                                          port='3306')
        self.cur = self.db.cursor()  # connecting it to cursor
        username= self.lineEdit.text()  # intializing username and password to respective fields
        password= self.lineEdit_2.text()


        sql=''' SELECT * FROM users'''   # select all the data from user table

        self.cur.execute(sql)  # executing the sql command
        data =self.cur.fetchall()  # all the data in the data base is fetched


        for row in data:
            if username ==row[1] and password == row[3]:  # here taking usercolumn and database column and printing both are equal
                print("user match")
                self.window2=MainApp()  # if both matches then main window will open
                self.close()
                self.window2.show()

            else:
                self.label.setText('Enter correct username and password')   # wrong password this output will be shown

    def light_themes(self):   # ui will change its color to white
        style = open('themes/light.css', 'r')  # reading the css file
        style = style.read()
        self.setStyleSheet(style)


class MainApp(QMainWindow ,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)  # this funtion control the changes taking place in the ui
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()
        self.Qdark_themes()



        self.Show_Author()
        self.show_Category()
        self.Show_Publisher()

        self.show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()

        self.show_All_Books()
        self.Show_All_Clients()
        self.Show_All_operations()

    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)  # hiding the tab bar

    def Handel_Buttons(self):  # this functions controls all the button in the ui  like submit
        self.pushButton_5.clicked.connect(self.show_Themes)
        self.pushButton_8.clicked.connect(self.Hiding_Themes)

        self.pushButton.clicked.connect(self.Open_day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_25.clicked.connect(self.Open_Clients_tab)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_10.clicked.connect(self.search_books)
        self.pushButton_9.clicked.connect(self.Edit_Books)
        self.pushButton_11.clicked.connect(self.Delete_books)

        self.pushButton_18.clicked.connect(self.Add_category)
        self.pushButton_19.clicked.connect(self.Add_Author)
        self.pushButton_20.clicked.connect(self.Add_publisher)

        self.pushButton_12.clicked.connect(self.Add_New_User)
        self.pushButton_15.clicked.connect(self.Login)
        self.pushButton_17.clicked.connect(self.Edit_user)
        ## themes button

        self.pushButton_21.clicked.connect(self.Dark_orange_themes)
        self.pushButton_27.clicked.connect(self.Dark_Blue_Themes)
        self.pushButton_22.clicked.connect(self.Dark_Gray_Themes)
        self.pushButton_28.clicked.connect(self.Qdark_themes)
        self.pushButton_13.clicked.connect(self.light_themes)


        ##client buttons

        self.pushButton_14.clicked.connect(self.Add_New_client)
        self.pushButton_23.clicked.connect(self.Search_clients)
        self.pushButton_24.clicked.connect(self.Edit_Client)
        self.pushButton_16.clicked.connect(self.Delete_Clients)


        ##day to day to operations

        self.pushButton_6.clicked.connect(self.Handel_Day_Operations)

        ## exporting to excel

        self.pushButton_30.clicked.connect(self.Export_Day_operations)
        self.pushButton_26.clicked.connect(self.Export_books)
        self.pushButton_29.clicked.connect(self.Export_clients)


        ### handling funtions

        self.pushButton_31.clicked.connect(self.create_functions)





    def show_Themes(self):
        self.groupBox_2.show()

    def Hiding_Themes(self):
        self.groupBox_2.hide()

    ##################################
    ########opening tabs##############
###########################setting each tab to push button######################
    def Open_day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)


    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)


    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(2)


    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Clients_tab(self):
        self.tabWidget.setCurrentIndex(4)


    ############################################################################
    ####################day to day operations###################################


    ###########handeling day operations########################

    def Handel_Day_Operations(self):
        book_title =self.lineEdit.text()
        client_name=self.lineEdit_5.text()
        type=self.comboBox.currentText()
        days_number=self.comboBox_2.currentIndex() + 1
        today_date=datetime.date.today()
        to_date= today_date+ datetime.timedelta(days=days_number)
        print(today_date)
        print(to_date)



        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()           #connecting to data base

        self.cur.execute('''
           INSERT INTO day_operations(book_name ,client ,type ,days ,date ,to_date)  
            VALUES(%s ,%s ,%s ,%s ,%s ,%s) ;
        ''', (book_title ,client_name ,type ,days_number ,today_date ,to_date))  ######inserting contents into day_operations table

        self.db.commit()
        self.statusBar().showMessage('New operation added')  #this happens when data is succesfully entered
        self.Show_All_operations()



    def Show_All_operations(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')  # connecting to library database
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book_name ,client ,type ,date ,to_date FROM day_operations  
        ''')   # here ur selecting contents from day operations and showing it in eneumerate form

        data =self.cur.fetchall()  # fetching all the rows
        print(data)
        self.tableWidget.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row ,form in enumerate(data):
            for column ,item in enumerate(form):
                self.tableWidget_6.setItem(row ,column ,QTableWidgetItem(str(item)))
                column += 1

            row_position =self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)


















    ##################################
    ########books#####################

    def show_All_Books(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()  # connecting to data base
        self.cur.execute('''SELECT book_code ,book_name ,book_description ,book_category ,book_author ,book_publisher ,book_price FROM book''') # selecting all the column from book table and displaying it
        data= self.cur.fetchall()

        print(data)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)

        for row ,form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget_4.setItem(row ,column , QTableWidgetItem(str(item)))
                column +=1
            row_position =self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)

        self.db.close()




    def Add_New_Book(self):  # function is for inserting new book
        self.db=mysql.connector.connect(host='localhost',user='root' ,password='123654@gm' ,database='library',port='3306')
        self.cur= self.db.cursor()  # connecting it to the database

        book_title=self.lineEdit_3.text()
        book_description = self.textEdit_2.toPlainText()

        book_code=self.lineEdit_2.text()
        book_category=self.comboBox_3.currentText()
        book_author=self.comboBox_4.currentText()
        book_publisher=self.comboBox_5.currentText()
        book_price=self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book (book_name,book_description,book_code,book_category,book_author,book_publisher,book_price)
            VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s );
       ''',(book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))  # inserting data into book table


        self.db.commit()
        self.statusBar().showMessage('New Book Added')  # message shown after insertion
        # shown after insertion

        self.lineEdit_3.setText('')
        self.textEdit_2.setPlainText('')
        self.lineEdit_2.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.show_All_Books()















    def search_books(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')  # connecting to the data base
        self.cur = self.db.cursor()
        book_title=self.lineEdit_8.text()
        sql='''SELECT * FROM book WHERE book_name =%s '''
        self.cur.execute(sql ,[(book_title)])  # selecting all the books from book title

        data =self.cur.fetchone() # fetching the book table
        print(data)


        self.lineEdit_11.setText(data[1])
        self.textEdit.setPlainText(data[2])
        self.lineEdit_9.setText(data[3])
        self.comboBox_9.setCurrentText(data[4])
        self.comboBox_10.setCurrentText(data[5])
        self.comboBox_11.setCurrentText(data[6])
        self.lineEdit_10.setText(str(data[7]))






    def Edit_Books(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')
        self.cur = self.db.cursor() # connecting to data base

        book_title = self.lineEdit_11.text()
        book_description = self.textEdit.toPlainText()

        book_code = self.lineEdit_9.text()
        book_category = self.comboBox_9.currentIndex()
        book_author = self.comboBox_10.currentIndex()
        book_publisher = self.comboBox_11.currentIndex()
        book_price = self.lineEdit_10.text()

        search_book_title = self.lineEdit_8.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s ,book_description =%s ,book_code =%s ,book_category=%s ,book_author =%s ,book_publisher=%s ,book_price=%s WHERE book_name=%s

        ''',(book_title,book_description,book_code,book_category,book_author,book_publisher,book_price,search_book_title)) # in this updation takes in book table wat user have entered

        self.db.commit() #
        self.statusBar().showMessage('book updated ')
        self.show_All_Books()



    def Delete_books(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')
        self.cur = self.db.cursor()  # inserting into data base

        book_title=self.lineEdit_8.text()
        warning=QMessageBox.warning(self, 'Delete book',"Are you sure u want to delete this book or not",QMessageBox.Yes | QMessageBox.No)  # showing warning box
        if warning == QMessageBox.Yes:
            sql='''DELETE FROM book WHERE book_name = %s ;'''  # deleting from book table and entire row get deleted
            self.cur.execute(sql,[(book_title)])
            self.db.commit()
            print(book_title)
            self.statusBar().showMessage("book deleted")
        else:
            pass

        self.show_All_Books()

        ##########################################################################
        ###############################CLIENTS#####################################


    def Show_All_Clients(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()# connecting to database
        self.cur.execute('''SELECT client_name ,client_email ,client_nationalid FROM clients''')    # selecting all contents from database and displaying it in enumerate form
        data= self.cur.fetchall()

        print(data)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row ,form in enumerate(data):  # ins
            for column , item in enumerate(form):
                self.tableWidget_5.setItem(row ,column , QTableWidgetItem(str(item)))
                column +=1
            row_position =self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)

        self.db.close()





    def Add_New_client(self):
        client_name=self.lineEdit_6.text()
        client_email=self.lineEdit_7.text()
        client_nationalid=self.lineEdit_20.text()


        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306') # connecting to database
        self.cur = self.db.cursor()

        self.cur.execute('''
        INSERT INTO clients(client_name ,client_email ,client_nationalid)
        VALUES(%s,%s,%s);
        ''',(client_name ,client_email ,client_nationalid))  # inserting contents to clients table

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('new client added') # shows after contents are updated
        self.Show_All_Clients()












    def Search_clients(self):
        client_nationalid=self.lineEdit_16.text()

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')
        self.cur = self.db.cursor()

        sql=''' SELECT * FROM clients WHERE client_nationalid = %s '''  # selecting all column from clients table and displaying it
        self.cur.execute(sql,[(client_nationalid)])
        data=self.cur.fetchone()
        self.lineEdit_18.setText(data[1])
        self.lineEdit_17.setText(data[2])
        self.lineEdit_19.setText(data[3])


    def Edit_Client(self):
        client_original_nationalid=self.lineEdit_16.text()
        client_name=self.lineEdit_18.text()
        client_email=self.lineEdit_17.text()
        client_nationalid=self.lineEdit_19.text()


        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')
        self.cur = self.db.cursor() # connecting to database table

        self.cur.execute('''
        UPDATE clients SET client_name= %s ,client_email= %s ,client_nationalid= %s WHERE client_nationalid =%s;
        ''',(client_name ,client_email ,client_nationalid,client_original_nationalid)) # updating database list
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('client data updated')  # # message shown after updation
        self.Show_All_Clients()


    def Delete_Clients(self):
        client_original_nationalid=self.lineEdit_16.text()
        warning_message=QMessageBox.warning(self,"deleting client","are u sure do u want to delete your client",QMessageBox.Yes|QMessageBox.No)
        if warning_message ==QMessageBox.Yes:
            self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                              port='3306')
            self.cur = self.db.cursor()
            sql = '''DELETE FROM clients WHERE client_nationalid =%s'''
            self.cur.execute(sql,[(client_original_nationalid)])
            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('client deleted')
            self.Show_All_Clients()











    ##################################
    ########users#####################

    def Add_New_User(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')
        self.cur = self.db.cursor()
        username=self.lineEdit_12.text()
        email=self.lineEdit_13.text()
        password=self.lineEdit_14.text()
        confirm_password=self.lineEdit_15.text()

        if password ==confirm_password:
            self.cur.execute('''
            INSERT INTO users(user_name ,user_email ,user_password) 
            VALUES (%s,%s,%s);
            ''',(username ,email, password))
            self.db.commit()
            self.statusBar().showMessage('new user added')
        else:
            self.label_9.setText('please add a valid password twice')


    def Login(self):


        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port='3306')
        self.cur = self.db.cursor()
        username=self.lineEdit_25.text()
        password=self.lineEdit_24.text()

        sql=''' SELECT * FROM users'''

        self.cur.execute(sql)
        data =self.cur.fetchall()


        for row in data:
            if username ==row[1] and password == row[3]:
                print("user match")
                self.statusBar().showMessage('valid username & password')
                self.groupBox_4.setEnabled(True)
                self.lineEdit_31.setText(row[1])
                self.lineEdit_28.setText(row[2])
                self.lineEdit_30.setText(row[3])



    def Edit_user(self):

        username=self.lineEdit_31.text()
        email=self.lineEdit_28.text()
        password=self.lineEdit_30.text()
        confirm_password=self.lineEdit_29.text()

        original_name=self.lineEdit_25.text()

        if password ==confirm_password:

            self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                              port='3306')
            self.cur = self.db.cursor()
            self.cur.execute('''
            UPDATE users SET user_name =%s, user_email= %s ,user_password =%s WHERE user_name=%s
            ''',(username ,email ,password ,original_name))

            self.db.commit()
            self.statusBar().showMessage('user data updated successfully')

        else:
            print('make sure you entered your password correctly')




    ##################################
    ########settings##################

    def Add_category(self):
        print("adding category",self.lineEdit_32.text()) ## displaying the category name entered to the console
        self.db=mysql.connector.connect(host='localhost',user='root' ,password='123654@gm' ,database='library',port=3306)  ## connecting it to the database
        self.cur= self.db.cursor()
        category_name =self.lineEdit_32.text()
        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s);
        ''',(category_name,))## passing the category nametaken to the database
        self.db.commit()
        self.statusBar().showMessage('New Category Added')  ##message is displayed when u click on the button when each category is added
        self.lineEdit_32.setText('') ## clears the name list from the line edit box
        self.show_Category() ## this is like showing all the categories enetred after the table wiget has been entered
        self.show_Category_Combobox()

    def show_Category(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port=3306)  ## connecting it to the database
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ;''')  ## fetching data from database
        data=self.cur.fetchall()
        if data:

            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row ,form in enumerate(data):
                for column ,item in enumerate(form):
                    self.tableWidget.setItem(row , column ,QTableWidgetItem(str(item)))
                    column += 1
                row_position=self.tableWidget.rowCount()  ## checking number of rows already present
                self.tableWidget.insertRow(row_position) ## those parameters are passed and inserted into table widegt









    def Add_Author(self):
        print("adding author",self.lineEdit_33.text()) ## displaying the category name entered to the console
        self.db=mysql.connector.connect(host='localhost',user='root' ,password='123654@gm' ,database='library',port=3306)  ## connecting it to the database
        self.cur= self.db.cursor()
        author_name=self.lineEdit_33.text()
        self.cur.execute('''
            INSERT INTO authors (authors_name) VALUES (%s);
        ''',(author_name,))## passing the category nametaken to the database
        self.db.commit()
        self.statusBar().showMessage('New author Added')  ##message is displayed when u click on the button when each category is added
        self.lineEdit_33.setText('')
        self.Show_Author()
        self.Show_Author_Combobox()

    def Show_Author(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port=3306)  ## connecting it to the database
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT authors_name FROM authors ;''')  ## fetching data from database
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_2.rowCount()  ## checking number of rows already present
                self.tableWidget_2.insertRow(row_position)

    def Add_publisher(self):## this message is displayed when u click add publisher in ui
        print("adding publisher",self.lineEdit_34.text()) ## displaying the category name entered to the console
        self.db=mysql.connector.connect(host='localhost',user='root' ,password='123654@gm' ,database='library',port=3306)  ## connecting it to the database
        self.cur= self.db.cursor()
        publisher_name=self.lineEdit_34.text()
        self.cur.execute('''
            INSERT INTO publisher (publisher_name) VALUES (%s);
        ''',(publisher_name,))## passing the category nametaken to the database
        self.db.commit()
        self.statusBar().showMessage('New publisher Added')  ##message is displayed when u click on the button when each category is added
        self.lineEdit_34.setText('')
        self.Show_Publisher()
        self.Show_Publisher_Combobox()

    def Show_Publisher(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port=3306)  ## connecting it to the database
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ;''')  ## fetching data from database
        data = self.cur.fetchall()
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_3.rowCount()  ## checking number of rows already present
                self.tableWidget_3.insertRow(row_position)




    ##################################
    ########showing new strings in ui##################

    def show_Category_Combobox(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port=3306)  ## connecting it to the database
        self.cur = self.db.cursor()

        self.cur.execute('''  SELECT category_name FROM category ''')
        data =self.cur.fetchall()
        self.comboBox_3.clear() #going to clear the combobox when ever u new value is entered
        for category in data:
            self.comboBox_3.addItem(category[0])  ## fetching all the data from combobox
            self.comboBox_9.addItem(category[0])

    def Show_Author_Combobox(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port=3306)  ## connecting it to the database
        self.cur = self.db.cursor()

        self.cur.execute('''  SELECT authors_name FROM authors ''')
        data =self.cur.fetchall()
        self.comboBox_4.clear()
        for authors in data:
            self.comboBox_4.addItem(authors[0])
            self.comboBox_10.addItem(authors[0])

    def Show_Publisher_Combobox(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',
                                          port=3306)  ## connecting it to the database
        self.cur = self.db.cursor()

        self.cur.execute('''  SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_11.addItem(publisher[0])

#################################################################################################
############################Export to excel file#################################################

    def Export_Day_operations(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book_name ,client ,type ,date ,to_date FROM day_operations
        ''')

        data =self.cur.fetchall()

        wb=Workbook('day_operations.xlsx')

        sheet1 = wb.add_worksheet()
        sheet1.write(0,0,'book title')
        sheet1.write(0, 1, 'client name')
        sheet1.write(0, 2, 'type')
        sheet1.write(0, 3, 'from_date')
        sheet1.write(0, 4, 'to_date')


        row_number =1
        for row in data:
            column_number =0
            for item in row :
                sheet1.write(row_number ,column_number ,str(item))
                column_number +=1
            row_number +=1





        wb.close()
        self.statusBar().showMessage('report created Successfully')



    def Export_books(self):

        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT book_code ,book_name ,book_description ,book_category ,book_author ,book_publisher ,book_price FROM book''')
        data= self.cur.fetchall()



        print('hello')
        print(data)

        wb=Workbook('all_books.xlsx')

        sheet1 = wb.add_worksheet()
        sheet1.write(0,0,'book code')
        sheet1.write(0, 1, 'book name')
        sheet1.write(0, 2, 'book description')
        sheet1.write(0, 3, 'book category')
        sheet1.write(0, 4, 'book author')
        sheet1.write(0,5,'book publisher')
        sheet1.write(0,6,'book price')



        row_number =1
        for row in data:
            column_number =0
            for item in row :
                sheet1.write(row_number ,column_number ,str(item))
                column_number +=1
            row_number +=1
        wb.close()
        self.statusBar().showMessage('report created Successfully')


    def Export_clients(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT client_name ,client_email ,client_nationalid FROM clients''')
        data= self.cur.fetchall()
        print(data)

        wb=Workbook('all_clients.xlsx')

        sheet1 = wb.add_worksheet()
        sheet1.write(0,0,'client name ')
        sheet1.write(0, 1, 'client email')
        sheet1.write(0, 2, 'client nationalid')


        row_number =1
        for row in data:
            column_number =0
            for item in row :
                sheet1.write(row_number ,column_number ,str(item))
                column_number +=1
            row_number +=1
        wb.close()
        self.statusBar().showMessage('report created Successfully')





        row_number =1
        for row in data:
            column_number =0
            for item in row :
                sheet1.write(row_number ,column_number ,str(item))
                column_number +=1
            row_number +=1
        wb.close()
        self.statusBar().showMessage('report created Successfully')



#########################################################################################
################################ UI themes #########################################


    def Dark_Blue_Themes(self):
        style= open('themes/darkblue.css','r')
        style=style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Themes(self):
        style = open('themes/darkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_orange_themes(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Qdark_themes(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def light_themes(self):
        style=open('themes/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)



####################################################################################################################
#########################################creating triggers and functions##########################################################

    def create_functions(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='123654@gm', database='library',port='3306')
        self.cur = self.db.cursor()
        self.cur.execute('''
            SELECT COUNT(*) FROM book;  
        ''',) # showing total number of books present in book table
        data=self.cur.fetchone()
        self.db.close
        print(data)
        print("no of elements")
        print(data)
        self.lineEdit_21.setText(str(data))
        

        

        









def main():  # main function
    app = QApplication(sys.argv)
    window=login()
    window.show()
    app.exec_()


if __name__ =='__main__':
    main()





