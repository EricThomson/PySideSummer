# -*- coding: utf-8 -*-
"""
ships-dictPyside.py
Annotated PySide port of ships-dict.pyw from Chapter 14
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Calls shipPyside.py

Notes on program:
Shows how to use convienience item widgets.

Creates three convenience item view widgets (e.g., QTreeWidget).
These are views with default models and delegates aggregated inside them
Give less control than pure view widgets (see ships-modelPyside) such as
QTreeiew that let you determine the model (e.g., QStringListModel), but 
still use a default delegate (which controls how items are painted and
edited). In ships-delegatePyside.py, we will create custom delegates that
give much finer control (e.g., letting you put a combobox in a table instead
of just text).

Shows the three views side by side (splitter layout), and in the tab view you
can sort the ships by different criteria. Adding/removing shiops updates all
three views simultaneously.

Some default behavior (from documentation online):
QListWidget
By default, items are enabled, selectable, checkable, and can be 
the source of drag and drop operations. Each item’s flags can be changed 
by calling PySide.QtGui.QListWidgetItem.setFlags() with the appropriate 
value (see Qt.ItemFlags ). Checkable items can be checked, unchecked and 
partially checked with the PySide.QtGui.QListWidgetItem.setCheckState() function. 
The corresponding PySide.QtGui.QListWidgetItem.checkState() function indicates 
the item’s current check state.

QTableWidget
By default, items are enabled, editable, selectable, checkable, 
and can be used both as the source of a drag and drop operation 
and as a drop target. Each item’s flags can be changed by calling 
PySide.QtGui.QTableWidgetItem.setFlags() with the appropriate value 
(see Qt.ItemFlags ). Checkable items can be checked and unchecked 
with the PySide.QtGui.QTableWidgetItem.setCheckState() function. 
The corresponding PySide.QtGui.QTableWidgetItem.checkState() function 
indicates whether the item is currently checked.

QTreeWidget
By default, items are enabled, selectable, checkable, and 
can be the source of a drag and drop operation. Each item’s 
flags can be changed by calling PySide.QtGui.QTreeWidgetItem.setFlags() 
with the appropriate value (see Qt.ItemFlags ). Checkable 
items can be checked and unchecked with the 
PySide.QtGui.QTreeWidgetItem.setCheckState() function. 
The corresponding PySide.QtGui.QTreeWidgetItem.checkState() function 
indicates whether the item is currently checked.


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
        QtGui.QDialog.__init__(self, parent)
        
        #Create convenience item view widgets
        #QListWidget
        listLabel = QtGui.QLabel("&List")
        self.listWidget = QtGui.QListWidget()
        listLabel.setBuddy(self.listWidget)
        
        #QTableWidget
        tableLabel = QtGui.QLabel("&Table")
        self.tableWidget = QtGui.QTableWidget()
        tableLabel.setBuddy(self.tableWidget)
        
        #QTreeWidget
        treeLabel = QtGui.QLabel("Tre&e")
        self.treeWidget = QtGui.QTreeWidget()
        treeLabel.setBuddy(self.treeWidget)
        
        #Add buttons for UI
        addShipButton = QtGui.QPushButton("&Add Ship")
        removeShipButton = QtGui.QPushButton("&Remove Ship")
        quitButton = QtGui.QPushButton("&Quit")
        #On 'nofocus, see page 218 of book: basically MACS are a pain
        if not MAC:
            addShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            removeShipButton.setFocusPolicy(QtCore.Qt.NoFocus)
            quitButton.setFocusPolicy(QtCore.Qt.NoFocus)

        #Lay out widgets and buttons
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        #List
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(listLabel)
        vbox.addWidget(self.listWidget)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        
        #Table
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tableLabel)
        vbox.addWidget(self.tableWidget)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        
        #Tree
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(treeLabel)
        vbox.addWidget(self.treeWidget)
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        
        #Buttons
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        
        #Combine splitter and buttons into one layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        #Setting connections
        self.tableWidget.itemChanged.connect(self.tableItemChanged) #default of table is it is editable
        addShipButton.clicked.connect(self.addShip)
        removeShipButton.clicked.connect(self.removeShip)        
        quitButton.clicked.connect(self.accept)
 
         #self.ships is the dictionary containing all ships  (id is key, value is other data)
        self.ships = shipsPyside.ShipContainer("ships.dat") #
        self.setWindowTitle("Ships (dict)")
        QtCore.QTimer.singleShot(0, self.initialLoad) #see page 184 of text for why we do this single shot trick


    def initialLoad(self):
        if not QtCore.QFile.exists(self.ships.filename):
            for ship in shipsPyside.generateFakeShips():
                self.ships.addShip(ship)
            self.ships.dirty = False
        else:
            try:
                self.ships.load()
            except IOError as e:
                QtGui.QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {}".format(e))
        self.populateList()
        self.populateTable()
        self.tableWidget.sortItems(0)
        self.populateTree()


    def reject(self):
        self.accept()


    def accept(self):
        if (self.ships.dirty and
            QtGui.QMessageBox.question(self, "Ships - Save?",
                    "Save unsaved changes?",
                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                    QtGui.QMessageBox.Yes):
            try:
                self.ships.save()
            except IOError as e:
                QtGui.QMessageBox.warning(self, "Ships - Error",
                        "Failed to save: {}".format(e))
        QtGui.QDialog.accept(self)


    def populateList(self, selectedShip=None):
        selected = None
        self.listWidget.clear()
        for ship in self.ships.inOrder():
            item = QtGui.QListWidgetItem("{} of {}/{} ({:,})".format(
                     ship.name, ship.owner, ship.country, ship.teu))
            self.listWidget.addItem(item)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
        if selected is not None:
            selected.setSelected(True)
            self.listWidget.setCurrentItem(selected)

    #START HERE (user role)
    def populateTable(self, selectedShip=None):
        selected = None
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(self.ships))
        headers = ["Name", "Owner", "Country", "Description", "TEU"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        for row, ship in enumerate(self.ships):
            item = QtGui.QTableWidgetItem(ship.name)  #ship.name is set to text of item
            
            #User role is an itemdatarole (see page 231 where this is first introduced)
            #http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum
            #http://stackoverflow.com/questions/11485243/setting-and-getting-data-from-pyqt-widget-items
            #http://stackoverflow.com/a/7997524/1886357
            #user data            
            item.setData(QtCore.Qt.UserRole, int(id(ship)))  #set user data associated with item: ship id
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.tableWidget.setItem(row, shipsPyside.NAME, item) #NAME etc are integers
            self.tableWidget.setItem(row, shipsPyside.OWNER,
                    QtGui.QTableWidgetItem(ship.owner))
            self.tableWidget.setItem(row, shipsPyside.COUNTRY,
                    QtGui.QTableWidgetItem(ship.country))
            self.tableWidget.setItem(row, shipsPyside.DESCRIPTION,
                    QtGui.QTableWidgetItem(ship.description))
            item = QtGui.QTableWidgetItem("{:10}".format(ship.teu))
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(row, shipsPyside.TEU, item)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)  #note difference b/w selected and current
            self.tableWidget.setCurrentItem(selected)


    def populateTree(self, selectedShip=None):
        selected = None
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(["Country/Owner/Name", "TEU"])
        self.treeWidget.setItemsExpandable(True)
        parentFromCountry = {}
        parentFromCountryOwner = {}
        for ship in self.ships.inCountryOwnerOrder():
            #country is root node
            ancestor = parentFromCountry.get(ship.country)
            if ancestor is None:
                ancestor = QtGui.QTreeWidgetItem(self.treeWidget, [ship.country])
                parentFromCountry[ship.country] = ancestor  #dictionary entry
            countryowner = ship.country + "/" + ship.owner
            parent = parentFromCountryOwner.get(countryowner)
            if parent is None:
                parent = QtGui.QTreeWidgetItem(ancestor, [ship.owner])
                parentFromCountryOwner[countryowner] = parent
            item = QtGui.QTreeWidgetItem(parent, [ship.name, "{:,}".format(ship.teu)])
            item.setTextAlignment(1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            if selectedShip is not None and selectedShip == id(ship):
                selected = item
            self.treeWidget.expandItem(parent)
            self.treeWidget.expandItem(ancestor)
        self.treeWidget.resizeColumnToContents(0)
        self.treeWidget.resizeColumnToContents(1)
        if selected is not None:
            selected.setSelected(True)
            self.treeWidget.setCurrentItem(selected)


    def addShip(self):
        ship = shipsPyside.Ship(" Unknown", " Unknown", " Unknown")
        self.ships.addShip(ship)
        self.populateList()
        self.populateTree()
        self.populateTable(id(ship))
        self.tableWidget.setFocus()
        self.tableWidget.editItem(self.tableWidget.currentItem())


    def tableItemChanged(self, item):
        ship = self.currentTableShip()
        if ship is None:
            return
        column = self.tableWidget.currentColumn()
        if column == shipsPyside.NAME:
            ship.name = item.text().strip()
        elif column == shipsPyside.OWNER:
            ship.owner = item.text().strip()
        elif column == shipsPyside.COUNTRY:
            ship.country = item.text().strip()
        elif column == shipsPyside.DESCRIPTION:
            ship.description = item.text().strip()
        elif column == shipsPyside.TEU:
            ship.teu = int(item.text())
        self.ships.dirty = True
        self.populateList()
        self.populateTree()


    def currentTableShip(self):
        item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if item is None:
            return None
        return self.ships.ship(int(item.data(QtCore.Qt.UserRole)))
        

    def removeShip(self):
        ship = self.currentTableShip()
        if ship is None:
            return
        if (QtGui.QMessageBox.question(self, "Ships - Remove", 
                "Remove {} of {}/{}?".format(ship.name, ship.owner, ship.country),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.No):
            return
        self.ships.removeShip(ship)
        self.populateList()
        self.populateTree()
        self.populateTable()


app = QtGui.QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()

