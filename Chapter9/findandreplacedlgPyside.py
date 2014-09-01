# -*- coding: utf-8 -*-
"""
findandreplacedlgPyside.py
Annotated PySide port of findandreplacedlg.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

To expand an extant widget, use a QFrame that is set to hidden until a button
is pushed, and make sure its size policy is set to fixed size so when you show it, 
the widget will expand and show it.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import sys
from PySide import QtGui, QtCore


class FindAndReplaceDlg(QtGui.QDialog):

    #Define signals (is this right?)
    find=QtCore.Signal(str, bool, bool, bool, bool, bool)
    replace = QtCore.Signal(str, str, bool, bool, bool, bool, bool)

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Find and Replace")
        
        #A: First define the collection of widgets
        findLabel = QtGui.QLabel("Find &what:")
        self.findLineEdit = QtGui.QLineEdit()
        findLabel.setBuddy(self.findLineEdit)
        
        replaceLabel = QtGui.QLabel("Replace w&ith:")
        self.replaceLineEdit = QtGui.QLineEdit()
        replaceLabel.setBuddy(self.replaceLineEdit)
        
        self.caseCheckBox = QtGui.QCheckBox("&Case sensitive")
        self.wholeCheckBox = QtGui.QCheckBox("Wh&ole words")
        self.wholeCheckBox.setChecked(True)
        
        #The 'more' frame bits
        #The frame that will appear/disappear when 'more' is toggled
        moreFrame = QtGui.QFrame()
        moreFrame.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.backwardsCheckBox = QtGui.QCheckBox("Search &Backwards")
        self.regexCheckBox = QtGui.QCheckBox("Regular E&xpression")
        self.ignoreNotesCheckBox = QtGui.QCheckBox("Ignore foot&notes "
                                                   "and endnotes")
                                          
        #vertical line and RHS push buttons                                          
        line = QtGui.QFrame()
        line.setFrameStyle(QtGui.QFrame.VLine|QtGui.QFrame.Sunken)
        self.findButton = QtGui.QPushButton("&Find")
        self.replaceButton = QtGui.QPushButton("&Replace")
        closeButton = QtGui.QPushButton("Close")
        moreButton = QtGui.QPushButton("&More")
        moreButton.setCheckable(True)

        self.findButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.replaceButton.setFocusPolicy(QtCore.Qt.NoFocus)
        #Not sure why the following are needed
        closeButton.setFocusPolicy(QtCore.Qt.NoFocus)  #?
        moreButton.setFocusPolicy(QtCore.Qt.NoFocus)  #?


        #B: Second, lay out the collection of widgets
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(findLabel, 0, 0)
        gridLayout.addWidget(self.findLineEdit, 0, 1)
        gridLayout.addWidget(replaceLabel, 1, 0)
        gridLayout.addWidget(self.replaceLineEdit, 1, 1)
        frameLayout = QtGui.QVBoxLayout()
        frameLayout.addWidget(self.backwardsCheckBox)
        frameLayout.addWidget(self.regexCheckBox)
        frameLayout.addWidget(self.ignoreNotesCheckBox)
        moreFrame.setLayout(frameLayout)
        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addLayout(gridLayout)
        leftLayout.addWidget(self.caseCheckBox)
        leftLayout.addWidget(self.wholeCheckBox)
        leftLayout.addWidget(moreFrame)
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(self.findButton)
        buttonLayout.addWidget(self.replaceButton)
        buttonLayout.addWidget(closeButton)
        buttonLayout.addWidget(moreButton)
        buttonLayout.addStretch()
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(line)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)


        moreFrame.hide()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        #setVisible is a built-in function--this clever trick feeds
        #the toggled bool output to the setVisible(bool) built-in
        moreButton.toggled.connect(moreFrame.setVisible)  
        self.findLineEdit.textEdited.connect(self.updateUi)
        self.findButton.clicked.connect(self.findClicked)
        self.replaceButton.clicked.connect(self.replaceClicked)

        self.updateUi()



    def updateUi(self):
        enable = bool(self.findLineEdit.text())
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
  

    #Slots for replace/find clicks: populates values of all the toggles
    @QtCore.Slot()
    def findClicked(self):
        self.find.emit(self.findLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),
                self.ignoreNotesCheckBox.isChecked())
                       
    @QtCore.Slot()
    def replaceClicked(self):
        self.replace.emit(self.findLineEdit.text(),
                self.replaceLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),
                self.ignoreNotesCheckBox.isChecked())
        

if __name__ == "__main__":

    def findSlot(what, *args):
        print("Find {} {}".format(what, [x for x in args]))

    def replaceSlot(old, new, *args):
        print("Replace {} with {} {}".format(
              old, new, [x for x in args]))
    app = QtGui.QApplication(sys.argv)
    form = FindAndReplaceDlg()
    form.find.connect(findSlot)
    form.replace.connect(replaceSlot)
    form.show()
    app.exec_()

