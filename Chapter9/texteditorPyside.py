# -*- coding: utf-8 -*-
"""
texteditorPyside.py
Annotated PySide port of texteditor.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

http://qt-project.org/wiki/Transition_from_Qt_4.x_to_Qt5#529c4b0ac2bb03c19bf96de0b6fb2636
http://qt-project.org/forums/viewthread/33907

QWorkspace deprecated, so used suggested QMdiArea instead. This had repurcussions
for most of the methods. The most obvious is that where you would call 'fooWindow' 
you now call 'fooSubWindow'. For example: QWorksspace.activateNextWindow() becomes 
QMdiArea.activeateNextSubWindow(). 

Also, you need to use QMdiArea.activeWindow().widget() to get the active TextEdit object.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtCore, QtGui
import texteditPyside
import resource_rc

__version__ = "1.0.0"

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.mdi = QtGui.QMdiArea() #QtGui.QWorkSpace() is deprecated
        self.setCentralWidget(self.mdi)
        self.create_actions()
        self.load_settings()
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        self.updateWindowMenu()
        self.setWindowTitle("Text Editor")
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
                      
        #Window actions
        self.windowNextAction = self.createAction("&Next",
                self.mdi.activateNextSubWindow, QtGui.QKeySequence.NextChild)
        #following doesn't work exactly right (ctrl-shift-tab)
        self.windowPrevAction = self.createAction("&Previous",
                self.mdi.activatePreviousSubWindow, QtGui.QKeySequence.PreviousChild)
        self.windowCascadeAction = self.createAction("Casca&de",
                self.mdi.cascadeSubWindows)
        self.windowTileAction = self.createAction("&Tile",
                self.mdi.tileSubWindows)
        self.windowMinimizeAction = self.createAction("&Iconize All",
                self.windowMinimizeAll)
        self.windowRestoreAction = self.createAction("&Restore All",
                self.windowRestoreAll) #un-minimize            
                
        #Icons are not movable by default with QMdiArea: so no need to rearrange
        #self.windowArrangeIconsAction = self.createAction(
        #        "&Arrange Icons", self.mdi.arrangeIcons)
        
        self.windowCloseAction = self.createAction("&Close",
                self.mdi.closeActiveSubWindow, QtGui.QKeySequence.Close)

        self.windowMapper = QtCore.QSignalMapper(self)
        self.windowMapper.mapped.connect(self.mdi.setActiveSubWindow)  #setActiveSubWindow is built-in slot

        #Define menus
        #File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                None, fileQuitAction))
        #Edit menu
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction))
        #Window menu
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        #Define toolbars
        #File toolbar
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
                                      
        #Edit toolbar
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction))

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
        for subWindow in self.mdi.subWindowList():
            textEdit=subWindow.widget()
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
        #print "about to closeAllSubWindows"
        self.mdi.closeAllSubWindows()

    def save_settings(self):
        settings = QtCore.QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        files = []
        for subWindow in self.mdi.subWindowList():
            textEdit=subWindow.widget()           
            if not textEdit.filename.startswith("Unnamed"):
                files.append(textEdit.filename)
        settings.setValue("CurrentFiles", files)

    def loadFiles(self):
        if len(sys.argv) > 1:
            for filename in sys.argv[1:31]: # Load at most 30 files
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
        self.mdi.addSubWindow(textEdit)
        textEdit.show()

    def fileOpen(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                "Text Editor -- Open File")[0]
        if filename:
            #If already open, then just activate it
            for subWindow in self.mdi.subWindowList():
                textEdit = subWindow.widget()
                if textEdit.filename == filename:
                    self.mdi.setActiveSubWindow(subWindow)
                    break
            else:
                self.loadFile(filename)

    def loadFile(self, filename):
        #print "loadFile filename: " , filename
        textEdit = texteditPyside.TextEdit(filename=filename)
        try:
            textEdit.load()
        except (IOError, OSError), err:
            print filename
            QtGui.QMessageBox.warning(self, "Text Editor -- Load Error",
                    "Failed to load {0}: {1}".format(filename, err))
            textEdit.close()
            del textEdit
        else:
            self.mdi.addSubWindow(textEdit)
            textEdit.show()


    def fileSave(self):
        #print "fileSave: Trying to save..."
        textEdit = self.mdi.activeSubWindow().widget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return True
        try:
            print "fileSave saving: {0}".format(textEdit.filename)
            textEdit.save()
            return True
        except (IOError, OSError), err:
            QtGui.QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save {0}:\\n{1}".format(textEdit.filename, err))
            return False
        except Exception as err:
            QtGui.QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save {0}:\n{1}".format(textEdit.filename, err))
            return False

    def fileSaveAs(self):
        textEdit = self.mdi.activeSubWindow().widget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        filename = QtGui.QFileDialog.getSaveFileName(self,
                        "Text Editor -- Save File As",
                        textEdit.filename, "Text files (*.txt *.*)")[0]
        if filename:
            textEdit.filename = filename
            return self.fileSave()
        return True

    def fileSaveAll(self):
        errors = []
        for subWindow in self.mdi.subWindowList():
            textEdit = subWindow.widget()
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
        textEdit = self.mdi.activeSubWindow().widget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QtGui.QApplication.clipboard()
            clipboard.setText(text)

    def editCut(self):
        textEdit = self.mdi.activeSubWindow().widget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QtGui.QApplication.clipboard()
            clipboard.setText(text)

    def editPaste(self):
        textEdit = self.mdi.activeSubWindow().widget()
        if textEdit is None or not isinstance(textEdit, QtGui.QTextEdit):
            return
        clipboard = QtGui.QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())

    def windowRestoreAll(self):
        for subWindow in self.mdi.subWindowList():
            textEdit=subWindow.widget()
            textEdit.showNormal() #inherited from qwidget--restores to size pre-minimization or maximization

    def windowMinimizeAll(self):
        for subWindow in self.mdi.subWindowList():
            textEdit = subWindow.widget()
            textEdit.showMinimized()  #showminimized inherited from qwidget

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.addActions(self.windowMenu, (self.windowNextAction,
                self.windowPrevAction, self.windowCascadeAction,
                self.windowTileAction, self.windowRestoreAction,
                self.windowMinimizeAction,
                None,
                self.windowCloseAction))  #self.windowArrangeIconsAction,
        textEdits = [subMenu.widget() for subMenu in self.mdi.subWindowList()]
        if not textEdits:
            #print "Checking for text edits in menu list"
            return
        self.windowMenu.addSeparator()
        i = 1
        menu = self.windowMenu
        for textEdit in textEdits:
            title = textEdit.windowTitle()
            if i == 10:
                self.windowMenu.addSeparator()
                menu = menu.addMenu("&More")
            accel = ""
            if i < 10:
                accel = "&{0} ".format(i)
            elif i < 36:
                accel = "&{0} ".format(chr(i + ord("@") - 9))
            action = menu.addAction("{0}{1}".format(accel, title))
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, textEdit)
            i += 1


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    app.setOrganizationName("PySideSummer")
    app.setOrganizationDomain("https://github.com/EricThomson/PySideSummer")
    app.setApplicationName("Text Editor")  
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    
    form = MainWindow()
    form.show()
    app.exec_()
