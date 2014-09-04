# -*- coding: utf-8 -*-
"""
customdraganddropPyside.py
Annotated PySide port of customdraganddrop.pyw from Chapter 10
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Shows how to drag and drop a custom MIME type.

----            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import os
import sys
from PySide import QtGui, QtCore

class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent) 
        self.create_widgets()
        self.layout_widgets()
        self.setWindowTitle("Custom Drag and Drop")


    def create_widgets(self):
        #Drag/drop list initially populated
        self.dndListWidget = DnDListWidget()
        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QtGui.QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QtGui.QIcon(os.path.join(path,
                                   "images/{0}".format(image))))
                self.dndListWidget.addItem(item)
        #unpopulated drag 'n' drop list widget, put in icon mode
        self.dndIconListWidget = DnDListWidget()
        self.dndIconListWidget.setViewMode(QtGui.QListWidget.IconMode)
        #The drag-n-drop widget panel
        self.dndWidget = DnDWidget("Drag to me!")
        #Line to drop, not drag, stuff from
        self.dropLineEdit = DropLineEdit()


    def layout_widgets(self):
        layout = QtGui.QGridLayout()
        layout.addWidget(self.dndListWidget, 0, 0)
        layout.addWidget(self.dndIconListWidget, 0, 1)
        layout.addWidget(self.dndWidget, 1, 0)
        layout.addWidget(self.dropLineEdit, 1, 1)
        self.setLayout(layout)
        


#drag and drop list widget (left top: list view, right top: icon view)
class DnDListWidget(QtGui.QListWidget):

    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            text = stream.readQString()
            #print "dropEvent DnDList text and type(text) \n", text, type(text), "\n"
            icon = QtGui.QIcon()
            stream >> icon
            item = QtGui.QListWidgetItem(text, self)
            item.setIcon(icon)
            event.setDropAction(QtCore.Qt.MoveAction)  #this is sent to startDrag
            event.accept()
        else:
            event.ignore()

    def startDrag(self, dropActions):
        item = self.currentItem()
        icon = item.icon()
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream << icon
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QtCore.QPoint(12, 12))
        drag.setPixmap(pixmap)
        #changed .start() to .exec_()
        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            self.takeItem(self.row(item))


#Custom widget for dragging/dropping x-icon-and-text data (bottom left)
class DnDWidget(QtGui.QWidget):
    def __init__(self, text, icon=QtGui.QIcon(), parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setAcceptDrops(True)
        #print text
        self.text = text
        self.icon = icon

    def minimumSizeHint(self):
        fm = QtGui.QFontMetricsF(self.font())
        if self.icon.isNull():
            return QtCore.QSize(fm.width(self.text), fm.height() * 1.5)
        return QtCore.QSize(34 + fm.width(self.text), max(34, fm.height() * 1.5))

    def paintEvent(self, event):
        height = QtGui.QFontMetricsF(self.font()).height()
        painter = QtGui.QPainter(self)
        #should the following two be bitwise orred?
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.fillRect(self.rect(), QtGui.QColor(QtCore.Qt.yellow).lighter())
        if self.icon.isNull():
            painter.drawText(10, height, self.text)
        else:
            #print "paintEvent  text and type(text) \n", self.text, type(self.text), "\n"
            pixmap = self.icon.pixmap(24, 24)
            painter.drawPixmap(0, 5, pixmap)
            painter.drawText(34, height,
                             self.text + " (Drag to or from me!)")
                                
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            self.text = stream.readQString()
            self.icon = QtGui.QIcon()
            stream >> self.icon
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            self.updateGeometry()
            #print "dropEvent self.text: ", self.text
            self.update()
        else:
            event.ignore()
              
    #this is activated with mouse click+move
    def mouseMoveEvent(self, event):
        self.startDrag()
        QtGui.QWidget.mouseMoveEvent(self, event)

    def startDrag(self):
        icon = self.icon
        if icon.isNull():
            return
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream.writeQString(self.text)
        stream << icon
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QtCore.QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.start(QtCore.Qt.CopyAction)



#bottom right, just drop text, not icon, and no dragging
class DropLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent) 
        self.setAcceptDrops(True)  

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text") #extract data
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly) #create datastream to read data
            #note this one doesn't pull icon data 
            text = stream.readQString()
            self.setText(text)  #sets text in QLineEdit
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
