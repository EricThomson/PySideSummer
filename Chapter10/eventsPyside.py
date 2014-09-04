# -*- coding: utf-8 -*-
"""
eventsPyside.py
Annotated PySide port of events.pyw from Chapter 10
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

A multitude of events handled in one widget. Shows how to catch tab keypress
before it is sent to the default focus-changing, by reimplementing the widget's
event method.

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtGui, QtCore

class Widget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent) 
        self.justDoubleClicked = False
        self.key = ""
        self.text = ""
        self.message = ""
        self.resize(400, 300)
        self.move(100, 100)
        self.setWindowTitle("Events")
        QtCore.QTimer.singleShot(0, self.giveHelp) # Avoids first resize msg


    def giveHelp(self):
        self.text = "Click to toggle mouse tracking,\ndouble click to reimplement double click,\n"\
                " right-click to see context menu,\n  and press various keys (even Tab) to see\n "\
                "key press events painted to screen."
        self.update()


    def closeEvent(self, event):
        print("Closed")


    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        oneAction = menu.addAction("&One")
        twoAction = menu.addAction("&Two")
        oneAction.triggered.connect(self.one)
        twoAction.triggered.connect(self.two)
        if not self.message:
            menu.addSeparator()
            threeAction = menu.addAction("Thre&e")
            threeAction.triggered.connect(self.three)
        menu.exec_(event.globalPos())  #wait you can do this?

    def one(self):
        self.message = "Menu option One"
        self.update() #built-in repaints widget (inherited from QWidget)

    def two(self):
        self.message = "You selected context menu option two."
        self.update()

    def three(self):
        self.message = "Menu option Three"
        self.update()

    #will cover painting in Chapter 11, but for now, just know that this
    #reimplementation draws appropriate text (from self.text for various
    #actions, from self.key for key press, and self.message for messages 
    #from context menu).
    def paintEvent(self, event):
        #print "paintEvent reimplementation"
        text = self.text
        i = text.find("\n\n")
        if i >= 0:
            text = text[:i]
        if self.key:
            text += "\n\nYou pressed: {}".format(self.key)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, text)
        if self.message:
            painter.drawText(self.rect(), QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter,
                             self.message)
            QtCore.QTimer.singleShot(5000, self.clearMessage) #replaced QString.clear()
            QtCore.QTimer.singleShot(5000, self.update)

    def clearMessage(self):
        self.message=""
        #print "Clearing message"

    def resizeEvent(self, event):
        self.text = "Resized to ({0}, {1})".format(
                            event.size().width(), event.size().height())
        self.update()

        
    def mouseReleaseEvent(self, event):
        #if mouse was released after double click, reset double back to false,
        #do not track mouse
        if self.justDoubleClicked:
            self.justDoubleClicked = False
        else:
            #boolean self.hasMouseTracking() value is toggled
            self.setMouseTracking(not self.hasMouseTracking())
            #print self.hasMouseTracking()
            if self.hasMouseTracking():
                self.text = u"Mouse tracking is on.\n"\
                        "Try moving the mouse!\n"\
                        "Single click to switch it off"
            else:
                self.text = u"Mouse tracking is off.\n"\
                             "Single click to switch it on"
            self.update()

    #When self.hasMouseTracking() is True
    def mouseMoveEvent(self, event):
        if not self.justDoubleClicked:
            #print "mouseMoveEvent reimplementation"
            globalPos = self.mapToGlobal(event.pos())
            self.text = "The mouse is at\n({0}, {1}) "\
                    "in widget coords, and\n"\
                    "({2}, {3}) in screen coords".format(
                    event.pos().x(), event.pos().y(), globalPos.x(),
                    globalPos.y())
            self.update()


    def mouseDoubleClickEvent(self, event):
        self.justDoubleClicked = True
        self.text = "Double-clicked."
        self.update()


    def keyPressEvent(self, event):
        self.key = ""
        if event.key() == QtCore.Qt.Key_Home:
            self.key = "Home"
        elif event.key() == QtCore.Qt.Key_End:
            self.key = "End"
        elif event.key() == QtCore.Qt.Key_PageUp:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.key = "Ctrl+PageUp"
            else:
                self.key = "PageUp"
        elif event.key() == QtCore.Qt.Key_PageDown:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.key = "Ctrl+PageDown"
            else:
                self.key = "PageDown"
        elif QtCore.Qt.Key_A <= event.key() <= QtCore.Qt.Key_Z:
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                self.key = "Shift+"
            self.key += event.text()
        #If we handle event, update window (calls repaint), otherwise
        #pass event to parent (not sure why that is needed, thought 
        #unhandled events automatically went to base class.
        if self.key:
            self.update()
        else:
            QtGui.QWidget.keyPressEvent(self, event)

    #Tab key is special (typically is used to pass control among
    #different widget elements), so need to reimplement event itself
    #to catch it first. If Tab key is pressed, update self.key, otherwise
    #pass event along to base class
    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            event.key() == QtCore.Qt.Key_Tab):
            self.key = "Tab captured in event()"
            self.update()
            return True
        return QtGui.QWidget.event(self, event)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Widget()
    form.show()
    app.exec_()
