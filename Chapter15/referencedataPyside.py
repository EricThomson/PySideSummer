# -*- coding: utf-8 -*-
"""
referencedataPyside.py: one "solution" to exercise in Chapter 15
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

It actually doesn't follow the instructions (e.g., it is a food db, I didn't use a
QDialogButtonBox to make the buttons, and has lots of additional features). 

Basically I liked this project a lot, so ended up making a module to display databases
in a way I would personally find interesting and useful, that does everything
laid out in the exercise, but not using the same methods.

Summerfield has an answer on his site too which 
follows the instructions laid out, to the letter, which
is probably better than my solution.

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import os
import sys
from PySide import QtGui, QtCore, QtSql

ID = 0
CATEGORY = 1
SHORTDESC = 3

class DatabaseInspector(QtGui.QDialog):

    def __init__(self, tableName, dbName, parent = None):
        QtGui.QDialog.__init__(self, parent) 
       
        self.tableName = tableName
        self.dbName = dbName
        
        #References
        #define model
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.select()

        #set tableview to display data in model
        self.view = QtGui.QTableView()
        self.view.setModel(self.model)

        #Bells/whistles
        self.view.resizeColumnsToContents()  
        self.view.setAlternatingRowColors(True) 
        
        
        #finish up and show
        self.setWindowTitle("{0}:  {1}".format(dbName, tableName))

        #BUttons
        self.quitButton = QtGui.QPushButton("Quit")
        self.addButton = QtGui.QPushButton("Add")
        self.removeButton = QtGui.QPushButton("Remove")
        self.sortButton = QtGui.QPushButton("Sort By")
        
        #Sort button/menu and create mapping/connection to slot
        sortMenu = QtGui.QMenu(self.sortButton)
        idSort = sortMenu.addAction("ID")
        categorySort = sortMenu.addAction("Category")
        shortDescSort = sortMenu.addAction("Short desc")
        self.sortButton.setMenu(sortMenu)
        #Use qsignalmapper to carry value
        sortMapping = QtCore.QSignalMapper(self)
        sortMapping.setMapping(idSort, 0)
        sortMapping.setMapping(categorySort, 1)
        sortMapping.setMapping(shortDescSort, 2)
        #connections
        idSort.triggered.connect(sortMapping.map)
        categorySort.triggered.connect(sortMapping.map)
        shortDescSort.triggered.connect(sortMapping.map)
        #connect to mapping
        sortMapping.mapped[int].connect(self.sortData) 
                
        
        #Make other connections
        self.quitButton.clicked.connect(self.accept)
        self.addButton.clicked.connect(self.addRow)
        self.removeButton.clicked.connect(self.remRow)
        
        #Set layout        
        buttonLayout = QtGui.QHBoxLayout()  #horiz button layout (replace with q
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        buttonLayout.addWidget(self.sortButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.quitButton)                           
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)  #table view
        layout.addLayout(buttonLayout)  #pushbutton
        
        self.setLayout(layout)
                 
        #self.setWindowTitle("Database inspector")
        self.show()   
        QtGui.QApplication.processEvents()
        self.resizeWindowToColumns()  #resize window to fit columns


    @QtCore.Slot(int)
    def sortData(self, selection):
        if selection == 0:
            #print "Sort by ID"
            self.model.setSort(ID, QtCore.Qt.AscendingOrder)
        elif selection == 1:
            #print "Sort by category"
            self.model.setSort(CATEGORY, QtCore.Qt.AscendingOrder)
        elif selection == 2:
            #print "Sort by short description"
            self.model.setSort(SHORTDESC, QtCore.Qt.AscendingOrder)           
        self.model.select()
        
    def remRow(self):
        index = self.view.currentIndex()  #how to upull row from index?
        if not index.isValid():
            return
        rowNum = index.row()
        #print "Trying to remove row ", rowNum
        QtSql.QSqlDatabase.database().transaction()  #begin transaction
        record = self.model.record(index.row())
        rowID = int(record.value(ID))
            
        #dialog to ask user if they are sure
        msg = "<font color=red>Delete</font> <b>row {}</b><br>from {}?".format(rowNum, self.tableName)
        if (QtGui.QMessageBox.question(self, "Delete row", msg,
                                       QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) 
                                       == QtGui.QMessageBox.No):
            QtSql.QSqlDatabase.database().rollback()
            return
            
        #If user has verified they want row deleted, do it
        query = QtSql.QSqlQuery()  
        query.exec_("DELETE FROM {} WHERE id = {}".format(self.tableName, rowID))
        self.model.removeRow(index.row())
        self.model.submitAll()  #commits change to database
        QtSql.QSqlDatabase.database().commit() #commit transaction

    def addRow(self):
        row = (self.view.currentIndex().row() if self.view.currentIndex().isValid() else 0)
        #print "add new entry to db row ", row
        QtSql.QSqlDatabase.database().transaction() #start transaction
        self.model.insertRow(row)
        index = self.model.index(row, CATEGORY)
        self.view.setCurrentIndex(index)
        QtSql.QSqlDatabase.database().commit() #commit transaction
        self.view.edit(index)

#    #following was used to help tweak resizeWindowToColumns    
#    def resizeEvent(self, event):                           
#        print "Resized to ({0}, {1})".format(event.size().width(), event.size().height())


    def event(self, event): 
        if event.type() == QtCore.QEvent.EnterWhatsThisMode:
            QtGui.QWhatsThis.leaveWhatsThisMode()  #self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Database Inspector")
            msgBox.setText("Database Inspector 0.0.1")
            msgBox.setInformativeText("A simple platform to inspect and edit database tables")            
            msgBox.exec_()
            return True
        return QtGui.QDialog.event(self, event)
        
    def resizeWindowToColumns(self):
        #Based on: 
        #http://stackoverflow.com/questions/26960006/in-qdialog-resize-window-to-contain-all-columns-of-qtableview
        margins = self.layout().contentsMargins()
        marginWidth = margins.left() + margins.right()
        frameWidth = self.view.frameWidth() * 2
        vertHeaderWidth = self.view.verticalHeader().width()
        horizHeaderWidth =self.view.horizontalHeader().length()
        vertScrollWidth = self.view.style().pixelMetric(QtGui.QStyle.PM_ScrollBarExtent)  
        newWidth = marginWidth + frameWidth + vertHeaderWidth + horizHeaderWidth + vertScrollWidth
        if newWidth <= 800:
            self.resize(newWidth, self.height())
        else:
            self.resize(800, self.height())
 
def databaseConnect():
    '''Connect to sqlite database'''
    #hack needed to load db (see http://stackoverflow.com/a/15941779/1886357)
    import site
    site_pack_path = site.getsitepackages()[1]
    QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))

    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    return db
    
    
def databaseInitialize(db, dbName):
    '''Initialize database: checks to see if it exists, and if it does not, calls
    function to create food database'''
    fullFilePath = os.path.join(os.path.dirname(__file__), dbName) #;print fullFilePath
    dbExists = QtCore.QFile.exists(fullFilePath) #does it already exist in directory?
    
    db.setDatabaseName(fullFilePath) 
    if not db.open():  #.open() creates empty dbName.db file, or loads pre-existing file. returns T/F success/fail
        QtGui.QMessageBox.warning(None, "databaseViewer",
            "Error initializing database. Error message:\n{}".format(db.lastError().text()))
        return False

    if dbExists:
        print "Database already exists...initialization complete"
        return True
    else:
        print "Creating database..."
        if not populateDatabase():
            return False
        else:
            #QtGui.QApplication.processEvents()
            return True

def populateDatabase():
    '''Create 'favorites' table of favorite food'''

    query = QtSql.QSqlQuery()
    if not query.exec_("""CREATE TABLE favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                category VARCHAR(40) NOT NULL,
                number INTEGER NOT NULL,
                shortdesc VARCHAR(20) NOT NULL,
                longdesc VARCHAR(80))"""):
                print "Failed to create table"
                return False
            
    print "Populating table..."
    categories = ("Apples", "Chocolate chip cookies", "Favra beans")
    numbers = (1, 2, 3)
    shortDescs = ("Crispy", "Yummy", "Clarice?")
    longDescs = ("Healthy and tasty", "Never not good...", "")
    query.prepare("""INSERT INTO favorites (category, number, shortdesc, longdesc)
                     VALUES (:category, :number, :shortdesc, :longdesc)""") 
    for category, number, shortDesc, longDesc in zip(categories, numbers, shortDescs, longDescs):
        print category, number, shortDesc, longDesc
        query.bindValue(":category",  category)
        query.bindValue(":number", number)
        query.bindValue(":shortdesc", shortDesc)
        query.bindValue(":longdesc",  longDesc)        
        if not query.exec_():
            print "Failed to populate table"
            return False 
    QtGui.QApplication.processEvents()  #is this needed?
    return True  

def printTable(tableName):
    '''Print out all contents of a table (header names, and each row)'''
    #print "Printing contents of table '{}'".format(tableName)
    
    query = QtSql.QSqlQuery()
    if not query.exec_("""SELECT * FROM {}""".format(tableName)):
        print "Failure to execute SELECT in displayTable"
        return False
    record = query.record()
    
    #display fields
    numFields = record.count() #; print "There are {} fields".format(numFields);  
    fieldNames=()
    print "\nFields:"
    for fieldNum in range(numFields):
        fieldNames = fieldNames + (record.fieldName(fieldNum),)
    print fieldNames
               
    #display values
    print "Values:"
    while query.next():
        values = []
        for field in range(numFields):
            values.append(query.value(field))
        print values  
        
    QtGui.QApplication.processEvents()
    return True

      
def main():
    app = QtGui.QApplication(sys.argv)
    
    #Connect to/initialize database
    dbName = "food.db"
    tableName = "favorites"
    db = databaseConnect()
    if not databaseInitialize(db, dbName):
        print "Failure to initialize...application terminated."
        db.close() 
        del db
        sys.exit(1)
    else:
        printTable(tableName)
        
    #Display database in table view 
    dataTable = DatabaseInspector(tableName, dbName)
    #dataTable.view.show()
    sys.exit(app.exec_())
    
    #Close and delete database: is this needed, or will it be garbage collected?
    db.close()
    del db
    

if __name__ == "__main__":
    main()
    


    


    


        
