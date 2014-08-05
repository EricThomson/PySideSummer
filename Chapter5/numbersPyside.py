# -*- coding: utf-8 -*-
'''
numbersPyside.py
Heavily annotated PySide adaptation of numbersPyside.pyw from Chapter 5
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

XXX More comments here

Usage:
XXX Blah blah

Note: I have stopped writing down the old-style signals/slots 
alongside the new-style. To see them in parallel, see adaptations of
programs from Chapter 4.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
'''
from PySide import QtGui, QtCore
import math
import random
import string  #can we not use this?
import sys
import numberformatdlg1Pyside
import numberformatdlg2Pyside
import numberformatdlg3Pyside


class Form(QtGui.QDialog):

    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.numberFormatDlg = None
        self.format = dict(thousandsseparator=",", decimalmarker=".",
                decimalplaces=2, rednegatives=False)
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000

        self.table = QtGui.QTableWidget()
        formatButton1 = QtGui.QPushButton("Set Number Format... (&Modal)")
        formatButton2 = QtGui.QPushButton("Set Number Format... (Modele&ss)")
        formatButton3 = QtGui.QPushButton("Set Number Format... (`&Live')")

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(formatButton1)
        buttonLayout.addWidget(formatButton2)
        buttonLayout.addWidget(formatButton3)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.setWindowTitle("Numbers")

        formatButton1.clicked.connect(self.setNumberFormat1)
        formatButton2.clicked.connect(self.setNumberFormat2)
        formatButton3.clicked.connect(self.setNumberFormat3)

        self.refreshTable()


    def refreshTable(self):
        self.table.clear()
        self.table.setColumnCount(self.X_MAX)
        self.table.setRowCount(self.Y_MAX)
        self.table.setHorizontalHeaderLabels(
                list(string.ascii_uppercase))
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x, y)])
                sign = "-" if whole < 0 else ""
                whole = "{}".format(int(math.floor(abs(whole))))
                digits = []
                for i, digit in enumerate(reversed(whole)):
                    if i and i % 3 == 0:
                        digits.insert(0, self.format["thousandsseparator"])
                    digits.insert(0, digit)
                if self.format["decimalplaces"]:
                    fraction = "{0:.7f}".format(abs(fraction))
                    fraction = (self.format["decimalmarker"] +
                            fraction[2:self.format["decimalplaces"] + 2])
                else:
                    fraction = ""
                text = "{}{}{}".format(sign, "".join(digits), fraction)
                item = QtGui.QTableWidgetItem(text)
                item.setTextAlignment(QtCore.Qt.AlignRight|
                                      QtCore.Qt.AlignVCenter)
                                      
                if sign and self.format["rednegatives"]:
                    item.setBackground(QtGui.QColor("red"))
                    #setbackgroundcolor is deprecated:
                    #    http://srinikom.github.io/pyside-bz-archive/359.html
                    #item.setBackgroundColor(Qt.red)
                self.table.setItem(y, x, item)


    def setNumberFormat1(self):
        #Instantiate modal dialog, when closed get return values
        dialog = numberformatdlg1Pyside.NumberFormatDlg(self.format, self)
        if dialog.exec_():
            self.format = dialog.numberFormat() 
            self.refreshTable()


    def setNumberFormat2(self):
        dialog = numberformatdlg2Pyside.NumberFormatDlg(self.format, self)
        #'changed' is a custom signal defined/emitted in numberformatdlg2Pyside 
        dialog.changed.connect(self.refreshTable) 
        dialog.show()


    def setNumberFormat3(self):
        if self.numberFormatDlg is None:
            self.numberFormatDlg = \
                numberformatdlg3Pyside.NumberFormatDlg(self.format, self.refreshTable, self)
        self.numberFormatDlg.show()
        self.numberFormatDlg.raise_()
        self.numberFormatDlg.activateWindow()


qtApp = QtGui.QApplication(sys.argv)
form = Form()
form.show()
qtApp.exec_()

