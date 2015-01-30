# coding: utf-8
'''
newimagedlgPyside.py
Annotated PySide adaptation of newimagedlg.py from Chapter 6
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

This is imported by imagechangerPyside.py

Useful attributes of Qt to enumerate:
  PySide.QtCore.Qt.GlobalColor
  PySide.QtCore.Qt.BrushStyle
-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
'''

from PySide import QtCore, QtGui
import ui_newimagedlgPyside

#QtCore: QVariant, Qt, SIGNAL
#QtGui: QApplication, QBrush, QColorDialog, QDialog, QPainter, QPixmap)
        
class NewImageDlg(QtGui.QDialog, ui_newimagedlgPyside.Ui_NewImageDlg):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)  #imported from ui_newimagedlgPyside

        #Default color
        self.color = QtCore.Qt.red
        #Populate combobox with different patterns
        for value, text in (
                (QtCore.Qt.SolidPattern, self.tr("Solid")),
                (QtCore.Qt.Dense1Pattern, self.tr("Dense #1")),
                (QtCore.Qt.Dense2Pattern, self.tr("Dense #2")),
                (QtCore.Qt.Dense3Pattern, self.tr("Dense #3")),
                (QtCore.Qt.Dense4Pattern, self.tr("Dense #4")),
                (QtCore.Qt.Dense5Pattern, self.tr("Dense #5")),
                (QtCore.Qt.Dense6Pattern, self.tr("Dense #6")),
                (QtCore.Qt.Dense7Pattern, self.tr("Dense #7")),
                (QtCore.Qt.HorPattern, self.tr("Horizontal")),
                (QtCore.Qt.VerPattern, self.tr("Vertical")),
                (QtCore.Qt.CrossPattern, self.tr("Cross")),
                (QtCore.Qt.BDiagPattern, self.tr("Backward Diagonal")),
                (QtCore.Qt.FDiagPattern, self.tr("Forward Diagonal")),
                (QtCore.Qt.DiagCrossPattern, self.tr("Diagonal Cross"))) :
            self.brushComboBox.addItem(text, value) #second argument was: QtCore.QVariant(value)

        self.colorButton.clicked.connect(self.getColor)
        self.brushComboBox.activated.connect(self.setColor)   #int?
        self.setColor()
        self.widthSpinBox.setFocus()

    #http://srinikom.github.io/pyside-docs/PySide/QtGui/QColorDialog.html
    def getColor(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.black, self) #dialog initializes to black
        if color.isValid():
            self.color = color
            self.setColor()


    def setColor(self):
        pixmap = self._makePixmap(60, 30)
        self.colorLabel.setPixmap(pixmap)


    def image(self):
        pixmap = self._makePixmap(self.widthSpinBox.value(),
                                  self.heightSpinBox.value())
        return QtGui.QPixmap.toImage(pixmap)  #convert qpixmap to qimage


    def _makePixmap(self, width, height):  #why private?
        pixmap = QtGui.QPixmap(width, height)
        style = self.brushComboBox.itemData(
                self.brushComboBox.currentIndex())  #was: .toInt()[0]
        brush = QtGui.QBrush(self.color, QtCore.Qt.BrushStyle(style))
        painter = QtGui.QPainter(pixmap)
        painter.fillRect(pixmap.rect(), QtCore.Qt.white)
        painter.fillRect(pixmap.rect(), brush)
        return pixmap


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    form = NewImageDlg()
    form.show()
    app.exec_()

