#PySideSummer
Heavily annotated PySide adaptation of code from   Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). The book's web site is http://www.qtrac.eu/pyqtbook.html.

The goal is for the programs to run without mishap in your favorite Python environment, as long as you have PySide installed. It was built to run in Python 2.7. Unless otherwise noted, if the original name of Summerfield's script was _name.pyw_, the name of the adapted PySide script is _namePyside.py_.  
  
The contents of this repository are under a GPL v3 license.


##Table of contents
**Chapter 4**: Introduction to GUI Programming

**Chapter 5**: Dialogs


###Guidelines followed
1. Change old-style to new-style signals and slots.

2. Replace 'super' with explicit name of class.

3. Wrap app.exec_() in sys.exit(). 

4. Replace `from PyQt4.QtCore import *`-type imports with `from PySide import QtGui`-type imports.

5. Heavy annotations include comments, but also links to relevant documentation. When possible, PySide documentation is linked, but sometimes we have to go with Qt, as PySide documentation is way behind. Also, comments mention when something that had become obsolete or deprecated has been changed. If this repo is missing any such cases, please help out and change it or let us know.

6. I put the comment `#XXX` on lines where it isn't so clear what is happening, and we need to go back and figure it out.


####To Do:
1. Remove common notes from each program.
2. Add full table of contents to readme.
3. README.md for each chapter?
4. Chapter 4 [first draft done: proofread]
5. Chapter 5 
6. Chapter 6
7. Chapter 7
8. Chapter 8
9. Chapter 9
10. Chapter 10
11. Chapter 11
12. Chapter 12
13. Chapter 13
14. Chapter 14
15. Chapter 15
16. Formally add GPLv3 license.
17. Go through and clean up XXX's in code.
