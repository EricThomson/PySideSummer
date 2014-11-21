#PySideSummer
Annotated PySide port of code from Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). The book's web site is http://www.qtrac.eu/pyqtbook.html. 

The programs should run without mishap in your favorite Python environment, as long as you have PySide installed. It has thus far been tested on Python 2.7 in Windows 7. Unless otherwise noted, if the original name of Summerfield's script was _name.pyw_, the name of the adapted PySide script is _namePyside.py_.  

Annotations include comments in code, but each chapter also contains a _README_ file and a _usefulStuff_ file with curated excerpts from PySide documentation and other relevant resources. When possible, we link to PySide documentation, but sometimes we have to go with Qt or PyQt when it is better.
  

##Table of contents
**Chapter 4**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter4">Introduction to GUI Programming</a>

**Chapter 5**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter5">Dialogs</a>

**Chapter 6**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter6">Main Windows</a>

**Chapter 7**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter7">Using Qt Designer</a>

**Chapter 8**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter8">Data Handling and Custom File Formats</a>

**Chapter 9**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter9">Layouts and Multiple Documents</a>

**Chapter 10**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter10">Events, the Clipboard, and Drag and Drop</a>

**Chapter 11**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter11">Custom Widgets</a>

**Chapter 12**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter12">Item-Based Graphics</a>

**Chapter 13**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter13">Rich Text and Printing</a>

**Chapter 14**: <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter14">Model/View Programming</a>

**Chapter 15**:  <a href="https://github.com/EricThomson/PySideSummer/tree/master/Chapter15">Databases</a>

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

6. When opening files with `codecs` module, change the mode from "wt" to "w". 

7. Replace `QtGui.QWorkspace` (deprecated) with `QtGui.QMdiArea.` This entails a great deal of other relatively minor changes (see Chapter 9 texteditor code).

8. For drawpolygon to work (Chapter 11) change list of numbers to list of QPoints. 
For instance, change:
	drawPolygon(QtGui.QPolygon([x1, y1, x2, y2]))
to:
    drawPolygon(QtGui.QPolygon([QtCore.QPoint(x1, y1), QtCore.QPoint(x2,y2)]))
	
9. Replace deprecated `QMatrix` and `.matrix()` with 'QTransform' and '.transform()` (Chapter 12).
10. Replace the single line:

        self.assetView.selectionModel().currentRowChanged.connect(self.assetChanged)
        
 With the two lines:

        selectionModel = self.assetView.selectionModel()
        selectionModel.currentRowChanged.connect(self.assetChanged)
        
 This seems to be due to a bug in PySide (Chapter 15).

11. I could only find sqlite by adding the following before `QtSql.QSqlDatabase.adDatabase("QSQLITE")`:


	site_pack_path = site.getsitepackages()[1] 
    
    QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))
    
This uses the `site` package, so be sure to `import site`. Not sure how platform-dependent this problem
is. (Chapter 15)

###LICENSE
PySideSummer is under the GPL license (http://www.gnu.org/copyleft/gpl.html)


####To Do:
1. Chapter 16 [translation underway]
13. Chapter 17
14. Chapter 18
15. Chapter 19
16. Figure out answer to question about @QtCore.Slot() decorator for slots.
17. Add _usefulStuff.md_ to earlier chapters, and make sure formatting is decent, and consistent in all chapters, and remove extensive comments from the code itself.
18. Make sure you are consistent in removal of 'super'...