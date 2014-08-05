# coding: utf-8

'''
numberformatdlg3Pyside.py
Annotated PySide adaptation of numberformatdlg3.py from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

This is imported into numbersPyside.py

If you followed numbers 1 and 2, this one should seem relatively 
straightforward. The calling class (Form) passes a callback function
that allows for on-the-fly updating of the appearance of the table of numbers
we have been working with. We pay for this power with some loss
of modularity.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

'''

from PySide import QtGui, QtCore


class NumberFormatDlg(QtGui.QDialog):

    def __init__(self, format, callback, parent=None):
        QtGui.QDialog.__init__(self, parent)

        punctuationRe = QtCore.QRegExp(r"[ ,;:.]")
        thousandsLabel = QtGui.QLabel("&Thousands separator")
        self.thousandsEdit = QtGui.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QtGui.QRegExpValidator(
                punctuationRe, self))
        decimalMarkerLabel = QtGui.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtGui.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(QtGui.QRegExpValidator(
                punctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")
        
        decimalPlacesLabel = QtGui.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtGui.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])
        self.redNegativesCheckBox = QtGui.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        self.format = format
        self.callback = callback

        grid = QtGui.QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        self.setLayout(grid)
        self.setWindowTitle("Set Number Format (`Live')")

        #some of the following are probably custom signals
        self.thousandsEdit.textEdited.connect(self.checkAndFix)  #does textedited need [str]
        self.decimalMarkerEdit.textEdited.connect(self.checkAndFix)
        self.decimalPlacesSpinBox.valueChanged.connect(self.apply)
        self.redNegativesCheckBox.toggled.connect(self.apply)

    def checkAndFix(self):
        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()
        if thousands == decimal:
            self.thousandsEdit.clear()
            self.thousandsEdit.setFocus()
        if len(decimal) == 0:
            self.decimalMarkerEdit.setText(".")
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
        self.apply()


    def apply(self):
        self.format["thousandsseparator"] = self.thousandsEdit.text()
        self.format["decimalmarker"] = self.decimalMarkerEdit.text()
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        self.callback()


