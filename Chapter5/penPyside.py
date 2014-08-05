# coding: utf-8
'''
penPyside.py
Lightly annotated PySide adaptation of pen.pyw from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Shows use of a dumb widget both inline and as a separate class. See 
penClassonlyPyside.py for the class version, with more annotations.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

'''
from PySide import QtGui, QtCore
import sys

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
        
class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.width = 1
        self.beveled = False
        self.style = "Solid"

        #Create widgets
        penButtonInline = QtGui.QPushButton("Set Pen... (Dumb &inline)") 
        penButton = QtGui.QPushButton("Set Pen... (Dumb &class)") #XXX
        self.label = QtGui.QLabel("The Pen has not been set")
        self.label.setTextFormat(QtCore.Qt.RichText)
        #lay out widgets vertically
        layout = QtGui.QVBoxLayout()
        layout.addWidget(penButtonInline)
        layout.addWidget(penButton)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Pen")
        
        penButtonInline.clicked.connect(self.setPenInline) 
        penButton.clicked.connect(self.setPenProperties)  

        self.updateData()


    def updateData(self):
        bevel = ""
        if self.beveled:
            bevel = "<br>Beveled"
        self.label.setText("Width = {}<br>Style = {}{}".format(
                           self.width, self.style, bevel))


    def setPenInline(self):
        widthLabel = QtGui.QLabel("&Width:")
        widthSpinBox = QtGui.QSpinBox()
        widthLabel.setBuddy(widthSpinBox)
        widthSpinBox.setAlignment(QtCore.Qt.AlignRight)
        widthSpinBox.setRange(0, 24)
        widthSpinBox.setValue(self.width)
        beveledCheckBox = QtGui.QCheckBox("&Beveled edges")
        beveledCheckBox.setChecked(self.beveled)
        styleLabel = QtGui.QLabel("&Style:")
        styleComboBox = QtGui.QComboBox()
        styleLabel.setBuddy(styleComboBox)#XXX buddy?
        styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                "DashDotted", "DashDotDotted"])
        styleComboBox.setCurrentIndex(styleComboBox.findText(self.style))
        okButton = QtGui.QPushButton("&OK")
        cancelButton = QtGui.QPushButton("Cancel")

        #Lay out buttons in a row
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        #Set overall layout as grid (inc buttons)
        layout = QtGui.QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(widthSpinBox, 0, 1)
        layout.addWidget(beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(styleComboBox, 1, 1, 1, 2)
        layout.addLayout(buttonLayout, 2, 0, 1, 3)
        
        form = QtGui.QDialog() 
        form.setLayout(layout)
        form.setWindowTitle("Pen Properties")
        
        #connect buttons to slots
        okButton.clicked.connect(form.accept) 
        cancelButton.clicked.connect(form.reject)     

        if form.exec_(): 
            self.width = widthSpinBox.value()
            self.beveled = beveledCheckBox.isChecked()
            self.style = styleComboBox.currentText()
            self.updateData()


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



qtApp = QtGui.QApplication(sys.argv)
form = Form()
form.resize(200, 150)
form.show()
sys.exit(qtApp.exec_())

