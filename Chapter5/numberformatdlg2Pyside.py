from PySide import QtGui, QtCore

class NumberFormatDlg(QtGui.QDialog):
    changed=QtCore.Signal()
    
    def __init__(self, format, parent=None):
        QtGui.QDialog.__init__(self, parent)  #look at how this is called by me, originally he had it different
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  #XXX WHAT IS THIS? PySide.QtCore.Qt.WidgetAttribute

        punctuationRe = QtCore.QRegExp(r"[ ,;:.]")

        thousandsLabel = QtGui.QLabel("&Thousands separator")
        self.thousandsEdit = QtGui.QLineEdit(format["thousandsseparator"])
        thousandsLabel.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(
                QtGui.QRegExpValidator(punctuationRe, self))

        decimalMarkerLabel = QtGui.QLabel("Decimal &marker")
        self.decimalMarkerEdit = QtGui.QLineEdit(format["decimalmarker"])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(
                QtGui.QRegExpValidator(punctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimalPlacesLabel = QtGui.QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QtGui.QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])

        self.redNegativesCheckBox = QtGui.QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply|
                                     QtGui.QDialogButtonBox.Close)

        self.format = format

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
        
        buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.rejected.connect(self.reject)


    def apply(self):
        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()
        if thousands == decimal:
            QtGui.QMessageBox.warning(self, "Format Error",
                    "The thousands separator and the decimal marker "
                    "must be different.")
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        if len(decimal) == 0:
            QtGui.QMessageBox.warning(self, "Format Error",
                    "The decimal marker may not be empty.")
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = (
                self.decimalPlacesSpinBox.value())
        self.format["rednegatives"] = (
                self.redNegativesCheckBox.isChecked())
                
        self.changed.emit()  #self.emit(SIGNAL("changed"))  
#
#    rateChangedSig=QtCore.Signal(float)  #custom signal indicating tax rate
#            self.rateChangedSig.emit(self.rate)  #was s