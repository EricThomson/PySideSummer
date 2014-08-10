# coding: utf-8
"""
imagechangerPyside.py
Annotated PySide adaptation of imagechanger.pyw from Chapter 6
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Usage: Open it up and edit, create, and save images.

See PySideSummer/Chapter6/README.md for a detailed description of the 
structure of this project and how to get it working. 

For first-timers with this material, it may be helpful to peruse
usefulDocumentation.txt file, which contains extended exerpts from PySide docs
on some of the classes and methods used in this chapter.
-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import PySide
from PySide import QtGui, QtCore
import os
import platform
import sys
import helpformPyside
import newimagedlgPyside
import resource_rc  

__version__ = "1.0.2"

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #initialize attributes 
        self.setWindowTitle("Image Changer")
        self.image = QtGui.QImage()  #null image
        self.dirty = False  #is there an image with unsaved changes?
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False
        self.printer = None  #when user tries to print, QPrinter is instantiated
        
        #Image will be displayed as QLabel--this is the single central widget
        self.imageLabel = QtGui.QLabel() 
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)  #right-click menu for image
        self.setCentralWidget(self.imageLabel) 

        #Add a dockwidget to log activity in the program (it holds a QListWidget)
        logDockWidget = QtGui.QDockWidget("Log", self)
        logDockWidget.setObjectName("LogDockWidget")  #don't totally understand why this is needed
        logDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.listWidget = QtGui.QListWidget()
        logDockWidget.setWidget(self.listWidget)  #add qlistwidget to dock
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, logDockWidget) #add dock to main window
    
        #Status bar will display messages and a permanent widget to show dimensions of image
        #seems to automatically handle layout of two widgets
        status = self.statusBar()
        self.sizeLabel = QtGui.QLabel()
        self.sizeLabel.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)
        status.setSizeGripEnabled(False)   #this doesn't seem to do much
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000) #shows message for 5 seconds
        
        '''
        If you were to create each action "by hand"
        fileNewAction=QtGui.QAction("&New", self)
        fileNewAction.setIcon(QtGui.QIcon("images/filenew.png"))
        fileNewAction.setShortcut(QtGui.QKeySequence.New)  #qkeysequence lets qt select depending on OS (windows ctrl-N)
        #enum of QKeySequence for different systems:
        #http://srinikom.github.io/pyside-docs/PySide/QtGui/QKeySequence.html
        helpStatus="Click to open a new image"
        helpTool="New image"
        fileNewAction.setToolTip(helpTool) #causes text to appear over toolbar icon
        fileNewAction.setStatusTip(helpStatus) #will show in status bar or over menu item
        fileNewAction.triggered.connect(self.dumSlot)
        '''
        #File actions (all use the default signal (triggered) and checkable state (False))
        fileNewAction=self.createAction( "&New", slot=self.fileNew, shortcut=QtGui.QKeySequence.New,\
                                        icon="filenew", tip="Create a new image")
        fileOpenAction = self.createAction("&Open...", slot=self.fileOpen, shortcut = QtGui.QKeySequence.Open, 
                                           icon = "fileopen", tip = "Open an existing image file")
        fileSaveAction = self.createAction("&Save", slot=self.fileSave, shortcut = QtGui.QKeySequence.Save, 
                                           icon="filesave", tip="Save image")                                           
        fileSaveAsAction = self.createAction("Save &As", slot=self.fileSaveAs, icon="filesaveas",
                                             tip="Save image as...")   
        filePrintAction = self.createAction("&Print", slot=self.filePrint, shortcut=QtGui.QKeySequence.Print, 
                                            icon="fileprint", tip="Print the image")
        fileQuitAction = self.createAction("&Quit", slot=self.close, shortcut = "Ctrl+Q", 
                                           icon="filequit", tip="Close the application")                                     
        
        #Edit image actions
        editInvertAction = self.createAction("&Invert", slot=self.editInvert, shortcut = "Ctrl+I", 
                                             icon="editinvert", tip = "Invert the image's colors", 
                                             checkable=True, signal="toggled")
        editSwapRedAndBlueAction = self.createAction("Sw&ap Red and Blue", slot = self.editSwapRedAndBlue, shortcut= "Ctrl+A", 
                                                     icon = "editswap", tip = "Swap the image's red and blue color components", 
                                                     checkable=True, signal = "toggled")
        editZoomAction = self.createAction("&Zoom", slot=self.editZoom,  shortcut = "Alt+Z", 
                                           icon="editzoom", tip="Zoom the image")
                                           
        #Edit mirror actions in a QActionGroup
        #The QtGui.QActionGroup class groups actions together. In some situations 
        #it is useful to group actions together such that only one of these actions 
        #should be active at any one time. One simple way of achieving this is to 
        #group the actions together in an action group.                                         
        mirrorGroup = QtGui.QActionGroup(self)
        editUnMirrorAction = self.createAction("&Unmirror", slot = self.editUnMirror, shortcut = "Ctrl+U", 
                                               icon = "editunmirror", tip = "Unmirror the image", 
                                               checkable=True, signal="toggled")
        editMirrorHorizontalAction = self.createAction("Mirror &Horizontally", self.editMirrorHorizontal, shortcut = "Ctrl+H", 
                                                       icon = "editmirrorhoriz", tip = "Horizontally mirror the image", 
                                                       checkable = True, signal = "toggled")
        editMirrorVerticalAction = self.createAction("Mirror &Vertically", self.editMirrorVertical, shortcut = "Ctrl+V", 
                                                     icon = "editmirrorvert", tip = "Vertically mirror the image", 
                                                     checkable=True, signal = "toggled")
        mirrorGroup.addAction(editUnMirrorAction)      
        mirrorGroup.addAction(editMirrorHorizontalAction)        
        mirrorGroup.addAction(editMirrorVerticalAction)
        editUnMirrorAction.setChecked(True) #for exclusive group must pick one to be on    
        
        #help actions
        helpAboutAction = self.createAction("&About Image Changer", slot=self.helpAbout)
        helpHelpAction = self.createAction("&Help", slot=self.helpHelp, shortcut= QtGui.QKeySequence.HelpContents)
                         
        #Additional Widgets
        #spinbox widget for zooming
        self.zoomSpinBox = QtGui.QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomSpinBox.valueChanged.connect(self.showImage)  #showimage uses the spinbox attribute to scale image
                
        #Menus
        #QMainWindow.menuBar() creates and returns an empty menu bar if the menu bar does not exist 
        #addMenu(text) appends a new QMenu with title to the main menu bar. The menu bar takes 
        #ownership of the menu. 
        #File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, None, filePrintAction,
                fileQuitAction)
        #instead of addActions, we build connections on the fly in updateFileMenu
        self.fileMenu.aboutToShow.connect(self.updateFileMenu) #because recently opened files put in menu
                
        #Edit menu
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editInvertAction, editSwapRedAndBlueAction, editZoomAction))
        #create mirror menu and add it to editMenu
        #Submenu addition is same as main menu addition, except no need to call menuBar, only addMenu
        mirrorMenu = editMenu.addMenu(QtGui.QIcon(":/editmirror.png"), "&Mirror")
        self.addActions(mirrorMenu, (editUnMirrorAction, editMirrorHorizontalAction, editMirrorVerticalAction))
          
         #Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))         
          
        #Toolbars
        #QMainWindow.addToolBar creates a QtGui.QToolBar object, setting its 
        #window title to title , and inserts it into the top toolbar area.        
        #File toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, None, 
                                filePrintAction, fileQuitAction)  
        self.addActions(fileToolbar, self.fileMenuActions) #addActions is custom helper
        
        #Edit toolbars
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editInvertAction,
                editSwapRedAndBlueAction, editUnMirrorAction,
                editMirrorVerticalAction, editMirrorHorizontalAction))
        editToolbar.addWidget(self.zoomSpinBox) #add zoom spinbox widget

        #Add context menu (right click menu) to imagelabel
        self.addActions(self.imageLabel, (editInvertAction,
                editSwapRedAndBlueAction, editUnMirrorAction,
                editMirrorVerticalAction, editMirrorHorizontalAction))
        #Tuple of which actions reset to when new image or previously  unseen opened
        self.resettableActions = ((editInvertAction, False),
                                 (editSwapRedAndBlueAction, False),
                                 (editUnMirrorAction, True))

        #Before finishing initializing, restore settings from previous run
        #See main() for more details
        settings = QtCore.QSettings()  #qsettings to carry over info b/w sessions     
        self.recentFiles =settings.value("RecentFiles", [])
        self.restoreGeometry(settings.value("MainWindow/Geometry", QtCore.QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QtCore.QByteArray()))         
        #print "\nIn __init__: settings.allKeys()= " , settings.allKeys()
        
        #Set up file menu, and load initial file (if there is one)
        self.updateFileMenu()  
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

    #Create a new image (self.image)
    def fileNew(self):
        #check for dirty workspace, give option to save
        if not self.okToContinue():
            return
        #Dialog for making new simple image
        dialog = newimagedlgPyside.NewImageDlg(self)  #uses the gui-generated dialog
        if dialog.exec_():
            #print "Dialog info: ", dialog
            #print self.filename
            #if they accept, will overwrite present filename, so add it to recent files first
            self.addRecentFile(self.filename)  
            self.image = QtGui.QImage()  #clear data before resetting
            #resettable actions reset
            for action, check in self.resettableActions:
                action.setChecked(check)
            self.image = dialog.image()  #Qimage type returned by newimagedlgPyside
            #print "Image props: ", dir(self.image)
            self.filename = None  #resetting filename
            self.dirty = True  #hasn't been saved yet
            #show image and set label size to accommodate it
            self.showImage()
            self.sizeLabel.setText("{} x {}".format(self.image.width(),
                                                      self.image.height()))
            self.updateStatus("Created new image") #defined below
        
    #Loads pre-existing image
    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                for format in QtGui.QImageReader.supportedImageFormats()])  
        #print "fileOpen formats: ", formats
        fname = QtGui.QFileDialog.getOpenFileName(self,
                "Image Changer - Choose Image", dir,
                "Image files ({})".format(" ".join(formats)))[0] #[0] b/c returns 2-tuple, only need first elt
        #print "output of getopenfilename[0]: ", fname[0]
        if fname:
            self.loadFile(fname)  #this updates the status

    #Do you want to save unsaved changes? 
    #  If yes--> self.fileSave (which returns True if success)
    #  If no--->return True (ok to continue).
    #  If cancel, return False (will likely be used to cancel the calling operation)
    #Called by loadfile, filenew, fileopen, and reimplementation of close event (basically
    #used whenever you might lose unsaved changes).
    def okToContinue(self):
        if self.dirty:
            reply = QtGui.QMessageBox.question(self,
                    "Image Changer - Unsaved Changes",
                    "Save unsaved changes?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                return self.fileSave()
        return True

    #Display the image. Called by zoom
    def showImage(self, percent=None):
        if self.image.isNull():
            return
        if percent is None:
            percent = self.zoomSpinBox.value()
        factor = percent / 100.0
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio)  #makes a copy, so doesn't change original
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image)) #extract pixmap from image and display it
     
    #update log, status bar, title
    #Called by different edit functions, new file, basically when the
    #user does anything that changes the image, opens a new image, etc. (anything to log)
    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.listWidget.addItem(message)  #logging our activity
        if self.filename:
            self.setWindowTitle("Image Changer - {}[*]".format(
                                os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        #On setwindowmodified:
        #This property holds whether the document shown in the window has unsaved changes.
        #A modified window is a window whose content has changed but has not been saved to 
        #disk. This flag will have different effects varied by the platform. On Mac OS X 
        #the close button will have a modified look; on other platforms, the window title 
        #will have an ‘*’ (asterisk).
        #
        #The window title must contain a “[*]” placeholder, which indicates where the ‘*’ 
        #should appear. Normally, it should appear right after the file name 
        #(e.g., “document1.txt[*] - Text Editor”). If the window isn’t modified, the 
        #placeholder is simply removed.
        self.setWindowModified(self.dirty)        
         
         
    #Iif it exists, load the most recent file stored in settings("LastFile")
    def loadInitialFile(self):
        settings = QtCore.QSettings()
        #print "In loadInitialFile. settings.allKeys(): ", settings.allKeys()  #db
        fname = settings.value("LastFile")
        #print "settings.value('LastFile'): ", fname
        if fname and QtCore.QFile.exists(fname):
            self.loadFile(fname)
            
    #Construct file menu on the fly to include recent items, which are connected
    #individually to self.loadFile()
    def updateFileMenu(self):
        #print "Updating file menu"
        self.fileMenu.clear()       
        #Add all the actions, except quit
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        recentFiles = []
        #append recent files to menu, if they still exist and are not currently open
        current = self.filename  #image that is currently open (will be None if none open)
        for fname in self.recentFiles:
            #print fname
            if fname != current and QtCore.QFile.exists(fname):
                recentFiles.append(fname)
                
        #Add a separator and the recent files, if applicable 
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                #define new action for clicking recent files in menu
                action = QtGui.QAction(QtGui.QIcon(":/icon.png"), "&{number} {name}". \
                                       format(number=i + 1, name=QtCore.QFileInfo(fname).fileName()), self)
                action.setData(fname)  #how the filename is sneaked to loadFile, to which we are not here passing filename
                action.triggered.connect(self.loadFile)  #connecting to slot to load file
                self.fileMenu.addAction(action)
        #Add separator, then the last menu action, Quit
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])
        
    def loadFile(self, fname=None):
        #Case 1: loadfile called by selection in file menu where fname was not passed
        if fname is None:
            action = self.sender()  
            if isinstance(action, QtGui.QAction):
                fname = action.data()  #retrieving data set in action.setData(fname) within updateFileMenu
                if not self.okToContinue():
                    return
            else:
                return
        #Case 2: called with filename passed (e.g., fileOpen or loadInitialFIle)
        if fname:
            self.filename = None #clearing current filename (not sure why)
            image = QtGui.QImage(fname) #loading new image
            #if null, didn't load correctly
            if image.isNull():
                message = "Failed to read {}".format(fname)
            else:
                self.addRecentFile(fname)
                self.image = QtGui.QImage()  #reset to null image 
                #reset and update everything (this way resetting
                #checkables will have no side-effects)
                for action, check in self.resettableActions:
                    action.setChecked(check)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("{} x {}".format(
                                       image.width(), image.height()))
                message = "Loaded {}".format(os.path.basename(fname))
            self.updateStatus(message)
       
    #When user indicates they want to quit, reimplement close event to
    #double check they want to close (okToContinue) and save settings
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QtCore.QSettings()
            settings.setValue("LastFile", self.filename)
            settings.setValue("RecentFiles", self.recentFiles or [])
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
            #no event.accept() needed?
        else:
            event.ignore()  #discard the close event and keep the app running
                
    #Save the currently open image
    def fileSave(self):
        if self.image.isNull():
            return True
        if self.filename is None:
            return self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.updateStatus("Saved as {}".format(self.filename))
                self.dirty = False
                return True
            else:
                self.updateStatus("Failed to save {}".format(
                                  self.filename))
                return False
       
    def fileSaveAs(self):
        if self.image.isNull():
            return True
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                for format in QtGui.QImageWriter.supportedImageFormats()])
        fname = QtGui.QFileDialog.getSaveFileName(self,
                "Image Changer - Save Image", fname,
                "Image files ({})".format(" ".join(formats)))[0]
        if fname:
            if "." not in fname:
                print type(fname)
                fname += ".png"  
            self.addRecentFile(fname)
            self.filename = fname
            return self.fileSave()
        return False         
                
    #add filename to recent file list
    #Called by fileSaveAs, loadFile, fileNew
    def addRecentFile(self, fname):
        if fname is None:
            return
        if fname not in self.recentFiles:
            self.recentFiles = [fname] + self.recentFiles[:8]
            
    def filePrint(self):
        if self.image.isNull():
            return
        if self.printer is None:
            self.printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            self.printer.setPageSize(QtGui.QPrinter.Letter)
        form = QtGui.QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)
           
    #invert colors
    #'on' is state of 'toggled' signal that was connected here
    def editInvert(self, on):
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.showImage()
        self.dirty = True
        self.updateStatus("Inverted" if on else "Uninverted")
        
    def editSwapRedAndBlue(self, on):
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()
        self.showImage()
        self.dirty = True
        self.updateStatus(("Swapped Red and Blue"
                           if on else "Unswapped Red and Blue"))
                           
    #valuechange of spinbox is connected to showImage                                            
    def editZoom(self):
        if self.image.isNull():
            return
        percent, ok = QtGui.QInputDialog.getInteger(self,
                "Image Changer - Zoom", "Percent:",
                self.zoomSpinBox.value(), 1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)

    #if it was mirrored, turn them both off
    def editUnMirror(self, on):
        if self.image.isNull():
            return
        if self.mirroredhorizontally:
            self.editMirrorHorizontal(False)
        if self.mirroredvertically:
            self.editMirrorVertical(False)

    #change state of horrizontal mirror
    def editMirrorHorizontal(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.showImage()
        self.mirroredhorizontally = not self.mirroredhorizontally
        self.dirty = True
        self.updateStatus(("Mirrored Horizontally"
                           if on else "Unmirrored Horizontally"))

    def editMirrorVertical(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.showImage()
        self.mirroredvertically = not self.mirroredvertically
        self.dirty = True
        self.updateStatus(("Mirrored Vertically"
                           if on else "Unmirrored Vertically"))
                           
    def helpAbout(self):
        QtGui.QMessageBox.about(self, "About Image Changer",
                """<b>Image Changer</b> v {0}
                <p>Copyright &copy; 2008-14 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to perform
                simple image manipulations.
                <p>Python {1} - Qt {2} - PySide {3} on {4}""".format(
                __version__, platform.python_version(),
                QtCore.qVersion(), PySide.__version__,
                platform.system()))

    def helpHelp(self):
        form = helpformPyside.HelpForm("index.html", self)
        form.show()
                                     
    @QtCore.Slot()
    def dumSlot(self):
        print "I am not really serving any purpose, just used for good-old fashioned debugging"
        
		
def main():
    app = QtGui.QApplication(sys.argv)
    #The following are values that PySide uses to load and save application
    #settings for use between sessions (for instance, in Windows in the registry,
    #it will save stored information in the folder'PySideSummer/Image Changer'
    #for settings to use next time.
    app.setOrganizationName("PySideSummer")
    app.setOrganizationDomain("https://github.com/EricThomson/PySideSummer")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__=="__main__":
    main()