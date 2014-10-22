# -*- coding: utf-8 -*-
"""
pythoneditorPyside.py
Annotated PySide port of pythoneditor.pyw from Chapter 13
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import os
import sys
from PySide import QtGui, QtCore
import resource_rc


__version__ = "1.0.1"


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

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                self.fileSaveAction, self.fileSaveAsAction, None,
                fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (self.editCopyAction,
                self.editCutAction, self.editPasteAction))
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      self.fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (self.editCopyAction,
                self.editCutAction, self.editPasteAction))

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
        self.fileSaveAsAction.setEnabled(
                not self.editor.document().isEmpty())
        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered"):
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
                "Python files (*.py *.pyw)")[0]
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
            self.setWindowTitle("Python Editor - {}".format(
                    QtCore.QFileInfo(self.filename).fileName()))
        except EnvironmentError as e:
            QtGui.QMessageBox.warning(self, "Python Editor -- Load Error",
                    "Failed to load {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()


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
                "Python files (*.py *.pyw)")[0]
        if filename:
            self.filename = filename
            self.setWindowTitle("Python Editor - {}".format(
                    QtCore.QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False


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
        
class PythonHighlighter(QtGui.QSyntaxHighlighter):

    Rules = []

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)
        for pattern in ((r"\band\b", r"\bas\b", r"\bassert\b",
                r"\bbreak\b", r"\bclass\b", r"\bcontinue\b",
                r"\bdef\b", r"\bdel\b", r"\belif\b", r"\belse\b",
                r"\bexcept\b", r"\bexec\b", r"\bfinally\b", r"\bfor\b",
                r"\bfrom\b", r"\bglobal\b", r"\bif\b", r"\bimport\b",
                r"\bin\b", r"\bis\b", r"\blambda\b", r"\bnot\b",
                r"\bor\b", r"\bpass\b", r"\bprint\b", r"\braise\b",
                r"\breturn\b", r"\btry\b", r"\bwhile\b", r"\bwith\b",
                r"\byield\b")):
            PythonHighlighter.Rules.append((QtCore.QRegExp(pattern),
                                           keywordFormat))
        commentFormat = QtGui.QTextCharFormat()
        commentFormat.setForeground(QtGui.QColor(0, 127, 0))
        commentFormat.setFontItalic(True)
        PythonHighlighter.Rules.append((QtCore.QRegExp(r"#.*"),
                                        commentFormat))
        self.stringFormat = QtGui.QTextCharFormat()
        self.stringFormat.setForeground(QtCore.Qt.darkYellow)
        stringRe = QtCore.QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, self.stringFormat))
        self.stringRe = QtCore.QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe,
                                        self.stringFormat))
        self.tripleSingleRe = QtCore.QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QtCore.QRegExp(r'''"""(?!')''')


    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE = range(3)

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length, format)
                i = regex.indexIn(text, i + length)

        self.setCurrentBlockState(NORMAL)
        if self.stringRe.indexIn(text) != -1:
            return
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = len(text)
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3, self.stringFormat)
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, len(text), self.stringFormat)
                
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

