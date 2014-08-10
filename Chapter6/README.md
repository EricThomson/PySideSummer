#PySide Summer Chapter 6: Main Windows
A PySide port of the code from Chapter 6 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). The central module is _imagechanger.py_. It lets you load an image and edit it various ways. The port also includes an answer to the exercise (_imagechanger_ansPyside.py_ and its associated dialog builder _resizedlgPyside.py_).

Also, see usefulDocumentation.txt for helpful exerpts from the PySide documentation for relevant classes used in the files.

##Structure of Package
The main module is _imagechangerPyside.py_. It uses the following: 
*  newimagedlgPyside.py
*  helpformPyside.py
*  resources.qrc
*  newimagedlg.ui

This directory also includes a sample image, _buttfumble.png_, a picture from the most wonderful play of football in all time. Google it.

##Compiling the resource file
To compile the resource file (_resources.qrc_) you should use something like the following command at your system prompt, with the containing folder as working directory:

`pyside-rcc resources.qrc -o resource_rc.py` 

This assumes the folder containing pyside-rcc.exe is on your system path (you may have to add it yourself). 

As we are following the usual PySide conventions, we are naming the compiled file a little differently than Summerfield (_resource_rc.py_ instead of _qrc_resources.py_), but you can name it whatever you wish.

##Generating the dialog from the ui-file
The file _newimagedlg.ui_ was created by _Qt Designer_ (a GUI for designing Qt applications). Such ui files must be converted into  Python modules using a dedicated program (see Chapter 7). In PySide, you can perform this conversion using _pyside-uic.exe_ (whose containing directory should be added to your system path, if it isn't already there). With PySideSummer/Chapter 6 as your working directory, enter the following at your system prompt:

`pyside-uic newimagedlg.ui -o ui_newimagedlgPyside.py`

This should create the required Python module that is loaded into the program.

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

