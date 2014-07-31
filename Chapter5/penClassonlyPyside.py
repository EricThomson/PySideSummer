# coding: utf-8
'''
penClassonlyPyside.py
Heavily annotated PySide adaptation of pen.pyw from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

This version leaves out the inline version, to focus more on the logic of
the class version, which is the one Summerfield focuses on in the text. For
a translation of the full version, see penPyside.py

Main goal: 
Illustrate use of a simple dumb modal dialog box that is used to set
a small number of properties.

Usage:
Run it, and change the properties of the pen: width, beveling, linestyle.

To do: annotate this, go back over once, re-annotate.
Go oaver ch4, make PySideSummer repository, upload to Git.

'''
from PySide import QtGui, QtCore
import sys
       
class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.width = 1
        self.beveled = False
        self.style = "Solid"

        #Create widgets
        penButton = QtGui.QPushButton("Set &Pen", self) 
        self.label = QtGui.QLabel("The Pen has not been set")
        self.label.setTextFormat(QtCore.Qt.RichText)
        #lay out widgets vertically
        layout = QtGui.QVBoxLayout()
        layout.addWidget(penButton)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Pen setting metadialog")      
        penButton.clicked.connect(self.setPenProperties)  
        self.updateData()


    def updateData(self):
        bevel = ""
        if self.beveled:
            bevel = "<br>Beveled"
        self.label.setText("Width = {}<br>Style = {}{}".format(
                           self.width, self.style, bevel))

    def setPenProperties(self):
        dialog = PenPropertiesDlg(self)
        dialog.widthSpinBox.setValue(self.width)
        dialog.beveledCheckBox.setChecked(self.beveled)
        dialog.styleComboBox.setCurrentIndex(
                dialog.styleComboBox.findText(self.style))
        if dialog.exec_():
            self.width = dialog.widthSpinBox.value()
            self.beveled = dialog.beveledCheckBox.isChecked()
            self.style = dialog.styleComboBox.currentText()
            self.updateData()


class PenPropertiesDlg(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        #Set up widgets
        widthLabel = QtGui.QLabel("&Width:")
        self.widthSpinBox = QtGui.QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)
        self.beveledCheckBox = QtGui.QCheckBox("&Beveled edges")
        styleLabel = QtGui.QLabel("&Style:")
        self.styleComboBox = QtGui.QComboBox()
        styleLabel.setBuddy(self.styleComboBox) #XXX
        self.styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                     "DashDotted", "DashDotDotted"])
        okButton = QtGui.QPushButton("&OK")
        cancelButton = QtGui.QPushButton("Cancel")

        #Set layout
        #Buttons
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch() #XXX
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        #Widgets (including buttons) lay out in grid
        layout = QtGui.QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2) #XXX (params 3 and 4)
        layout.addLayout(buttonLayout, 2, 0, 1, 3) 
        self.setLayout(layout)
        self.setWindowTitle("Pen Properties")

        #Connect buttons to slots
        #Note that accept() and reject() are built-in methods of the QDialog widget.
        okButton.clicked.connect(self.accept) 
        cancelButton.clicked.connect(self.reject)
        
if __name__=="__main__":
    qtApp = QtGui.QApplication(sys.argv)
    form = Form()
    form.resize(200, 100)
    form.show()
    sys.exit(qtApp.exec_())

