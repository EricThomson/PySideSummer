'''
interestPyside.py
One person's attempt to solve the exercise at the end of Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
It is adapted from the currency example in the chapter.

Usage:
Run the module, and then play around with your money!

Notes
Annotations include comments and links to relevant documentation. When possible,
PySide documentation is linked, but sometimes we have to go with Qt, as PySide
documentation is way behind.

Most recent version can be pulled from GitHub:
XXXXX
Especially interested in improving Pythonicity of code.

To do:
1. Move repeated comments to readme
'''

from PySide import QtGui, QtCore
import sys


class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Compound it")

        #make widgets to display in QDialog
        #Principal amount
        principalLabel=QtGui.QLabel("Principal:", parent=self)
        self.principal=QtGui.QDoubleSpinBox(parent=self)
        self.principal.setRange(0.0, 10000000.00)
        self.principal.setValue(100.00)
        self.principal.setPrefix("$ ")
        
        #Interest rates
        rateLabel=QtGui.QLabel("Rate:", parent=self)
        self.rate=QtGui.QDoubleSpinBox(parent=self)
        self.rate.setRange(0.0, 1000.00)
        self.rate.setValue(5.00)
        self.rate.setSuffix(" %")
        
        #years to calculate
        yearLabel=QtGui.QLabel("Years:", parent=self)
        self.years=QtGui.QComboBox(parent=self)
        numYears=[str(i) for i in range(11)]  #0 to 10 years
        self.years.addItems(numYears)
        self.years.setCurrentIndex(1)

        #Amount
        amountLabel=QtGui.QLabel("Amount:", parent=self)
        initAmount="$100.00"
        self.amountValue=QtGui.QLabel(initAmount)
        self.updateUi()  #initialize values appropriately

        #Set layout using grid
        grid = QtGui.QGridLayout()
        grid.addWidget(principalLabel, 0, 0)  #why does dateLabel not property of self?
        grid.addWidget(self.principal, 0,1)
        grid.addWidget(rateLabel, 1, 0)
        grid.addWidget(self.rate, 1, 1)
        grid.addWidget(yearLabel, 2, 0)
        grid.addWidget(self.years, 2,1)
        grid.addWidget(amountLabel,3,0)
        grid.addWidget(self.amountValue, 3, 1)
        self.setLayout(grid)

        #Set up signals to connect to update slot when user interacts with widgets
        self.principal.valueChanged.connect(self.updateUi) #when starting amount changes
        self.rate.valueChanged.connect(self.updateUi) #change interest rates
        self.years.currentIndexChanged.connect(self.updateUi)  #index of years

    def updateUi(self):
        principal=float(self.principal.value())
        rate=float(self.rate.value())
        numYears=int(self.years.currentText())
        newAmount=principal*((1+(rate/100.0))**numYears)
        self.amountValue.setText("${0:.2f}".format(newAmount))


if __name__=="__main__":
    qtApp = QtGui.QApplication(sys.argv)
    #Customize the style:
    #  http://qt-project.org/doc/qt-4.8/gallery.html
    #Note not all styles available on your os, to print out styles 
    #available on your platform, uncomment the following line:
    #print QtGui.QStyleFactory.keys()
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))      
    form = Form()
    form.show()
    sys.exit(qtApp.exec_())

