# coding: utf-8
"""
buildingservicesclientPyside.py
Annotated PySide adaptation of buildingservicesclient.py from Chapter 19
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import sys
from PySide import QtCore, QtGui, QtNetwork


PORT = 9407
SIZEOF_UINT16 = 2


class BuildingServicesClient(QtGui.QWidget):

    def __init__(self, parent=None):
        super(BuildingServicesClient, self).__init__(parent)

        self.socket = QtNetwork.QTcpSocket()
        self.nextBlockSize = 0
        self.request = None

        roomLabel = QtGui.QLabel("&Room")
        self.roomEdit = QtGui.QLineEdit()
        roomLabel.setBuddy(self.roomEdit)
        regex = QtCore.QRegExp(r"[0-9](?:0[1-9]|[12][0-9]|3[0-4])")
        self.roomEdit.setValidator(QtGui.QRegExpValidator(regex, self))
        self.roomEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        dateLabel = QtGui.QLabel("&Date")
        self.dateEdit = QtGui.QDateEdit()
        dateLabel.setBuddy(self.dateEdit)
        self.dateEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.dateEdit.setDate(QtCore.QDate.currentDate().addDays(1))
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        responseLabel = QtGui.QLabel("Response")
        self.responseLabel = QtGui.QLabel()
        self.responseLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)

        self.bookButton = QtGui.QPushButton("&Book")
        self.bookButton.setEnabled(False)
        self.unBookButton = QtGui.QPushButton("&Unbook")
        self.unBookButton.setEnabled(False)
        quitButton = QtGui.QPushButton("&Quit")

        self.bookButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.unBookButton.setFocusPolicy(QtCore.Qt.NoFocus)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.bookButton)
        buttonLayout.addWidget(self.unBookButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtGui.QGridLayout()
        layout.addWidget(roomLabel, 0, 0)
        layout.addWidget(self.roomEdit, 0, 1)
        layout.addWidget(dateLabel, 0, 2)
        layout.addWidget(self.dateEdit, 0, 3)
        layout.addWidget(responseLabel, 1, 0)
        layout.addWidget(self.responseLabel, 1, 1, 1, 3)
        layout.addLayout(buttonLayout, 2, 1, 1, 4)
        self.setLayout(layout)

        self.socket.connected.connect(self.sendRequest)
        self.socket.readyRead.connect(self.readResponse)
        self.socket.disconnected.connect(self.serverHasStopped)
        self.socket.error.connect(self.serverHasError)
        self.roomEdit.textEdited.connect(self.updateUi)
        self.dateEdit.dateChanged.connect(self.updateUi)
        self.bookButton.clicked.connect(self.book)
        self.unBookButton.clicked.connect(self.unBook)
        quitButton.clicked.connect(self.close)

        self.setWindowTitle("Building Services")


    def updateUi(self):
        enabled = False
        if (self.roomEdit.text() and
            self.dateEdit.date() > QtCore.QDate.currentDate()):
            enabled = True
        if self.request is not None:
            enabled = False
        self.bookButton.setEnabled(enabled)
        self.unBookButton.setEnabled(enabled)


    def closeEvent(self, event):
        self.socket.close()
        event.accept()


    def book(self):
        self.issueRequest("BOOK", self.roomEdit.text(),
                          self.dateEdit.date())


    def unBook(self):
        self.issueRequest("UNBOOK", self.roomEdit.text(),
                          self.dateEdit.date())


    def issueRequest(self, action, room, date):
        self.request = QtCore.QByteArray()
        stream = QtCore.QDataStream(self.request, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString(action)
        stream.writeQString(room)
        stream << date
        stream.device().seek(0)
        stream.writeUInt16(self.request.size() - SIZEOF_UINT16)
        self.updateUi()
        if self.socket.isOpen():
            self.socket.close()
        self.responseLabel.setText("Connecting to server...")
        self.socket.connectToHost("localhost", PORT)


    def sendRequest(self):
        self.responseLabel.setText("Sending request...")
        self.nextBlockSize = 0
        self.socket.write(self.request)
        self.request = None
        

    def readResponse(self):
        stream = QtCore.QDataStream(self.socket)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT16:
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break
            action = stream.readQString()
            room = stream.readQString()
            date = QtCore.QDate()
            if action != "ERROR":
                stream >> date
            if action == "ERROR":
                msg = "Error: {}".format(room)
            elif action == "BOOK":
                msg = "Booked room {} for {}".format(room,
                       date.toString(QtCore.Qt.ISODate))
            elif action == "UNBOOK":
                msg = "Unbooked room {} for {}".format(room,
                       date.toString(QtCore.Qt.ISODate))
            self.responseLabel.setText(msg)
            self.updateUi()
            self.nextBlockSize = 0


    def serverHasStopped(self):
        self.responseLabel.setText(
                "Error: Connection closed by server")
        self.socket.close()


    def serverHasError(self, error):
        self.responseLabel.setText("Error: {}".format(
                self.socket.errorString()))
        self.socket.close()


app = QtGui.QApplication(sys.argv)
form = BuildingServicesClient()
form.show()
app.exec_()

