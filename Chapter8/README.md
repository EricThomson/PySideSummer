#PySide Summer Chapter 8 (Data Handling and Custom File Formats)
PySide translation of files for Chapter 8 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). The GUI design is similar to that for Chapter 6, but in this chapter this focus is on loading/saving data in different formats. The central medule is _mymoviesPyside.py_.

Also see `usefulStuff.md` for helpful excerpts from the PySide documentation for relevant classes used in the files.

##Structure of Package
The main module is _mymoviesPyside.py_. It uses the following: 
*  moviedataPyside.py 
*  addeditmoviedlgPyside.py (calls dialog)
*  addeditmoviedlg.ui (use `pyside-uic` to build ui_addeditmoviedlgPyside.py)
*  resources.qrc (use `pyside-rcc` to compile)
*  images/  (folder contains icons for the menus/toolbars)

The Chapter 8 directory also includes sample data: _mymovies.mqb_ is the original dataset Summerfield provides. It is useful to start with that, and go from there (to and from mqt, mpt, mpb, and XML, to make sure everything is working as expected).

There is a lot of test code in `__main__` in `moviedataPyside.py`. It is useful for debugging.

##Solution to exercise
Also included is one answer to the exercise. The new code is in _mymoviesPyside_ans.py_, _moviedataPyside_ans.py_, _addeditmoviedlgPyside_ans.py_, and _addeditmoviedlg_ans.ui_ (which you should convert to a ui_*.py file, as we've already covered in the previous two chapters). 

Summerfield also has answers (using PyQt) at the book's web site, which is probably better than my answer.

##Notes about translation of Chapter 8
Qt.escape() is no longer in use, so replace it with xml.sax.saxutils.escape().

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
