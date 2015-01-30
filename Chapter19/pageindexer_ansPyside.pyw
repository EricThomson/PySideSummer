# coding: utf-8
"""
pageindexer_ansPyside.py
Annotated PySide adaptation of pageindexer_ans.py from Chapter 19
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import collections
import os
import sys
from Shiboken import shiboken
from PySide import QtCore, QtGui

import walker_ansPyside as walker


def isAlive(qobj):
    return shiboken.isValid(qobj)          
    
class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.mutex = QtCore.QMutex()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        self.lock = QtCore.QReadWriteLock()
        self.path = QtCore.QDir.homePath()
        self.walkers = []
        self.completed = []
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
        self.pathButton.clicked.connect(self.setPath)
        self.findEdit.returnPressed.connect(self.find)


    def stopWalkers(self):
        for walkerInstance in self.walkers:
            if isAlive(walkerInstance) and walkerInstance.isRunning():
                walkerInstance.stop()
        for walkerInstance in self.walkers:
            if isAlive(walkerInstance) and walkerInstance.isRunning():
                walkerInstance.wait()
        self.walkers = []
        self.completed = []


    def setPath(self):
        self.stopWalkers()
        self.pathButton.setEnabled(False)
        path = QtGui.QFileDialog.getExistingDirectory(self,
                    "Choose a Path to Index", self.path)
        if not path:
            self.statusLabel.setText("Click the 'Set Path' "
                                     "button to start indexing")
            self.pathButton.setEnabled(True)
            return
        self.statusLabel.setText("Scanning directories...")
        QtGui.QApplication.processEvents() # Needed for Windows
        self.path = QtCore.QDir.toNativeSeparators(path)
        self.findEdit.setFocus()
        self.pathResultLabel.setText(self.path)
        self.statusLabel.clear()
        self.filesListWidget.clear()
        self.fileCount = 0
        self.filenamesForWords = collections.defaultdict(set)
        self.commonWords = set()
        nofilesfound = True
        files = []
        index = 0
        for root, dirs, fnames in os.walk(unicode(self.path)):
            for name in [name for name in fnames
                         if name.endswith((".htm", ".html"))]:
                files.append(os.path.join(root, name))
                if len(files) == 1000:
                    self.processFiles(index, files[:])
                    files = []
                    index += 1
                    nofilesfound = False
        if files:
            self.processFiles(index, files[:])
            nofilesfound = False
        if nofilesfound:
            self.finishedIndexing()
            self.statusLabel.setText(
                    "No HTML files found in the given path")


    def processFiles(self, index, files):
        thread = walker.Walker(index, self.lock, files,
                self.filenamesForWords, self.commonWords, self)
        thread.indexed.connect(self.indexed)
        thread.finished.connect(self.finished)
        thread.finished.connect(thread.deleteLater)
        self.walkers.append(thread)
        self.completed.append(False)
        thread.start()
        thread.wait(300) # Needed for Windows


    def find(self):
        word = unicode(self.findEdit.text())
        if not word:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Enter a word to find in files")
            finally:
                self.mutex.unlock()
            return
        try:
            self.mutex.lock()
            self.statusLabel.clear()
            self.filesListWidget.clear()
        finally:
            self.mutex.unlock()
        word = word.lower()
        if " " in word:
            word = word.split()[0]
        try:
            self.lock.lockForRead()
            found = word in self.commonWords
        finally:
            self.lock.unlock()
        if found:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Common words like '{0}' "
                        "are not indexed".format(word))
            finally:
                self.mutex.unlock()
            return
        try:
            self.lock.lockForRead()
            files = self.filenamesForWords.get(word, set()).copy()
        finally:
            self.lock.unlock()
        if not files:
            try:
                self.mutex.lock()
                self.statusLabel.setText("No indexed file contains "
                        "the word '{0}'".format(word))
            finally:
                self.mutex.unlock()
            return
        files = [QtCore.QDir.toNativeSeparators(name) for name in
                 sorted(files, key=unicode.lower)]
        try:
            self.mutex.lock()
            self.filesListWidget.addItems(files)
            self.statusLabel.setText(
                    "{0} indexed files contain the word '{1}'".format(
                    len(files), word))
        finally:
            self.mutex.unlock()


    def indexed(self, fname, index):
        try:
            self.mutex.lock()
            self.statusLabel.setText(fname)
            self.fileCount += 1
            count = self.fileCount
        finally:
            self.mutex.unlock()
        if count % 25 == 0:
            try:
                self.lock.lockForRead()
                indexedWordCount = len(self.filenamesForWords)
                commonWordCount = len(self.commonWords)
            finally:
                self.lock.unlock()
            try:
                self.mutex.lock()
                self.filesIndexedLCD.display(count)
                self.wordsIndexedLCD.display(indexedWordCount)
                self.commonWordsLCD.display(commonWordCount)
            finally:
                self.mutex.unlock()
        elif count % 101 == 0:
            try:
                self.lock.lockForRead()
                words = self.commonWords.copy()
            finally:
                self.lock.unlock()
            try:
                self.mutex.lock()
                self.commonWordsListWidget.clear()
                self.commonWordsListWidget.addItems(sorted(words))
            finally:
                self.mutex.unlock()


    def finished(self, completed, index):
        done = False
        if self.walkers:
            self.completed[index] = True
            if all(self.completed):
                try:
                    self.mutex.lock()
                    self.statusLabel.setText("Finished")
                    done = True
                finally:
                    self.mutex.unlock()
        else:
            try:
                self.mutex.lock()
                self.statusLabel.setText("Finished")
                done = True
            finally:
                self.mutex.unlock()
        if done:
            self.finishedIndexing()


    def reject(self):
        if not all(self.completed):
            self.stopWalkers()
            self.finishedIndexing()
        else:
            self.accept()


    def closeEvent(self, event=None):
        self.stopWalkers()


    def finishedIndexing(self):
        self.filesIndexedLCD.display(self.fileCount)
        self.wordsIndexedLCD.display(len(self.filenamesForWords))
        self.commonWordsLCD.display(len(self.commonWords))
        self.pathButton.setEnabled(True)
        QtGui.QApplication.processEvents() # Needed for Windows


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
