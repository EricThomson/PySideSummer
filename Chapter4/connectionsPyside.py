# coding: utf-8
'''
connectionsPyside.py
Heavily annotated PySide adaptation of connections.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

Shows how slots can tell what widget sent it a signal. It shows this with
4 different methods.

Usage:
Run the module and start a' clickin': You should see a different message for each
button you click.

--------
Useful references:
1. Similar example using new-style signals/slots:
http://www.blog.pythonlibrary.org/2013/04/10/pyside-connecting-multiple-widgets-to-the-same-slot/

2. On partial functions:
http://www.learnpython.org/en/Partial_functions
http://www.techrepublic.com/article/partial-function-application-in-python/

3. On lambda functions:
http://www.diveintopython.net/power_of_introspection/lambda_functions.html
http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
'''

from PySide import QtGui, QtCore
import functools
import sys

class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        #define your widgets
        button1 = QtGui.QPushButton("One")
        button2 = QtGui.QPushButton("Two")
        button3 = QtGui.QPushButton("Three")
        button4 = QtGui.QPushButton("Four")
        button5 = QtGui.QPushButton("Five")
        self.label = QtGui.QLabel("Click a button...") #is used elsewhere, so attached to self

        #Set layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addStretch()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle("Connections")        

        #Connect buttons to slot
        #Button 1: build its own custom slot
        button1.clicked.connect(self.one) #special-purpose slot for button 1
        #Button 2: build callback using 'functools.partial'
        button2.clicked.connect(functools.partial(self.anyButton, "Two") )
        #Button 3:  build callback function with lambda
        button3.clicked.connect(lambda who="Three" : self.anyButton(who))
        #Buttons 4 and 5: slot uses 'sender' to access clicked widget (see warnings above)
        button4.clicked.connect(self.clickedButton)
        button5.clicked.connect(self.clickedButton)
        
        #Same connections set using old style
        #self.connect(button1, SIGNAL("clicked()"), self.one)
        #self.button2callback = functools.partial(self.anyButton, "Two")
        #self.connect(button2, SIGNAL("clicked()"),
        #             self.button2callback)
        #self.button3callback = lambda who="Three": self.anyButton(who)
        #self.connect(button3, SIGNAL("clicked()"),
        #             self.button3callback)
        #self.connect(button4, SIGNAL("clicked()"), self.clicked)
        #self.connect(button5, SIGNAL("clicked()"), self.clicked)

    @QtCore.Slot()
    def one(self):
        self.label.setText("You clicked button 'One'")

    @QtCore.Slot()
    def anyButton(self, who):
        self.label.setText("You clicked button '{}'".format(who))
    
    #Note: The use of 'sender' is frowned upon sometimes for being nonmodular.
    #It is also used a lot, and extremely convenient, so you should be familiar with it. 
    #@QtCore.Slot() breaks this slot
    def clickedButton(self):
        button = self.sender() #how could something so awesome be frowned upon?
        if button is None or not isinstance(button, QtGui.QPushButton):
            return
        self.label.setText("You clicked button {0}".format(button.text()))


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()

