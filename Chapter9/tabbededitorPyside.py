# -*- coding: utf-8 -*-
"""
tabbededitorPyside.py
One solution to exercise from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Note Summerfield also has a solution, at the book's web site, which is probably better than 
mine. 
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtCore, QtGui
import texteditPyside
import resource_rc

__version__ = "0.0.9"

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.centralTabWindow = QtGui.QTabWidget()      
        self.setCentralWidget(self.centralTabWindow)
        self.create_actions()
        self.load_settings()
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        self.setWindowTitle("Tabbed Text Editor")
        QtCore.QTimer.singleShot(0, self.loadFiles)

    def create_actions(self):
        #Creating the actions
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
                self.fileSaveAll, "filesave",
                tip="Save all the files")
        fileCloseTabAction=self.createAction("Close Tab",\
                self.fileCloseTab, icon = "editdelete", tip= "Close present tab")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
                
        #Edit actions
        editCopyAction = self.createAction("&Copy", self.editCopy,
                QtGui.QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        editCutAction = self.createAction("Cu&t", self.editCut,
                QtGui.QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        editPasteAction = self.createAction("&Paste", self.editPaste,
                QtGui.QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")
                      
        #Window actions--seem to be completely unneeded on my system, so commenting out
        nextTabAction = self.createAction("Next tab",
                self.nextTab, QtGui.QKeySequence.NextChild)
        previousTabAction = self.createAction("Previous tab",
                self.previousTab, QtGui.QKeySequence.PreviousChild)
     
        #Define menus
        #File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,\
                fileSaveAction, fileSaveAsAction, fileSaveAllAction, \
                None, fileCloseTabAction, fileQuitAction))
        #Edit menu
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction))
                                   
        #Tabs menu
        tabsMenu =  self.menuBar().addMenu("Tabs")
        self.addActions(tabsMenu, (nextTabAction, previousTabAction))                       

        #Define toolbars
        #File toolbar
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,\
                                      fileSaveAction, None, fileCloseTabAction))
                                      
        #Edit toolbar
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction))
                                                         

    def fileCloseTab(self):
        self.fileSave()
        currentIndex=self.centralTabWindow.currentIndex()
        #print "Closing tab", currentIndex
        self.centralTabWindow.removeTab(currentIndex)
        
    def load_settings(self):
        settings = QtCore.QSettings()
        self.restoreGeometry(
                settings.value("MainWindow/Geometry"))
        self.restoreState(
                settings.value("MainWindow/State"))


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

    #when application is quit
    def closeEvent(self, event):
        failures = []
        for tabNum in range(self.centralTabWindow.count()):
            textEdit = self.centralTabWindow.widget(tabNum) 
            if textEdit.isModified():
                try:
                    textEdit.save()
                except IOError, err:
                    print "closeEvent error: {0}".format(err)
                    failures.append(unicode(err))
                except Exception as err:
                    print "closeEvent error: {0}".format(err)
                    failures.append(unicode(err))
        #print "closeEvent failures:", failures
        if (failures and
            QtGui.QMessageBox.warning(self, "Text Editor -- Save Error...",
                    "Failed to save {0}\nQuit anyway?".format(
                    "\n\t".join(failures)),
                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                    QtGui.QMessageBox.No):
            event.ignore()
            return
        self.save_settings()


    def save_settings(self):
        settings = QtCore.QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        files = []
        for tabNum in range(self.centralTabWindow.count()):
            textEdit = self.centralTabWindow.widget(tabNum)          
            if not textEdit.filename.startswith("Unnamed"):
                files.append(textEdit.filename)
        settings.setValue("CurrentFiles", files)

    def loadFiles(self):
        if len(sys.argv) > 1:
            for filename in sys.argv[1:10]: # Load at most 30 files
                if QtCore.QFileInfo(filename).isFile():
                    self.loadFile(filename)
                    QtGui.QApplication.processEvents()
        else:
            settings = QtCore.QSettings()
            files = settings.value("CurrentFiles")
            #print "loadFiles: ", files
            for filename in files:
                if QtCore.QFile.exists(filename):
                    self.loadFile(filename)
                    QtGui.QApplication.processEvents()

    def fileNew(self):
        textEdit = texteditPyside.TextEdit()
        self.centralTabWindow.addTab(textEdit, textEdit.filename)
        textEdit.show()
        self.centralTabWindow.setCurrentWidget(textEdit)

    def fileOpen(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                "Text Editor -- Open File")[0]
        if filename:
            #If already open, just activate it, otherwise, load
            for tabNum in range(self.centralTabWindow.count()):
                textEdit = self.centralTabWindow.widget(tabNum)
                if textEdit.filename == filename:
                    self.centralTabWindow.setCurrentWidget(textEdit)
                    break
            else:
                self.loadFile(filename)

    def loadFile(self, filename):
        #print "loadFile filename: " , filename
        textEdit = texteditPyside.TextEdit(filename=filename)
        try:
            textEdit.load()
        except (IOError, OSError), err:
            #print "loadFile error: ", filename
            QtGui.QMessageBox.warning(self, "Text Editor -- Load Error",
                    "Failed to load {0}: {1}".format(filename, err))
            textEdit.close()
            del textEdit
        else:
            pathlessName=QtCore.QFileInfo(textEdit.filename).fileName()
            self.centralTabWindow.addTab(textEdit, pathlessName)
            textEdit.show()
            self.centralTabWindow.setCurrentWidget(textEdit)


    def fileSave(self):
        error=None
        textEdit = self.centralTabWindow.currentWidget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return True
        try:
            textEdit.save()
            pathlessName=QtCore.QFileInfo(textEdit.filename).fileName()
            #print "tabbededitor.fileSave(), textEdit.save().\nSuccessfully saved:\n", pathlessName
            self.centralTabWindow.setTabText(self.centralTabWindow.currentIndex(), \
                pathlessName)
            return True
        except (IOError, OSError), err:
            error=err
            return False
        except Exception as err:
            error=err
        if error is not None:
            QtGui.QMessageBox.warning(self, "Tabbed Editor -- fileSave error",
                    "Failed to save {0}: {1}".format(textEdit.filename, error))
            return False

    def fileSaveAs(self):
        textEdit = self.centralTabWindow.currentWidget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        filename = QtGui.QFileDialog.getSaveFileName(self,
                        "Tabbed Editor -- fileSaveAs",
                        textEdit.filename, "Text files (*.txt *.*)")[0]
        if filename:
            textEdit.filename = filename
            return self.fileSave()
        return True

    def fileSaveAll(self):
        errors = []
        for tabNum in range(self.centralTabWindow.count()):
            textEdit = self.centralTabWindow.widget(tabNum)
            if textEdit.isModified():
                try:
                    textEdit.save()
                except (IOError, OSError), err:
                    errors.append("{0}: {1}".format(textEdit.filename, err))
        if errors:
            QtGui.QMessageBox.warning(self,
                    "Text Editor -- Save All Error",
                    "Failed to save\n{0}".format("\n".join(errors)))

    def editCopy(self):
        textEdit = self.centralTabWindow.currentWidget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QtGui.QApplication.clipboard()
            clipboard.setText(text)


        
    def editCut(self):
        textEdit = self.centralTabWindow.currentWidget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QtGui.QApplication.clipboard()
            clipboard.setText(text)

    def editPaste(self):
        textEdit = self.centralTabWindow.currentWidget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        clipboard = QtGui.QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())

    def nextTab(self):   
        #print "next tab called"
        currentIndex=self.centralTabWindow.currentIndex()
        #print currentIndex
        numTabs=self.centralTabWindow.count()
        if currentIndex == numTabs-1:
            nextIndex=0
        else:
            nextIndex=currentIndex+1
        self.centralTabWindow.setCurrentIndex(nextIndex)
        #print "Tab set to next"
        
    def previousTab(self):
        currentIndex=self.centralTabWindow.currentIndex()
        #print currentIndex
        numTabs=self.centralTabWindow.count()
        if currentIndex == 0:
            previousIndex=numTabs-1
        else:
            previousIndex=currentIndex-1
        self.centralTabWindow.setCurrentIndex(previousIndex)
        #print "Tab set to previous"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    app.setOrganizationName("PySideSummer")
    app.setOrganizationDomain("https://github.com/EricThomson/PySideSummer")
    app.setApplicationName("Tabbed Text Editor")  
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    
    form = MainWindow()
    form.show()
    app.exec_()



