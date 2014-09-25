# -*- coding: utf-8 -*-
"""
sditexteditorPyside.py
Annotated PySide port of sditexteditor.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Note I removed all use of 'isAlive' and related methods, as they use 'sip' which
is a PyQt package, and I couldn't get shiboken (which is used to bind PySide to Qt)
to work properly. Instead, to update the Instances variable, I just removed
the present instance in the reimplementation of closeEvent (MainWindow.Instances.remove(self))
updates the list.

"""
#from __future__ import unicode_literals
import codecs
import sys
from PySide import QtGui, QtCore
import resource_rc

__version__ = "1.0.0"


class MainWindow(QtGui.QMainWindow):

    
    NextId = 1  #each time a new window is opened, so it can display (untilted-2, -3, -4, etc). sdi.py uses sequenceNumber
    Instances = [] #list of active window instances (sdi.py uses windowList)

    #create instance 
    def __init__(self, filename="", parent=None):
        QtGui.QMainWindow.__init__(self, parent) 
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  #destroys when user closes
        MainWindow.Instances.append(self)  

        self.editor = QtGui.QTextEdit()
        self.setCentralWidget(self.editor)

        #Create actions
        #File actions
        fileNewAction = self.createAction("&New", self.fileNew,
                QtGui.QKeySequence.New, "filenew", "Create a text file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QtGui.QKeySequence.Open, "fileopen",
                "Open an existing text file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QtGui.QKeySequence.Save, "filesave", "Save the text")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the text using a new filename")
        fileSaveAllAction = self.createAction("Save A&ll",
                self.fileSaveAll, icon="filesave",
                tip="Save all the files")
        fileCloseAction = self.createAction("&Close", self.close,
                QtGui.QKeySequence.Close, "fileclose",
                "Close this text editor")
        fileQuitAction = self.createAction("&Quit", self.fileQuit,
                "Ctrl+Q", "filequit", "Close the application")
        #Edit actions
        editCopyAction = self.createAction("&Copy", self.editor.copy,
                QtGui.QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        editCutAction = self.createAction("Cu&t", self.editor.cut,
                QtGui.QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        editPasteAction = self.createAction("&Paste",
                self.editor.paste, QtGui.QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")

        #Menus
        #File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                None, fileCloseAction, fileQuitAction))
        #Edit menu
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction))
        #Window menu                           
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        #Toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction))
                                      
        #Status bar                             
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.resize(500, 600)

        self.filename = filename
        if not self.filename:
            self.filename = unicode("Unnamed-{0}.txt".format(MainWindow.NextId))
            MainWindow.NextId += 1
            self.editor.document().setModified(False)
            self.setWindowTitle("SDI Text Editor - {0}".format(self.filename))
        else:
            self.loadFile()

        #on destroyed: http://srinikom.github.io/pyside-docs/PySide/QtCore/QObject.html
        #self.destroyed.connect(MainWindow.updateInstances)  #instead of repopulating, just remove
        
        
#    @staticmethod
#    def updateInstances():
#        print "Updating instances"
#        #MainWindow.Instances.remove = (set([window for window
#        #        in MainWindow.Instances if isAlive(window)]))  
#         
                
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    #checks to see if they want to save, and removes from instances list
    def closeEvent(self, event):
        if (self.editor.document().isModified() and
            QtGui.QMessageBox.question(self,
                "SDI Text Editor - Unsaved Changes",
                "Save unsaved changes in {0}?".format(self.filename),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.Yes):
            self.fileSave()
        MainWindow.Instances.remove(self)

    def fileQuit(self):
        QtGui.QApplication.closeAllWindows() #built-in of qapplication

    
    def fileNew(self):
        MainWindow().show()

    def fileOpen(self):
        filename, flt = QtGui.QFileDialog.getOpenFileName(self,
                "SDI Text Editor -- Open File")
        #print "\nfileOpen:\nFilename: {0} \nType: {1}".\
        #        format(filename, type(filename))
                
        if filename:
            if (not self.editor.document().isModified() and
                self.filename.startswith("Unnamed")):
                self.filename = filename
                self.loadFile()
            else:
                MainWindow(filename).show()

    def loadFile(self):
        try:
            with codecs.open(self.filename, encoding="utf-8") as file:
                self.editor.setPlainText(file.read())
                self.editor.document().setModified(False)
        except (IOError, OSError), err:
            QtGui.QMessageBox.warning(self,
                    "SDI Text Editor -- Load Error",
                    "Failed to load {0}: {1}".format(self.filename, err))
        self.editor.document().setModified(False)
        self.setWindowTitle("SDI Text Editor - {0}".format(
                QtCore.QFileInfo(self.filename).fileName()))

    def fileSave(self):
        if self.filename.startswith("Unnamed"):
            return self.fileSaveAs()
        try:
            with codecs.open(self.filename, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())
            self.editor.document().setModified(False)
        except (IOError, OSError) as err:
            QtGui.QMessageBox.warning(self,
                    "SDI Text Editor -- Save Error",
                    "Failed to save {0}: {1}".format(self.filename, err))
            return False
        except Exception as err:
            print "Failed to save: {0}".format(err)
            return False
            
        return True

    def fileSaveAs(self):
        filename, flt = QtGui.QFileDialog.getSaveFileName(self,
                "SDI Text Editor -- Save File As", self.filename,
                "SDI Text files (*.txt *.*)")
        if filename:
            self.filename = filename
            self.setWindowTitle("SDI Text Editor - {0}".format(
                    QtCore.QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False

    def fileSaveAll(self):
        count = 0
        for window in MainWindow.Instances:
            if window.editor.document().isModified():
                if window.fileSave():
                    count += 1
        self.statusBar().showMessage("Saved {0} of {1} files".format(
                count, len(MainWindow.Instances)), 5000)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        for window in MainWindow.Instances:
            #if isAlive(window):
            self.windowMenu.addAction(window.windowTitle(), self.raiseWindow)

 
    def raiseWindow(self):
        action = self.sender()
        if not isinstance(action, QtGui.QAction):
            return
        for window in MainWindow.Instances:
            if (window.windowTitle() == action.text()):
                window.activateWindow()
                window.raise_()
                break
  
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    MainWindow().show()  #this seems to be sufficient to open a window
    MainWindow().show()  #yep, another window opens
    sys.exit(app.exec_())