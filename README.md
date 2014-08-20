#PySideSummer
Heavily annotated PySide port of code from Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). The book's web site is http://www.qtrac.eu/pyqtbook.html. 

The programs should run without mishap in your favorite Python environment, as long as you have PySide installed. It has thus far been tested on Python 2.7 in Windows 7. Unless otherwise noted, if the original name of Summerfield's script was _name.pyw_, the name of the adapted PySide script is _namePyside.py_.  
  

##Table of contents
**Chapter 4**: Introduction to GUI Programming

**Chapter 5**: Dialogs

**Chapter 6**: Main Windows

**Chapter 7**: Using Qt Designer

**Chapter 8**: Data Handling and Custom File Formats

**Chapter 9**: Layouts and Multiple Documents

**Chapter 10**: Events, the Clipboard, and Drag and Drop

**Chapter 11**: Custom Widgets

**Chapter 12**: Item-Based Graphics

**Chapter 13**: Rich Text and Printing

**Chapter 14**: Model/View Programming

**Chapter 15**: Databases

**Chapter 16**: Advanced Model/View Programming

**Chapter 17**: Online Help and Internationalization

**Chapter 18**: Networking

**Chapter 19**: Multithreading

###Some of the guidelines followed
1. Follow recommendations of Summerfield for converting to Pyside (http://www.qtrac.eu/pyqtbook.html#pyside).

2. Change old-style to new-style signals and slots.

3. Replace `from PyQt4.QtCore import *`-type imports with `from PySide import QtGui`-type imports.

4. Replace 'super' with explicit base class (this is largely a matter of taste). 

5. Replace `Qt.escape()`, which is deprecated, with `xml.sax.saxutils.escape()`.

6. Heavy annotations include comments in code, but also each chapter contains a _README_ file, and most chapters contain a _usefulStuff_ file with curated exerpts from PySide documentation and other relevant recources. When possible, we link to PySide documentation, but sometimes we have to go with Qt because PySide documentation lags Qt so much.

###LICENSE
PySideSummer is under the GPL license (http://www.gnu.org/copyleft/gpl.html)


####To Do:
1. Chapter 9 [translation underway]
6. Chapter 10
7. Chapter 11
8. Chapter 12
9. Chapter 13
10. Chapter 14
11. Chapter 15
12. Chapter 16
13. Chapter 17
14. Chapter 18
15. Chapter 19
16. Figure out answer to question about @QtCore.Slot() decorator for slots.
17. Add _usefulStuff.md_ to earlier chapters.

####Interesting links
Interesting to me, anyway.

http://comments.gmane.org/gmane.comp.lib.qt.pyside/2038

http://www.qtrac.eu/pyqtbook.html#pyside
