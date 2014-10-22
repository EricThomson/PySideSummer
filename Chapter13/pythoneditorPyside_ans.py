# -*- coding: utf-8 -*-
"""
pythoneditorPyside_ans.py
Annotated PySide port of pythoneditor_ans.py from Chapter 14
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Note, unlike all the other chapters in PySide Summer, I did not do this
solution on my own. I was lazy and just used Summerfield's.

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import os
import sys
from PySide import QtGui, QtCore
import resource_rc

# from PyQt4.QtCore import (QtCore.QEvent, QtCore.QFile, QtCore.QFileInfo, QtCore.QIODevice, QtCore.QRegExp,
        # QtCore.QTextStream, Qt)
# from PyQt4.QtCore import pyqtSignal as Signal
# from PyQt4.QtGui import (QtGui.QAction, QApplication, QtGui.QColor, QtGui.QCursor,
        # QtGui.QFileDialog, QtGui.QFont, QtGui.QIcon, QtGui.QKeySequence, QtGui.QMainWindow,
        # QtGui.QMessageBox, QtGui.QSyntaxHighlighter, QtGui.QTextCharFormat, QtGui.QTextCursor,
        # QtGui.QTextEdit)
		
__version__ = "1.1.0"


class PythonHighlighter(QtGui.QSyntaxHighlighter):

    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = ["and", "as", "assert", "break", "class",
                "continue", "def", "del", "elif", "else", "except",
                "exec", "finally", "for", "from", "global", "if",
                "import", "in", "is", "lambda", "not", "or", "pass",
                "print", "raise", "return", "try", "while", "with",
                "yield"]
        BUILTINS = ["abs", "all", "any", "basestring", "bool",
                "callable", "chr", "classmethod", "cmp", "compile",
                "complex", "delattr", "dict", "dir", "divmod",
                "enumerate", "eval", "execfile", "exit", "file",
                "filter", "float", "frozenset", "getattr", "globals",
                "hasattr", "hex", "id", "int", "isinstance",
                "issubclass", "iter", "len", "list", "locals", "map",
                "max", "min", "object", "oct", "open", "ord", "pow",
                "property", "range", "reduce", "repr", "reversed",
                "round", "set", "setattr", "slice", "sorted",
                "staticmethod", "str", "sum", "super", "tuple", "type",
                "vars", "zip"] 
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QtCore.QRegExp(
                "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                "keyword"))
        PythonHighlighter.Rules.append((QtCore.QRegExp(
                "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                "builtin"))
        PythonHighlighter.Rules.append((QtCore.QRegExp(
                "|".join([r"\b%s\b" % constant
                for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QtCore.QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                "number"))
        PythonHighlighter.Rules.append((QtCore.QRegExp(
                r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QtCore.QRegExp(r"\b@\w+\b"),
                "decorator"))
        stringRe = QtCore.QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QtCore.QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QtCore.QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QtCore.QRegExp(r'''"""(?!')''')


    @staticmethod
    def initializeFormats():
        baseFormat = QtGui.QTextCharFormat()
        baseFormat.setFontFamily("courier")
        baseFormat.setFontPointSize(12)
        for name, color in (("normal", QtCore.Qt.black),
                ("keyword", QtCore.Qt.darkBlue), ("builtin", QtCore.Qt.darkRed),
                ("constant", QtCore.Qt.darkGreen),
                ("decorator", QtCore.Qt.darkBlue), ("comment", QtCore.Qt.darkGreen),
                ("string", QtCore.Qt.darkYellow), ("number", QtCore.Qt.darkMagenta),
                ("error", QtCore.Qt.darkRed), ("pyqt", QtCore.Qt.darkCyan)):
            format = QtGui.QTextCharFormat(baseFormat)
            format.setForeground(QtGui.QColor(color))
            if name in ("keyword", "decorator"):
                format.setFontWeight(QtGui.QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format


    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = len(text)
        prevState = self.previousBlockState()

        self.setFormat(0, textLength,
                       PythonHighlighter.Formats["normal"])

        if text.startswith("Traceback") or text.startswith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return
        if (prevState == ERROR and
            not (text.startswith(sys.ps1) or text.startswith("#"))):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length,
                               PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QtCore.QRegExp(r"#.*"), "comment"))
        if not text:
            pass
        elif text[0] == "#":
            self.setFormat(0, len(text),
                           PythonHighlighter.Formats["comment"])
        else:
            stack = []
            for i, c in enumerate(text):
                if c in ('"', "'"):
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c == "#" and len(stack) == 0:
                    self.setFormat(i, len(text),
                                   PythonHighlighter.Formats["comment"])
                    break

        self.setCurrentBlockState(NORMAL)

        if self.stringRe.indexIn(text) != -1:
            return
        # This is fooled by triple quotes inside single quoted strings
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = len(text)
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3,     
                               PythonHighlighter.Formats["string"])
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, len(text),
                               PythonHighlighter.Formats["string"])


    def rehighlight(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(
                                                    QtCore.Qt.WaitCursor))
        QtGui.QSyntaxHighlighter.rehighlight(self)
        QtGui.QApplication.restoreOverrideCursor()


