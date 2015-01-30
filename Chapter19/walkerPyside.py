# coding: utf-8
"""
walkerPyside.py
Annotated PySide adaptation of walker.py from Chapter 19
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""


import codecs
import htmlentitydefs
import os
import re
import sys
from PySide import QtCore

class Walker(QtCore.QThread):

    finished = QtCore.Signal(bool)
    indexed = QtCore.Signal(str)

    COMMON_WORDS_THRESHOLD = 250
    MIN_WORD_LEN = 3
    MAX_WORD_LEN = 25
    INVALID_FIRST_OR_LAST = frozenset("0123456789_")
    STRIPHTML_RE = re.compile(r"<[^>]*?>", re.IGNORECASE|re.MULTILINE)
    ENTITY_RE = re.compile(r"&(\w+?);|&#(\d+?);")
    SPLIT_RE = re.compile(r"\W+", re.IGNORECASE|re.MULTILINE)

    def __init__(self, lock, parent=None):
        super(Walker, self).__init__(parent)
        self.lock = lock
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.path = None
        self.completed = False


    def initialize(self, path, filenamesForWords, commonWords):
        self.stopped = False
        self.path = path
        self.filenamesForWords = filenamesForWords
        self.commonWords = commonWords
        self.completed = False


    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True


    def isStopped(self):
        with QtCore.QMutexLocker(self.mutex):
            return self.stopped


    def run(self):
        self.processFiles(self.path)
        self.stop()
        self.finished.emit(self.completed)


    def processFiles(self, path):
        for root, dirs, files in os.walk(path):
            if self.isStopped():
                return
            for name in [name for name in files
                         if name.endswith((".htm", ".html"))]:
                fname = os.path.join(root, name)
                if self.isStopped():
                    return
                self.processOneFile(fname)
        self.completed = True



    def processOneFile(self, fname):
        words = set()
        text = self.readFile(fname)
        if text is None or self.isStopped():
            return
        text = self.STRIPHTML_RE.sub("", text)
        text = self.ENTITY_RE.sub(unichrFromEntity, text)
        text = text.lower()
        for word in self.SPLIT_RE.split(text):
            if (self.MIN_WORD_LEN <= len(word) <=
                self.MAX_WORD_LEN and
                word[0] not in self.INVALID_FIRST_OR_LAST and
                word[-1] not in self.INVALID_FIRST_OR_LAST):
                with QtCore.QReadLocker(self.lock):
                    new = word not in self.commonWords
                if new:
                    words.add(word)
        if self.isStopped():
            return
        for word in words:
            with QtCore.QWriteLocker(self.lock):
                files = self.filenamesForWords[word]
                if len(files) > self.COMMON_WORDS_THRESHOLD:
                    del self.filenamesForWords[word]
                    self.commonWords.add(word)
                else:
                    files.add(unicode(fname))
        self.indexed.emit(fname)


    def readFile(self, fname):
        try:
            with codecs.open(fname, "r", "UTF8", "ignore") as file:
                return file.read()
        except (IOError, OSError), err:
            sys.stderr.write("Error: {0}\n".format(err))


def unichrFromEntity(match):
    text = match.group(match.lastindex)
    if text.isdigit():
        return unichr(int(text))
    u = htmlentitydefs.name2codepoint.get(text)
    return unichr(u) if u is not None else ""

