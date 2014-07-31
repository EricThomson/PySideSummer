# coding: utf-8
'''
calculatePyside.py
Heavily annotated PySide adaptation of calculate.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

Provides opportunity to work with some widgets, see how they talk to one 
another (signals/slots), and how to set layouts.

Usage:
Run the module, and play with the calculator.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html


'''

from __future__ import division

import sys
from PySide import QtGui, QtCore
from math import *  #not great practice to import all, but in this case the point is to show a small example

class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Pyside Calculator")

        #Make widgets
        #Is it bad form to put parent=self in here?
        self.browser = QtGui.QTextBrowser(parent=self)  #read-only html display
        self.lineedit = QtGui.QLineEdit("Type an expression and press Enter", parent=self)  #single editable line
        self.lineedit.selectAll()  #so when user starts typing, initial text is replaced

        #Set layout
        layout = QtGui.QVBoxLayout()  #will align widgets vertically
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()  #gives focus to lineedit, so user will enter text there first (must come after layout)

        #Connect editor to browser with signals/slots
        self.lineedit.returnPressed.connect(self.updateUI)  #was: self.connect(self.lineedit, SIGNAL("returnPressed()"), self.updateUi)

    #Useful to use @QtCore.Slot decorator, even though not technically necessary:
    #   http://stackoverflow.com/questions/14421897/is-the-pyside-slot-decorator-necessary
    @QtCore.Slot()
    def updateUI(self):
        try:
            text = unicode(self.lineedit.text())  #pull text from editor line
            self.browser.append("{0} = <b>{1}</b>".format(text, eval(text)))  #note eval is dangerous!
        except:  #bare exception frowned upon, but in this context let's not have a hissy fit.
            self.browser.append("<font color=red>'{0}' is too advanced for me!</font>".format(text))

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

