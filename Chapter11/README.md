#PySide Summer Chapter 11 (Custom Widgets)
PySide translation of files for Chapter 11 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). Also see `usefulStuff.md` for helpful excerpts from the PySide documentation for relevant classes used in the files.

##Solution to exercise
Also included is one answer to the exercise. The new code is in _countersPyside.py_. Summerfield also has an answer at the book's web site, which is probably better than mine.

##Notes about translation of Chapter 11
For drawPolygon, needed to change list of floats to list of QPoints. That is, if you see:
     painter.drawPolygon(QtGui.QPolygon([x1, y1, x2, y2]))
change it to:
    painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(x1, y1), QtCore.QPoint(x2,y2)]))


###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
