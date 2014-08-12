# -*- coding: utf-8 -*-
"""
ticketorderdlg1Pyside.py

Main file in solution to the exercise in Chapter 7 of 
Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Note Summerfield provides a different solution on his web site.

#to do:
3. working well
4. read over instructions do it up 

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import sys
from PySide import QtGui, QtCore
from ui_ticketorderdlg1Pyside import Ui_TicketOrderDlg
#Ui_TicketOrderDlg brings in following attributes of the dialog:
#customerLabel,customerLineEdit
#priceLabel, priceSpinBox
#quantityLabel, quantitySpinBox
#whenLabel, dateTimeEdit (QtGui.QDateTimeEdit)
#amountLabel, amountLineEdit
#self.buttonBox (with QtGui.QDialogButtonBox.Cancel and QtGui.QDialogButtonBox.Ok)




class TicketDialog(QtGui.QDialog, Ui_TicketOrderDlg):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)  #method in Ui_TicketOrderDlg
        self.priceSpinBox.setPrefix("$ ")
        self.dateTimeEdit.setMinimumDateTime(QtCore.QDateTime.currentDateTime().addDays(1))
        self.dateTimeEdit.setMaximumDateTime(QtCore.QDateTime.currentDateTime().addDays(365))
        self.dateTimeEdit.setDisplayFormat("MM/dd/yyyy hh:mm ap")       
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True) #disable OK button until data is valid
        self.setValues()

        
    def result(self):
        return self.customer, self.dateTime.toPython(), self.price, self.quantity
        
    def setValues(self):
        self.customer=self.customerLineEdit.text()
        self.price=self.priceSpinBox.value()
        self.quantity=self.quantitySpinBox.value() 
        self.dateTime=self.dateTimeEdit.dateTime()
        self.updateAmount()
        self.checkValid()
        
    def updateAmount(self):
        self.amount=self.price*self.quantity
        self.amountLineEdit.setText("${amnt: 0.2f}".format(amnt=self.amount))
        self.checkValid()
        
    #reimplement accept
    def accept(self):
        if self.checkValid():
            QtGui.QDialog.accept(self)
        else:
            return               
        
    def checkValid(self):
        if self.customer == "":
            #print "No customer"
            return False
        if self.amount <= 0:
            #print "Need a valid purchase"
            return False
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(False)         
        return True
            
    def printInfo(self):
        if self.checkValid():
            prettyDateTime=self.dateTimeEdit.dateTime().toPython().strftime("%m/%d/%Y @ %I:%M %p")
            print "\nTime of show: {dt} \n{person} purchased {number} ticket(s) @ ${price: 0.2f} each.\n"\
                  "The total cost of the transaction is ${amount: 0.2f}.\n".\
                    format(dt=prettyDateTime, person=self.customer, number=self.quantity,\
                    price=self.price, amount=self.amount)           
        else:
            print "Please make sure your information is valid, and there is a customer."

    @QtCore.Slot(float)
    def on_priceSpinBox_valueChanged(self, value):
        self.price=self.priceSpinBox.value()
        self.updateAmount()
        
            
    @QtCore.Slot(int)
    def on_quantitySpinBox_valueChanged(self, value):
        self.quantity=self.quantitySpinBox.value() 
        self.updateAmount()
            
    @QtCore.Slot(str)
    def on_customerLineEdit_textEdited(self, text):
        self.customer=self.customerLineEdit.text()
        self.checkValid()

    #this is not necessary, but just did it for fun
    @QtCore.Slot(QtCore.QDateTime)
    def on_dateTimeEdit_dateTimeChanged(self, dt):
        #http://stackoverflow.com/a/8468984/1886357
        dtInit=self.dateTimeEdit.dateTime().toPython()
        print "dateTime set to ", dtInit.strftime("%m/%d/%Y @ %I:%M %p")
    
    
    
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    ticketDlg = TicketDialog()
    if ticketDlg.exec_():
        ticketDlg.printInfo()
    else:
        print "Well that didn't go so well..."
    print "\nResult: ", ticketDlg.result()