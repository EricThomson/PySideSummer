from PySide import QtGui, QtCore

class NumberFormatDlg(QtGui.QDialog):

    def __init__(self, format, parent=None):  #XXX Format?
        QtGui.QDialog.__init__(self, parent)  #XXX Format?

        thousandsLabel = QtGui.QLabel("&Thousands separator")
        self.thousandsEdit = QtGui.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        decimalMarkerLabel = QtGui.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtGui.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        decimalPlacesLabel = QtGui.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtGui.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])
        self.redNegativesCheckBox = QtGui.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)

        self.format = format.copy()

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
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)




    def accept(self):
        class ThousandsError(Exception): pass
        class DecimalError(Exception): pass
        Punctuation = frozenset(" ,;:.")

        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()
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
            QtGui.QMessageBox.warning(self, "Thousands Separator Error", e)
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        except DecimalError as e:
            #Note if you enter decimal that is math symbol get warning
            QtGui.QMessageBox.warning(self, "Decimal Marker Error", e)
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = (
                self.decimalPlacesSpinBox.value())
        self.format["rednegatives"] = (
                self.redNegativesCheckBox.isChecked())
        QtGui.QDialog.accept(self)


    def numberFormat(self):
        return self.format


