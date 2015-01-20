# -*- coding: utf-8 -*-
"""
ships-delegatePyside.py
Annotated PySide port of ships-delegate.pyw from Chapter 14
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

To do: 
This is not formatting properly. His 2.7 does, but this is modified from his Python 3, 
so need to figure out what's going on.

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
from __future__ import unicode_literals  #ET

import sys
from PySide import QtGui, QtCore
import shipsPyside

MAC = True
try:
    from PyQt4.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

        

class MainForm(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.model = shipsPyside.ShipTableModel("ships.dat")
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setWindowTitle("Ships (delegate)")
        QtCore.QTimer.singleShot(0, self.initialLoad)


    def create_widgets(self):
        self.tableLabel1 = QtGui.QLabel("Table &1")
        self.tableView1 = QtGui.QTableView()
        self.tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)
        self.tableView1.setItemDelegate(shipsPyside.ShipDelegate(self))
        self.tableLabel2 = QtGui.QLabel("Table &2")
        self.tableView2 = QtGui.QTableView()
        self.tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)
        self.tableView2.setItemDelegate(shipsPyside.ShipDelegate(self))

        self.addShipButton = QtGui.QPushButton("&Add Ship")
        self.removeShipButton = QtGui.QPushButton("&Remove Ship")
        self.quitButton = QtGui.QPushButton("&Quit")
        if not MAC:
            self.addShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.removeShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.quitButton.setFocusPolicy(QtCore.Qt.NoFocus)


    def layout_widgets(self):
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.addShipButton)
        buttonLayout.addWidget(self.removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.quitButton)
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)


    def create_connections(self):
        for tableView in (self.tableView1, self.tableView2):
            header = tableView.horizontalHeader()
            header.sectionClicked.connect(self.sortTable)
        self.addShipButton.clicked.connect(self.addShip)
        self.removeShipButton.clicked.connect(self.removeShip)
        self.quitButton.clicked.connect(self.accept)


    def initialLoad(self):
        if not QtCore.QFile.exists(self.model.filename):
            for ship in shipsPyside.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(unicode(ship.owner))
                self.model.countries.add(unicode(ship.country))
            self.model.reset()
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError, err:
                QtGui.QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {0}".format(err))
        self.model.sortByName()
        self.resizeColumns()


    def resizeColumns(self):
        self.tableView1.resizeColumnsToContents()
        self.tableView2.resizeColumnsToContents()


    def reject(self):
        self.accept()


    def accept(self):
        if (self.model.dirty and
            QtGui.QMessageBox.question(self, "Ships - Save?",
                    "Save unsaved changes?",
                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                    QtGui.QMessageBox.Yes):
            try:
                self.model.save()
            except IOError, err:
                QtGui.QMessageBox.warning(self, "Ships - Error",
                        "Failed to save: {0}".format(err))
        QtGui.QDialog.accept(self)

    
    def sortTable(self, section):
        if section in (shipsPyside.OWNER, shipsPyside.COUNTRY):
            self.model.sortByCountryOwner()
        else:
            self.model.sortByName()
        self.resizeColumns()


    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRows(row)
        index = self.model.index(row, 0)
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        tableView.setFocus()
        tableView.setCurrentIndex(index)
        tableView.edit(index)


    def removeShip(self):
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        index = tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(
                    self.model.index(row, shipsPyside.NAME)).toString()
        owner = self.model.data(
                    self.model.index(row, shipsPyside.OWNER)).toString()
        country = self.model.data(
                    self.model.index(row, shipsPyside.COUNTRY)).toString()
        if (QtGui.QMessageBox.question(self, "Ships - Remove", 
                "Remove {} of {}/{}?".format(name, owner, country),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.No):
            return
        self.model.removeRows(row)
        self.resizeColumns()
        

        
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()
