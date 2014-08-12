#PySide Summer Chapter 7 (Using Qt Designer)
PySide translation of files for Chapter 7 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). This chapter goes over building Dialogs using Qt Designer, the visual design tool for GUI construction.

###Generating the GUI module
As with the .ui file in Chapter 6, once we have saved the desired .ui file built in the first part of the chapter, to use it we convert it into a Python file. To do this, as we discussed in more detail in the README for Chapter 6, we use pyside-uic.exe:

`pyside-uic findandreplacedlg.ui -o ui_findandreplacedlgPyside.py`

This will create, in the same folder, the designated Python file which is ready to be used as a base class. The same applies to the exercise, which I've called ticketorderdlg1.ui here. Frankly, I focused more on doing the exercise than the example from the chapter, as the main goal is to learn to use Qt Designer. So `findandreplacedlgPyside.py` could probably use some work.

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

