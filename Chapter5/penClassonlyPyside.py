# coding: utf-8
'''
penClassonlyPyside.py
Heavily annotated PySide adaptation of pen.pyw from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

This version leaves out the inline version, to focus more on the logic of
the class version, which is what Summerfield focuses on in the text. For
a less annotated translation of the full version, see penPyside.py

This illustrates use of a simple dumb modal dialog box that is used to set
a small number of properties.

Usage:
Run it, and change the properties of the pen: width, beveling, linestyle.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

'''
from PySide import QtGui, QtCore
import sys
       
class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        #default properties of pen
        self.width = 1
        self.beveled = False
        self.style = "Solid"

        #Create widgets
        #Push this button to initiate modal dialog
        buttonOpenDialog = QtGui.QPushButton("Set &Pen Properties", self) #&P: alt-P shortcut    
        #Label to display pen properties
        self.label = QtGui.QLabel("")
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.updateData() #show the default properties
                
        #lay out widgets vertically
        layout = QtGui.QVBoxLayout()
        layout.addWidget(buttonOpenDialog)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Start a dialog with me")     
        
        #Connect button to method that creates dialog
        buttonOpenDialog.clicked.connect(self.setPenProperties)  


    #shows data in label below button
    def updateData(self):
        bevel = ""
        if self.beveled:
            bevel = "Beveled"
        else:
            bevel="Not beveled"
        self.label.setText("Width = {}<br>Style = {}<br>{}".format(
                           self.width, self.style, bevel))

    def setPenProperties(self):
        dialog = PenPropertiesDlg(self)  #instance of pen property setter dialog is a child of Form
        #show extant property values
        dialog.widthSpinBox.setValue(self.width)
        dialog.beveledCheckBox.setChecked(self.beveled)
        dialog.styleComboBox.setCurrentIndex(
                dialog.styleComboBox.findText(self.style))
        #setting new property values based on user interaction
        if dialog.exec_():  #waits for dialog.exec_(), at which case it pulls the values
            self.width = dialog.widthSpinBox.value()
            self.beveled = dialog.beveledCheckBox.isChecked()
            self.style = dialog.styleComboBox.currentText()
            self.updateData() #show new values in label below button

'''
Create new PenPropertiesDlg class instance is invoked by Form, as a child of From.
QDialog is unique in that when it is instantiated as a child, it is immediately painted
on top of its parent. When its 'accept' or 'reject' slot is invoked, it closes and 
returns 1 or 0 to the parent, respectively. When accepted its exec_ method is invoked,
which involves going through and pulling values from all the widgets (see 
dialogExploreExec.py, included in Chapter 5 of PySideSummer repository, 
for a simple example of this).

From http://srinikom.github.io/pyside-docs/PySide/QtGui/QDialog.html
  A dialog is always a top-level widget, but if it has a parent, its default location 
  is centered on top of the parent’s top-level widget (if it is not top-level itself). 

  Typically, to get the dialog to close and return the appropriate value, we connect 
  a default button, e.g. OK , to the PySide.QtGui.QDialog.accept() slot and a Cancel 
  button to the PySide.QtGui.QDialog.reject() slot.
  
'''
class PenPropertiesDlg(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        #Set up widgets
        #Spinbox to set width
        widthLabel = QtGui.QLabel("&Width:")
        self.widthSpinBox = QtGui.QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)  #@W is set to put focus on WidthSpinbox
        self.widthSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)
        
        #Checkbox to set beveling
        self.beveledCheckBox = QtGui.QCheckBox("&Beveled edges")
        
        #Combobox to set style
        styleLabel = QtGui.QLabel("&Style:")
        self.styleComboBox = QtGui.QComboBox()
        styleLabel.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                     "DashDotted", "DashDotDotted"])
        #Buttons to accept or reject Dialog contents
        okButton = QtGui.QPushButton("&OK")
        cancelButton = QtGui.QPushButton("Cancel")

        #Set layout
        #Buttons (note addstretch is sort of like adding an additional widget:
        #depending on when you add it, it has different effects)
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch() #pushes buttons to the right (adds blank space to left)
        buttonLayout.addWidget(okButton)
        #buttonLayout.addStretch() #pushes buttons to the side (adds blank space in middle)
        buttonLayout.addWidget(cancelButton)
        #buttonLayout.addStretch() #pushes buttons to the left (adds blank space to right)
 
        #Widgets (including buttons) lay out in grid
        layout = QtGui.QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2) #takes up 1 row, 2 columns
        layout.addLayout(buttonLayout, 2, 0, 1, 3) #takes up 1 row, 3 columns
        self.setLayout(layout)
        self.setWindowTitle("Pen Properties")

        #Connect buttons to slots
        #Note that accept() and reject() are built-in methods of the dialog
        #that give control back to the caller
        okButton.clicked.connect(self.accept) 
        cancelButton.clicked.connect(self.reject)
        
        
if __name__=="__main__":
    qtApp = QtGui.QApplication(sys.argv)
    form = Form()
    form.resize(200, 100)
    form.show()
    sys.exit(qtApp.exec_())

