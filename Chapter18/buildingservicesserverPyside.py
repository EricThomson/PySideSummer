# coding: utf-8
"""
buildingservicesclientPyside.py
Annotated PySide adaptation of buildingservicesserver.py from Chapter 18
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

-------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import bisect
import collections
import sys
from PySide import QtCore, QtGui, QtNetwork


PORT = 10000
SIZEOF_UINT16 = 2
MAX_BOOKINGS_PER_DAY = 5

# Key = date, value = list of room IDs
Bookings = collections.defaultdict(list)

def printBookings():
    for key in sorted(Bookings):
        print(key, Bookings[key])
    print()


class Socket(QtNetwork.QTcpSocket):

    def __init__(self, parent=None):
        super(Socket, self).__init__(parent)
        self.readyRead.connect(self.readRequest)
        self.disconnected.connect(self.deleteLater)
        self.nextBlockSize = 0


    def readRequest(self):
        print "Server reqding request"
        stream = QtCore.QDataStream(self)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)

        if self.nextBlockSize == 0:
            if self.bytesAvailable() < SIZEOF_UINT16:
                return
            self.nextBlockSize = stream.readUInt16()
        if self.bytesAvailable() < self.nextBlockSize:
            return

        action = stream.readQString()
        date = QtCore.QDate()
        if action in ("BOOK", "UNBOOK"):
            room = stream.readQString()
            stream >> date
            bookings = Bookings.get(date.toPython())
            uroom = room
        if action == "BOOK":
            if bookings is None:
                bookings = Bookings[date.toPython()]
            if len(bookings) < MAX_BOOKINGS_PER_DAY:
                if uroom in bookings:
                    self.sendError("Cannot accept duplicate booking")
                else:
                    bisect.insort(bookings, uroom)
                    self.sendReply(action, room, date)
            else:
                self.sendError("{} is fully booked".format(
                               date.toString(QtCore.Qt.ISODate)))
        elif action == "UNBOOK":
            if bookings is None or uroom not in bookings:
                self.sendError("Cannot unbook nonexistent booking")
            else:
                bookings.remove(uroom)
                self.sendReply(action, room, date)
        else:
            self.sendError("Unrecognized request")
        printBookings()


    def sendError(self, msg):
        print "Server sending error."
        reply = QtCore.QByteArray()
        stream = QtCore.QDataStream(reply, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString("ERROR")
        stream.writeQString(msg)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        self.write(reply)


    def sendReply(self, action, room, date):
        print "Server sending reply"
        reply = QtCore.QByteArray()
        stream = QtCore.QDataStream(reply, QtCore.QIODevice.WriteOnly)
        stream.setVersion(QtCore.QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream.writeQString(action)
        stream.writeQString(room)
        stream << date
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        self.write(reply)


class TcpServer(QtNetwork.QTcpServer):

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)


    def incomingConnection(self, socketId):
        socket = Socket(self)
        socket.setSocketDescriptor(socketId)
        

class BuildingServicesDlg(QtGui.QPushButton):

    def __init__(self, parent=None):
        super(BuildingServicesDlg, self).__init__(
                "&Close Server", parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.loadBookings()
        self.tcpServer = TcpServer(self)
        if not self.tcpServer.listen(QtNetwork.QHostAddress("0.0.0.0"), PORT):
            QtGui.QMessageBox.critical(self, "Building Services Server",
                    "Failed to start server: {}".format(
                    self.tcpServer.errorString()))
            self.close()
            return

        self.clicked.connect(self.close)

        font = self.font()
        font.setPointSize(24)
        self.setFont(font)
        self.setWindowTitle("Building Services Server")


    def loadBookings(self):
        # Generate fake data
        import random

        today = QtCore.QDate.currentDate()
        for i in range(10):
            date = today.addDays(random.randint(7, 60))
            for j in range(random.randint(1, MAX_BOOKINGS_PER_DAY)):
                # Rooms are 001..534 excl. 100, 200, ..., 500
                floor = random.randint(0, 5)
                room = random.randint(1, 34)
                bookings = Bookings[date.toPython()]
                if len(bookings) >= MAX_BOOKINGS_PER_DAY:
                    continue
                bisect.insort(bookings, "{0:1d}{1:02d}".format(
                              floor, room))
        printBookings()


app = QtGui.QApplication(sys.argv)
form = BuildingServicesDlg()
form.show()
form.move(0, 0)
app.exec_()

