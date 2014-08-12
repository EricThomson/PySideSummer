# coding: utf-8
"""
findandreplacedlgPyside.py
Annotated PySide adaptation of findandreplacedlg.py from Chapter 7
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Main goal of chapter is to show how to use Qt Designer, a GUI-making GUI.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import re #https://docs.python.org/2/library/re.html
from PySide import QtGui, QtCore
import ui_findandreplacedlgPyside


class FindAndReplaceDlg(QtGui.QDialog, ui_findandreplacedlgPyside.Ui_FindAndReplaceDlg):

    found = QtCore.Signal(int)
    notfound=QtCore.Signal()
    def __init__(self, text, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.__text = text
        self.__index = 0
        self.setupUi(self)  #this is the central method in the ui-based file
        self.findButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.replaceButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.replaceAllButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.closeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.updateUi()


    def makeRegex(self):
        findText = self.findLineEdit.text()
        if self.syntaxComboBox.currentText() == "Literal":
            findText = re.escape(findText)
        flags = re.MULTILINE|re.DOTALL|re.UNICODE
        if not self.caseCheckBox.isChecked():
            flags |= re.IGNORECASE
        if self.wholeCheckBox.isChecked():
            findText = r"\b{}\b".format(findText)
        return re.compile(findText, flags)

    @QtCore.Slot(str)
    def on_findLineEdit_textEdited(self, text):
        self.__index = 0
        self.updateUi()


    @QtCore.Slot()
    def on_findButton_clicked(self):
        regex = self.makeRegex()
        match = regex.search(self.__text, self.__index)
        if match is not None:
            self.__index = match.end()
            self.found.emit(match.start)
            #check it out
            print "dir(match): ", dir(match)
            print "match: " , match
            print "match.string: ", match.string
            print "match.lastindex: " , match.lastindex            
        else:
            self.notfound.emit()  #self.emit(SIGNAL("notfound"))
        
        
    @QtCore.Slot()
    def on_replaceButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(),
                                self.__text, 1)
        

    @QtCore.Slot()
    def on_replaceAllButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(),
                                self.__text)
        

    def updateUi(self):
        enable = bool(self.findLineEdit.text())
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)


    def text(self):
        return self.__text


if __name__ == "__main__":
    import sys

    text = \
    """    US experience shows that, unlike traditional patents,
    software patents do not encourage innovation and R&D, quite the
    contrary. In particular they hurt small and medium-sized enterprises
    and generally newcomers in the market. They will just weaken the market
    and increase spending on patents and litigation, at the expense of
    technological innovation and research. Especially dangerous are
    attempts to abuse the patent system by preventing interoperability as a
    means of avoiding competition with technological ability.
    --- Extract quoted from Linus Torvalds and Alan Cox's letter
    to the President of the European Parliament
    http://www.effi.org/patentit/patents_torvalds_cox.html"""

    def foundSlot(where):
        print "type(where): ", type(where)
        print "Found at {}".format(where)

    def nomore():
        print("No more found")

    app = QtGui.QApplication(sys.argv)
    form = FindAndReplaceDlg(text)
    form.found.connect(foundSlot)
    form.notfound.connect(nomore)
    form.show()
    app.exec_()
    print "form.text(): ", form.text()

