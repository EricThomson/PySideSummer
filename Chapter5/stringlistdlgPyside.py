# -*- coding: utf-8 -*-
"""
stringlistdlgPyside.py
One solution to the exercise in Chapter 5 of
Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

For fun I added buttons to let you sort in either ascending or descending order. 
Also, instead of making a list of strings to store and print the list, I just 
printed directly from the QListWidget using a custom method (printItemText). Note 
this is fairly different from Summerfield's solution, which you can  
find at his book web site. His is probably better. 
--------------
I am not annotating this, or other exercise solutions, as heavily. Part of the point 
is for people to figure these problems out for themselves. That said, the following 
documentation was helpful:
    http://srinikom.github.io/pyside-docs/PySide/QtGui/QListWidgetItem.html

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

"""

from PySide import QtGui, QtCore
import sys

class MyList(QtGui.QDialog):
    def __init__(self, categoryType, originalList, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.originalList=originalList
        self.category=categoryType
        self.initUI()

    def initUI(self):
        self.itemList=QtGui.QListWidget(self)
        self.itemList.addItems(self.originalList)
        self.itemList.setCurrentRow(0)
        
        #Close Window
        closeBut=QtGui.QPushButton("Close")
        closeBut.clicked.connect(self.closeDialog)  
        
        #add button
        addBut=QtGui.QPushButton("&Add an item")
        addBut.clicked.connect(self.addItem)
        
        #Edit button
        editBut=QtGui.QPushButton("&Edit selected item")
        editBut.clicked.connect(self.editItem)
        
        #Sort in ascending order
        sortAscBut=QtGui.QPushButton("&Sort Ascending")
        sortAscBut.clicked.connect(self.sortAsc)
        
        #Sort in descending order
        sortDescBut=QtGui.QPushButton("Sort &Descending")
        sortDescBut.clicked.connect(self.sortDesc)
        
        #Up
        upBut=QtGui.QPushButton("&Up")
        upBut.clicked.connect(self.moveUp)
        
        #Down
        downBut=QtGui.QPushButton("&Down")
        downBut.clicked.connect(self.moveDown)     
        #Remove button
        remBut=QtGui.QPushButton("&Remove selected item")
        remBut.clicked.connect(self.removeSelectedItem)
        
        #Set layout
        butLayout=QtGui.QVBoxLayout()
        butLayout.addWidget(addBut)
        butLayout.addWidget(editBut)
        butLayout.addWidget(remBut)
        butLayout.addWidget(sortAscBut)
        butLayout.addWidget(sortDescBut)
        butLayout.addWidget(upBut)
        butLayout.addWidget(downBut)
        butLayout.addWidget(closeBut)
        butLayout.addStretch()
        #whole layout
        layout=QtGui.QHBoxLayout()
        layout.addWidget(self.itemList)
        layout.addLayout(butLayout)
        #layout.addLayout(butLayout)
        self.setLayout(layout)
        self.setWindowTitle("Edit {0} list".format(self.category))        
              
    def printItemText(self):
        numItems=self.itemList.count()
        for row in range(numItems):
            print self.itemList.item(row).text()
        
    def swapRows(self, rowi, rowj):
        if rowi != rowj:
            rowiText=self.itemList.item(rowi).text()
            rowjText=self.itemList.item(rowj).text()
            #jtext into rowi
            self.itemList.item(rowi).setText(rowjText)
            #itext into row j
            self.itemList.item(rowj).setText(rowiText)
        else:
            print "Cannot switch a row with itself, silly"


    @QtCore.Slot()
    def addItem(self):
        text, ok=QtGui.QInputDialog.getText(self, unicode("Add item"),
                                            unicode("Enter another {0}".format(self.category)),
                                            QtGui.QLineEdit.Normal)
        if ok and text != '':
            self.itemList.addItem(unicode(text))

    @QtCore.Slot()
    def editItem(self):
        text, ok=QtGui.QInputDialog.getText(self, unicode("Edit item"),
                                    unicode("Edit the name:"),
                                    QtGui.QLineEdit.Normal)
        currentItem=self.itemList.currentItem()
        if ok and text != '':
            print "Changing: ", currentItem.text(), "-->", unicode(text)
            currentItem.setText(unicode(text))

    @QtCore.Slot()
    def removeSelectedItem(self):
        selectedRow=self.itemList.currentRow()
        item=self.itemList.takeItem(selectedRow)
        del item  #garbage collection?

    @QtCore.Slot()
    def sortAsc(self):
        self.itemList.sortItems(QtCore.Qt.AscendingOrder)

    @QtCore.Slot()
    def sortDesc(self):
        self.itemList.sortItems(QtCore.Qt.DescendingOrder)
 
    @QtCore.Slot()
    def moveUp(self):
        rowSelected=self.itemList.currentRow()
        if rowSelected == 0:
            print "You cannot move up from here"
        else:
            rowAbove=rowSelected-1
            self.swapRows(rowSelected, rowAbove)
            self.itemList.setCurrentRow(rowAbove)
            
    @QtCore.Slot()
    def moveDown(self):
        rowSelected=self.itemList.currentRow()
        if rowSelected == self.itemList.count()-1:
            print "You cannot move down from the bottom"
        else:
            rowBelow=rowSelected+1
            self.swapRows(rowSelected, rowBelow)
            self.itemList.setCurrentRow(rowBelow)
 
    #I frankly have little idea what the following is doing, as I never call it.
    def reject(self):
        self.accept()
        
    @QtCore.Slot()
    def closeDialog(self):
        closeReply=QtGui.QMessageBox.question(self, "Close dialog",
                                            "Are you sure you want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if closeReply == QtGui.QMessageBox.Yes:
            self.printItemText()
            QtGui.QDialog.accept(self)  #close it
        else:
            return  #return control to caller without closing

if __name__=="__main__":
    fruitList=["Banana", "Apple", "Crunchberry", "Leatherbulb", "Fig", "Sponge Orb", "Stinkberry"]
    qtApp=QtGui.QApplication(sys.argv)
    form=MyList("fruit", fruitList)
    form.exec_()