'''
currencyPyside.py
Heavily annotated PySide adaptation of currency.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

A currency converter laid out using gridlayout, where exchange rates are pulled from online.
The top row of widgets is the "from" row, which describes what kind of currency you have, and
how much you want to "sell". This currency amount is controllable using a spinbox. The second
"to" row is the derived currency, which shows how much you would receive in exchange for the
base currency amount you set.

Main goal: our final in our whirlwind tour of PyQt. THis shows a few new widgets and their signals,
the use of grid layout, and general demonstration of how to implement a GUI with more moving parts.

Usage:
Run the module, and then play around to find out how much you can sell your money for
(e.g., in Croatia).

'''

from PySide import QtGui, QtCore
#Qt subclasses we use in this program:
#QtCore: Qt
#QtGui: QApplication, QComboBox, QDialog, QDoubleSpinBox, QGridLayout, QLabel

import sys
import urllib2


class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Sell your money!")

        #Get data about exchange rates
        #Note variables like date are not set as properties of self, as we do not use them outside this __init__ method.
        #The comboxes and such below, we do use in the other methods, so they are set as properties of self.
        date = self.getdata()  #adds self.rates dictionary (key: name of currency, value: exchange rates)
        currencyTypes = sorted(self.rates.keys())  #pull keys (name of currency) and sorts them

        #make widgets to display in QDialog
        dateLabel = QtGui.QLabel(date, parent=self)  #is this parent=self really needed?
        self.fromComboBox = QtGui.QComboBox(parent=self)
        self.fromComboBox.addItems(currencyTypes)
        self.fromSpinBox =  QtGui.QDoubleSpinBox(parent=self)
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QtGui.QComboBox(parent=self)
        self.toComboBox.addItems(currencyTypes)
        self.toLabel = QtGui.QLabel("1.00")

        #Set layout using grid
        grid = QtGui.QGridLayout()
        grid.addWidget(dateLabel, 0, 0)  #why does dateLabel not property of self?
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        #Set up signals to connect to update slot when user interacts with widgets
        self.fromComboBox.currentIndexChanged.connect(self.updateUi) #changing base currency
        self.toComboBox.currentIndexChanged.connect(self.updateUi) #changing derived currency
        self.fromSpinBox.valueChanged.connect(self.updateUi)  #when base currency amount is changed



    @QtCore.Slot()
    def updateUi(self):
        to = unicode(self.toComboBox.currentText())
        baseCurrency = unicode(self.fromComboBox.currentText())  #single trailing underscore to avoid conflict with built-in from
        amount = ((self.rates[baseCurrency] / self.rates[to]) *
                  self.fromSpinBox.value())
        self.toLabel.setText("{0:.2f}".format(amount))


    def getdata(self): # Idea taken from the Python Cookbook
        self.rates = {}
        try:
            date = "Unknown"  #default date string
            #Introduction to urllib2:
            #   https://docs.python.org/2/library/urllib2.html
            #   http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/
            #It seems the requests package has largely supplanted it:
            #   http://docs.python-requests.org/en/latest/
            #   http://stackoverflow.com/questions/2018026/should-i-use-urllib-or-urllib2-or-requests
            #However, this has nothing to do with Qt, so for our limited purposes, urllib2 is fine
            fileHandle = urllib2.urlopen("http://www.bankofcanada.ca"
                                 "/en/markets/csv/exchange_eng.csv")  #fileHandle=file handle?
            for line in fileHandle:
                line = line.rstrip() #remove trailing whitespace
                if not line or line.startswith(("#", "Closing ")):
                    continue
                fields = line.split(",")
                if line.startswith("Date "):  #the line with dates starts with "Date "
                    date = fields[-1]  #final element of line is most recent date
                else:
                    try:
                        value = float(fields[-1])  #last elt of other lines is rate
                        self.rates[unicode(fields[0])] = value  #sets dictionary entry
                    except ValueError:
                        pass
            return "Exchange Rates Date: " + date
        except Exception, e:  #if something was wrong with the network connection
            return "Failed to download:\n{0}".format(e)


app = QtGui.QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())

