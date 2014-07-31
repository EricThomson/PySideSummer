#PySideSummer
Learning to program in PySide. Heavily annotated PySide adaptation of code from   Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008).

Book's web site: http://www.qtrac.eu/pyqtbook.html

Programs should run without mishap in your favorite Python environment, as long as you have PySide installed. It was built to run in Python 2.7.*.

If the original name of Summerfield's script was _name.pyw_, the new name is _namePyside.py_.


##Table of contents
Chapter 4: 
Chapter 5: Dialogs

###Guidelines used to adapt the code
1. Old to new-style signals and slots.
2. Replaced 'super' with explicit name of class (this is personal taste: 'super' frightens me).
3. Added sys.exit to lines where application was executed (app.exec_()).

3. Heavy annotations include comments, but also links to relevant documentation. When possible, PySide documentation is linked, but sometimes we have to go with Qt, as PySide documentation is way behind. I also discuss when imports or syntax that Summerfield used has become obsolete or deprecated. If I am missing any such cases, I'd really like to know so we can keep this as modern as possible (ahem...within the confines of Python 2 instead of 3).


4. I put the comment '#XXX' on lines where I wasn't sure of what Summerfield was up to, and need
to go back and figure it out for an annotation.

###Where I need help
Especially interested in improving Pythonicity of code, and making it modern. The book the code is based on is from 2008, and a lot has changed since then, a lot of which I am probably not aware.

###To Do:
1. Remove common notes from each program.
2. Add table of contents to readme
3. Add url for book to each program and README
4. README.md for each chapter?
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
16. Go through and clean up XXX's in code.
