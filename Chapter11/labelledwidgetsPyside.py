# -*- coding: utf-8 -*-
"""
labelledwidgetsPyside.py
Annotated PySide port of labelledwidgets.py from Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Shows how to embed composite custom widgets (LabelelledLineEdit and 
LabelledTextEdit) in a QWidget.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtGui

#FOllowing toggles whether text appears above, or to left of, QTextEdit box
LEFT, ABOVE = range(2)

class Dialog(QtGui.QDialog):

    def __init__(self, address=None, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.create_widgets(address)
        self.layout_widgets()
        self.create_connections()
        self.setWindowTitle("Labelled Widgets")


    def create_widgets(self, address):
        #instantiating custom class defined below (LabelledLineEdit)
        self.street = LabelledLineEdit("&Street:", ABOVE)  #ABOVE/LEFT change layout 
        self.city = LabelledLineEdit("&City:", ABOVE)
        self.state = LabelledLineEdit("St&ate:", ABOVE)
        self.zipcode = LabelledLineEdit("&Zipcode:", ABOVE)
        self.notes = LabelledTextEdit("&Notes:", LEFT)
        
        #If they actually gave an address as a parameter
        if address is not None:
            self.street.lineEdit.setText(address.get("street",""))
            self.city.lineEdit.setText(address.get("city", ""))
            self.state.lineEdit.setText(address.get("state", ""))
            self.zipcode.lineEdit.setText(address.get("zipcode", ""))
            self.notes.textEdit.setPlainText(address.get("notes", ""))
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                          QtGui.QDialogButtonBox.Cancel)


    def layout_widgets(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.street, 0, 0)
        grid.addWidget(self.city, 0, 1)
        grid.addWidget(self.state, 1, 0)
        grid.addWidget(self.zipcode, 1, 1)
        grid.addWidget(self.notes, 2, 0, 1, 2)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        

    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
class LabelledLineEdit(QtGui.QWidget):
    #class to make qlineedit with associated label that are buddied up
    def __init__(self, labelText="", position=LEFT,
                 parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.label = QtGui.QLabel(labelText)
        self.lineEdit = QtGui.QLineEdit()
        self.label.setBuddy(self.lineEdit)
        
        #Layout depends on position selected
        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight
                if position == LEFT else QtGui.QBoxLayout.TopToBottom)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)


class LabelledTextEdit(QtGui.QWidget):

    def __init__(self, labelText="", position=LEFT,
                 parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.label = QtGui.QLabel(labelText)
        self.textEdit = QtGui.QTextEdit()
        self.label.setBuddy(self.textEdit)
        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight
                if position == LEFT else QtGui.QBoxLayout.TopToBottom)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)


if __name__ == "__main__":
    fakeAddress = dict(street="3200 Mount Vernon Memorial Highway",
                       city="Mount Vernon", state="Virginia",
                       zipcode="22121")
    app = QtGui.QApplication(sys.argv)
    form = Dialog(fakeAddress)
    form.show()
    app.exec_()
    print("Street:", unicode(form.street.lineEdit.text()))
    print("City:", unicode(form.city.lineEdit.text()))
    print("State:", unicode(form.state.lineEdit.text()))
    print("Zipcode:", unicode(form.zipcode.lineEdit.text()))
    print("\nNotes:")
    print(unicode(form.notes.textEdit.toPlainText()))

