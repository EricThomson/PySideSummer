# -*- coding: utf-8 -*-
"""
richtexteditPyside.py
Annotated PySide port of richtextedit.py from Chapter 13
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html
 
Simple one-line rich text editor that returns minimal html
when you close it.

Enter ctrl-k, ctrl-m and usual keyboard shortcuts to get back html, also
right-click for context menu.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import platform
import sys
from xml.sax.saxutils import escape as escape
from PySide import QtGui, QtCore

class RichTextLineEdit(QtGui.QTextEdit):

    (Bold, Italic, Underline, StrikeOut, Monospaced, Sans, Serif,
     NoSuperOrSubscript, Subscript, Superscript) = range(10)
    returnPressed = QtCore.Signal()

    def __init__(self, parent=None):
        super(RichTextLineEdit, self).__init__(parent)

        self.monofamily = "courier"
        self.sansfamily = "helvetica"
        self.seriffamily = "times"
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        fm = QtGui.QFontMetrics(self.font())
        h = int(fm.height() * (1.4 if platform.system() == "Windows"
                                   else 1.2))
        self.setMinimumHeight(h)
        self.setMaximumHeight(int(h * 1.2))
        self.setToolTip("Press <b>Ctrl+M</b> for the text effects "
                "menu and <b>Ctrl+K</b> for the color menu")

    
    def toggleItalic(self):
        self.setFontItalic(not self.fontItalic())


    def toggleUnderline(self):
        self.setFontUnderline(not self.fontUnderline())


    def toggleBold(self):
        self.setFontWeight(QtGui.QFont.Normal
                if self.fontWeight() > QtGui.QFont.Normal else QtGui.QFont.Bold)


    def sizeHint(self):
        return QtCore.QSize(self.document().idealWidth() + 5,
                     self.maximumHeight())


    def minimumSizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        return QtCore.QSize(fm.width("WWWW"), self.minimumHeight())


    def contextMenuEvent(self, event):
        self.textEffectMenu()

        
    def keyPressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            handled = False
            if event.key() == QtCore.Qt.Key_B:
                self.toggleBold()
                handled = True
            elif event.key() == QtCore.Qt.Key_I:
                self.toggleItalic()
                handled = True
            elif event.key() == QtCore.Qt.Key_K:
                self.colorMenu()
                handled = True
            elif event.key() == QtCore.Qt.Key_M:
                self.textEffectMenu()
                handled = True
            elif event.key() == QtCore.Qt.Key_U:
                self.toggleUnderline()
                handled = True
            if handled:
                event.accept()
                return
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.returnPressed.emit()
            event.accept()
        else:
            QtGui.QTextEdit.keyPressEvent(self, event)


    def colorMenu(self):
        pixmap = QtGui.QPixmap(22, 22)
        menu = QtGui.QMenu("Colour")
        for text, color in (
                ("&Black", QtCore.Qt.black),
                ("B&lue", QtCore.Qt.blue),
                ("Dark Bl&ue", QtCore.Qt.darkBlue),
                ("&Cyan", QtCore.Qt.cyan),
                ("Dar&k Cyan", QtCore.Qt.darkCyan),
                ("&Green", QtCore.Qt.green),
                ("Dark Gr&een", QtCore.Qt.darkGreen),
                ("M&agenta", QtCore.Qt.magenta),
                ("Dark Mage&nta", QtCore.Qt.darkMagenta),
                ("&Red", QtCore.Qt.red),
                ("&Dark Red", QtCore.Qt.darkRed)):
            color = QtGui.QColor(color)
            pixmap.fill(color)
            action = menu.addAction(QtGui.QIcon(pixmap), text, self.setColor)
            action.setData(color)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(
                   self.cursorRect().center()))


    def setColor(self):
        action = self.sender()
        if action is not None and isinstance(action, QtGui.QAction):
            color = QtGui.QColor(action.data())
            if color.isValid():
                self.setTextColor(color)


    def textEffectMenu(self):
        format = self.currentCharFormat()
        menu = QtGui.QMenu("Text Effect")
        for text, shortcut, data, checked in (
                ("&Bold", "Ctrl+B", RichTextLineEdit.Bold,
                 self.fontWeight() > QtGui.QFont.Normal),
                ("&Italic", "Ctrl+I", RichTextLineEdit.Italic,
                 self.fontItalic()),
                ("Strike &out", None, RichTextLineEdit.StrikeOut,
                 format.fontStrikeOut()),
                ("&Underline", "Ctrl+U", RichTextLineEdit.Underline,
                 self.fontUnderline()),
                ("&Monospaced", None, RichTextLineEdit.Monospaced,
                 format.fontFamily() == self.monofamily),
                ("&Serifed", None, RichTextLineEdit.Serif,
                 format.fontFamily() == self.seriffamily),
                ("S&ans Serif", None, RichTextLineEdit.Sans,
                 format.fontFamily() == self.sansfamily),
                ("&No super or subscript", None,
                 RichTextLineEdit.NoSuperOrSubscript,
                 format.verticalAlignment() ==
                 QtGui.QTextCharFormat.AlignNormal),
                ("Su&perscript", None, RichTextLineEdit.Superscript,
                 format.verticalAlignment() ==
                 QtGui.QTextCharFormat.AlignSuperScript),
                ("Subs&cript", None, RichTextLineEdit.Subscript,
                 format.verticalAlignment() ==
                 QtGui.QTextCharFormat.AlignSubScript)):
            action = menu.addAction(text, self.setTextEffect)
            if shortcut is not None:
                action.setShortcut(QtGui.QKeySequence(shortcut))
            action.setData(data)
            action.setCheckable(True)
            action.setChecked(checked)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(
                   self.cursorRect().center()))


    def setTextEffect(self):
        action = self.sender()
        if action is not None and isinstance(action, QtGui.QAction):
            print "setTextEffect action.data and action.data type:\n", action.data(), "\n", type(action.data())
            what = int(action.data())
            if what == RichTextLineEdit.Bold:
                self.toggleBold()
                return
            if what == RichTextLineEdit.Italic:
                self.toggleItalic()
                return
            if what == RichTextLineEdit.Underline:
                self.toggleUnderline()
                return
            format = self.currentCharFormat()
            if what == RichTextLineEdit.Monospaced:
                format.setFontFamily(self.monofamily)
            elif what == RichTextLineEdit.Serif:
                format.setFontFamily(self.seriffamily)
            elif what == RichTextLineEdit.Sans:
                format.setFontFamily(self.sansfamily)
            if what == RichTextLineEdit.StrikeOut:
                format.setFontStrikeOut(not format.fontStrikeOut())
            if what == RichTextLineEdit.NoSuperOrSubscript:
                format.setVerticalAlignment(
                        QtGui.QTextCharFormat.AlignNormal)
            elif what == RichTextLineEdit.Superscript:
                format.setVerticalAlignment(
                        QtGui.QTextCharFormat.AlignSuperScript)
            elif what == RichTextLineEdit.Subscript:
                format.setVerticalAlignment(
                        QtGui.QTextCharFormat.AlignSubScript)
            self.mergeCurrentCharFormat(format)


    def toSimpleHtml(self):
        html = ""
        black = QtGui.QColor(QtCore.Qt.black)
        block = self.document().begin()
        while block.isValid():
            iterator = block.begin()
            while iterator != block.end():
                fragment = iterator.fragment()
                if fragment.isValid():
                    format = fragment.charFormat()
                    family = format.fontFamily()
                    color = format.foreground().color()
                    text = escape(fragment.text())
                    if (format.verticalAlignment() ==
                        QtGui.QTextCharFormat.AlignSubScript):
                        text = "<sub>{}</sub>".format(text)
                    elif (format.verticalAlignment() ==
                          QtGui.QTextCharFormat.AlignSuperScript):
                        text = "<sup>{}</sup>".format(text)
                    if format.fontUnderline():
                        text = "<u>{}</u>".format(text)
                    if format.fontItalic():
                        text = "<i>{}</i>".format(text)
                    if format.fontWeight() > QtGui.QFont.Normal:
                        text = "<b>{}</b>".format(text)
                    if format.fontStrikeOut():
                        text = "<s>{}</s>".format(text)
                    if color != black or family:
                        attribs = ""
                        if color != black:
                            attribs += ' color="{}"'.format(color.name())
                        if family:
                            attribs += ' face="{}"'.format(family)
                        text = "<font{}>{}</font>".format(attribs, text)
                    html += text
                iterator += 1
            block = block.next()
        return html


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    lineedit = RichTextLineEdit()
    lineedit.show()
    lineedit.setWindowTitle("RichTextEdit")
    app.exec_()
    print(lineedit.toHtml())
    print(lineedit.toPlainText())
    print(lineedit.toSimpleHtml())


