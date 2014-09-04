# -*- coding: utf-8 -*-
"""
draganddropPyside.py
Annotated PySide port of draganddrop.pyw from Chapter 10
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Shows how easy it is to do basic drag and drop basically setting .setAcceptDrops
if you want dragged items to be able to be planted there, and .setDragEnabled to 
True when you want to drag items from a widget.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import os
import sys
from PySide import QtGui, QtCore

class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.create_widgets()
        self.layout_widgets()
        self.setWindowTitle("Drag and Drop")


    def create_widgets(self):
        #listWidget on left
        self.listWidget = QtGui.QListWidget()
        self.listWidget.setAcceptDrops(True)
        #self.listWidget.setDragEnabled(True)
        path = os.path.dirname(__file__)
        print path, "\n\n", os.listdir(path)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QtGui.QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QtGui.QIcon(os.path.join(path,
                                   "images/{0}".format(image))))
                self.listWidget.addItem(item)
                
        #large icon listwidget middle
        self.iconListWidget = QtGui.QListWidget()
        self.iconListWidget.setAcceptDrops(True)
        self.iconListWidget.setDragEnabled(True)
        #notice for this you have to set iconmode on
        self.iconListWidget.setViewMode(QtGui.QListWidget.IconMode)
        
        #Table widget right
        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Column #1",
                "Column #2"])
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.setDragEnabled(True)

    #note unlike main window, don't have central widget, so we 
    #set layout in qwidget to show properly
    def layout_widgets(self):
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.listWidget)
        splitter.addWidget(self.iconListWidget)
        splitter.addWidget(self.tableWidget)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
