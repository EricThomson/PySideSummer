# coding: utf-8
"""
resizedlgPyside.py
Resizing dialog for Image Changer.

One aspect of a solution to the exercise in Chapter 6 of 
Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Note Summerfield provides a slightly different solution on his web site

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

"""

from PySide import QtGui, QtCore
import sys

class ResizeDlg(QtGui.QDialog):
    def __init__(self, width, height, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Resize dialog")
        self.height=int(height)
        self.width=int(width)

        maxWidth=self.width*4
        maxHeight=self.height*4
        #Width
        widthLabel=QtGui.QLabel("&Width:")
        self.widthSpinbox=QtGui.QDoubleSpinBox()
        self.widthSpinbox.setRange(4, maxWidth)
        self.widthSpinbox.setValue(width)
        self.widthSpinbox.setDecimals(0)
        widthLabel.setBuddy(self.widthSpinbox)
        #Height
        heightLabel=QtGui.QLabel("&Height:")
        self.heightSpinbox=QtGui.QDoubleSpinBox()
        self.heightSpinbox.setRange(4, maxHeight)
        self.heightSpinbox.setValue(height)
        self.heightSpinbox.setDecimals(0)
        heightLabel.setBuddy(self.heightSpinbox)
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept) #accepted goes with OK automatically (reimplement accept)
        buttonBox.rejected.connect(self.reject) #rejected goes with cancel automatically
        
        #Layout
        layout=QtGui.QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinbox,0,1)
        layout.addWidget(heightLabel,1,0)
        layout.addWidget(self.heightSpinbox, 1,1)
        layout.addWidget(buttonBox, 2, 1, 2)
        self.setLayout(layout)
      
    def accept(self):
        self.width = int(self.widthSpinbox.value())
        self.height = int(self.heightSpinbox.value())
        QtGui.QDialog.accept(self)  #calling base classes accept method (what will be returned to exec_)

    def result(self):
        return self.width, self.height
    
    
    

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    sizeDialog=ResizeDlg(100,100)
    sizeDialog.show()
    if sizeDialog.exec_():
        print "Done", sizeDialog.result()  #dialog is hidden, not deleted, so can still get attributes
        print sizeDialog.width
    else:
        print "Cancelled"
  
    
    
    