class TextEdit(QtGui.QTextEdit):

    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)


    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            event.key() == QtCore.Qt.Key_Tab):
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
        return QtGui.QTextEdit.event(self, event)


class MainWindow(QtGui.QMainWindow):

    def __init__(self, filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        font = QtGui.QFont("Courier", 11)
        font.setFixedPitch(True)
        self.editor = TextEdit()
        self.editor.setFont(font)
        self.highlighter = PythonHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction("&New...", self.fileNew,
                QtGui.QKeySequence.New, "filenew", "Create a Python file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QtGui.QKeySequence.Open, "fileopen",
                "Open an existing Python file")
        self.fileSaveAction = self.createAction("&Save", self.fileSave,
                QtGui.QKeySequence.Save, "filesave", "Save the file")
        self.fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the file using a new name")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        self.editCopyAction = self.createAction("&Copy",
                self.editor.copy, QtGui.QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        self.editCutAction = self.createAction("Cu&t", self.editor.cut,
                QtGui.QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        self.editPasteAction = self.createAction("&Paste",
                self.editor.paste, QtGui.QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")
        self.editIndentAction = self.createAction("&Indent",
                self.editIndent, "Ctrl+]", "editindent",
                "Indent the current line or selection")
        self.editUnindentAction = self.createAction("&Unindent",
                self.editUnindent, "Ctrl+[", "editunindent",
                "Unindent the current line or selection")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                self.fileSaveAction, self.fileSaveAsAction, None,
                fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (self.editCopyAction,
                self.editCutAction, self.editPasteAction, None,
                self.editIndentAction, self.editUnindentAction))
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      self.fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (self.editCopyAction,
                self.editCutAction, self.editPasteAction, None,
                self.editIndentAction, self.editUnindentAction))


        self.editor.selectionChanged.connect(self.updateUi)
        self.editor.document().modificationChanged.connect(self.updateUi)
        QtGui.QApplication.clipboard().dataChanged.connect(self.updateUi)

        self.resize(800, 600)
        self.setWindowTitle("Python Editor")
        self.filename = filename
        if self.filename is not None:
            self.loadFile()
        self.updateUi()


    def updateUi(self, arg=None):
        self.fileSaveAction.setEnabled(
                self.editor.document().isModified())
        enable = not self.editor.document().isEmpty()
        self.fileSaveAsAction.setEnabled(enable)
        self.editIndentAction.setEnabled(enable)
        self.editUnindentAction.setEnabled(enable)
        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        if not self.okToContinue():
            event.ignore()


    def okToContinue(self):
        if self.editor.document().isModified():
            reply = QtGui.QMessageBox.question(self,
                            "Python Editor - Unsaved Changes",
                            "Save unsaved changes?",
                            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|
                            QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                return self.fileSave()
        return True


    def fileNew(self):
        if not self.okToContinue():
            return
        document = self.editor.document()
        document.clear()
        document.setModified(False)
        self.filename = None
        self.setWindowTitle("Python Editor - Unnamed")
        self.updateUi()


    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        fname = QtGui.QFileDialog.getOpenFileName(self,
                "Python Editor - Choose File", dir,
                "Python files (*.py *.pyw)")
        if fname:
            self.filename = fname
            self.loadFile()


    def loadFile(self):
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setCodec("UTF-8")
            self.editor.setPlainText(stream.readAll())
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QtGui.QMessageBox.warning(self, "Python Editor -- Load Error",
                    "Failed to load {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle("Python Editor - {}".format(
                QtCore.QFileInfo(self.filename).fileName()))


    def fileSave(self):
        if self.filename is None:
            return self.fileSaveAs()
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QtGui.QMessageBox.warning(self, "Python Editor -- Save Error",
                    "Failed to save {}: {}".format(self.filename, e))
            return False
        finally:
            if fh is not None:
                fh.close()
        return True


    def fileSaveAs(self):
        filename = self.filename if self.filename is not None else "."
        filename = QtGui.QFileDialog.getSaveFileName(self,
                "Python Editor -- Save File As", filename,
                "Python files (*.py *.pyw)")
        if filename:
            self.filename = filename
            self.setWindowTitle("Python Editor - {}".format(
                    QtCore.QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False


    def editIndent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()
            cursor.setPosition(pos)
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            while pos <= end:
                cursor.insertText("    ")
                cursor.movePosition(QtGui.QTextCursor.Down)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                QtGui.QTextCursor.KeepAnchor, end - start)
        else:
            pos = cursor.position()
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            cursor.insertText("    ")
            cursor.setPosition(pos + 4)
        cursor.endEditBlock()


    def editUnindent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.setPosition(pos)
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            while pos <= end:
                cursor.clearSelection()
                cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                    QtGui.QTextCursor.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QtGui.QTextCursor.Down)
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                QtGui.QTextCursor.KeepAnchor, end - start)
        else:
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                QtGui.QTextCursor.KeepAnchor, 4)
            if cursor.selectedText() == "    ":
                cursor.removeSelectedText()
        cursor.endEditBlock()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    form = MainWindow(fname)
    form.show()
    app.exec_()


main()

