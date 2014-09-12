# -*- coding: utf-8 -*-
"""
contactdlgPyside.py
Annotated PySide port of contactdlg.py from Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtGui

#note if you try 'QtGui.QComboBox' stylesheet will not work
class ContactDlg(QtGui.QDialog):
    StyleSheet = """
QComboBox { color: darkblue; }  
QLineEdit { color: darkgreen; }
QLineEdit[mandatory="1"] {
    background-color: rgb(255, 255, 127);
    color: darkblue;
}
"""
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        #Note that fax, mobile phone, address are not mandatory
        #These lineedits will be highlighted in yellow
        self.mandatoryLineEdits = (self.forenameEdit, self.surnameEdit,
                self.companyEdit, self.phoneEdit, self.emailEdit)
        for lineEdit in self.mandatoryLineEdits:
            lineEdit.setProperty("mandatory", 1)
            lineEdit.textEdited.connect(self.updateUi)
            
        self.setStyleSheet(ContactDlg.StyleSheet)
        self.setWindowTitle("Add Contact")


    def create_widgets(self):
        self.forenameLabel = QtGui.QLabel("&Forename:")
        self.forenameEdit = QtGui.QLineEdit()
        self.forenameLabel.setBuddy(self.forenameEdit)
        
        self.surnameLabel = QtGui.QLabel("&Surname:")
        self.surnameEdit = QtGui.QLineEdit()
        self.surnameLabel.setBuddy(self.surnameEdit)
        
        #determines whether company name is mandatory
        self.categoryLabel = QtGui.QLabel("&Category:")
        self.categoryComboBox = QtGui.QComboBox()
        self.categoryLabel.setBuddy(self.categoryComboBox)
        self.categoryComboBox.addItems(["Business", "Domestic",
                                        "Personal"])
                                        
        self.companyLabel = QtGui.QLabel("C&ompany:")
        self.companyEdit = QtGui.QLineEdit()
        self.companyLabel.setBuddy(self.companyEdit)
        
        self.addressLabel = QtGui.QLabel("A&ddress:")
        self.addressEdit = QtGui.QLineEdit()
        self.addressLabel.setBuddy(self.addressEdit)
        
        self.phoneLabel = QtGui.QLabel("&Phone:")
        self.phoneEdit = QtGui.QLineEdit()
        self.phoneLabel.setBuddy(self.phoneEdit)
        
        self.mobileLabel = QtGui.QLabel("&Mobile:")
        self.mobileEdit = QtGui.QLineEdit()
        self.mobileLabel.setBuddy(self.mobileEdit)
        
        self.faxLabel = QtGui.QLabel("Fa&x:")
        self.faxEdit = QtGui.QLineEdit()
        self.faxLabel.setBuddy(self.faxEdit)
        
        self.emailLabel = QtGui.QLabel("&Email:")
        self.emailEdit = QtGui.QLineEdit()
        self.emailLabel.setBuddy(self.emailEdit)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                          QtGui.QDialogButtonBox.Cancel)
        #change name of OK button (i.e., button has QMessageBox.AcceptRole)                             
        addButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        addButton.setText("&Add")
        addButton.setEnabled(False)


    def layout_widgets(self):
        grid = QtGui.QGridLayout()
        grid.addWidget(self.forenameLabel, 0, 0)
        grid.addWidget(self.forenameEdit, 0, 1)
        grid.addWidget(self.surnameLabel, 0, 2)
        grid.addWidget(self.surnameEdit, 0, 3)
        grid.addWidget(self.categoryLabel, 1, 0)
        grid.addWidget(self.categoryComboBox, 1, 1)
        grid.addWidget(self.companyLabel, 1, 2)
        grid.addWidget(self.companyEdit, 1, 3)
        grid.addWidget(self.addressLabel, 2, 0)
        grid.addWidget(self.addressEdit, 2, 1, 1, 3)
        grid.addWidget(self.phoneLabel, 3, 0)
        grid.addWidget(self.phoneEdit, 3, 1)
        grid.addWidget(self.mobileLabel, 3, 2)
        grid.addWidget(self.mobileEdit, 3, 3)
        grid.addWidget(self.faxLabel, 4, 0)
        grid.addWidget(self.faxEdit, 4, 1)
        grid.addWidget(self.emailLabel, 4, 2)
        grid.addWidget(self.emailEdit, 4, 3)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.categoryComboBox.activated[int].connect(self.updateUi)


    def updateUi(self):
        #update whether companyEdit is mandatory, depending on category
        mandatory = bool(int(self.companyEdit.property("mandatory")))
        #print "mandatory, type(mandatory):\n", mandatory, " , ", type(mandatory), "\n\n"
        if self.categoryComboBox.currentText() == "Business":
            if not mandatory:
                self.companyEdit.setProperty("mandatory", 1)
        elif mandatory:
            self.companyEdit.setProperty("mandatory", 0)
            
        #if value of mandatory has changed, then update style sheet   
        if (mandatory != bool(int(self.companyEdit.property("mandatory")))):
            self.setStyleSheet(ContactDlg.StyleSheet)
            
        #check on enabling of buttonbox
        enable = True
        for lineEdit in self.mandatoryLineEdits:
            if (bool(int(lineEdit.property("mandatory"))) and
                not lineEdit.text()):
                enable = False
                break
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(enable)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ContactDlg()
    form.show()
    app.exec_()
