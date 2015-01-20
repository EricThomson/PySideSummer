# -*- coding: utf-8 -*-
"""
genericdelegatesPyside.py
Annotated PySide port of genericdelegates.py from Chapter 16
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Imported in carehirelogPyside.py
Imports richtextlineedit

Notes on translation:
backgroundcolorrole to backgroundrole

Same line:
color = (palette.highlight().color() if option.state & QtGui.QStyle.State_Selected
         else QtGui.QColor(index.model().data(index,  QtCore.Qt.BackgroundRole).color())) 
Previous had no .color(), was returning brush, and getting error sent up from Qt

To ask MS: he says at his site that there is a way, in qt 4.2, to set up generic delegates...Is this true?
Is this gthe jargon?

Watch his video on generic delegates first...

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

"""

from PySide import QtCore, QtGui
import richtextlineeditPyside


   
class GenericDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}

    def insertColumnDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate

    def removeColumnDelegate(self, column):
        if column in self.delegates:
            del self.delegates[column]

    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QtGui.QStyledItemDelegate.paint(self, painter, option, index)

    def createEditor(self, parent, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QtGui.QStyledItemDelegate.createEditor(self, parent, option,
                                                    index)

    def setEditorData(self, editor, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QtGui.QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QtGui.QStyledItemDelegate.setModelData(self, editor, model, index)


class IntegerColumnDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum

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


class DateColumnDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, minimum=QtCore.QDate(),
                 maximum=QtCore.QDate.currentDate(),
                 dateFormat="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = dateFormat

    def createEditor(self, parent, option, index):
        dateedit = QtGui.QDateEdit(parent)
        dateedit.setDateRange(self.minimum, self.maximum)
        dateedit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        dateedit.setDisplayFormat(self.format)
        dateedit.setCalendarPopup(True)
        return dateedit

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setDate(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.date())


class PlainTextColumnDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(PlainTextColumnDelegate, self).__init__(parent)


    def createEditor(self, parent, option, index):
        lineedit = QtGui.QLineEdit(parent)
        return lineedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setText(value)


    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())


class RichTextColumnDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(RichTextColumnDelegate, self).__init__(parent)


    def paint(self, painter, option, index):
        text = index.model().data(index, QtCore.Qt.DisplayRole)
        palette = QtGui.QApplication.palette()
        document = QtGui.QTextDocument()
        document.setDefaultFont(option.font)
        if option.state & QtGui.QStyle.State_Selected:
            document.setHtml("<font color={}>{}</font>".format(
                    palette.highlightedText().color().name(), text))
        else:
            document.setHtml(text)
        painter.save()
        #if state is selected, highlight color else background color
        color = (palette.highlight().color() if option.state & QtGui.QStyle.State_Selected
                 else QtGui.QColor(index.model().data(index,  QtCore.Qt.BackgroundRole).color())) #index.model().data(index, QtCore.Qt.BackgroundRole)))
                 
 
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)
        painter.restore()


    def sizeHint(self, option, index):
        text = index.model().data(index)
        document = QtGui.QTextDocument()
        document.setDefaultFont(option.font)
        document.setHtml(text)
        return QtCore.QSize(document.idealWidth() + 5,
                     option.fontMetrics.height())


    def createEditor(self, parent, option, index):
        lineedit = richtextlineeditPyside.RichTextLineEdit(parent)
        return lineedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setHtml(value)


    def setModelData(self, editor, model, index):
        model.setData(index, editor.toSimpleHtml())


