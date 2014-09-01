# -*- coding: utf-8 -*-
"""
mymoviesPyside.py
Annotated PySide adaptation of mymovies.pyw from Chapter 8
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import platform
import sys
import PySide
from PySide import QtGui, QtCore
import moviedataPyside
import resource_rc
import addeditmoviedlgPyside

__version__="1.0.0"

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.movies = moviedataPyside.MovieContainer() 
        self.table = QtGui.QTableWidget()
        self.setCentralWidget(self.table)
        self.setWindowTitle("My Movies")
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        #Actions
        #File actions
        fileNewAction=self.createAction( "&New", slot=self.fileNew, shortcut=QtGui.QKeySequence.New,\
                                        icon="filenew", tip="Create a movie data file")
        fileOpenAction = self.createAction("&Open...", slot=self.fileOpen, shortcut = QtGui.QKeySequence.Open, 
                                           icon = "fileopen", tip = "Open an existing  movie data file")
        fileSaveAction = self.createAction("&Save", slot=self.fileSave, shortcut = QtGui.QKeySequence.Save, 
                                           icon="filesave", tip="Save the movie data")                                       
        fileSaveAsAction = self.createAction("Save &As", slot=self.fileSaveAs, icon="filesaveas",
                                             tip = "Save the movie data using a new name")
        fileQuitAction = self.createAction("&Quit", slot=self.close, shortcut = "Ctrl+Q", 
                                           icon="filequit", tip="Close the application")  

        #Edit actions
        editAddAction = self.createAction("&Add...", slot=self.editAdd,shortcut="Ctrl+A", \
                                        icon = "editadd", tip = "Add a movie")
        editEditAction = self.createAction("&Edit...", slot=self.editEdit, shortcut = "Ctrl+E",\
                                            icon="editedit", tip="Edit the current movie's data")
        editRemoveAction = self.createAction("&Remove...", slot = self.editRemove, shortcut = "Del", 
                                             icon = "editdelete", tip="Delete a movie")
        #Help actions
        helpAboutAction = self.createAction("&About", slot=self.helpAbout,
                                            tip="About the application")

        #XML import/export actions
        fileImportDOMAction = \
            self.createAction("&Import from XML (DOM)", slot=self.fileImportDOM,
                tip="Import the movie data from an XML file")
        fileImportSAXAction = self.createAction("I&mport from XML (SAX)", slot = self.fileImportSAX,
                tip="Import the movie data from an XML file")
        fileExportXmlAction = self.createAction("E&xport as XML", self.fileExportXml,
                tip="Export the movie data to an XML file")
                          
        #Menus
        #File menus
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction,\
            None,  fileExportXmlAction, fileImportDOMAction, fileImportSAXAction,None, fileQuitAction))
        #Edit menu
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editAddAction, editEditAction, editRemoveAction))
        #Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction,))      
                   
        #Toolbars
        #File toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,  fileSaveAsAction))
        #Edit toolbars
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editAddAction, editEditAction, editRemoveAction))
                
        #Double click or click enter over row to edit
        self.table.itemDoubleClicked.connect(self.editEdit)                      
        QtGui.QShortcut(QtGui.QKeySequence("Return"), self.table, self.editEdit)


        #Before finishing initializing, restore settings from previous run                     
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QtCore.QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QtCore.QByteArray()))
        
        QtCore.QTimer.singleShot(0, self.loadInitialFile)


            
    #createAction: adding manually would take up more space than a cricket in a thimble.
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot) #old-style: self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    #helper function to add multiple actions to a menu/toolbar
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)    
            
    def fileNew(self):
        if not self.okToContinue():
            return
        self.movies.clear()
        self.statusBar().clearMessage()
        self.updateTable()

    def fileSave(self):
        if not self.movies.filename():
            return self.fileSaveAs()
        else:
            ok, msg = self.movies.save()
            self.statusBar().showMessage(msg, 5000)
            return ok

    #load pre-existing movie container data
    def fileOpen(self):
        if not self.okToContinue():
            return
        path = (QtCore.QFileInfo(self.movies.filename()).path()
                if self.movies.filename() else ".")
        fname = QtGui.QFileDialog.getOpenFileName(self,
                "My Movies - Load Movie Data", path,
                "My Movies data files ({})".format(self.movies.formats()))[0]
        if fname:
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()
                
    def fileSaveAs(self):
        fname = self.movies.filename() if self.movies.filename() else "."  #folder
        fname = QtGui.QFileDialog.getSaveFileName(self,
                "My Movies - Save Movie Data", fname,
                "My Movies data files ({})".format(self.movies.formats()))[0]
        if fname:
            if "." not in fname:
                fname += ".mqb"
            ok, msg = self.movies.save(fname)
            self.statusBar().showMessage(msg, 5000)
            return ok
        return False
 
    def loadInitialFile(self):
        settings = QtCore.QSettings()
        fname = settings.value("LastFile")
        if fname and QtCore.QFile.exists(fname):
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)
        self.updateTable()

    def editAdd(self):
        #print dir(addeditmoviedlgPyside)
        form = addeditmoviedlgPyside.AddEditMovieDlg(self.movies, None, self)
        #print dir(form)
        if form.exec_():
            self.updateTable(id(form.movie))

    def editEdit(self):
        movie = self.currentMovie()
        if movie is not None:
            form = addeditmoviedlgPyside.AddEditMovieDlg(self.movies, movie, self)
            if form.exec_():
                self.updateTable(id(movie))

    def editRemove(self):
        movie = self.currentMovie()
        if movie is not None:
            year = (" {}".format(movie.year)
                    if movie.year != movie.UNKNOWNYEAR else "")
            if (QtGui.QMessageBox.question(self, "My Movies - Delete Movie",
                    "Delete Movie `{}' {}?".format(movie.title, year),
                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes):
                self.movies.delete(movie)
                self.updateTable()
                
    #Rewrite table when data changes. If current is set to an index, then it will
    #highlight that one and scroll to it
    def updateTable(self, current=None):
        self.table.clear()
        self.table.setRowCount(len(self.movies))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Mins",
                "Acquired", "Notes"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.table.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        #not sure what selected is doing, why you would change it each iteration 
        #until the last, instead of just setting the last one selected after the fact.
        selected = None  
        #redraw each item in the table
        for row, movie in enumerate(self.movies):
            #Title
            item = QtGui.QTableWidgetItem(movie.title)
            if current is not None and current == id(movie):
                selected = item  
            item.setData(QtCore.Qt.UserRole, int(id(movie)))
            self.table.setItem(row, 0, item)
            #Year
            year = movie.year
            if year != movie.UNKNOWNYEAR:
                item = QtGui.QTableWidgetItem("{}".format(year))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row, 1, item)
            #Duration
            minutes = movie.minutes
            if minutes != movie.UNKNOWNMINUTES:
                item = QtGui.QTableWidgetItem("{}".format(minutes))
                item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.table.setItem(row, 2, item)
            #Date acquired
            item = QtGui.QTableWidgetItem(movie.acquired.toString(moviedataPyside.DATEFORMAT))
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
            #Notes
            notes = movie.notes
            if len(notes) > 40:
                notes = notes[:39] + "..."
            self.table.setItem(row, 4, QtGui.QTableWidgetItem(notes))
        self.table.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)
        
             
    #Do you want to save unsaved changes? 
    #  If yes--> self.fileSave (which returns True if success)
    #  If no--->return True (ok to continue).
    #  If cancel, return False (will likely be used to cancel the calling operation)
    def okToContinue(self):
        if self.movies.isDirty():
            reply = QtGui.QMessageBox.question(self,
                    "My Movies - Unsaved Changes",
                    "Save unsaved changes?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                return self.fileSave()
        return True
 
   
    #When user indicates they want to quit, reimplement close event to
    #double check they want to close (okToContinue) and save settings
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QtCore.QSettings()
            settings.setValue("LastFile", self.movies.filename())
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()  
            

    def currentMovie(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0)
            id = int(item.data(QtCore.Qt.UserRole))
            #print id
            return self.movies.movieFromId(id)
        return None
        
        
    def helpAbout(self):
        QtGui.QMessageBox.about(self, "My Movies - About",
                """<b>My Movies</b> v {0}
                <p>Copyright &copy; 2008-14 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to view some basic
                information about movies and to load and save the 
                movie data in a variety of custom file formats.
                <p>Python {1} - Qt {2} - PySide {3} on {4}""".\
                format(__version__, platform.python_version(),
                QtCore.qVersion(), PySide.__version__,
                platform.system()))
               
    def fileImportDOM(self):
        self.fileImport("dom")


    def fileImportSAX(self):
        self.fileImport("sax")


    def fileImport(self, format):
        if not self.okToContinue():
            return
        path = (QtCore.QFileInfo(self.movies.filename()).path()
                if self.movies.filename() else ".")
        fname = QtGui.QFileDialog.getOpenFileName(self,
                "My Movies - Import Movie Data", path,
                "My Movies XML files (*.xml)")[0]
        if fname:
            if format == "dom":
                ok, msg = self.movies.importDOM(fname)
            else:
                ok, msg = self.movies.importSAX(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()

    def fileExportXml(self):
        fname = self.movies.filename()
        if not fname:
            fname = "."
        else:
            i = fname.rfind(".")
            if i > 0:
                fname = fname[:i]
            #print type(fname)
            fname += ".xml"
        fname = QtGui.QFileDialog.getSaveFileName(self,
                "My Movies - Export Movie Data", fname,
                "My Movies XML files (*.xml)")[0]
        if fname:
            if "." not in fname:
                fname += ".xml"
            ok, msg = self.movies.exportXml(fname)
            self.statusBar().showMessage(msg, 5000)
            
                    
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    
    app.setOrganizationName("PySideSummer")
    app.setOrganizationDomain("https://github.com/EricThomson/PySideSummer")
    app.setApplicationName("My Movies")
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_() 