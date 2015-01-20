# -*- coding: utf-8 -*-
"""
bargrapherPyside.py
Annotated PySide port of solution to Chapter 15 exercise
bargrapher.pyw from Chapter 16
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import random
import sys
from PySide import QtGui, QtCore

class BarGraphModel(QtCore.QAbstractListModel):

    def __init__(self):
        super(BarGraphModel, self).__init__()
        self.__data = []
        self.__colors = {}
        self.minValue = 0
        self.maxValue = 0


    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.__data)


    def insertRows(self, row, count):
        extra = row + count
        if extra >= len(self.__data):
            self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
            self.__data.extend([0] * (extra - len(self.__data) + 1))
            self.endInsertRows()
            return True
        return False


    def flags(self, index):
        return (QtCore.QAbstractTableModel.flags(self, index)| QtCore.Qt.ItemIsEditable)


    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if not index.isValid() or 0 > row >= len(self.__data):
            return False
        changed = False
        if role == QtCore.Qt.DisplayRole:
            value = int(value)
            self.__data[row] = value
            if self.minValue > value:
                self.minValue = value
            if self.maxValue < value:
                self.maxValue = value
            changed = True
        elif role == QtCore.Qt.UserRole:
            self.__colors[row] = value
            self.dataChanged.emit(index, index)
            changed = True
        if changed:
            self.dataChanged.emit(index, index)
        return changed


    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if not index.isValid() or 0 > row >= len(self.__data):
            return None
        if role == QtCore.Qt.DisplayRole:
            return self.__data[row]
        if role == QtCore.Qt.UserRole:
            return self.__colors.get(row,
                    QtGui.QColor(QtCore.Qt.red))
        if role == QtCore.Qt.DecorationRole:
            color = QtGui.QColor(self.__colors.get(row,
                    QtGui.QColor(QtCore.Qt.red)))
            pixmap = QtGui.QPixmap(20, 20)
            pixmap.fill(color)
            return pixmap
        return None


class BarGraphDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(BarGraphDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum


    def paint(self, painter, option, index):
        myoption = QtGui.QStyleOptionViewItem(option)
        myoption.displayAlignment |= (QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        QtGui.QStyledItemDelegate.paint(self, painter, myoption, index)


    def createEditor(self, parent, option, index):
        spinbox = QtGui.QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return spinbox


    def setEditorData(self, editor, index):
        value = int(index.model().data(index, QtCore.Qt.DisplayRole))
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, editor.value())


class BarGraphView(QtGui.QWidget):

    WIDTH = 20

    def __init__(self, parent=None):
        super(BarGraphView, self).__init__(parent)
        self.model = None


    def setModel(self, model):
        self.model = model
        self.model.dataChanged.connect(self.update)
        self.model.modelReset.connect(self.update)

    def sizeHint(self):
        return self.minimumSizeHint()


    def minimumSizeHint(self):
        if self.model is None:
            return QtCore.QSize(BarGraphView.WIDTH * 10, 100)
        return QtCore.QSize(BarGraphView.WIDTH * self.model.rowCount(), 100)


    def paintEvent(self, event):
        if self.model is None:
            return
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        span = self.model.maxValue - self.model.minValue
        painter.setWindow(0, 0, BarGraphView.WIDTH * self.model.rowCount(),
                          span)
        for row in range(self.model.rowCount()):
            x = row * BarGraphView.WIDTH
            index = self.model.index(row)
            color = QtGui.QColor(self.model.data(index, QtCore.Qt.UserRole))
            y = int(self.model.data(index))
            painter.fillRect(x, span - y, BarGraphView.WIDTH, y, color)


class MainForm(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = BarGraphModel()
        self.barGraphView = BarGraphView()
        self.barGraphView.setModel(self.model)
        self.listView = QtGui.QListView()
        self.listView.setModel(self.model)
        self.listView.setItemDelegate(BarGraphDelegate(0, 1000, self))
        self.listView.setMaximumWidth(100)
        self.listView.setEditTriggers(QtGui.QListView.DoubleClicked|
                                      QtGui.QListView.EditKeyPressed)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.listView)
        layout.addWidget(self.barGraphView, 1)
        self.setLayout(layout)

        self.setWindowTitle("Bar Grapher")
        QtCore.QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        # Generate fake data
        count = 20
        self.model.insertRows(0, count - 1)
        for row in range(count):
            value = random.randint(1, 150)
            color = QtGui.QColor(random.randint(0, 255), random.randint(0, 255),
                           random.randint(0, 255))
            index = self.model.index(row)
            self.model.setData(index, value)
            self.model.setData(index, color, QtCore.Qt.UserRole)


app = QtGui.QApplication(sys.argv)
form = MainForm()
form.resize(600, 400)
form.show()
app.exec_()

