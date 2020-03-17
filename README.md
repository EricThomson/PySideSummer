# PySideSummer
Annotated PySide port of code from Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). The book's web site is at:
 http://www.qtrac.eu/pyqtbook.html. 

The programs should run without mishap in your favorite Python environment, as long as you have PySide installed. It has thus far been tested on Python 2.7 in Windows 7. Unless otherwise noted, if the original name of Summerfield's script was _name.pyw_, the name of the adapted PySide script is _namePyside.py_.  

Annotations include comments in code, but each chapter also contains_README.md_ and _usefulStuff.md_ files (the latter contains curated excerpts from PySide documentation and links from other relevant resources). When possible, we link to PySide documentation, but sometimes we have to go with Qt or PyQt when it is better.

Thanks to Mark Summerfield for encouragement, suggestions for improvement in innumerable places.
  

## Table of contents
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

**Chapter 16**: <a href = "https://github.com/EricThomson/PySideSummer/tree/master/Chapter16">Advanced Model/View Programming</a>

**Chapter 17**: <a href = "https://github.com/EricThomson/PySideSummer/tree/master/Chapter17">Online Help and Internationalization</a>

**Chapter 18**: <a href = "https://github.com/EricThomson/PySideSummer/tree/master/Chapter18">Networking</a>

**Chapter 19**: <a href = "https://github.com/EricThomson/PySideSummer/tree/master/Chapter19">Multithreading</a>

### Some of the guidelines followed
1. Follow <a href="http://www.qtrac.eu/pyqtbook.html#pyside">Summerfield's recommendations</a> for converting to Pyside, unless that would conflict with the remaining guidelines.

2. Change old-style to new-style signals and slots.

3. Replace `from PyQt4.QtCore import *`-type imports with `from PySide import QtGui`-type imports.

4. Replace `Qt.escape()`, which is not used in PySide, with `xml.sax.saxutils.escape()` (see <a href="http://srinikom.github.io/pyside-bz-archive/229.html">http://srinikom.github.io/pyside-bz-archive/229.html</a> ).

5. When opening files with `codecs` module, change the mode from "wt" to "w". 

6. Replace `QtGui.QWorkspace` (deprecated) with `QtGui.QMdiArea.` This entails a great deal of other relatively minor changes (see Chapter 9 texteditor code).

7. For drawpolygon to work (Chapter 11) change list of numbers to list of QPoints. 
For instance, change:
	drawPolygon(QtGui.QPolygon([x1, y1, x2, y2]))
to:
    drawPolygon(QtGui.QPolygon([QtCore.QPoint(x1, y1), QtCore.QPoint(x2,y2)]))
	
8. Replace deprecated `QMatrix` and `.matrix()` with 'QTransform' and '.transform()` (Chapter 12).

9. Replace the single line:

          self.assetView.selectionModel().currentRowChanged.connect(self.assetChanged)
        
 With the two lines:

        selectionModel = self.assetView.selectionModel()
        selectionModel.currentRowChanged.connect(self.assetChanged)
        
 This seems to be due to a bug in PySide (Chapter 15).

10. Get sqlite to work by adding:

        site_pack_path = site.getsitepackages()[1] 
        QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))

 Before `QtSql.QSqlDatabase.adDatabase("QSQLITE")`.  Be sure to `import site`. Not sure how platform-dependent this problem  is. (Chapter 15)

11. Replace obsolete `Qt.TextColorRole` with `Qt.ForegroundRole`.

12. Replace `.toPyDateTime()` with `.toPython()` 

13. For Chapter 17, to get the *_fr.html pages to show up in the help pages, add:

        QtCore.QLocale.setDefault(QtCore.QLocale(locale)) 

 Where 'locale' is the value entered by the user at the command line. Note this may not be required on all systems. I needed it in Python 2.7.6, Qt 4.8.4, PySide 1.2.1 on Windows 7.

14. Replace `isAlive(qObj)` function, which uses sip, with:

        from Shiboken import shiboken
        def isAlive(qObj):
            return shiboken.isValid(qObj)

 If you get the error that shiboken is not installed, in Windows command line:

	pip install --use-wheel -U shiboken

 Not sure what to do in Linux/Mac.


15. At least in the first few chapters, we replace 'super' with explicit base class initialization, just to try it both ways (see <a href="http://stackoverflow.com/questions/23981625/why-is-super-used-so-much-in-pyside-pyqt">http://stackoverflow.com/questions/23981625/why-is-super-used-so-much-in-pyside-pyqt</a>).
    
### LICENSE
PySideSummer is under the GPL license (<a href="http://www.gnu.org/copyleft/gpl.html">http://www.gnu.org/copyleft/gpl.html</a>)


