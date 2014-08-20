Useful stuff to accompany Chapter 7 of PySideSummer repository: 
https://github.com/EricThomson/PySideSummer

#Useful links
On using code generated in Qt Designer:
http://pyqt.sourceforge.net/Docs/PyQt4/designer.html#using-the-generated-code
There are three main ways discussed, and Summerfield uses the third. I show examples
of all three in Chapter7/working/openDlgi.py (i=1-3), which I have not yet exported to GitHub.

Some of the following material on autoconnecting with slots is adapted from:
http://joat-programmer.blogspot.com/2012/02/pyqt-signal-and-slots-to-capture-events.html


#Autoconnecting signals and slots 
The ui module created by pyside-uic contains the line:
    QCore.QMetaObject.connectSlotsByName(FindAndReplaceDlg)
This allows for the autoconnection of signals with slots, as long as the slot name follows the following conventions:
    @QtCore.Slot(<parameters>)
    def on_<object name>_<signal name>(<signal parameters>):
        <define slot here>
So, for example in Chapter 7 code we have:
    @QtCore.Slot(str)
    def on_findLineEdit_textEdited(self, text): 
This means that there exists an object named findLineEdit in our dialog (it is the QLineEdit object used to enter the text we want to find). When its `textEdited` signal is emitted, it autoconnects to the subsequently defined slot. Apparently Python knows this is a slot partly because of the `@QtCore.Slot()` decorator, though frankly when I comment that out things seem to work just fine.


#Useful PySide Documentation
  **QtGui.QDateTimeEdit**
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QDateTimeEdit.html
    The PySide.QtGui.QDateTimeEdit class provides a widget for editing dates and times.

    PySide.QtGui.QDateTimeEdit allows the user to edit dates by using the keyboard or the arrow keys to increase and decrease date and time values. The arrow keys can be used to move from section to section within the PySide.QtGui.QDateTimeEdit box. Dates and times appear in accordance with the format set; see PySide.QtGui.QDateTimeEdit.setDisplayFormat().

    getDateTime returns type QtCore.QDatetime type.

  **QDateTime class**
  http://srinikom.github.io/pyside-docs/PySide/QtCore/QDateTime.html
