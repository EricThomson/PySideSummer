# -*- coding: utf-8 -*-
"""
fractionsliderPyside.py
Annotated PySide port of fractionslider.py from Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html
 
Notes on translation:
 segColor = QtGui.QColor(QtCore.Qt.green).dark(120)--> darker
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

from __future__ import division

from PySide import QtCore, QtGui


class FractionSlider(QtGui.QWidget):

    valueChanged = QtCore.Signal(int, int)

    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"

    def __init__(self, numerator=0, denominator=10, parent=None):
        super(FractionSlider, self).__init__(parent)
        self.__numerator = numerator
        self.__denominator = denominator
        #moving wheel, clicking, or tab can move focus to slider
        #Note this does NOT mean that the mouse wheel will move the slider
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                       QtGui.QSizePolicy.Fixed))


    def decimal(self):
        return self.__numerator / float(self.__denominator)


    def fraction(self):
        return self.__numerator, self.__denominator


    def sizeHint(self):
        return self.minimumSizeHint()


    def minimumSizeHint(self):
        font = QtGui.QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QtGui.QFontMetricsF(font)
        return QtCore.QSize(fm.width(FractionSlider.WSTRING) *
                     self.__denominator,
                     (fm.height() * 4) + FractionSlider.YMARGIN)


    def setFraction(self, numerator, denominator=None):
        if denominator is not None:
            if 3 <= denominator <= 60:
                self.__denominator = denominator
            else:
                raise ValueError, "denominator out of range"
        if 0 <= numerator <= self.__denominator:
            self.__numerator = numerator
        else:
            raise ValueError, "numerator out of range"
        self.update()
        self.updateGeometry()


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QtGui.QWidget.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):
        self.moveSlider(event.x())


    def moveSlider(self, x):
        span = self.width() - (FractionSlider.XMARGIN * 2)
        offset = span - x + FractionSlider.XMARGIN
        numerator = int(round(self.__denominator *
                        (1.0 - (offset / span))))
        numerator = max(0, min(numerator, self.__denominator))
        if numerator != self.__numerator:
            self.__numerator = numerator
            self.valueChanged.emit(self.__numerator, self.__denominator)
            self.update()


    def keyPressEvent(self, event):
        change = 0
        if event.key() == QtCore.Qt.Key_Home:
            change = -self.__denominator
        elif event.key() in (QtCore.Qt.Key_Up, QtCore.Qt.Key_Right):
            change = 1
        elif event.key() == QtCore.Qt.Key_PageUp:
            change = (self.__denominator // 10) + 1
        elif event.key() in (QtCore.Qt.Key_Down, QtCore.Qt.Key_Left):
            change = -1
        elif event.key() == QtCore.Qt.Key_PageDown:
            change = -((self.__denominator // 10) + 1)
        elif event.key() == QtCore.Qt.Key_End:
            change = self.__denominator
        if change:
            numerator = self.__numerator
            numerator += change
            numerator = max(0, min(numerator, self.__denominator))
            if numerator != self.__numerator:
                self.__numerator = numerator
                self.valueChanged.emit(self.__numerator, self.__denominator)
                self.update()
            event.accept()
        else:
            QtGui.QWidget.keyPressEvent(self, event)


    def paintEvent(self, event=None):
        font = QtGui.QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QtGui.QFontMetricsF(font)
        fracWidth = fm.width(FractionSlider.WSTRING)
        indent = fm.boundingRect("9").width() / 2.0
        fracWidth *= 1.5
        span = self.width() - (FractionSlider.XMARGIN * 2)
        value = self.__numerator / float(self.__denominator)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QtGui.QPalette.Mid))
        painter.setBrush(self.palette().brush(
                QtGui.QPalette.AlternateBase))
        painter.drawRect(self.rect())
        segColor = QtGui.QColor(QtCore.Qt.green).darker(120)
        segLineColor = segColor.darker()
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(FractionSlider.XMARGIN,
                         FractionSlider.YMARGIN, span, fm.height())
        textColor = self.palette().color(QtGui.QPalette.Text)
        segWidth = span / self.__denominator
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(FractionSlider.WSTRING)
        x = FractionSlider.XMARGIN
        yOffset = segHeight + fm.height()
        for i in range(self.__denominator + 1):
            painter.setPen(segLineColor)
            painter.drawLine(x, FractionSlider.YMARGIN, x, segHeight)
            painter.setPen(textColor)
            y = segHeight
            rect = QtCore.QRectF(nRect)
            rect.moveCenter(QtCore.QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, QtCore.Qt.AlignCenter, "{}".format(i))               
            y = yOffset
            rect.moveCenter(QtCore.QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, QtCore.Qt.AlignCenter,
                             "{}".format(self.__denominator))
            painter.drawLine(QtCore.QPointF(rect.left() + indent, y),
                             QtCore.QPointF(rect.right() - indent, y))
            x += segWidth
        span = int(span)
        y = FractionSlider.YMARGIN - 0.5
        triangle = [QtCore.QPointF(value * span, y),
                    QtCore.QPointF((value * span) +
                            (2 * FractionSlider.XMARGIN), y),
                    QtCore.QPointF((value * span) +
                            FractionSlider.XMARGIN, fm.height())]
        painter.setPen(QtCore.Qt.yellow)
        painter.setBrush(QtCore.Qt.darkYellow)
        painter.drawPolygon(QtGui.QPolygonF(triangle))


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    form = QtGui.QDialog()
    sliderLabel = QtGui.QLabel("&Fraction")
    slider = FractionSlider(denominator=12)
    sliderLabel.setBuddy(slider)
    denominatorLabel = QtGui.QLabel("&Denominator")
    denominatorSpinBox = QtGui.QSpinBox()
    denominatorLabel.setBuddy(denominatorSpinBox)
    denominatorSpinBox.setRange(3, 60)
    denominatorSpinBox.setValue(slider.fraction()[1])
    denominatorSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    numeratorLabel = QtGui.QLabel("Numerator")
    numeratorLCD = QtGui.QLCDNumber()
    numeratorLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
    layout = QtGui.QGridLayout()
    layout.addWidget(sliderLabel, 0, 0)
    layout.addWidget(slider, 0, 1, 1, 5)
    layout.addWidget(numeratorLabel, 1, 0)
    layout.addWidget(numeratorLCD, 1, 1)
    layout.addWidget(denominatorLabel, 1, 2)
    layout.addWidget(denominatorSpinBox, 1, 3)
    form.setLayout(layout)

    def valueChanged(denominator):
        numerator = int(slider.decimal() * denominator)
        slider.setFraction(numerator, denominator)
        numeratorLCD.display(numerator)
        
    slider.valueChanged.connect(numeratorLCD.display)
    denominatorSpinBox.valueChanged.connect(valueChanged)
    form.setWindowTitle("Fraction Slider")
    form.show()
    app.exec_()

