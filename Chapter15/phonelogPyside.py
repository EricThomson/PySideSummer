# -*- coding: utf-8 -*-
"""
phonelogPyside.py
Annotated PySide port of phonelog.pyw from Chapter 15
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html


Processevents versus timer singleshot?
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""


import os
import sys
from PySide import QtGui, QtCore, QtSql
import resource_rc

ID, CALLER, STARTTIME, ENDTIME, TOPIC = range(5)
DATETIME_FORMAT = "yyyy-MM-dd hh:mm"


def createFakeData():
    import random

    print("Dropping table...")
    query = QtSql.QSqlQuery()
    query.exec_("DROP TABLE calls")
    QtGui.QApplication.processEvents()

    print("Creating table...")
    query.exec_("""CREATE TABLE calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                caller VARCHAR(40) NOT NULL,
                starttime DATETIME NOT NULL,
                endtime DATETIME NOT NULL,
                topic VARCHAR(80) NOT NULL)""")
    topics = ("Complaint", "Information request", "Off topic",
              "Information supplied", "Complaint", "Complaint")
    now = QtCore.QDateTime.currentDateTime()
    print("Populating table...")
    query.prepare("INSERT INTO calls (caller, starttime, endtime, "
                  "topic) VALUES (?, ?, ?, ?)")
    for name in ('Joshan Cockerall', 'Ammanie Ingham',
            'Diarmuid Bettington', 'Juliana Bannister',
            'Oakley-Jay Buxton', 'Reilley Collinge',
            'Ellis-James Mcgehee', 'Jazmin Lawton',
            'Lily-Grace Smythe', 'Coskun Lant', 'Lauran Lanham',
            'Millar Poindexter', 'Naqeeb Neild', 'Maxlee Stoddart',
            'Rebia Luscombe', 'Briana Christine', 'Charli Pease',
            'Deena Mais', 'Havia Huffman', 'Ethan Davie',
            'Thomas-Jack Silver', 'Harpret Bray', 'Leigh-Ann Goodliff',
            'Seoras Bayes', 'Jenna Underhill', 'Veena Helps',
            'Mahad Mcintosh', 'Allie Hazlehurst', 'Aoife Warrington',
            'Cameron Burton', 'Yildirim Ahlberg', 'Alissa Clayton',
            'Josephine Weber', 'Fiore Govan', 'Howard Ragsdale',
            'Tiernan Larkins', 'Seren Sweeny', 'Arisha Keys',
            'Kiki Wearing', 'Kyran Ponsonby', 'Diannon Pepper',
            'Mari Foston', 'Sunil Manson', 'Donald Wykes',
            'Rosie Higham', 'Karmin Raines', 'Tayyibah Leathem',
            'Kara-jay Knoll', 'Shail Dalgleish', 'Jaimie Sells'):
        start = now.addDays(-random.randint(1, 30))
        start = now.addSecs(-random.randint(60 * 5, 60 * 60 * 2))
        end = start.addSecs(random.randint(20, 60 * 13))
        topic = random.choice(topics)
        query.addBindValue(name)
        query.addBindValue(start)
        query.addBindValue(end)
        query.addBindValue(topic)
        query.exec_()
    QtGui.QApplication.processEvents()

    print("Calls:")
    query.exec_("SELECT id, caller, starttime, endtime, topic FROM calls "
                "ORDER by starttime")             
              
    while query.next():
        id = int(query.value(0))
        caller = query.value(1)
        starttime = query.value(2)
        endtime = query.value(3)
        topic = query.value(4)
        print("{0:02d}: {1} {2} - {3} {4}".format(id, caller,
              starttime, endtime, topic))       
    QtGui.QApplication.processEvents()


class PhoneLogDlg(QtGui.QDialog):

    FIRST, PREV, NEXT, LAST = range(4)

    def __init__(self, parent=None):
        super(PhoneLogDlg, self).__init__(parent)

        callerLabel = QtGui.QLabel("&Caller:")
        self.callerEdit = QtGui.QLineEdit()
        callerLabel.setBuddy(self.callerEdit)
        today = QtCore.QDate.currentDate()
        startLabel = QtGui.QLabel("&Start:")
        self.startDateTime = QtGui.QDateTimeEdit()
        startLabel.setBuddy(self.startDateTime)
        self.startDateTime.setDateRange(today, today)
        self.startDateTime.setDisplayFormat(DATETIME_FORMAT)
        endLabel = QtGui.QLabel("&End:")
        self.endDateTime = QtGui.QDateTimeEdit()
        endLabel.setBuddy(self.endDateTime)
        self.endDateTime.setDateRange(today, today)
        self.endDateTime.setDisplayFormat(DATETIME_FORMAT)
        topicLabel = QtGui.QLabel("&Topic:")
        topicEdit = QtGui.QLineEdit()
        topicLabel.setBuddy(topicEdit)
        firstButton = QtGui.QPushButton()
        firstButton.setIcon(QtGui.QIcon(":/first.png"))
        prevButton = QtGui.QPushButton()
        prevButton.setIcon(QtGui.QIcon(":/prev.png"))
        nextButton = QtGui.QPushButton()
        nextButton.setIcon(QtGui.QIcon(":/next.png"))
        lastButton = QtGui.QPushButton()
        lastButton.setIcon(QtGui.QIcon(":/last.png"))
        addButton = QtGui.QPushButton("&Add")
        addButton.setIcon(QtGui.QIcon(":/add.png"))
        deleteButton = QtGui.QPushButton("&Delete")
        deleteButton.setIcon(QtGui.QIcon(":/delete.png"))
        quitButton = QtGui.QPushButton("&Quit")
        quitButton.setIcon(QtGui.QIcon(":/quit.png"))

        addButton.setFocusPolicy(QtCore.Qt.NoFocus)
        deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)

        fieldLayout = QtGui.QGridLayout()
        fieldLayout.addWidget(callerLabel, 0, 0)
        fieldLayout.addWidget(self.callerEdit, 0, 1, 1, 3)
        fieldLayout.addWidget(startLabel, 1, 0)
        fieldLayout.addWidget(self.startDateTime, 1, 1)
        fieldLayout.addWidget(endLabel, 1, 2)
        fieldLayout.addWidget(self.endDateTime, 1, 3)
        fieldLayout.addWidget(topicLabel, 2, 0)
        fieldLayout.addWidget(topicEdit, 2, 1, 1, 3)
        navigationLayout = QtGui.QHBoxLayout()
        navigationLayout.addWidget(firstButton)
        navigationLayout.addWidget(prevButton)
        navigationLayout.addWidget(nextButton)
        navigationLayout.addWidget(lastButton)
        fieldLayout.addLayout(navigationLayout, 3, 0, 1, 2)
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(fieldLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("calls")
        self.model.setSort(STARTTIME, QtCore.Qt.AscendingOrder)
        self.model.select()

        #maps from widget to model (neet to set model)
        self.mapper = QtGui.QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.callerEdit, CALLER)
        self.mapper.addMapping(self.startDateTime, STARTTIME)
        self.mapper.addMapping(self.endDateTime, ENDTIME)
        self.mapper.addMapping(topicEdit, TOPIC)
        self.mapper.toFirst()

        firstButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.FIRST))
        prevButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.PREV))
        nextButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.NEXT))
        lastButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.LAST))
        addButton.clicked.connect(self.addRecord)
        deleteButton.clicked.connect(self.deleteRecord)
        quitButton.clicked.connect(self.accept)

        self.setWindowTitle("Phone Log")


    def reject(self):
        self.accept()


    def accept(self):
        self.mapper.submit()
        QtGui.QDialog.accept(self)

        
    def addRecord(self):
        row = self.model.rowCount()
        self.mapper.submit()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        now = QtCore.QDateTime.currentDateTime()
        self.startDateTime.setDateTime(now)
        self.endDateTime.setDateTime(now)
        self.callerEdit.setFocus()


    def deleteRecord(self):
        caller = self.callerEdit.text()
        starttime = self.startDateTime.dateTime().toString(
                                            DATETIME_FORMAT)
        if (QtGui.QMessageBox.question(self,
                "Delete",
                "Delete call made by<br>{0} on {1}?".format(caller, starttime),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.No):
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)


    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == PhoneLogDlg.FIRST:
            row = 0
        elif where == PhoneLogDlg.PREV:
            row = 0 if row <= 1 else row - 1
        elif where == PhoneLogDlg.NEXT:
            row += 1
            if row >= self.model.rowCount():
                row = self.model.rowCount() - 1
        elif where == PhoneLogDlg.LAST:
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)


def main():
    import site
    app = QtGui.QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "phonelog.db")
    create = not QtCore.QFile.exists(filename)

    #without following nothing works:
    site_pack_path = site.getsitepackages()[1]
    QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))


    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QtGui.QMessageBox.warning(None, "Phone Log",
            "Database Error: {}".format(db.lastError().text()))
        sys.exit(1)

    splash = None
    if create:
        #This cursor will be displayed in all the application’s widgets 
        #until PySide.QtGui.QApplication.restoreOverrideCursor() or another 
        #PySide.QtGui.QApplication.setOverrideCursor() is called.
        app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        splash = QtGui.QLabel()
        pixmap = QtGui.QPixmap(":/phonelogsplash.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())
        splash.setWindowFlags(QtCore.Qt.SplashScreen)
        rect = app.desktop().availableGeometry()
        splash.move((rect.width() - pixmap.width()) / 2,
                    (rect.height() - pixmap.height()) / 2)
        splash.show()
        app.processEvents()
        #consuming in Windows) step of creating fake data
        createFakeData()

    form = PhoneLogDlg()
    form.show()
    
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor() #back to standard cursor
    sys.exit(app.exec_())
    db.close()
    del db

main()

