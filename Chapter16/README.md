#PySide Summer Chapter 16 (Advanced Model/View Programming)
PySide translation of files in Chapter 16 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). Also see `usefulStuff.md` for helpful links and excerpts from the PySide documentation. 

##Notes about translation of Chapter 16
Notes on translation:

1. There is no 'contains' method. Replace with 'in'. For instance:
    if "unicode" in face: #instead of face.contains("unicode"):
    
2. Replace obsolete Qt.TextColorRole with Qt.ForegroundRole (perhaps mentioned this in ch5, but I need to go back and do this in previous chapters, eg 14, and make sure it is consistent once done)

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
