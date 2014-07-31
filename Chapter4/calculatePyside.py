'''
calculatePyside.py
Heavily annotated PySide adaptation of calculate.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

Usage:
Run the module, and play with the calculator!

Main goal: see some widgets, how they talk to one another (signals/slots), and
how to set layout using vertical layouts.

Notes
Annotations include comments and links to relevant documentation. When possible,
PySide documentation is linked, but sometimes we have to go with Qt, as PySide
documentation is way behind.

Most recent version can be pulled from GitHub:
XXXXX
Especially interested in improving Pythonicity of code.

To do:
1. Move notes to readme
'''

from __future__ import division

import sys
from PySide import QtGui, QtCore
#QtCore use Qt
#QtGui use QApplication, QDialog, QLineEdit, QTextBrowser, QVBoxLayout
from math import *  #not great practice to just import all, but in this case the point is to show a small example

#Parent class is QDialog, which starts out fairly minimal, without a menu or toolbar, basically
#simple interactions with user (a dialog). They can be closed by hitting the esc key.
#Documentation: http://srinikom.github.io/pyside-docs/PySide/QtGui/QDialog.html
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
        '''
        Old style signals/slots:
            self.connect(<object>, SIGNAL("<event>"), <slot>)

        New style signals and slots are more Pythonic
            <object>.<event>.connect(<slot>)

        Hence, what was:
                self.connect(self.lineedit, SIGNAL("returnPressed()"), self.updateUi)
        becomes:'''
        self.lineedit.returnPressed.connect(self.updateUI)  #when user hits return in line edit, connect to updateUI slot

    #Useful to use @QtCore.Slot decorator, even though not technically necessary:
    #   http://stackoverflow.com/questions/14421897/is-the-pyside-slot-decorator-necessary
    @QtCore.Slot()
    def updateUI(self):
        try:
            text = unicode(self.lineedit.text())  #pull text from editor line
            self.browser.append("{0} = <b>{1}</b>".format(text, eval(text)))  #note eval is dangerous!
        except:  #bare exception frowned upon, but in this context let's not have a hissy fit.
            self.browser.append("<font color=red>'{0}' is too advanced for me!</font>".format(text))

app = QtGui.QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())

