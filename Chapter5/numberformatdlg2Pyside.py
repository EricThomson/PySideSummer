# coding: utf-8

'''
numberformatdlg2Pyside.py
Annotated PySide adaptation of numberformatdlg2.py from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

This is imported into numbersPyside.py
-------
Uses regular expressions for preventative validation (as opposed to postmortem)
Regular expresses are basically text patterns that can be used for search/pattern matching/etc. 
Introduction here:
  http://srinikom.github.io/pyside-docs/PySide/QtCore/QRegExp.html
QRegExpValidator is used to check a string against a regular expression:
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QRegExpValidator.html
On set validator: 
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QLineEdit.html#PySide.QtGui.PySide.QtGui.QLineEdit.setValidator
On input masks:
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QLineEdit.html#PySide.QtGui.PySide.QtGui.QLineEdit.inputMask
-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

'''

from PySide import QtGui, QtCore

class NumberFormatDlg(QtGui.QDialog):
    changed=QtCore.Signal()  #custom signal to emit when user pushes 'apply' button
    
    def __init__(self, format, parent=None):
        QtGui.QDialog.__init__(self, parent) 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  #close because not modal. WA="widget attribute" (QtCore.Qt.WidgetAttribute)

        #Thousands place marker 
        punctuationRe = QtCore.QRegExp(r"[ ,;:.]")  #'r' signifies regular expression
        thousandsLabel = QtGui.QLabel("&Thousands separator")
        self.thousandsEdit = QtGui.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QtGui.QRegExpValidator(punctuationRe, self))
        #Decimal marker
        decimalMarkerLabel = QtGui.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtGui.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(
                QtGui.QRegExpValidator(punctuationRe, self)) #QtGui.QRegExpValidator takes in character class, and parent.
        self.decimalMarkerEdit.setInputMask("X") #says that at least one character is required
        #Decimal places
        decimalPlacesLabel = QtGui.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtGui.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])
        #Negatives shown red checkbox
        self.redNegativesCheckBox = QtGui.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])
        #Dialog for apply/close buttons
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply | QtGui.QDialogButtonBox.Close)

        self.format = format  #instead of copying (as in case 1), we directly refer, so can change it directly

        grid = QtGui.QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        grid.addWidget(buttonBox, 4, 0, 1, 2)
        self.setLayout(grid)
        self.setWindowTitle("Set Number Format (Modeless)")
  
        #apply is not a built-in signal, so we connect that particular button to a custom apply slot
        #that emits the custom signal that the format has changed
        buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.apply)  #retreive reference to button
        buttonBox.rejected.connect(self.reject)  #because of WA_DeleteOnClose, reject closes, doesn't just hide


    def apply(self):
        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()
        if thousands == decimal:
            QtGui.QMessageBox.warning(self, "Format Error", unicode("The thousands separator and the decimal marker must be different."))
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        if len(decimal) == 0:
            QtGui.QMessageBox.warning(self, "Format Error", unicode("The decimal marker may not be empty."))
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = (
                self.decimalPlacesSpinBox.value())
        self.format["rednegatives"] = (
                self.redNegativesCheckBox.isChecked())
                
        self.changed.emit()  #was: self.emit(SIGNAL("changed"))  
