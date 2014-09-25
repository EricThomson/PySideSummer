#PySide Summer Chapter 12 (Item-Based Graphics)
PySide translation of files for Chapter 12 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). Also see `usefulStuff.md` for helpful links and excerpts from the PySide documentation for relevant classes used in the files.

##Solution to exercise
Also included is one answer to the chapter exercise (see _pagedesignerPyside_ans.py_). Summerfield also has a solution (using PyQt) at the book's web site, which is likely better than my answer. 

##Notes about translation of Chapter 12
Nothing major: main thing is there is no QMatrix or matrix operation: it is now called QTransform. See notes associated with pagedesignerPyside.py for more details.

There is a slight issue with pagedesigner: if you open an old file and try to quit it, it asks you if you want to save (even if you haven't made any changes). I will get around to playing with this, but this is a faithful reproduction of the behavior of the original, so I will leave it for now as a future fix. The issue is with the way the Dirty flag is handled.


###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
