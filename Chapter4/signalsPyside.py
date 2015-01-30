'''
signalsPyside.py
Heavily annotated PySide adaptation of signals.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

This starts the exposition on signals and slots. It is effectively the beginning of 
a new chapter in his book, as it goes into some detail. It includes five different
applications, and you select which to run from the command line (see Usage).

Forms 1 and 2 (inputs 1 and 2, respectively)
A spinbox and dial are reciprically connected using built-in signals and built-in
slots. In PySide, Forms 1 and 2 are identical, but as you can see if you look at 
the commented out old-style code, they were used by Summerfield to show two different 
old-style ways of connecting to a slot.

Form 3 (input 3)
Similar to previous, but now we subclass spinbox, creating a ZeroSpinBox class
that tracks how often the spinbox has hit 0. Custom signal emission is actually
simpler in old-style signals/slots than new style. This is because, unlike in 
old-style signals and slots, this custom signal must be independently declared.

Form 4 (input 4)
Summerfield does not discuss this, but it is a simple example of connecting the
text from QLineEdit to the terminal. 

TaxRate (input 5)
A pure console application (i.e., it has no GUI component). It tells you if a new
rate is different from the old rate. The main point is that GUI classes are not the only
that can emit: rather, any old QtCore.QObject can take advantage of these signal and slot
mechanisms. In practice, this would be rather strange to do.

Usage:
At command line, enter:
    python signalsPyside.py <input>
Where <input> is a number between 1 and 5 corresponding to programs specified above.

-------
Note in this and all code involving Signals/Slots, I often am violating the convention 
of giving slots the same name as their signal. I don't like this for a few reasons:
1. Different names for different objects makes code more readable. 
2. There are often many slots for a given signal (or many signals for a given slot).
3. Explicit is better than implicit.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
'''

from PySide import QtGui, QtCore
#QtCore we use: QObject, Qt
#QtGui we use: QApplication, QDial, QDialog, QHBoxLayout, QLineEdit, QSpinBox
import sys


#CASE 1: reciprically connected spinbox and dial
class Form1(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        #Set up widgets
        dial = QtGui.QDial(parent=self)
        dial.setNotchesVisible(True)  #show tick marks on dial
        spinbox = QtGui.QSpinBox(parent=self)
        #Set up layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        self.setLayout(layout)
        self.setWindowTitle("Form 1 Signals/Slots")

        #Connect the two widgets so if one changes, the other keeps up
        dial.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(dial.setValue)
        #In old style:
        # self.connect(dial, SIGNAL("valueChanged(int)"), spinbox.setValue)
        # self.connect(spinbox, SIGNAL("valueChanged(int)"), dial.setValue)


#CASE 2: same as above, but originally different old-style method uses to connect
class Form2(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        dial = QtGui.QDial()
        dial.setNotchesVisible(True)
        spinbox = QtGui.QSpinBox()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)
        self.setLayout(layout)
        self.setWindowTitle("Form 2 Signals/Slots")

        dial.valueChanged.connect(spinbox.setValue)
        spinbox.valueChanged.connect(dial.setValue)
        #old style connection from Summerfield
        #self.connect(dial, SIGNAL("valueChanged(int)"),
        #             spinbox, SLOT("setValue(int)"))
        #self.connect(spinbox, SIGNAL("valueChanged(int)"),
        #             dial, SLOT("setValue(int)"))


#Case 3: custom signal emitted
class Form3(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        dial = QtGui.QDial()
        dial.setNotchesVisible(True)
        zerospinbox = ZeroSpinBox(self) #custom class inherits from qspinbox

        #set layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(zerospinbox)
        self.setLayout(layout)
        self.setWindowTitle("Form 3 Signals/Slots")

        #standard recipricol connection
        dial.valueChanged.connect(zerospinbox.setValue)
        zerospinbox.valueChanged.connect(dial.setValue)
        zerospinbox.atzero.connect(self.announce)   #new method based on custom atzero signal
        #old-style methods
        # self.connect(dial, SIGNAL("valueChanged(int)"),
        #              zerospinbox, SLOT("setValue(int)"))
        # self.connect(zerospinbox, SIGNAL("valueChanged(int)"),
        #              dial, SLOT("setValue(int)"))
        # self.connect(zerospinbox, SIGNAL("atzero"), self.announce)  

    def announce(self, zeros):
        print("ZeroSpinBox has been at zero {0} times".format(zeros))


class ZeroSpinBox(QtGui.QSpinBox):
    numZeros = 0
    atzero=QtCore.Signal(int)  #old-style didn't have to do this (http://stackoverflow.com/a/5186812/1886357)

    def __init__(self, parent=None):
        QtGui.QSpinBox.__init__(self, parent)
        self.valueChanged.connect(self.checkzero) 
        #old style: self.connect(self, SIGNAL("valueChanged(int)"), self.checkzero)

    #define the signal to emit
    @QtCore.Slot()  #this isn't really necessary is it?
    def checkzero(self):
        if self.value() == 0:
            self.numZeros += 1
            self.atzero.emit(self.numZeros)
            #old style would dynamically make signal, which was admittedly nice
            #self.emit(SIGNAL("atzero"), self.numZ7eros)
            

#Case 4: console echo example
class Form4(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        lineedit = QtGui.QLineEdit()
        
        #set layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(lineedit)      
        self.setLayout(layout)
        self.setWindowTitle("Form 4 Signals/Slots")
        
        #connect built-in textChanged signal to consoleEcho Python slot
        lineedit.textChanged.connect(self.consoleEcho)
        #old-style: self.connect(lineedit, SIGNAL("textChanged(QString)"), self.consoleEcho)

    def consoleEcho(self, text):
        print unicode(text)

              

#Case 5: pure console with no GUI still uses signals/slots...
class TaxRate(QtCore.QObject):
    rateChangedSig=QtCore.Signal(float)  #custom signal indicating tax rate

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.rate = 17.5

    def getRate(self):
        return self.rate

    def setRate(self, newRate):
        if newRate != self.rate:
            self.rate = newRate
            self.rateChangedSig.emit(self.rate)  #was self.emit(SIGNAL("rateChanged"), self.rate)

#custom slot that prints value
def rateChangedSlot(value):
    print "Tax rate changed to {0:.2}".format(value)


if __name__=="__main__":
    form = None
    if len(sys.argv) == 1 or sys.argv[1] == "1": 
        qtApp = QtGui.QApplication(sys.argv)
        form = Form1()
    elif sys.argv[1] == "2":
        qtApp = QtGui.QApplication(sys.argv)
        form = Form2()  
    elif sys.argv[1] == "3":
        qtApp = QtGui.QApplication(sys.argv)
        form = Form3()
    elif sys.argv[1] == "4":
        qtApp = QtGui.QApplication(sys.argv)
        form = Form4()
        
    if form is not None:
        form.show()
        sys.exit(qtApp.exec_())
    elif sys.argv[1] == "5":
        vat = TaxRate()
        vat.rateChangedSig.connect(rateChangedSlot) #connect custom signal to custom slot
        #old-style vat.connect(vat, SIGNAL("rateChanged"), rateChanged)
        vat.setRate(8.5)     # A change will occur (new rate is different)
        #vat.setRate(17.5)    # No change will occur (new rate is the same)



