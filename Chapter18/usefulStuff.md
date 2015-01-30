Things that might be useful when working through Chapter 18 of Rapid GUI Programming by Summerfield.
Part of PySideSummer repository (https://github.com/EricThomson/PySideSummer)


#Useful links

#Useful Documentation

##QtNetwork.QTcpSocket
http://srinikom.github.io/pyside-docs/PySide/QtNetwork/QTcpSocket.html

The PySide.QtNetwork.QTcpSocket class provides a TCP socket. TCP (Transmission Control Protocol) is a reliable, stream-oriented, connection-oriented transport protocol. It is especially well suited for continuous transmission of data. PySide.QtNetwork.QTcpSocket is a convenience subclass of PySide.QtNetwork.QAbstractSocket that allows you to establish a TCP connection and transfer streams of data. See the PySide.QtNetwork.QAbstractSocket documentation for details.

##QtNetwork.QAbstractSocket
http://srinikom.github.io/pyside-docs/PySide/QtNetwork/QAbstractSocket.html

    The PySide.QtNetwork.QAbstractSocket class provides the base functionality common to all socket types.

    PySide.QtNetwork.QAbstractSocket is the base class for PySide.QtNetwork.QTcpSocket and PySide.QtNetwork.QUdpSocket and contains all common functionality of these two classes. If you need a socket, you have two options:

        1. Instantiate PySide.QtNetwork.QTcpSocket or PySide.QtNetwork.QUdpSocket.
        2. Create a native socket descriptor, instantiate PySide.QtNetwork.QAbstractSocket, and call PySide.QtNetwork.QAbstractSocket.setSocketDescriptor() to wrap the native socket.

    TCP (Transmission Control Protocol) is a reliable, stream-oriented, connection-oriented transport protocol. UDP (User Datagram Protocol) is an unreliable, datagram-oriented, connectionless protocol. In practice, this means that TCP is better suited for continuous transmission of data, whereas the more lightweight UDP can be used when reliability isn’t important.

    PySide.QtNetwork.QAbstractSocket‘s API unifies most of the differences between the two protocols. For example, although UDP is connectionless, PySide.QtNetwork.QAbstractSocket.connectToHost() establishes a virtual connection for UDP sockets, enabling you to use PySide.QtNetwork.QAbstractSocket in more or less the same way regardless of the underlying protocol. Internally, PySide.QtNetwork.QAbstractSocket remembers the address and port passed to PySide.QtNetwork.QAbstractSocket.connectToHost(), and functions like PySide.QtCore.QIODevice.read() and PySide.QtCore.QIODevice.write() use these values.

    At any time, PySide.QtNetwork.QAbstractSocket has a state (returned by PySide.QtNetwork.QAbstractSocket.state() ). The initial state is UnconnectedState. After calling PySide.QtNetwork.QAbstractSocket.connectToHost(), the socket first enters HostLookupState. If the host is found, PySide.QtNetwork.QAbstractSocket enters ConnectingState and emits the PySide.QtNetwork.QAbstractSocket.hostFound() signal. When the connection has been established, it enters ConnectedState and emits PySide.QtNetwork.QAbstractSocket.connected(). If an error occurs at any stage, PySide.QtNetwork.QAbstractSocket.error() is emitted. Whenever the state changes, PySide.QtNetwork.QAbstractSocket.stateChanged() is emitted. For convenience, PySide.QtNetwork.QAbstractSocket.isValid() returns true if the socket is ready for reading and writing, but note that the socket’s state must be ConnectedState before reading and writing can occur.

    Read or write data by calling PySide.QtCore.QIODevice.read() or PySide.QtCore.QIODevice.write(), or use the convenience functions PySide.QtCore.QIODevice.readLine() and PySide.QtCore.QIODevice.readAll(). PySide.QtNetwork.QAbstractSocket also inherits PySide.QtCore.QIODevice.getChar(), PySide.QtCore.QIODevice.putChar(), and PySide.QtCore.QIODevice.ungetChar() from PySide.QtCore.QIODevice, which work on single bytes. The PySide.QtCore.QIODevice.bytesWritten() signal is emitted when data has been written to the socket (i.e., when the client has read the data). Note that Qt does not limit the write buffer size. You can monitor its size by listening to this signal.

    The PySide.QtCore.QIODevice.readyRead() signal is emitted every time a new chunk of data has arrived. PySide.QtNetwork.QAbstractSocket.bytesAvailable() then returns the number of bytes that are available for reading. Typically, you would connect the PySide.QtCore.QIODevice.readyRead() signal to a slot and read all available data there. If you don’t read all the data at once, the remaining data will still be available later, and any new incoming data will be appended to PySide.QtNetwork.QAbstractSocket ‘s internal read buffer. To limit the size of the read buffer, call PySide.QtNetwork.QAbstractSocket.setReadBufferSize().

    To close the socket, call PySide.QtNetwork.QAbstractSocket.disconnectFromHost(). PySide.QtNetwork.QAbstractSocket enters QAbstractSocket.ClosingState. After all pending data has been written to the socket, PySide.QtNetwork.QAbstractSocket actually closes the socket, enters QAbstractSocket::ClosedState, and emits PySide.QtNetwork.QAbstractSocket.disconnected(). If you want to abort a connection immediately, discarding all pending data, call PySide.QtNetwork.QAbstractSocket.abort() instead. If the remote host closes the connection, PySide.QtNetwork.QAbstractSocket will emit error( QAbstractSocket.RemoteHostClosedError ), during which the socket state will still be ConnectedState, and then the PySide.QtNetwork.QAbstractSocket.disconnected() signal will be emitted.

    The port and address of the connected peer is fetched by calling PySide.QtNetwork.QAbstractSocket.peerPort() and PySide.QtNetwork.QAbstractSocket.peerAddress(). PySide.QtNetwork.QAbstractSocket.peerName() returns the host name of the peer, as passed to PySide.QtNetwork.QAbstractSocket.connectToHost(). PySide.QtNetwork.QAbstractSocket.localPort() and PySide.QtNetwork.QAbstractSocket.localAddress() return the port and address of the local socket.

    PySide.QtNetwork.QAbstractSocket provides a set of functions that suspend the calling thread until certain signals are emitted. These functions can be used to implement blocking sockets:

        PySide.QtNetwork.QAbstractSocket.waitForConnected() blocks until a connection has been established.
        PySide.QtNetwork.QAbstractSocket.waitForReadyRead() blocks until new data is available for reading.
        PySide.QtNetwork.QAbstractSocket.waitForBytesWritten() blocks until one payload of data has been written to the socket.
        PySide.QtNetwork.QAbstractSocket.waitForDisconnected() blocks until the connection has closed.

    We show an example:
        numRead = 0
        numReadTotal = 0
        while(True):
            buffer  = socket.read(50)
            # do whatever with array
            numReadTotal += buffer.size()
            if (buffer.size() == 0 && !socket.waitForReadyRead()):
                break

    If PySide.QtCore.QIODevice.waitForReadyRead() returns false, the connection has been closed or an error has occurred.

    Programming with a blocking socket is radically different from programming with a non-blocking socket. A blocking socket doesn’t require an event loop and typically leads to simpler code. However, in a GUI application, blocking sockets should only be used in non-GUI threads, to avoid freezing the user interface. See the network/fortuneclient and network/blockingfortuneclient examples for an overview of both approaches.

    Note:

    We discourage the use of the blocking functions together with signals. One of the two possibilities should be used.

    PySide.QtNetwork.QAbstractSocket can be used with PySide.QtCore.QTextStream and PySide.QtCore.QDataStream ‘s stream operators (operator<<() and operator>>()). There is one issue to be aware of, though: You must make sure that enough data is available before attempting to read it using operator>>().
    
##QtNetwork.QTcpServer
http://srinikom.github.io/pyside-docs/PySide/QtNetwork/QTcpServer.html

    The PySide.QtNetwork.QTcpServer class provides a TCP-based server.

    This class makes it possible to accept incoming TCP connections. You can specify the port or have PySide.QtNetwork.QTcpServer pick one automatically. You can listen on a specific address or on all the machine’s addresses.

    Call PySide.QtNetwork.QTcpServer.listen() to have the server listen for incoming connections. The PySide.QtNetwork.QTcpServer.newConnection() signal is then emitted each time a client connects to the server.

    Call PySide.QtNetwork.QTcpServer.nextPendingConnection() to accept the pending connection as a connected PySide.QtNetwork.QTcpSocket. The function returns a pointer to a PySide.QtNetwork.QTcpSocket in QAbstractSocket.ConnectedState that you can use for communicating with the client.

    If an error occurs, PySide.QtNetwork.QTcpServer.serverError() returns the type of error, and PySide.QtNetwork.QTcpServer.errorString() can be called to get a human readable description of what happened.

    When listening for connections, the address and port on which the server is listening are available as PySide.QtNetwork.QTcpServer.serverAddress() and PySide.QtNetwork.QTcpServer.serverPort().

    Calling PySide.QtNetwork.QTcpServer.close() makes PySide.QtNetwork.QTcpServer stop listening for incoming connections.

    Although PySide.QtNetwork.QTcpServer is mostly designed for use with an event loop, it’s possible to use it without one. In that case, you must use PySide.QtNetwork.QTcpServer.waitForNewConnection(), which blocks until either a connection is available or a timeout expires.
