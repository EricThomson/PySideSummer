# -*- coding: utf-8 -*-
"""
newsreaderPyside.py
Annotated PySide port of newsreader.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

See Figure 9.6 in Summerfield's book for a nice graph of the layout. 
Note also this has a cool way of setting up the toolbars/menus, different from those
in Chapters 6 and 8.

Note: see splitterPlay.py
in the working folder (not on GitHub) for basics of stretch factor.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtGui, QtCore
import resource_rc


__version__ = "1.0.0"


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        #As usual, make a collection of widgets. Then lay them out.
        self.groupsList = QtGui.QListWidget()
        self.messagesList = QtGui.QListWidget()
        self.messageView = QtGui.QTextBrowser()

        #right hand side widgets (vertical split)
        self.messageSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.messageSplitter.addWidget(self.messagesList)
        self.messageSplitter.addWidget(self.messageView)
        
        #Central widget is a splitter (horizontal)
        self.mainSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.mainSplitter.addWidget(self.groupsList)
        self.mainSplitter.addWidget(self.messageSplitter)
        self.setCentralWidget(self.mainSplitter)

        #QtGui.QSplitter.setStretchFactor(index, stretch)
        self.mainSplitter.setStretchFactor(0, 1) #left side smaller
        self.mainSplitter.setStretchFactor(1, 3) #right side larger
        self.messageSplitter.setStretchFactor(0, 1) #top smaller
        self.messageSplitter.setStretchFactor(1, 2) #bottom larger

        self.createMenusAndToolbars()

        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry",
                QtCore.QByteArray()))
        self.restoreState(settings.value("MainWindow/State",
                QtCore.QByteArray()))
        self.messageSplitter.restoreState(settings.value("MessageSplitter",
                QtCore.QByteArray()))
        self.mainSplitter.restoreState(settings.value("MainSplitter",
                QtCore.QByteArray()))

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        self.setWindowTitle("News Reader")
        self.generateFakeData()

    #this is a really nice way to adding menus/toolbars
    def createMenusAndToolbars(self):
        #File menus/toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        fileMenu = self.menuBar().addMenu("&File")
        for icon, text in (("new", "&New..."), ("open", "&Open..."),
                ("save", "&Save"), ("save", "Save &As..."),
                (None, None), ("quit", "&Quit")):
            if icon is None:
                fileMenu.addSeparator()
            else:
                action = QtGui.QAction(QtGui.QIcon(":/file{}.png".format(icon)),
                                 text, self)
                if icon == "quit":
                    action.triggered.connect(self.close)
                elif text != "Save &As...":
                    fileToolbar.addAction(action)
                fileMenu.addAction(action)
        editMenu = self.menuBar().addMenu("&Edit")

        #Edit menus/toolbars
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        for icon, text in (("add", "&Add..."), ("edit", "&Edit..."),
                           ("delete", "&Remove")):
            action = QtGui.QAction(QtGui.QIcon(":/edit{}.png".format(icon)),
                             text, self)
            editToolbar.addAction(action)
            editMenu.addAction(action)


    def closeEvent(self, event):
        if self.okToContinue():
            settings = QtCore.QSettings()
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
            settings.setValue("MessageSplitter",
                    self.messageSplitter.saveState())
            settings.setValue("MainSplitter", self.mainSplitter.saveState())
        else:
            event.ignore()


    def okToContinue(self):
        return True

    
    def generateFakeData(self):
        for group in ("ada", "apl", "asm.*", "asm370", "awk", "basic.*",
                "beta", "c.*", "c++.*", "clarion", "clipper.*", "clos",
                "clu", "cobol", "dylan", "eiffel", "forth.*",
                "fortran.*", "functional", "haskell", "hermes", "icon",
                "idl", "idl-pvwave", "java.*", "javascript", "labview",
                "limbo", "lisp.*", "logo", "misc", "ml.*", "modula2",
                "modula3", "mumps", "oberon", "objective-c", "pascal.*",
                "perl.*", "php.*", "pl1", "pop", "postscript",
                "prograph", "prolog", "python.*", "rexx.*", "ruby",
                "sathe", "scheme.*", "sigplan", "smalltalk.*", "tcl.*",
                "verilog", "vhdl", "visual.*", "vrml"):
            self.groupsList.addItem("comp.lang.{}".format(group))
        for topic, author in (
                ("ANN: Einf\u00FChrung in die Programmierung mit Python",
                 "Ian Ozsvald",),
                ("SQLObject 0.7.3", "Oleg Broytmann",),
                ("ANN: Pyrex 0.9.5.1", "greg",),
                ("ANN: gozerbot IRC and JABBER bot", "bthate",),
                ("Extended deadline: CfP IEEE Software Special Issue on "
                 "Rapid Application Development with Dynamically Typed "
                 "Languages", "Laurence Tratt",),
                ("ANN: New python software community website in Chinese, "
                 "PythonNet.com", "Wenshan Du",),
                ("ANN: Plex 1.1.5 (Repost)", "greg",),
                ("ANN: Pyrex 0.9.5", "greg",),
                ("ftputil 2.2.1", "Stefan Schwarzer",),
                ("FlightFeather Social Networking Platform 0.3.1",
                 "George Belotsky",),
                ("OSCON 2007 Call for Participation Ends Soon",
                 "Kevin Altis",),
                ("ANN: tl.googlepagerank", "Thomas Lotze",),
                ("Dejavu 1.5.0RC1", "Robert Brewer",),
                ("PyCon: one week left for hotel registration",
                 "A.M. Kuchling",),
                ("FlightFeather Social Networking Platform 0.3.0",
                "George Belotsky",),
                ("SQLObject 0.8.0b2", "Oleg Broytmann",),
                ("SQLObject 0.7.3b1", "Oleg Broytmann",),
                ("ANN: Updated TkTreectrl wrapper module", "klappnase",),
                ("PyPy Trillke Sprints Feb/March 2007", "holger krekel",),
                ("wxPython 2.8.1.1", "Robin Dunn",),
                ("Movable Python 2.0.0 Final Available", "Fuzzyman",),
                ("ANN: Phebe 0.1.1", "Thomas Lotze",),
                ("Exception #03. Python seminar in Kiev city (Ukraine).",
                 "Mkdir",),
                ("FlightFeather Social Networking Platform 0.2.8",
                "George Belotsky",),
                ("ANN: Python Installation", "Ian Ozsvald",),
                ("ANN: pyGame Basics", "Ian Ozsvald",),
                ("PythonTidy 1.10", "Chuck Rhode",),
                ("Shed Skin Optimizing Python-to-C++ Compiler 0.0.10",
                 "Mark Dufour",),
                ("ANN : Karrigell 2.3.3", "Pierre Quentel",),
                ("ANN: amplee 0.4.0", "Sylvain Hellegouarch")):
            self.messagesList.addItem("{} from {}".format(topic, author))
        self.messageView.setHtml("""<table bgcolor=yellow>
