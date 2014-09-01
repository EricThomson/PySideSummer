# -*- coding: utf-8 -*-
"""
vehiclerentaldlgPyside.py
Annotated PySide port of vehiclerentaldlg.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Shows stacked widgets, which involve a little more signalling overhead 
than tabs.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtGui, QtCore


class VehicleRentalDlg(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Vehicle Rental")
        
        #Vehicle combobox (determines which widget is shown)
        vehicleLabel = QtGui.QLabel("&Vehicle Type:")
        self.vehicleComboBox = QtGui.QComboBox()
        vehicleLabel.setBuddy(self.vehicleComboBox)
        self.vehicleComboBox.addItems(["Car", "Van"])
        
        #Vehicle color combobox
        colorLabel = QtGui.QLabel("Co&lor:")
        self.colorComboBox = QtGui.QComboBox()
        colorLabel.setBuddy(self.colorComboBox)
        self.colorComboBox.addItems(["Black", "Blue", "Green", "Red",
                                     "Silver", "White", "Yellow"])
                                     
        #Vehicle number of seats
        seatsLabel = QtGui.QLabel("&Seats:")
        self.seatsSpinBox = QtGui.QSpinBox()
        seatsLabel.setBuddy(self.seatsSpinBox)
        self.seatsSpinBox.setRange(2, 12)
        self.seatsSpinBox.setValue(4)
        self.seatsSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        #Vehicle weight
        weightLabel = QtGui.QLabel("&Weight:")
        self.weightSpinBox = QtGui.QSpinBox()
        weightLabel.setBuddy(self.weightSpinBox)
        self.weightSpinBox.setRange(1, 8)
        self.weightSpinBox.setValue(1)
        self.weightSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.weightSpinBox.setSuffix(" tons")
        
        #Vehicle volume
        volumeLabel = QtGui.QLabel("Volu&me")
        self.volumeSpinBox = QtGui.QSpinBox()
        volumeLabel.setBuddy(self.volumeSpinBox)
        self.volumeSpinBox.setRange(4, 22)
        self.volumeSpinBox.setValue(10)
        self.volumeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.volumeSpinBox.setSuffix(" cu m")
        
        #Vehicle mileage
        mileageLabel = QtGui.QLabel("Max. Mileage")
        self.mileageLabel = QtGui.QLabel("1000 miles")
        self.mileageLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.mileageLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        
        
        #OK/Cancel buttonbox dialog
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                          QtGui.QDialogButtonBox.Cancel)

        #Stack two widgets on one another: car and van
        self.stackedWidget = QtGui.QStackedWidget()
        #Car
        carWidget = QtGui.QWidget()
        carLayout = QtGui.QGridLayout()
        carLayout.addWidget(colorLabel, 0, 0)
        carLayout.addWidget(self.colorComboBox, 0, 1)
        carLayout.addWidget(seatsLabel, 1, 0)
        carLayout.addWidget(self.seatsSpinBox, 1, 1)
        carWidget.setLayout(carLayout)
        self.stackedWidget.addWidget(carWidget)
        #Van
        vanWidget = QtGui.QWidget()
        vanLayout = QtGui.QGridLayout()
        vanLayout.addWidget(weightLabel, 0, 0)
        vanLayout.addWidget(self.weightSpinBox, 0, 1)
        vanLayout.addWidget(volumeLabel, 1, 0)
        vanLayout.addWidget(self.volumeSpinBox, 1, 1)
        vanWidget.setLayout(vanLayout)
        self.stackedWidget.addWidget(vanWidget)

        #Vehicle combobox--in common (top)
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(vehicleLabel)
        topLayout.addWidget(self.vehicleComboBox)
        #Mileage label--in common (bottom)
        bottomLayout = QtGui.QHBoxLayout()
        bottomLayout.addWidget(mileageLabel)
        bottomLayout.addWidget(self.mileageLabel)
        
        #Overall layout
        layout = QtGui.QVBoxLayout()
        layout.addLayout(topLayout) #vehicle
        layout.addWidget(self.stackedWidget) #stack
        layout.addLayout(bottomLayout) #mileage
        layout.addWidget(self.buttonBox) #button box
        self.setLayout(layout)

        #Connect signals and slots
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #Note initially in what follows didn't have [str] and it didn't work. We want
        #to send the actual value (str) not the index of the new selection.
        #http://stackoverflow.com/questions/11902109/overloaded-pyside-signals-qcombobox
        self.vehicleComboBox.currentIndexChanged[str].connect(self.setWidgetStack)
        self.weightSpinBox.valueChanged.connect(self.weightChanged)


    @QtCore.Slot(str)
    def setWidgetStack(self, text):
        if text == "Car":
            self.stackedWidget.setCurrentIndex(0)
            self.mileageLabel.setText("1000 miles")
        else:
            self.stackedWidget.setCurrentIndex(1)
            self.weightChanged(self.weightSpinBox.value())


    def weightChanged(self, amount):
        self.mileageLabel.setText("{} miles".format(8000 / amount))


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = VehicleRentalDlg()
    form.show()
    app.exec_()

