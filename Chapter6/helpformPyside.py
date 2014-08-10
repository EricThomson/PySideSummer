# coding: utf-8
'''
helpformPyside.py
Annotated PySide adaptation of helpform.py from Chapter 6
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

This is imported by imagechangerPyside.py

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
'''
from PySide import QtGui, QtCore
import resource_rc

#QtCore: QUrl, Qt, SIGNAL, SLOT
#QtGui: QAction, QApplication, QDialog, QIcon,
#        QKeySequence, QLabel, QTextBrowser, QToolBar, QVBoxLayout

class HelpForm(QtGui.QDialog):

    def __init__(self, page, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_GroupLeader)

        backAction = QtGui.QAction(QtGui.QIcon(":/back.png"), "&Back", self)
        backAction.setShortcut(QtGui.QKeySequence.Back)
        homeAction = QtGui.QAction(QtGui.QIcon(":/home.png"), "&Home", self)
        homeAction.setShortcut("Home")
        self.pageLabel = QtGui.QLabel()

        toolBar = QtGui.QToolBar()
        toolBar.addAction(backAction)
        toolBar.addAction(homeAction)
        toolBar.addWidget(self.pageLabel)
        self.textBrowser = QtGui.QTextBrowser()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(toolBar)
        layout.addWidget(self.textBrowser, 1)
        self.setLayout(layout)
        
        backAction.triggered.connect(self.textBrowser.backward)
        homeAction.triggered.connect(self.textBrowser.home)
        self.textBrowser.sourceChanged[QtCore.QUrl].connect(self.updatePageTitle)  #not sure if qurl needed


        self.textBrowser.setSearchPaths([":/help"])
        self.textBrowser.setSource(QtCore.QUrl(page))
        self.resize(400, 600)
        self.setWindowTitle("{0} Help".format(
                QtGui.QApplication.applicationName()))


    def updatePageTitle(self):
        self.pageLabel.setText(self.textBrowser.documentTitle())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    form = HelpForm("index.html")
    form.show()
    app.exec_()