<tr><td>Groups:</td><td>comp.lang.python.announce</td></tr>
<tr><td>From:</td><td>"Fuzzyman" &lt;fuzzy...@gmail.com&gt;</td></tr>
<tr><td>Subject:</td><td><b>[ANN] Movable Python 2.0.0 Final
Available</b></td></tr>
</table>

<h3>Movable Python 2.0.0 Final</h3>
<p>
<a href="http://www.voidspace.org.uk/python/movpy/">
http://www.voidspace.org.uk/python/movpy/</a>
is now available.

<p>
The new binaries are available for download from the groups page :

<p>Movable Python Groups Page
<a href="http://voidspace.tradebit.com/groups.php">
http://voidspace.tradebit.com/groups.php</a>
<p>
Binaries are uploaded for Python 2.2.3, 2.3.5, 2.4.4, 2.5 and the
MegaPack
<a href="http://www.voidspace.org.uk/python/movpy/megapack.html">
http://www.voidspace.org.uk/python/movpy/megapack.html</a>.
<p>
There is also a fresh version of the free demo, based on Python 2.3.5:

<p>Movable Python Trial Version
<a href="http://voidspace.tradebit.com/files.php/7007">
http://voidspace.tradebit.com/files.php/7007</a>

<h3>What is Movable Python</h3>

<p>
<b><i>Movable Python</i></b> is a distribution of Python, for Windows,
that can run without being installed. It means you can carry a full
development environment round on a USB stick.

<p>
It is also useful for testing programs with a 'clean Python install',
and testing programs with multiple versions of Python.

<p>
The GUI program launcher makes it a useful programmers tool, including
features like :

<ul>
<li>Log the output of all Python scripts run
<li>Enable Psyco for all scripts
<li>Quick Launch buttons for commonly used programs
<li>Configure multiple interpreters for use from a single interface
</ul>
<p>
It comes with the Pythonwin IDE and works fine with other IDEs like
SPE
<a href="http://developer.berlios.de/projects/python/">
http://developer.berlios.de/projects/python/</a>.
<p>
Plus many other features and bundled libraries.""")


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("PySideSummer")
    app.setOrganizationDomain("https://github.com/EricThomson/PySideSummer")
    app.setApplicationName("News Reader")
    form = MainWindow()
    form.show()
    app.exec_()


