# coding: utf-8
'''
connectionsPyside.py
Heavily annotated PySide adaptation of connections.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

This example continues Summerfield's tutorial on signals and slots. How to
get different responses to a bunch of similar widgets (e.g., five pushbuttons).
This program shows you how to do that using 4 of the 6 main ways (consstruct
a different slot for each button (inefficient!), or use lambda functions, partial
functions, or the sender method). 

Note the sixth, often preferable way to map from widget signal to slot is to 
use using QSignalMapper: it is covered in Chapter 9.

The use of 'sender' is frowned upon sometimes (details in program). 
It is also used a lot, and extremely convenient, so you should be familiar with it. 


Usage:
Run the module and start a' clickin'! You should see a different message for each
button you click.


Useful references:
1. Similar example using new-style signals/slots:
http://www.blog.pythonlibrary.org/2013/04/10/pyside-connecting-multiple-widgets-to-the-same-slot/

2. On partial functions:
http://www.learnpython.org/en/Partial_functions
http://www.techrepublic.com/article/partial-function-application-in-python/

3. On lambda functions:
http://www.diveintopython.net/power_of_introspection/lambda_functions.html
http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/

Notes
Why is sender frowned upon? 
A couple of reasons. From the qt web page:
http://qt-project.org/wiki/PySide_Pitfalls#f1984e960c02bfeb7cfe9992b1294439
"If you want to get the object that emitted a signal, you can do so using
QtCore.QObject.sender(), although you should really think twice before using
it (see the API docs of QObject for details). If you really, really decide
that you have to use it, be aware that right now, you cannot call it as a
static method, but only from within a QObject slot."

From the API docs:
http://srinikom.github.io/pyside-docs/PySide/QtCore/QObject.html#PySide.QtCore.PySide.QtCore.QObject.sender
"This function violates the object-oriented principle of modularity. However, getting
access to the sender might be useful when many signals are connected to a single slot."
and:
'The return value of this function is not valid when the slot is called via a Qt.DirectConnection from a thread different from this object’s thread. Do not
use this function in this type of scenario."

On violation of modular programming. Recall one principle of modular programming from:
http://www.guruzon.com/1/oop-concepts/modularity/what-is-modularity-example-tutorial-advantages-pros-why-how-works
"The overall goal of modularity is to decompose the source code into small modules 
such that it should be possible to design, develop, test and maintain the individual 
modules independent of each other. It should be possible to change the implementation 
of one module without knowing or affecting the implementation of other modules."

Seems fine on that front. Change button text, whatevs.

Or from http://en.wikipedia.org/wiki/Modular_programming:
Modular programming is a software design technique that emphasizes separating the 
functionality of a program into independent, interchangeable modules, such that each 
contains everything necessary to execute only one aspect of the desired functionality

Or from http://linux.about.com/cs/linux101/g/modularprogramm.htm:
"Modular programming is a programming style that breaks down program functions into 
modules, each of which accomplishes one function and contains all the source code 
and variables needed to accomplish that function. Modular programming is a solution 
to the problem of very large programs that are difficult to debug and maintain. By 
segmenting the program into modules that perform clearly defined functions, you can 
determine the source of program errors more easily. "

If this violates it, doesn't standard model/view programming violate it with internalPointers
that basically act like a sender? It is not clear at all how sender is that bad. Seems
like a dogma.

Annotations include comments and links to relevant documentation. When possible,
PySide documentation is linked, but sometimes we have to go with Qt, as PySide
documentation is way behind.

Most recent version can be pulled from GitHub:
xxxx
Especially interested in improving Pythonicity of code.

To do:
1. Move repeated comments to readme
2. Respond to this:
http://stackoverflow.com/questions/4642716/how-to-determine-who-emitted-the-signal
Especially that first douchey comment by caleb huitt. typical SO bullshit.
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


    def one(self):
        self.label.setText("You clicked button 'One'")


    def anyButton(self, who):
        self.label.setText("You clicked button '{}'".format(who))

    #@QtCore.Slot()
    #The above breaks it.d This is a known thing:
    #http://stackoverflow.com/questions/18015684/pyside-qtcore-slot-decorator-does-not-work-with-self-sender-inside-a-method

    #I need to ask about so-called c++ verus python slots, and this answer:
    #  http://stackoverflow.com/questions/14421897/is-the-pyside-slot-decorator-necessary
    #@AustinPhillips does this really hold in PySide? Do we even provide C++ 
    #signatures in PySide? (I think those are the arguments to signal?
    #Note also when I include @QtCore.Slot() before some slots 
    #(e.g., those in which I use the .sender() function), it doesn't even work. Further, 
    #if a slot is a Qt slot (as opposed to a Python slot?), why would we define it anyway?
    #
    #Do we even provide C++ signatures in PySide? What is a 'Qt' slot, that is, what 
    #differentiates a Qt slot from a non-Qt slot in Pyside?  
    def clickedButton(self):
        button = self.sender() #how could something so awesome be frowned upon?
        if button is None or not isinstance(button, QtGui.QPushButton):
            return
        self.label.setText("You clicked button {0}".format(button.text()))


app = QtGui.QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

