# coding: utf-8
'''
numberformatdlg1Pyside.py
Annotated PySide adaptation of numberformatdlg1.py from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

Instantiated within numbersPyside.py: modal dialog to set format of numbers
displayed in table. If formatting is set incorrectly, a warning message
pops up.

This is imported into numbersPyside.py
-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

'''

from PySide import QtGui, QtCore

class NumberFormatDlg(QtGui.QDialog):

    def __init__(self, format, parent=None): 
        QtGui.QDialog.__init__(self, parent)  
        #set up and initialize formatting widgets
        #Thousandths place marker
        thousandsLabel = QtGui.QLabel("&Thousands separator")
        self.thousandsEdit = QtGui.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        #Decimal marker
        decimalMarkerLabel = QtGui.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtGui.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        #Decimal places
        decimalPlacesLabel = QtGui.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtGui.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])
        #Show negative numbers as red
        self.redNegativesCheckBox = QtGui.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        #Buttons to accept or reject (OK and Cancel buttons automatically
        #emit accepted/rejected signals) (See pages 145, 149ff)
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept) #accepted goes with OK automatically
        buttonBox.rejected.connect(self.reject) #rejected goes with cancel automatically
        

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
        self.setWindowTitle("Set Number Format (Modal)")
        
        self.format = format.copy()  #copy so you don't change it directly


    #for parent class to pull values
    def numberFormat(self):
        return self.format

    #Reimplement accept slot to perform postmortem validation of entries
    def accept(self):
        class ThousandsError(Exception): pass
        class DecimalError(Exception): pass
        Punctuation = frozenset(" ,;:.")

        thousands = unicode(self.thousandsEdit.text())
        decimal = unicode(self.decimalMarkerEdit.text())
        try:
            if len(decimal) == 0:
                raise DecimalError("The decimal marker may not be "
                                   "empty.")
            if len(thousands) > 1:
                raise ThousandsError("The thousands separator may "
                                     "only be empty or one character.")
            if len(decimal) > 1:
                raise DecimalError("The decimal marker must be "
                                   "one character.")
            if thousands == decimal:
                raise ThousandsError("The thousands separator and "
                              "the decimal marker must be different.")
            if thousands and thousands not in Punctuation:
                raise ThousandsError("The thousands separator must "
                                     "be a punctuation symbol.")
            if decimal not in Punctuation:
                raise DecimalError("The decimal marker must be a "
                                   "punctuation symbol.")
        except ThousandsError as e:
            #warning dialog takes in parent, title, message
            #If no other inputs, just puts an 'OK' button
            QtGui.QMessageBox.warning(self, "Thousands Separator Error", unicode(e))
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return  #returns control to caller
        except DecimalError as e:
            QtGui.QMessageBox.warning(self, "Decimal Marker Error", unicode(e))
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return  #returns control to caller

        #If no errors, reset values of the formatting, and accept
        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = (
                self.decimalPlacesSpinBox.value())
        self.format["rednegatives"] = (
                self.redNegativesCheckBox.isChecked())
        QtGui.QDialog.accept(self)  #tells parent with self as child to accept this?
        
