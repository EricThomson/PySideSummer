# -*- coding: utf-8 -*-
"""
paymentdlgPyside.py
Annotated PySide adaptation of paymentdlg.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Shows tabs (for different payment types) within a dialog. Nice thing about 
QTabWidgets is when you click the program takes care of displaying the
different page: no extra work needed (compare to stack widget)
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtCore, QtGui

class PaymentDlg(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Payment Form")
        
        #Common information to all payment types
        #First name
        firstnameLabel = QtGui.QLabel("&First name:")
        self.firstnameLineEdit = QtGui.QLineEdit()
        firstnameLabel.setBuddy(self.firstnameLineEdit)
        #Last name
        lastnameLabel = QtGui.QLabel("&Last name:")
        self.lastnameLineEdit = QtGui.QLineEdit()
        lastnameLabel.setBuddy(self.lastnameLineEdit)
        #Invoice number
        invoiceLabel = QtGui.QLabel("&Invoice No.:")
        self.invoiceSpinBox = QtGui.QSpinBox()
        invoiceLabel.setBuddy(self.invoiceSpinBox)
        self.invoiceSpinBox.setRange(1, 10000000)
        self.invoiceSpinBox.setValue(100000)
        self.invoiceSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        #Amount due
        amountLabel = QtGui.QLabel("&Amount due:")
        self.amountSpinBox = QtGui.QDoubleSpinBox()
        amountLabel.setBuddy(self.amountSpinBox)
        self.amountSpinBox.setRange(0, 5000.0)
        self.amountSpinBox.setPrefix("$ ")
        self.amountSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        #Create individual widgets to be placed in different tabs
        #Cash
        self.paidCheckBox = QtGui.QCheckBox("&Paid")
        
        #Check
        #  Check number
        checkNumLabel = QtGui.QLabel("Check &No.:")
        self.checkNumLineEdit = QtGui.QLineEdit()
        checkNumLabel.setBuddy(self.checkNumLineEdit)
        #  Bank name
        bankLabel = QtGui.QLabel("&Bank:")
        self.bankLineEdit = QtGui.QLineEdit()
        bankLabel.setBuddy(self.bankLineEdit)
        #  Account number
        accountNumLabel = QtGui.QLabel("Acco&unt No.:")
        self.accountNumLineEdit = QtGui.QLineEdit()
        accountNumLabel.setBuddy(self.accountNumLineEdit)
        #  Sort code (this is a British thing)
        sortCodeLabel = QtGui.QLabel("Sort &Code:")
        self.sortCodeLineEdit = QtGui.QLineEdit()
        sortCodeLabel.setBuddy(self.sortCodeLineEdit)
        
        #Credit card
        #  CC number
        creditCardLabel = QtGui.QLabel("&Number:")
        self.creditCardLineEdit = QtGui.QLineEdit()
        creditCardLabel.setBuddy(self.creditCardLineEdit)
        #  CC valid start date
        validFromLabel = QtGui.QLabel("&Valid From:")
        self.validFromDateEdit = QtGui.QDateEdit()
        validFromLabel.setBuddy(self.validFromDateEdit)
        self.validFromDateEdit.setDisplayFormat("MMM yyyy")
        self.validFromDateEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        # CC expiration date        
        expiryLabel = QtGui.QLabel("E&xpiry Date:")
        self.expiryDateEdit = QtGui.QDateEdit()
        expiryLabel.setBuddy(self.expiryDateEdit)
        self.expiryDateEdit.setDisplayFormat("MMM yyyy")
        self.expiryDateEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                          QtGui.QDialogButtonBox.Cancel)

        #QTabWidget and related classes: see Chapter9/usefulStuff.md
        #Define tab widget
        tabWidget = QtGui.QTabWidget()
        #Define/add cash widget
        cashWidget = QtGui.QWidget()
        cashLayout = QtGui.QHBoxLayout()
        cashLayout.addWidget(self.paidCheckBox)
        cashWidget.setLayout(cashLayout)
        tabWidget.addTab(cashWidget, "Cas&h")
        #Define/add check widget
        checkWidget = QtGui.QWidget()
        checkLayout = QtGui.QGridLayout()
        checkLayout.addWidget(checkNumLabel, 0, 0)
        checkLayout.addWidget(self.checkNumLineEdit, 0, 1)
        checkLayout.addWidget(bankLabel, 0, 2)
        checkLayout.addWidget(self.bankLineEdit, 0, 3)
        checkLayout.addWidget(accountNumLabel, 1, 0)
        checkLayout.addWidget(self.accountNumLineEdit, 1, 1)
        checkLayout.addWidget(sortCodeLabel, 1, 2)
        checkLayout.addWidget(self.sortCodeLineEdit, 1, 3)
        checkWidget.setLayout(checkLayout)
        tabWidget.addTab(checkWidget, "Chec&k")
        #Define/add creditWidget
        creditWidget = QtGui.QWidget()
        creditLayout = QtGui.QGridLayout()
        creditLayout.addWidget(creditCardLabel, 0, 0)
        creditLayout.addWidget(self.creditCardLineEdit, 0, 1, 1, 3)
        creditLayout.addWidget(validFromLabel, 1, 0)
        creditLayout.addWidget(self.validFromDateEdit, 1, 1)
        creditLayout.addWidget(expiryLabel, 1, 2)
        creditLayout.addWidget(self.expiryDateEdit, 1, 3)
        creditWidget.setLayout(creditLayout)
        tabWidget.addTab(creditWidget, "Credit Car&d")
        #Layout common widgets (e.g., name etc)
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(firstnameLabel, 0, 0)
        gridLayout.addWidget(self.firstnameLineEdit, 0, 1)
        gridLayout.addWidget(lastnameLabel, 0, 2)
        gridLayout.addWidget(self.lastnameLineEdit, 0, 3)
        gridLayout.addWidget(invoiceLabel, 1, 0)
        gridLayout.addWidget(self.invoiceSpinBox, 1, 1)
        gridLayout.addWidget(amountLabel, 1, 2)
        gridLayout.addWidget(self.amountSpinBox, 1, 3)
        #Add common widgets, tabs, and buttonbox to main QDialog
        layout = QtGui.QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addWidget(tabWidget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        #Set up connections. Connect any edits to updateUi
        for lineEdit in (self.firstnameLineEdit, self.lastnameLineEdit,
                self.checkNumLineEdit, self.accountNumLineEdit,
                self.bankLineEdit, self.sortCodeLineEdit,
                self.creditCardLineEdit):
            lineEdit.textEdited.connect(self.updateUi)
        for dateEdit in (self.validFromDateEdit, self.expiryDateEdit):
            dateEdit.dateChanged.connect(self.updateUi)
        self.paidCheckBox.clicked.connect(self.updateUi)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.updateUi()  #enables OK pushbutton if certain criteria met


    #Enable OK button if valid data is in 
    def updateUi(self):
        today = QtCore.QDate.currentDate()
        nameEnable = (bool(self.firstnameLineEdit.text()) and
                  bool(self.lastnameLineEdit.text()))
        if nameEnable: 
            enableAll = (self.paidCheckBox.isChecked() or  #cash, or
                  (bool(self.checkNumLineEdit.text()) and  #check
                   bool(self.accountNumLineEdit.text()) and
                   bool(self.bankLineEdit.text()) and
                   bool(self.sortCodeLineEdit.text())) or
                  (bool(self.creditCardLineEdit.text()) and  #cc
                   self.validFromDateEdit.date() <= today and
                   self.expiryDateEdit.date() >= today))
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(enableAll)

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = PaymentDlg()
    form.show()
    app.exec_()

