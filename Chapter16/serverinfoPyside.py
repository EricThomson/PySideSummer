# -*- coding: utf-8 -*-
"""
serverinfoPyside.py
Annotated PySide port of serverinfo.pyw from Chapter 16
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Needs treeoftable, servers.txt, and /flags folder with images

----
Notes on translation:
Fairly straightforward. But note separator different than '*' breaks it.

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import os
import sys
from PySide import QtGui, QtCore
import treeoftablePyside


class ServerModel(treeoftablePyside.TreeOfTableModel):

    def __init__(self, parent=None):
        super(ServerModel, self).__init__(parent)


    def data(self, index, role):
        #inherits from base, unless decoration role (add pixmap for that)
        if role == QtCore.Qt.DecorationRole:
            node = self.nodeFromIndex(index)
            if node is None:
                return None
            if isinstance(node, treeoftablePyside.BranchNode):
                if index.column() != 0:
                    return None
                filename = node.toString().replace(" ", "_")
                parent = node.parent.toString()
                if parent and parent != "USA":
                    return None
                if parent == "USA":
                    filename = "USA_" + filename
                filename = os.path.join(os.path.dirname(__file__),
                                        "flags", filename + ".png")
                #print filename
                pixmap = QtGui.QPixmap(filename)
                if pixmap.isNull():
                    return None
                return pixmap
        return treeoftablePyside.TreeOfTableModel.data(self, index, role)


class TreeOfTableWidget(QtGui.QTreeView):

    index_activated = QtCore.Signal(list)
    
    def __init__(self, filename, nesting, separator, parent=None):
        super(TreeOfTableWidget, self).__init__(parent)
        self.setSelectionBehavior(QtGui.QTreeView.SelectItems)
        self.setUniformRowHeights(True)
        model = ServerModel(self)
        self.setModel(model)
        try:
            model.load(filename, nesting, separator)
        except IOError as e:
            QtGui.QMessageBox.warning(self, "Server Info - Error", e)
        
        self.activated.connect(self.indexActivated)
        self.expanded.connect(self.treeExpanded)
        self.treeExpanded()


    def currentFields(self):
        #print "self model asrecord currentindex:" , self.model().asRecord(self.currentIndex())
        return self.model().asRecord(self.currentIndex())


    def indexActivated(self, index):
        self.index_activated.emit(self.model().asRecord(index))



    def treeExpanded(self):
        for column in range(self.model().columnCount(QtCore.QModelIndex())):
            self.resizeColumnToContents(column)



class MainForm(QtGui.QMainWindow):

    def __init__(self, filename, nesting, separator, parent=None):
        super(MainForm, self).__init__(parent)
        headers = ["Country/State (US)/City/Provider", "Server", "IP"]
        if nesting != 3:
            if nesting == 1:
                headers = ["Country/State (US)", "City", "Provider",
                           "Server"]
            elif nesting == 2:
                headers = ["Country/State (US)/City", "Provider",
                           "Server"]
            elif nesting == 4:
                headers = ["Country/State (US)/City/Provider/Server"]
            headers.append("IP")
        self.separator = separator #ET added
        self.treeWidget = TreeOfTableWidget(filename, nesting,
                                            self.separator)
        self.treeWidget.model().headers = headers
        self.setCentralWidget(self.treeWidget)

        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, self.close)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)

        self.treeWidget.index_activated.connect(self.activated)

        self.setWindowTitle("Server Info")
        self.statusBar().showMessage("Ready...", 5000)


    def picked(self): 
        return self.treeWidget.currentFields()


    def activated(self, fields):
        #print "activated fields: ", fields, type(fields) #"*".join(fields)
        try:
            self.statusBar().showMessage(self.separator.join(fields), 60000)  #ET replaced "*" with separator
        except TypeError as e:
            print "typeerror: ", e

app = QtGui.QApplication(sys.argv)
nesting = 3
if len(sys.argv) > 1:
    try:
        nesting = int(sys.argv[1])
    except:
        pass
    if nesting not in (1, 2, 3, 4):
        nesting = 3

dataFilename = os.path.join(os.path.dirname(__file__), "servers.txt")  #print dataFilename
separatorUsed = "*"  #this is separator usd in dataFilename: they have to match
form = MainForm(dataFilename, nesting, separatorUsed)
form.resize(750, 550)
form.show()
app.exec_()
#returns the one that was picked
print "*".join(form.picked())

