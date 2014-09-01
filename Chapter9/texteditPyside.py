# -*- coding: utf-8 -*-
"""
texteditPyside.py
Annotated PySide port of textedit.pyw from Chapter 9
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Imported by texteditorPyside.py

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import codecs
from PySide import QtGui, QtCore

class TextEdit(QtGui.QTextEdit):

    #for unnamed files
    NextId = 1

    def __init__(self, filename="", parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #print "TextEdit init filename: ", filename
        self.filename = filename
        if self.filename=="":
            self.filename = unicode("Unnamed-{0}.txt".format(TextEdit.NextId))
            TextEdit.NextId += 1
        self.document().setModified(False)
        #print "type(self.document()): ", type(self.document())
        #print "type(self): ", type(self)
        pathlessName=QtCore.QFileInfo(self.filename).fileName()
        self.setWindowTitle(pathlessName)
    
    def closeEvent(self, event):
        error=None
        if (self.document().isModified() and 
            QtGui.QMessageBox.question(self,
                   "Text Editor - Unsaved Changes",
                   "Save unsaved changes in {0}?".format(self.filename),
                   QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) ==
                QtGui.QMessageBox.Yes):
            try:
                self.save()
            except (IOError, OSError), err:
                error=err
            except Exception as err:
                error=err
            if error is not None:
                QtGui.QMessageBox.warning(self,
                        "textedit closeEvent save error",
                        "Failed to save {0}: {1}".format(self.filename, error))       

    def isModified(self):
        #print "checking to see if modified file type: ", type(self.document())
        #built-in isModified() returns true if the text has been modified since 
        #it was either loaded or since the last call to setModified with false 
        #as argument. 
        return self.document().isModified()  #qtextedit built-in method 

    def save(self):
        #If no name yet, query for name
        if self.filename.startswith("Unnamed"):
            filename = QtGui.QFileDialog.getSaveFileName(self,
                    "Text Editor -- file needs name", self.filename,
                    "Text files (*.txt *.*)")[0]
            #print "textEdit.save() filename: ", filename
            if filename=="":
                return
            self.filename = filename
             
        #In the following, why not replace argument with self.filename?
        self.setWindowTitle(QtCore.QFileInfo(self.filename).fileName())
        #print "textedit save: filename ", self.filename
        with codecs.open(self.filename, "w", encoding="utf-8") as file:
            #print "textedit save codecs opened ", self.filename
            try:
                file.write(self.toPlainText())
            except Exception as err:
                print "textedit save failed with Exception {0}".format(err)
            self.document().setModified(False)

    def load(self):
        with codecs.open(self.filename, encoding="utf-8") as file:
            #print "textedit class self.filename: ", self.filename
            self.setPlainText(file.read())
            self.document().setModified(False)
