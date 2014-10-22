# -*- coding: utf-8 -*-
"""
ships-modelPyside.py
Annotated PySide port of ships-model.pyw from Chapter 14
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

called by ships-modelPyside.py

Different degrees of customizability, with concomitant responsibilities:

General subclassing:
    When subclassing QtCore.QAbstractTableModel, you must implement 
    QtCore.QAbstractItemModel.rowCount(), QtCore.QAbstractItemModel.columnCount(), 
    and QtCore.QAbstractItemModel.data(). Most models will 
    also implement QtCore.QAbstractItemModel.headerData(). 
    
    Default implementations of the 
    QtCore.QAbstractTableModel.index() and QtCore.QAbstractTableModel.parent() 
    functions are provided by QtCore.QAbstractTableModel. 

Sortable model:
    Unlike the convenience classes, you have to handle sorting yourself (add a slot connected
    to click of header).
    
Editable model:
    Editable models need to implement QtCore.QAbstractItemModel.setData(), and 
    implement QtCore.QAbstractItemModel.flags() to return a value containing Qt.ItemIsEditable.

Resizable model:
    Models that provide interfaces to resizable data structures should provide implementations 
    of QtCore.QAbstractItemModel.insertRows(), QtCore.QAbstractItemModel.removeRows(), 
    QtCore.QAbstractItemModel.insertColumns(), and QtCore.QAbstractItemModel.removeColumns(). 
    And note you ahve the whole 'beginInsertRows' and 'endInsertRows' needed to make sure
    multiple views of the same model will update appropriately.

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
from __future__ import unicode_literals  #ET

import sys
from PySide import QtGui, QtCore
import shipsPyside

MAC = "qt_mac_set_native_menubar" in dir()


class MainForm(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = shipsPyside.ShipTableModel("ships.dat")  #in shipsPyside
        
        tableLabel1 = QtGui.QLabel("Table &1")
        self.tableView1 = QtGui.QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)
        
        tableLabel2 = QtGui.QLabel("Table &2")
        self.tableView2 = QtGui.QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)

        addShipButton = QtGui.QPushButton("&Add Ship")
        removeShipButton = QtGui.QPushButton("&Remove Ship")
        quitButton = QtGui.QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            removeShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            quitButton.setFocusPolicy(QtCore.Qt.NoFocus)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        for tableView in (self.tableView1, self.tableView2):
            header = tableView.horizontalHeader()
            header.sectionClicked.connect(self.sortTable)
        addShipButton.clicked.connect(self.addShip)
        removeShipButton.clicked.connect(self.removeShip)
        quitButton.clicked.connect(self.accept)

        self.setWindowTitle("Ships (model)")
        QtCore.QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        if not QtCore.QFile.exists(self.model.filename):
            for ship in shipsPyside.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(ship.owner)
                self.model.countries.add(ship.country)
            self.model.reset()
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError as e:
                QtGui.QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {}".format(e))
        self.model.sortByName()
        self.resizeColumns()


    def resizeColumns(self):
        for tableView in (self.tableView1, self.tableView2):
            for column in (shipsPyside.NAME, shipsPyside.OWNER, shipsPyside.COUNTRY,
                           shipsPyside.TEU):
                tableView.resizeColumnToContents(column)


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
            except IOError as e:
                QtGui.QMessageBox.warning(self, "Ships - Error",
                        "Failed to save: {}".format(e))
        QtGui.QDialog.accept(self)

    
    def sortTable(self, section):
        if section in (shipsPyside.OWNER, shipsPyside.COUNTRY):
            self.model.sortByCountryOwner()
        else:
            self.model.sortByName()
        self.resizeColumns()


    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
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
                    self.model.index(row, shipsPyside.NAME))
        owner = self.model.data(
                    self.model.index(row, shipsPyside.OWNER))
        country = self.model.data(
                    self.model.index(row, shipsPyside.COUNTRY))
        if (QtGui.QMessageBox.question(self, "Ships - Remove", 
                "Remove {} of {}/{}?".format(name, owner, country),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.No):
            return
        self.model.removeRow(row)
        self.resizeColumns()


app = QtGui.QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()

