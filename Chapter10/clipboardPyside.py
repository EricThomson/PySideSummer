# -*- coding: utf-8 -*-
"""
clipboardPyside.py
Annotated PySide port of clipboard.pyw from Chapter 10
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

class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        textCopyButton = QtGui.QPushButton("&Copy Text")
        textPasteButton = QtGui.QPushButton("Paste &Text")
        htmlCopyButton = QtGui.QPushButton("C&opy HTML")
        htmlPasteButton = QtGui.QPushButton("Paste &HTML")
        imageCopyButton = QtGui.QPushButton("Co&py Image")
        imagePasteButton = QtGui.QPushButton("Paste &Image")
        self.textLabel = QtGui.QLabel("Original text")
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setPixmap(QtGui.QPixmap(os.path.join(
                os.path.dirname(__file__), "images/clock.png")))

        layout = QtGui.QGridLayout()
        layout.addWidget(textCopyButton, 0, 0)
        layout.addWidget(imageCopyButton, 0, 1)
        layout.addWidget(htmlCopyButton, 0, 2)
        layout.addWidget(textPasteButton, 1, 0)
        layout.addWidget(imagePasteButton, 1, 1)
        layout.addWidget(htmlPasteButton, 1, 2)
        layout.addWidget(self.textLabel, 2, 0, 1, 2)
        layout.addWidget(self.imageLabel, 2, 2)
        self.setLayout(layout)

        textCopyButton.clicked.connect(self.copyText)
        textPasteButton.clicked.connect(self.pasteText)
        htmlCopyButton.clicked.connect(self.copyHtml)
        htmlPasteButton.clicked.connect(self.pasteHtml)
        imageCopyButton.clicked.connect(self.copyImage)
        imagePasteButton.clicked.connect(self.pasteImage)

        self.setWindowTitle("Clipboard")


    def copyText(self):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText("I've been clipped!")


    def pasteText(self):
        clipboard = QtGui.QApplication.clipboard()
        self.textLabel.setText(clipboard.text())


    def copyImage(self):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setPixmap(QtGui.QPixmap(os.path.join(
                os.path.dirname(__file__), "images/gvim.png")))

    def pasteImage(self):
        clipboard = QtGui.QApplication.clipboard()
        self.imageLabel.setPixmap(clipboard.pixmap())


    def copyHtml(self):
        mimeData = QtCore.QMimeData()
        mimeData.setHtml("<b>Bold</b> and <font color=red>Red</font>")
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setMimeData(mimeData)


    def pasteHtml(self):
        clipboard = QtGui.QApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasHtml():
            self.textLabel.setText(mimeData.html())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
