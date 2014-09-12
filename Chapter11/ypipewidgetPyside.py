# -*- coding: utf-8 -*-
"""
ypipewidgetPyside.py
Annotated PySide port of ypipewidget.py from Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Notes on translation: 
1. Polygon draw did not work, had to change list of floats to list of QPoints.
  drawPolygon(QtGui.QPolygon([x1,x2])) ---> drawPolygon(QtGui.QPolygon([QtCore.QPoint(x1, x2)])
For more, see README.md for Chapter 11. 
 
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

from PySide import QtGui, QtCore


class YPipeWidget(QtGui.QWidget):

    value_changed = QtCore.Signal(int, int)

    def __init__(self, leftFlow=0, rightFlow=0, maxFlow=100,
                 parent=None):
        QtGui.QWidget.__init__(self, parent)

        #Left to pick red liquid
        self.leftSpinBox = QtGui.QSpinBox(self)
        self.leftSpinBox.setRange(0, maxFlow)
        self.leftSpinBox.setValue(leftFlow)
        self.leftSpinBox.setSuffix(" L/s")
        self.leftSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.leftSpinBox.valueChanged.connect(self.valueChanged)

        #Right to pick blue liquid
        self.rightSpinBox = QtGui.QSpinBox(self)
        self.rightSpinBox.setRange(0, maxFlow)
        self.rightSpinBox.setValue(rightFlow)
        self.rightSpinBox.setSuffix(" L/s")
        self.rightSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.rightSpinBox.valueChanged.connect(self.valueChanged)

        #Create label for combination of read and liquid (bottom of Widget)
        self.label = QtGui.QLabel(self)
        self.label.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        fm = QtGui.QFontMetricsF(self.font())
        self.label.setMinimumWidth(fm.width(" 999 L/s "))

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding))                  
        self.setMinimumSize(self.minimumSizeHint())
        self.valueChanged()

    def valueChanged(self):
        a = self.leftSpinBox.value()
        b = self.rightSpinBox.value()
        self.label.setText("{0} L/s".format(a + b))
        self.value_changed.emit(a, b)
        self.update() #repaint (calls paintEvent)

    def values(self):
        return self.leftSpinBox.value(), self.rightSpinBox.value()

    def minimumSizeHint(self):
        return QtCore.QSize(self.leftSpinBox.width() * 3,
                     self.leftSpinBox.height() * 5)

    def resizeEvent(self, event=None):
        fm = QtGui.QFontMetricsF(self.font())
        x = (self.width() - self.label.width()) / 2
        y = self.height() - (fm.height() * 1.5)
        self.label.move(x, y)
        y = self.height() / 60.0
        x = (self.width() / 4.0) - self.leftSpinBox.width()
        self.leftSpinBox.move(x, y)
        x = self.width() - (self.width() / 4.0)
        self.rightSpinBox.move(x, y)

    def paintEvent(self, event=None):
        LogicalSize = 100.0

        def logicalFromPhysical(length, side):
            return (length / side) * LogicalSize
        
        fm = QtGui.QFontMetricsF(self.font())
        ymargin = ((LogicalSize / 30.0) +
                   logicalFromPhysical(self.leftSpinBox.height(),
                                       self.height()))
        ymax = (LogicalSize -
                logicalFromPhysical(fm.height() * 2, self.height()))
        width = LogicalSize / 4.0
        cx, cy = LogicalSize / 2.0, LogicalSize / 3.0
        ax, ay = cx - (2 * width), ymargin
        bx, by = cx - width, ay
        dx, dy = cx + width, ay
        ex, ey = cx + (2 * width), ymargin
        fx, fy = cx + (width / 2), cx + (LogicalSize / 24.0)
        gx, gy = fx, ymax
        hx, hy = cx - (width / 2), ymax
        ix, iy = hx, fy

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        side = min(self.width(), self.height())
        painter.setViewport((self.width() - side) / 2,
                            (self.height() - side) / 2, side, side)
        painter.setWindow(0, 0, LogicalSize, LogicalSize)

        painter.setPen(QtCore.Qt.NoPen)

        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0),
                                         QtCore.QPointF(0, 100))
                                         
        #Draw left branch
        gradient.setColorAt(0, QtCore.Qt.white)
        a = self.leftSpinBox.value()
        gradient.setColorAt(1, (QtCore.Qt.red if a != 0 else QtCore.Qt.white))
        painter.setBrush(QtGui.QBrush(gradient))   
        #print "ax, type(ax):\n", ax, "," , type(ax)
        #print "QPoint(ax), type(QtCore.QPoint(ax)):\n", QtCore.QPoint(ax, ay), "," , type(QtCore.QPoint(ax, ay))
        
        polyCoordsLeft = [QtCore.QPoint(ax, ay), QtCore.QPoint(bx, by), QtCore.QPoint(cx, cy), QtCore.QPoint(ix, iy)]    
        #print polyInputs1
        painter.drawPolygon(QtGui.QPolygon(polyCoordsLeft))

        #Draw right branch
        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 100))
        gradient.setColorAt(0, QtCore.Qt.white)
        b = self.rightSpinBox.value()
        gradient.setColorAt(1, (QtCore.Qt.blue if b != 0
                                else QtCore.Qt.white))
        painter.setBrush(QtGui.QBrush(gradient))
        
        polyCoordsRight=[QtCore.QPoint(cx, cy), QtCore.QPoint(dx, dy), QtCore.QPoint(ex, ey), QtCore.QPoint(fx, fy)]  
        painter.drawPolygon(QtGui.QPolygon(polyCoordsRight))

        #Draw central branch
        if (a + b) == 0:
            color = QtGui.QColor(QtCore.Qt.white)
        else:
            ashare = (float(a) / (a + b)) * 255.0  #or could use future division
            bshare = 255.0 - ashare
            #print "paintEvent (a,b): ({0}, {1})".format(a,b)   
            #print "paintEvent: (ashare, bshare) = (", ashare, ",", bshare, ")"
            color = QtGui.QColor(ashare, 0, bshare)
        #print "paintEvent: color=", color
        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 100))
        gradient.setColorAt(0, QtCore.Qt.white)
        gradient.setColorAt(1, color)
        painter.setBrush(QtGui.QBrush(gradient))
        polyCoordsMiddle=[QtCore.QPoint(cx, cy), QtCore.QPoint(fx, fy), QtCore.QPoint(gx, gy),\
                          QtCore.QPoint(hx, hy) , QtCore.QPoint(ix, iy)]
        painter.drawPolygon(QtGui.QPolygon(polyCoordsMiddle))

        #Outline pipe edges
        painter.setPen(QtCore.Qt.black)
        lineCoordsLeft = [QtCore.QPoint(ax, ay), QtCore.QPoint(ix, iy), QtCore.QPoint(hx, hy)]
        lineCoordsRight = [QtCore.QPoint(gx, gy), QtCore.QPoint(fx, fy), QtCore.QPoint(ex, ey)] 
        lineCoordsMiddle = [QtCore.QPoint(bx, by), QtCore.QPoint(cx, cy), QtCore.QPoint(dx, dy)] 
        painter.drawPolyline(QtGui.QPolygon(lineCoordsLeft))
        painter.drawPolyline(QtGui.QPolygon(lineCoordsRight))
        painter.drawPolyline(QtGui.QPolygon(lineCoordsMiddle))


if __name__ == "__main__":
    import sys

    def printValues(a, b):
        print(a, b)

    app = QtGui.QApplication(sys.argv)
    form = YPipeWidget()
    form.value_changed.connect(printValues)
    form.setWindowTitle("YPipe Flows")
    form.move(0, 0)
    form.show()
    form.resize(400, 400)
    app.exec_()

