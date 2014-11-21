# -*- coding: utf-8 -*-
"""
phonelog-fkPyside.py
Annotated PySide port of phonelog-fk.pyw from Chapter 15
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import site
import os
import sys
from PySide import QtCore, QtGui, QtSql
import resource_rc    
                
ID, CALLER, STARTTIME, ENDTIME, TOPIC, OUTCOMEID = range(6)
DATETIME_FORMAT = "yyyy-MM-dd hh:mm"


def createFakeData():
    import random

    print("Dropping tables...")
    query = QtSql.QSqlQuery()
    query.exec_("DROP TABLE calls")
    query.exec_("DROP TABLE outcomes")
    QtGui.QApplication.processEvents()

    print("Creating tables...")
    query.exec_("""CREATE TABLE outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL)""")

    query.exec_("""CREATE TABLE calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                caller VARCHAR(40) NOT NULL,
                starttime DATETIME NOT NULL,
                endtime DATETIME NOT NULL,
                topic VARCHAR(80) NOT NULL,
                outcomeid INTEGER NOT NULL,
                FOREIGN KEY (outcomeid) REFERENCES outcomes)""")
    QtGui.QApplication.processEvents()
    print("Populating tables...")
    for name in ("Resolved", "Unresolved", "Calling back", "Escalate",
                 "Wrong number"):
        query.exec_("INSERT INTO outcomes (name) VALUES ('{0}')".format(
                    name))
    topics = ("Complaint", "Information request", "Off topic",
              "Information supplied", "Complaint", "Complaint")
    now = QtCore.QDateTime.currentDateTime()
    query.prepare("INSERT INTO calls (caller, starttime, endtime, "
                  "topic, outcomeid) VALUES (:caller, :starttime, "
                  ":endtime, :topic, :outcomeid)")
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
        outcomeid = int(random.randint(1, 5))
        query.bindValue(":caller", QtCore.QVariant(QtCore.QString(name)))
        query.bindValue(":starttime", QtCore.QVariant(start))
        query.bindValue(":endtime", QtCore.QVariant(end))
        query.bindValue(":topic", QtCore.QVariant(QtCore.QString(topic)))
        query.bindValue(":outcomeid", QtCore.QVariant(outcomeid))
        query.exec_()
    QtGui.QApplication.processEvents()

    print("Calls:")
    query.exec_("SELECT calls.id, calls.caller, calls.starttime, "
                "calls.endtime, calls.topic, calls.outcomeid, "
                "outcomes.name FROM calls, outcomes "
                "WHERE calls.outcomeid = outcomes.id "
                "ORDER by calls.starttime")
    while query.next():
        id = query.value(ID).toInt()[0]
        caller = unicode(query.value(CALLER).toString())
        starttime = (unicode(query.value(STARTTIME).toDateTime() 
                    .toString(DATETIME_FORMAT)))
        endtime = (unicode(query.value(ENDTIME).toDateTime()
                   .toString(DATETIME_FORMAT)))
        topic = unicode(query.value(TOPIC).toString())
        outcome = unicode(query.value(6).toString())
        print("{0:02d}: {1} {2} - {3} {4} [{5}]".format(id, caller,
              starttime, endtime, topic, outcome))
    QtGui.QApplication.processEvents()


class PhoneLogDlg(QtGui.QDialog):

    FIRST, PREV, NEXT, LAST = range(4)

    def __init__(self, parent=None):
        super(PhoneLogDlg, self).__init__(parent)
        self.create_widgets()
        self.layout_widgets()
        self.create_model()
        self.create_connections()
        self.setWindowTitle("Phone Log")


    def create_widgets(self):
        self.callerLabel = QtGui.QLabel("&Caller:")
        self.callerEdit = QtGui.QLineEdit()
        self.callerLabel.setBuddy(self.callerEdit)
        today = QtCore.QDate.currentDate()
        self.startLabel = QtGui.QLabel("&Start:")
        self.startDateTime = QtGui.QDateTimeEdit()
        self.startLabel.setBuddy(self.startDateTime)
        self.startDateTime.setDateRange(today, today)
        self.startDateTime.setDisplayFormat(DATETIME_FORMAT)
        self.endLabel = QtGui.QLabel("&End:")
        self.endDateTime = QtGui.QDateTimeEdit()
        self.endLabel.setBuddy(self.endDateTime)
        self.endDateTime.setDateRange(today, today)
        self.endDateTime.setDisplayFormat(DATETIME_FORMAT)
        self.topicLabel = QtGui.QLabel("&Topic:")
        self.topicEdit = QtGui.QLineEdit()
        self.topicLabel.setBuddy(self.topicEdit)
        self.outcomeLabel = QtGui.QLabel("&Outcome:")
        self.outcomeComboBox = QtGui.QComboBox()
        self.outcomeLabel.setBuddy(self.outcomeComboBox)
        self.firstButton = QtGui.QPushButton()
        self.firstButton.setIcon(QtGui.QIcon(":/first.png"))
        self.prevButton = QtGui.QPushButton()
        self.prevButton.setIcon(QtGui.QIcon(":/prev.png"))
        self.nextButton = QtGui.QPushButton()
        self.nextButton.setIcon(QtGui.QIcon(":/next.png"))
        self.lastButton = QtGui.QPushButton()
        self.lastButton.setIcon(QtGui.QIcon(":/last.png"))
        self.addButton = QtGui.QPushButton("&Add")
        self.addButton.setIcon(QtGui.QIcon(":/add.png"))
        self.deleteButton = QtGui.QPushButton("&Delete")
        self.deleteButton.setIcon(QtGui.QIcon(":/delete.png"))
        self.quitButton = QtGui.QPushButton("&Quit")
        self.quitButton.setIcon(QtGui.QIcon(":/quit.png"))

        self.addButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)


    def layout_widgets(self):
        fieldLayout = QtGui.QGridLayout()
        fieldLayout.addWidget(self.callerLabel, 0, 0)
        fieldLayout.addWidget(self.callerEdit, 0, 1, 1, 3)
        fieldLayout.addWidget(self.startLabel, 1, 0)
        fieldLayout.addWidget(self.startDateTime, 1, 1)
        fieldLayout.addWidget(self.endLabel, 1, 2)
        fieldLayout.addWidget(self.endDateTime, 1, 3)
        fieldLayout.addWidget(self.topicLabel, 2, 0)
        fieldLayout.addWidget(self.topicEdit, 2, 1, 1, 3)
        fieldLayout.addWidget(self.outcomeLabel, 3, 0)
        fieldLayout.addWidget(self.outcomeComboBox, 3, 1, 1, 3)
        navigationLayout = QtGui.QHBoxLayout()
        navigationLayout.addWidget(self.firstButton)
        navigationLayout.addWidget(self.prevButton)
        navigationLayout.addWidget(self.nextButton)
        navigationLayout.addWidget(self.lastButton)
        fieldLayout.addLayout(navigationLayout, 4, 0, 1, 2)
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.quitButton)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(fieldLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)


    def create_model(self):
        #because of foreign keys, need to use qsqlrelationaltablemodel
        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable("calls")
        #setRelation establishes a relationship between two tables
        self.model.setRelation(OUTCOMEID,
                QtSql.QSqlRelation("outcomes", "id", "name"))
        self.model.setSort(STARTTIME, QtCore.Qt.AscendingOrder)
        self.model.select()

        self.mapper = QtGui.QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.callerEdit, CALLER)
        self.mapper.addMapping(self.startDateTime, STARTTIME)
        self.mapper.addMapping(self.endDateTime, ENDTIME)
        self.mapper.addMapping(self.topicEdit, TOPIC)
        relationModel = self.model.relationModel(OUTCOMEID)
        self.outcomeComboBox.setModel(relationModel)
        self.outcomeComboBox.setModelColumn(
                relationModel.fieldIndex("name"))
        self.mapper.addMapping(self.outcomeComboBox, OUTCOMEID)
        self.mapper.toFirst()


    def create_connections(self):
        self.firstButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.FIRST))
        self.prevButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.PREV))
        self.nextButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.NEXT))
        self.lastButton.clicked.connect(
                lambda: self.saveRecord(PhoneLogDlg.LAST))
        self.addButton.clicked.connect(self.addRecord)
        self.deleteButton.clicked.connect(self.deleteRecord)
        self.quitButton.clicked.connect(self.done)


    def done(self, result=None):
        self.mapper.submit()
        QtGui.QDialog.done(self, True)

        
    def addRecord(self):
        row = self.model.rowCount()
        self.mapper.submit()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        now = QtCore.QDateTime.currentDateTime()
        self.startDateTime.setDateTime(now)
        self.endDateTime.setDateTime(now)
        self.outcomeComboBox.setCurrentIndex(
                self.outcomeComboBox.findText("Unresolved"))
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
    app = QtGui.QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "phonelog-fk.db")
    create = not QtCore.QFile.exists(filename)

    #without following nothing works:
    site_pack_path = site.getsitepackages()[1]
    QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))

    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QtGui.QMessageBox.warning(None, "Phone Log",
            QtCore.QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)

    splash = None
    if create:
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
        createFakeData()

    form = PhoneLogDlg()
    form.show()
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    sys.exit(app.exec_())

main()

