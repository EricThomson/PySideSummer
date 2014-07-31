# coding: utf-8
'''
alertPyside.py
Heavily annotated PySide adaptation of alert.pyw from Chapter 4
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)

Illustrates idea of event loop execution by a QApplication.

Usage:
In your system (not Python) terminal, enter:
   python alertPyside.py HH:MM "Ugly QLabel alert!"
where HH:MM is time you want message (in this case, "Ugly QLabel alert!") to trigger.

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
'''

from PySide import QtCore, QtGui
import sys
import time


#Set up the message you want to show
print "You entered {0} arguments: {1}".format(len(sys.argv), sys.argv) #unnecessary readout of arguments (not in original)
alarmTime = QtCore.QTime.currentTime() #QTime: http://srinikom.github.io/pyside-docs/PySide/QtCore/QTime.html
try:
    #If only one input given (alertPyside.py) raise exception
    if len(sys.argv) < 2:
        raise ValueError
    
    #at least two arguments given
    message = "Default message alert!"
    hours, mins = sys.argv[1].split(":")
    alarmTime = QtCore.QTime(int(hours), int(mins))
    if not alarmTime.isValid():
        raise ValueError

    #Case 3: three (or more) arguments given
    if len(sys.argv) > 2:
        message =  " ".join(sys.argv[2:])

except ValueError:
    message = "In terminal: alertPyside.py HH:MM {Optional message}" # 24hr clock

# check every 20 seconds to see if alarmTime is greater than current time
while QtCore.QTime.currentTime() < alarmTime:
    time.sleep(20)

#Gui programming really starts now
qtApp = QtGui.QApplication(sys.argv)
#QLabels work with a limited set of html tags: https://qt-project.org/doc/qt-4.8/richtext-html-subset.html
#   label = QtGui.QLabel("<font color=red size=72><b>{0}</b></font>".format(message)) #original
#While original example used html, style sheets seem to be recommended nowadays.
# List of supported style sheet properties:  
#    http://qt-project.org/doc/qt-4.8/stylesheet-reference.html#list-of-properties
label=QtGui.QLabel(message)
label.setStyleSheet("QLabel { color: rgb(255, 0, 0); font-weight: bold; font-size: 25px; background-color: rgb(0,0,0); \
   border: 5px solid rgba(0 , 255, 0, 200)}")

#Flags that define behavior of label are set with the bitwise OR operator |.
#Splashscreen documentation: http://srinikom.github.io/pyside-docs/PySide/QtGui/QSplashScreen.html
#Lots of potential flags to explore: srinikom.github.io/pyside-docs/PySide/QtCore/Qt.html
label.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
label.show()
waitTime=3000  #in milliseconds

#show the label, wait 3000 ms, then quit the application (close the windows)
QtCore.QTimer.singleShot(waitTime, qtApp.quit) #http://srinikom.github.io/pyside-docs/PySide/QtCore/QTimer.html

#Start the event loop with .exec_(), sys.exit makes clean exit more likely
sys.exit(qtApp.exec_())

