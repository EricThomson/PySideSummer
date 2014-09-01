#PySide Summer Chapter 9 (Layouts and Multiple Documents)
PySide translation of files for Chapter 9 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). Also see `usefulStuff.md` for helpful excerpts from the PySide documentation for relevant classes used in the files.

##Solution to exercise
Also included is one answer to the exercise. The new code is in _tabbededitorPyside.py_. Summerfield also has answers (using PyQt) at the book's web site, which is probably better than my answer. 

##Notes about translation of Chapter 9
As Summerfield notes at his web site, it is nontrivial in PySide to check to see if an instance of an object has been deleted or not (this is what his isAlive method did). See my notes in _sditexteditorPyside.py_ for a workaround that works nicely.

Because QWorkspace is deprecated, I used the recommended QMdiArea class instead for the MDI editor. See texteditorPyside.py for a description of what this change entailed, and UsefulStuff.md for some of the more helpful documentation.

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
