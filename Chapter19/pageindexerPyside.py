# coding: utf-8
"""
pageindexerPyside.py
Annotated PySide adaptation of pageindexer.py from Chapter 19
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import collections
import sys
from PySide import QtGui, QtCore
import walkerPyside as walker


class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.lock = QtCore.QReadWriteLock()
        self.path = QtCore.QDir.homePath()
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setWindowTitle("Page Indexer")


    def create_widgets(self):
        self.pathLabel = QtGui.QLabel("Indexing path:")
        self.pathResultLabel = QtGui.QLabel()
        self.pathResultLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.pathButton = QtGui.QPushButton("Set &Path...")
        self.pathButton.setAutoDefault(False)
        self.findLabel = QtGui.QLabel("&Find word:")
        self.findEdit = QtGui.QLineEdit()
        self.findLabel.setBuddy(self.findEdit)
        self.commonWordsLabel = QtGui.QLabel("&Common words:")
        self.commonWordsListWidget = QtGui.QListWidget()
        self.commonWordsLabel.setBuddy(self.commonWordsListWidget)
        self.filesLabel = QtGui.QLabel("Files containing the &word:")
        self.filesListWidget = QtGui.QListWidget()
        self.filesLabel.setBuddy(self.filesListWidget)
        self.filesIndexedLabel = QtGui.QLabel("Files indexed")
        self.filesIndexedLCD = QtGui.QLCDNumber()
        self.filesIndexedLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.wordsIndexedLabel = QtGui.QLabel("Words indexed")
        self.wordsIndexedLCD = QtGui.QLCDNumber()
        self.wordsIndexedLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.commonWordsLCDLabel = QtGui.QLabel("Common words")
        self.commonWordsLCD = QtGui.QLCDNumber()
        self.commonWordsLCD.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.statusLabel = QtGui.QLabel("Click the 'Set Path' "
                                  "button to start indexing")
        self.statusLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)


    def layout_widgets(self):
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.pathLabel)
        topLayout.addWidget(self.pathResultLabel, 1)
        topLayout.addWidget(self.pathButton)
        topLayout.addWidget(self.findLabel)
        topLayout.addWidget(self.findEdit, 1)
        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addWidget(self.filesLabel)
        leftLayout.addWidget(self.filesListWidget)
        rightLayout = QtGui.QVBoxLayout()
        rightLayout.addWidget(self.commonWordsLabel)
        rightLayout.addWidget(self.commonWordsListWidget)
        middleLayout = QtGui.QHBoxLayout()
        middleLayout.addLayout(leftLayout, 1)
        middleLayout.addLayout(rightLayout)
        bottomLayout = QtGui.QHBoxLayout()
        bottomLayout.addWidget(self.filesIndexedLabel)
        bottomLayout.addWidget(self.filesIndexedLCD)
        bottomLayout.addWidget(self.wordsIndexedLabel)
        bottomLayout.addWidget(self.wordsIndexedLCD)
        bottomLayout.addWidget(self.commonWordsLCDLabel)
        bottomLayout.addWidget(self.commonWordsLCD)
        bottomLayout.addStretch()
        layout = QtGui.QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addLayout(middleLayout)
        layout.addLayout(bottomLayout)
        layout.addWidget(self.statusLabel)
        self.setLayout(layout)


    def create_connections(self):
        self.walker = walker.Walker(self.lock, self)
        self.walker.indexed.connect(self.indexed)
        self.walker.finished.connect(self.finished)
        self.pathButton.clicked.connect(self.setPath)
        self.findEdit.returnPressed.connect(self.find)


    def setPath(self):
        self.pathButton.setEnabled(False)
        if self.walker.isRunning():
            self.walker.stop()
            self.walker.wait()
        path = QtGui.QFileDialog.getExistingDirectory(self,
                    "Choose a Path to Index", self.path)
        if not path:
            self.statusLabel.setText("Click the 'Set Path' "
                                     "button to start indexing")
            self.pathButton.setEnabled(True)
            return
        self.path = QtCore.QDir.toNativeSeparators(path)
        self.findEdit.setFocus()
        self.pathResultLabel.setText(self.path)
        self.statusLabel.clear()
        self.filesListWidget.clear()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.walker.initialize(unicode(self.path),
                self.filenamesForWords, self.commonWords)
        self.walker.start()


    def find(self):
        word = unicode(self.findEdit.text())
        if not word:
            self.statusLabel.setText("Enter a word to find in files")
            return
        self.statusLabel.clear()
        self.filesListWidget.clear()
        word = word.lower()
        if " " in word:
            word = word.split()[0]
        with QtCore.QReadLocker(self.lock):
            found = word in self.commonWords
        if found:
            self.statusLabel.setText(
                    "Common words like '{0}' are not indexed".format(word))
            return
        with QtCore.QReadLocker(self.lock):
            files = self.filenamesForWords.get(word, set()).copy()
        if not files:
            self.statusLabel.setText(
                    "No indexed file contains the word '{0}'".format(word))
            return
        files = [QtCore.QDir.toNativeSeparators(name) for name in
                 sorted(files, key=unicode.lower)]
        self.filesListWidget.addItems(files)
        self.statusLabel.setText(
                "{0} indexed files contain the word '{1}'".format(
                len(files), word))


    def indexed(self, fname):
        self.statusLabel.setText(fname)
        self.fileCount += 1
        if self.fileCount % 25 == 0:
            self.filesIndexedLCD.display(self.fileCount)
            with QtCore.QReadLocker(self.lock):
                indexedWordCount = len(self.filenamesForWords)
                commonWordCount = len(self.commonWords)
            self.wordsIndexedLCD.display(indexedWordCount)
            self.commonWordsLCD.display(commonWordCount)
        elif self.fileCount % 101 == 0:
            self.commonWordsListWidget.clear()
            with QtCore.QReadLocker(self.lock):
                words = self.commonWords.copy()
            self.commonWordsListWidget.addItems(sorted(words))


    def finished(self, completed):
        self.statusLabel.setText("Indexing complete"
                                 if completed else "Stopped")
        self.finishedIndexing()


    def reject(self):
        if self.walker.isRunning():
            self.walker.stop()
            self.finishedIndexing()
        else:
            self.accept()


    def closeEvent(self, event=None):
        self.walker.stop()
        self.walker.wait()


    def finishedIndexing(self):
        self.walker.wait()
        self.filesIndexedLCD.display(self.fileCount)
        self.wordsIndexedLCD.display(len(self.filenamesForWords))
        self.commonWordsLCD.display(len(self.commonWords))
        self.pathButton.setEnabled(True)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
