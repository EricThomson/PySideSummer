# -*- coding: utf-8 -*-
"""
assetmanagerPyside.py
Annotated PySide adaptation of assetmanager.pyw from Chapter 15
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Sets up master-detail view of inventory (assets), with a log of interactions 
for each item in the inventory. Can edit/remove assets/log entries.

For details of port to PySide, see README.md for this chapter. Briefly, it required
three changes:
1. Explicitly add path to database drivers (this could be platform-specific 
requirement).
2. Replace pyqt version with qt version.
3. Known bug in Pyside: methods for selection model will not work unless you
use an intermediate variable.

To do:
1. Within a session, adding record doesn't seem to actually add a record. 
Same with adding categories. But they both seem to be added when a new app
is opened.

On 1: could this be a clue from the docs?
"Note that calling QtSql.QSqlTableModel.select() will revert any unsubmitted changes 
and remove any inserted columns."
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
#from future_builtins import *  #needed?

import os
import sys
from PySide import QtGui, QtCore, QtSql
import PySide
import site 
import resource_rc

MAC = True
try:
    from PySide.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


print "Asset manager is running with PySide version", PySide.__version__
print "It is using Qt version", QtCore.__version__

ID = 0
NAME = ASSETID = 1
CATEGORYID = DATE = DESCRIPTION = 2
ROOM = ACTIONID = 3

ACQUIRED = 1


class MainForm(QtGui.QDialog):

    def __init__(self):
        super(MainForm, self).__init__()

        #Assets
        #define model
        self.assetModel = QtSql.QSqlRelationalTableModel(self)
        self.assetModel.setTable("assets")
        self.assetModel.setRelation(CATEGORYID,
                QtSql.QSqlRelation("categories", "id", "name"))
        self.assetModel.setSort(ROOM, QtCore.Qt.AscendingOrder)
        self.assetModel.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.assetModel.setHeaderData(NAME, QtCore.Qt.Horizontal, "Name")
        self.assetModel.setHeaderData(CATEGORYID, QtCore.Qt.Horizontal, "Category")
        self.assetModel.setHeaderData(ROOM, QtCore.Qt.Horizontal, "Room")
        self.assetModel.select()

        #set tableview to display data pulled by model
        self.assetView = QtGui.QTableView()
        self.assetView.setModel(self.assetModel)
        self.assetView.setItemDelegate(AssetDelegate(self))
        self.assetView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.assetView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.assetView.setColumnHidden(ID, True)
        self.assetView.resizeColumnsToContents()
        assetLabel = QtGui.QLabel("A&ssets")
        assetLabel.setBuddy(self.assetView)

        #LOG
        #Define model
        self.logModel = QtSql.QSqlRelationalTableModel(self)
        self.logModel.setTable("logs")
        self.logModel.setRelation(ACTIONID,
                QtSql.QSqlRelation("actions", "id", "name"))
        self.logModel.setSort(DATE, QtCore.Qt.AscendingOrder)
        self.logModel.setHeaderData(DATE, QtCore.Qt.Horizontal, "Date")
        self.logModel.setHeaderData(ACTIONID, QtCore.Qt.Horizontal,
                "Action")
        self.logModel.select()
        #View of log
        self.logView = QtGui.QTableView()
        self.logView.setModel(self.logModel)
        self.logView.setItemDelegate(LogDelegate(self))
        self.logView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.logView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.logView.setColumnHidden(ID, True)
        self.logView.setColumnHidden(ASSETID, True)
        self.logView.resizeColumnsToContents()
        self.logView.horizontalHeader().setStretchLastSection(True)
        logLabel = QtGui.QLabel("&Logs")
        logLabel.setBuddy(self.logView)

        addAssetButton = QtGui.QPushButton("&Add Asset")
        deleteAssetButton = QtGui.QPushButton("&Delete Asset")
        addActionButton = QtGui.QPushButton("Add A&ction to Log")
        deleteActionButton = QtGui.QPushButton("Delete Ac&tion from Log")
        editActionsButton = QtGui.QPushButton("&Edit Actions...")
        editCategoriesButton = QtGui.QPushButton("Ed&it Categories...")
        quitButton = QtGui.QPushButton("&Quit")
        for button in (addAssetButton, deleteAssetButton,
                addActionButton, deleteActionButton,
                editActionsButton, editCategoriesButton, quitButton):
            if MAC:
                button.setDefault(False)
                button.setAutoDefault(False)
            else:
                button.setFocusPolicy(QtCore.Qt.NoFocus)

        dataLayout = QtGui.QVBoxLayout()
        dataLayout.addWidget(assetLabel)
        dataLayout.addWidget(self.assetView, 1)
        dataLayout.addWidget(logLabel)
        dataLayout.addWidget(self.logView)
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(addAssetButton)
        buttonLayout.addWidget(deleteAssetButton)
        buttonLayout.addWidget(addActionButton)
        buttonLayout.addWidget(deleteActionButton)
        buttonLayout.addWidget(editActionsButton)
        buttonLayout.addWidget(editCategoriesButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(dataLayout, 1)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        #print "\nSetting connections"
        addAssetButton.clicked.connect(self.addAsset)
        deleteAssetButton.clicked.connect(self.deleteAsset)
        addActionButton.clicked.connect(self.addAction)
        deleteActionButton.clicked.connect(self.deleteAction)
        editActionsButton.clicked.connect(self.editActions)
        editCategoriesButton.clicked.connect(self.editCategories)
        quitButton.clicked.connect(self.done)

        
        #following needed to be broken up #Eric
        #self.assetView.selectionModel().currentRowChanged.connect(self.assetChanged)
        selModel = self.assetView.selectionModel()
        #print "seleciton model connection"
        selModel.currentRowChanged.connect(self.assetChanged)
        #print "selection model connection succeeded"
        
        self.assetChanged(self.assetView.currentIndex())
        self.setMinimumWidth(650)
        self.setWindowTitle("Asset Manager")

    def done(self, result=1):
        query = QtSql.QSqlQuery()
        query.exec_("DELETE FROM logs WHERE logs.assetid NOT IN"
                    "(SELECT id FROM assets)")
        QtGui.QDialog.done(self, 1) #another way to terminate app

    def assetChanged(self, index):
        #print "changing asset"
        if index.isValid():
            record = self.assetModel.record(index.row())
            id = int(record.value("id"))
            self.logModel.setFilter("assetid = {}".format(id))
        else:
            self.logModel.setFilter("assetid = -1")
        self.logModel.reset() # workaround for Qt <= 4.3.3/SQLite bug
        self.logModel.select()
        self.logView.horizontalHeader().setVisible(self.logModel.rowCount() > 0)
        if QtCore.__version__ < "4.1.0":
            self.logView.setColumnHidden(ID, True)
            self.logView.setColumnHidden(ASSETID, True)

    def addAsset(self):
        #print "add new asset to db"
        row = (self.assetView.currentIndex().row()\
               if self.assetView.currentIndex().isValid() else 0)

        QtSql.QSqlDatabase.database().transaction() #start transaction
        self.assetModel.insertRow(row)
        index = self.assetModel.index(row, NAME)
        self.assetView.setCurrentIndex(index)
        assetid = 1
        query = QtSql.QSqlQuery()
        query.exec_("SELECT MAX(id) FROM assets")
        if query.next():
            assetid = int(query.value(0))
        #populate log with acquired/date
        query.prepare("INSERT INTO logs (assetid, date, actionid) "
                      "VALUES (:assetid, :date, :actionid)")
        query.bindValue(":assetid", assetid + 1)
        query.bindValue(":date", QtCore.QDate.currentDate())
        query.bindValue(":actionid", ACQUIRED)
        query.exec_()
        QtSql.QSqlDatabase.database().commit() #commit transaction
        
        self.assetView.edit(index)

    def deleteAsset(self):
        #print "deleted asset from table/base"
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
            
        QtSql.QSqlDatabase.database().transaction()  #begin transaction
        record = self.assetModel.record(index.row())
        assetid = int(record.value(ID))
        #how many log records with current asset?
        logrecords = 1 
        query = QtSql.QSqlQuery(
                "SELECT COUNT(*) FROM logs WHERE assetid = {}".format(assetid))
        if query.next():
            logrecords = int(query.value(0)) #how many log records
            
        #dialog to ask user if they are sure
        msg = ("<font color=red>Delete</font><br><b>{}</b>"
               "<br>from room {}".format(
               record.value(NAME), record.value(ROOM)))
        if logrecords > 1:
            msg += ", along with {} log records".format(
                   logrecords)
        msg += "?"
        if (QtGui.QMessageBox.question(self, "Delete Asset", msg,
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.No):
            QtSql.QSqlDatabase.database().rollback()
            return
            
        #If user has verified they want asset deleted, do it
        query.exec_("DELETE FROM logs WHERE assetid = {}".format(
                    assetid))
        self.assetModel.removeRow(index.row())
        self.assetModel.submitAll()
        QtSql.QSqlDatabase.database().commit() #commit transaction
        
        self.assetChanged(self.assetView.currentIndex())

    def addAction(self):
        #print "action add to current log"
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        #Start transaction so if asset is deleted before action
        #is done adding, it will not add it..
        QtSql.QSqlDatabase.database().transaction()
        record = self.assetModel.record(index.row())
        assetid = int(record.value(ID))

        #add at end of current log table
        #add id,  default to current date
        row = self.logModel.rowCount()
        self.logModel.insertRow(row)
        self.logModel.setData(self.logModel.index(row, ASSETID),
                              assetid)
        self.logModel.setData(self.logModel.index(row, DATE),
                              QtCore.QDate.currentDate())
        QtSql.QSqlDatabase.database().commit()  #commit transaction
        
        index = self.logModel.index(row, ACTIONID)
        self.logView.setCurrentIndex(index)
        self.logView.edit(index)

    def deleteAction(self):
        #print "action delete from current log"
        index = self.logView.currentIndex()
        if not index.isValid():
            return
        record = self.logModel.record(index.row())
        action = record.value(ACTIONID)
        if action == "Acquired":
            QtGui.QMessageBox.information(self, "Delete Log",
                    "The 'Acquired' log record cannot be deleted.<br>"
                    "You could delete the entire asset instead.")
            return
        when = record.value(DATE)
        if (QtGui.QMessageBox.question(self, "Delete Log",
                "Delete log<br>{} {}?".format(when, action),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.No):
            return
        self.logModel.removeRow(index.row())
        self.logModel.submitAll()  #updates the underlying database

    def editActions(self):
        #print "edit action list for logs"
        form = ReferenceDataDlg("actions", "Action", self)
        form.exec_()
        

    def editCategories(self):
        #print "edit asset categories"
        form = ReferenceDataDlg("categories", "Category", self)
        form.exec_()
        
        
class ReferenceDataDlg(QtGui.QDialog):

    def __init__(self, table, title, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        #print table, title
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable(table)
        self.model.setSort(NAME, QtCore.Qt.AscendingOrder)
        self.model.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(NAME, QtCore.Qt.Horizontal, "Name")
        self.model.setHeaderData(DESCRIPTION, QtCore.Qt.Horizontal,
                                 "Description")
        self.model.select()

        self.view = QtGui.QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.view.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()

        addButton = QtGui.QPushButton("&Add")
        deleteButton = QtGui.QPushButton("&Delete")
        okButton = QtGui.QPushButton("&OK")
        if not MAC:
            addButton.setFocusPolicy(QtCore.Qt.NoFocus)
            deleteButton.setFocusPolicy(QtCore.Qt.NoFocus)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        addButton.clicked.connect(self.addRecord)
        deleteButton.clicked.connect(self.deleteRecord)
        okButton.clicked.connect(self.accept)

        self.setWindowTitle(
                "Asset Manager - Edit {} Reference Data".format(title))

    def addRecord(self):
        #print "add Record"
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, NAME)
        self.view.setCurrentIndex(index)
        self.view.edit(index)
        #try updating on the fly
        self.model.submitAll()


    def deleteRecord(self):
        #print "delete REcord"
        index = self.view.currentIndex()
        if not index.isValid():
            return
        #QtSql.QSqlDatabase.database().transaction()
        record = self.model.record(index.row())
        id = int(record.value(ID))
        table = self.model.tableName()
        query = QtSql.QSqlQuery()
        if table == "actions":
            query.exec_("SELECT COUNT(*) FROM logs "
                        "WHERE actionid = {}".format(id))
        elif table == "categories":
            query.exec_("SELECT COUNT(*) FROM assets "
                        "WHERE categoryid = {}".format(id))
        count = 0
        if query.next():
            count = int(query.value(0))
        if count:
            QtGui.QMessageBox.information(self,
                    "Delete {}".format(table),
                    "Cannot delete {}<br>"
                    "from the {} table because it is used by "
                    "{} records".format(
                    record.value(NAME), table, count))
            #QtSql.QSqlDatabase.database().rollback()
            return
        self.model.removeRow(index.row())
        self.model.submitAll()

        #QtSql.QSqlDatabase.database().commit()

class AssetDelegate(QtSql.QSqlRelationalDelegate):

    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        #print "asset delegate paint"
        myoption = QtGui.QStyleOptionViewItem(option)  #?
        if index.column() == ROOM:
            myoption.displayAlignment |= (QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        QtSql.QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        if index.column() == ROOM:
            editor = QtGui.QLineEdit(parent)
            regex = QtCore.QRegExp(r"(?:0[1-9]|1[0124-9]|2[0-7])"
                                   r"(?:0[1-9]|[1-5][0-9]|6[012])")
            validator = QtGui.QRegExpValidator(regex, parent)
            editor.setValidator(validator)
            editor.setInputMask("9999")
            editor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            return editor
        else:
            return QtSql.QSqlRelationalDelegate.createEditor(self, parent,
                                                       option, index)
    def setEditorData(self, editor, index):
        #print "setting editor data (asset)"
        if index.column() == ROOM:
            text = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setText(text)
        else:
            QtSql.QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        #print "setting model data (asset)"
        if index.column() == ROOM:
            #print "text: ", editor.text()
            model.setData(index, editor.text())
        else:
            QtSql.QSqlRelationalDelegate.setModelData(self, editor, model,
                                                index)


class LogDelegate(QtSql.QSqlRelationalDelegate):

    def __init__(self, parent=None):
        super(LogDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        myoption = QtGui.QStyleOptionViewItem(option)
        if index.column() == DATE:
            myoption.displayAlignment |= (QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        QtSql.QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        
        if index.column() == ACTIONID:
            text = index.model().data(index, QtCore.Qt.DisplayRole)
            #if text.isdigit() and int(text) == ACQUIRED:
            if text == ACQUIRED:
                return # Acquired is read-only             
                
        if index.column() == DATE:
            editor = QtGui.QDateEdit(parent)
            editor.setMaximumDate(QtCore.QDate.currentDate())
            editor.setDisplayFormat("yyyy-MM-dd")
            if QtCore.__version__ >= "4.1.0":
                editor.setCalendarPopup(True)
            editor.setAlignment(QtCore.Qt.AlignRight|
                                QtCore.Qt.AlignVCenter)
            return editor
        else:
            return QtSql.QSqlRelationalDelegate.createEditor(self, parent,
                                                       option, index)

    def setEditorData(self, editor, index):
        #print "setting editor data (log)"
        if index.column() == DATE:
            date = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setDate(date)
        else:
            QtSql.QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        #print "setting model data (log)"
        if index.column() == DATE:
            model.setData(index, editor.date())
        else:
            QtSql.QSqlRelationalDelegate.setModelData(self, editor, model,
                                                index)


def createFakeData():
    import random

    print("Dropping tables...")
    query = QtSql.QSqlQuery()
    query.exec_("DROP TABLE assets")
    query.exec_("DROP TABLE logs")
    query.exec_("DROP TABLE actions")
    query.exec_("DROP TABLE categories")
    QtGui.QApplication.processEvents()

    print("Creating tables...")
    query.exec_("""CREATE TABLE actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)""")
    query.exec_("""CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)""")
    query.exec_("""CREATE TABLE assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                categoryid INTEGER NOT NULL,
                room VARCHAR(4) NOT NULL,
                FOREIGN KEY (categoryid) REFERENCES categories)""")
    query.exec_("""CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                assetid INTEGER NOT NULL,
                date DATE NOT NULL,
                actionid INTEGER NOT NULL,
                FOREIGN KEY (assetid) REFERENCES assets,
                FOREIGN KEY (actionid) REFERENCES actions)""")
    QtGui.QApplication.processEvents()

    print("Populating tables...")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Acquired', 'When installed')")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Broken', 'When failed and unusable')")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Repaired', 'When back in service')")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Routine maintenance', "
                "'When tested, refilled, etc.')")
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Computer Equipment', "
                "'Monitors, System Units, Peripherals, etc.')")
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Furniture', 'Chairs, Tables, Desks, etc.')")
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Electrical Equipment', 'Non-computer electricals')")
    today = QtCore.QDate.currentDate()
    floors = list(range(1, 12)) + list(range(14, 28))
    monitors = (('17" LCD Monitor', 1),
                ('20" LCD Monitor', 1),
                ('21" LCD Monitor', 1),
                ('21" CRT Monitor', 1),
                ('24" CRT Monitor', 1))
    computers = (("Computer (32-bit/80GB/0.5GB)", 1),
                 ("Computer (32-bit/100GB/1GB)", 1),
                 ("Computer (32-bit/120GB/1GB)", 1),
                 ("Computer (64-bit/240GB/2GB)", 1),
                 ("Computer (64-bit/320GB/4GB)", 1))
    printers = (("Laser Printer (4 ppm)", 1),
                ("Laser Printer (6 ppm)", 1),
                ("Laser Printer (8 ppm)", 1),
                ("Laser Printer (16 ppm)", 1))
    chairs = (("Secretary Chair", 2),
              ("Executive Chair (Basic)", 2),
              ("Executive Chair (Ergonimic)", 2),
              ("Executive Chair (Hi-Tech)", 2))
    desks = (("Desk (Basic, 3 drawer)", 2),
             ("Desk (Standard, 3 drawer)", 2),
             ("Desk (Executive, 3 drawer)", 2),
             ("Desk (Executive, 4 drawer)", 2),
             ("Desk (Large, 4 drawer)", 2))
    furniture = (("Filing Cabinet (3 drawer)", 2),
                 ("Filing Cabinet (4 drawer)", 2),
                 ("Filing Cabinet (5 drawer)", 2),
                 ("Bookcase (4 shelves)", 2),
                 ("Bookcase (6 shelves)", 2),
                 ("Table (4 seater)", 2),
                 ("Table (8 seater)", 2),
                 ("Table (12 seater)", 2))
    electrical = (("Fan (3 speed)", 3),
                  ("Fan (5 speed)", 3),
                  ("Photocopier (4 ppm)", 3),
                  ("Photocopier (6 ppm)", 3),
                  ("Photocopier (8 ppm)", 3),
                  ("Shredder", 3))
    query.prepare("INSERT INTO assets (name, categoryid, room) "
                  "VALUES (:name, :categoryid, :room)")
    logQuery = QtSql.QSqlQuery()
    logQuery.prepare("INSERT INTO logs (assetid, date, actionid) "
                     "VALUES (:assetid, :date, :actionid)")
    assetid = 1
    for i in range(20):
        print "populating row #", i
        room = "{0:02d}{1:02d}".format(
                random.choice(floors), random.randint(1, 62))
        for name, category in (random.choice(monitors),
                random.choice(computers), random.choice(chairs),
                random.choice(desks), random.choice(furniture)):
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec_()
            
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec_()
            
            if random.random() > 0.7:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid",
                            random.choice((2, 4)))
                    logQuery.exec_()
            assetid += 1
        if random.random() > 0.8:
            name, category = random.choice(printers)
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec_()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec_()
            if random.random() > 0.6:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid",
                            random.choice((2, 4)))
                    logQuery.exec_()
            assetid += 1
        if random.random() > 0.6:
            name, category = random.choice(electrical)
            query.bindValue(":name", name)
            query.bindValue(":categoryid", category)
            query.bindValue(":room", room)
            query.exec_()
            logQuery.bindValue(":assetid", assetid)
            when = today.addDays(-random.randint(7, 1500))
            logQuery.bindValue(":date", when)
            logQuery.bindValue(":actionid", ACQUIRED)
            logQuery.exec_()
            if random.random() > 0.5:
                logQuery.bindValue(":assetid", assetid)
                when = when.addDays(random.randint(1, 1500))
                if when <= today:
                    logQuery.bindValue(":date", when)
                    logQuery.bindValue(":actionid",
                            random.choice((2, 4)))
                    logQuery.exec_()
            assetid += 1
        QtGui.QApplication.processEvents()

    print("Assets:")
    
    query.exec_('''SELECT id, name, categoryid, room 
                   FROM assets 
                   ORDER by id''')
    categoryQuery = QtSql.QSqlQuery()
    
    while query.next():
        #print "doing query"
        #print "query value 0 and type", query.value(0), type(query.value(0))
        id = int(query.value(0))
        name = query.value(1)
        categoryid = int(query.value(2))
        room = query.value(3)
        categoryQuery.exec_("SELECT name FROM categories "
                "WHERE id = {}".format(categoryid))
        category = "{}".format(categoryid)
        if categoryQuery.next():
            category = categoryQuery.value(0)
        print("{0}: {1} [{2}] {3}".format(id, name, category, room))
    #print "done printing values about to processEvents"
    QtGui.QApplication.processEvents()
    
    
def main():
    app = QtGui.QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "assets.db")
    
    create = not QtCore.QFile.exists(filename) #if filename isn't there, then create it
    
    #PySide connection hack
    site_pack_path = site.getsitepackages()[1] 
    QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))
    
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QtGui.QMessageBox.warning(None, "Asset Manager",
            "Database Error: {}".format(db.lastError().text()))
        sys.exit(1)

    splash = None
    if create:
        app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        splash = QtGui.QLabel()
        pixmap = QtGui.QPixmap(":/assetmanagersplash.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())
        splash.setWindowFlags(QtCore.Qt.SplashScreen)
        rect = app.desktop().availableGeometry()
        splash.move((rect.width() - pixmap.width()) / 2,
                    (rect.height() - pixmap.height()) / 2)
        splash.show()
        app.processEvents()
        #print "main about to create fake data"
        createFakeData()
        #print "making fake data"

    form = MainForm()
    form.show()
    if create:
        #print "closing splash"
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()
    app.exec_()
    del form
    del db


main()

