Things that might be useful when working through Chapter 19 of Rapid GUI Programming by Summerfield.
Part of PySideSummer repository (https://github.com/EricThomson/PySideSummer)


#Useful links

##What is a mutex? From stackoverflow
http://stackoverflow.com/questions/34524/what-is-a-mutex

#Useful Documentation
##QtCore.QThread
http://srinikom.github.io/pyside-docs/PySide/QtCore/QThread.html

    The PySide.QtCore.QThread class provides platform-independent threads.

    A PySide.QtCore.QThread represents a separate thread of control within the program; it shares data with all the other threads within the process but executes independently in the way that a separate program does on a multitasking operating system. Instead of starting in main() , QThreads begin executing in PySide.QtCore.QThread.run() . By default, PySide.QtCore.QThread.run() starts the event loop by calling exec() (see below). To create your own threads, subclass PySide.QtCore.QThread and reimplement PySide.QtCore.QThread.run() . For example:

        class MyThread (QThread):
            def run():
                socket = QTcpSocket()
                # connect QTcpSocket's signals somewhere meaningful
                # ...
                socket.connectToHost(hostName, portNumber)
                self.exec_()

    This will create a PySide.QtNetwork.QTcpSocket in the thread and then execute the thread’s event loop. Use the PySide.QtCore.QThread.start() method to begin execution. Execution ends when you return from PySide.QtCore.QThread.run() , just as an application does when it leaves main(). PySide.QtCore.QThread will notifiy you via a signal when the thread is PySide.QtCore.QThread.started() , PySide.QtCore.QThread.finished() , and PySide.QtCore.QThread.terminated() , or you can use PySide.QtCore.QThread.isFinished() and PySide.QtCore.QThread.isRunning() to query the state of the thread. Use PySide.QtCore.QThread.wait() to block until the thread has finished execution.

    Each thread gets its own stack from the operating system. The operating system also determines the default size of the stack. You can use PySide.QtCore.QThread.setStackSize() to set a custom stack size.

    Each PySide.QtCore.QThread can have its own event loop. You can start the event loop by calling exec() ; you can stop it by calling PySide.QtCore.QThread.exit() or PySide.QtCore.QThread.quit() . Having an event loop in a thread makes it possible to connect signals from other threads to slots in this thread, using a mechanism called queued connections . It also makes it possible to use classes that require the event loop, such as PySide.QtCore.QTimer and PySide.QtNetwork.QTcpSocket , in the thread. Note, however, that it is not possible to use any widget classes in the thread.

    In extreme cases, you may want to forcibly PySide.QtCore.QThread.terminate() an executing thread. However, doing so is dangerous and discouraged. Please read the documentation for PySide.QtCore.QThread.terminate() and PySide.QtCore.QThread.setTerminationEnabled() for detailed information.

    The static functions PySide.QtCore.QThread.currentThreadId() and PySide.QtCore.QThread.currentThread() return identifiers for the currently executing thread. The former returns a platform specific ID for the thread; the latter returns a PySide.QtCore.QThread pointer.

    PySide.QtCore.QThread also provides platform independent sleep functions in varying resolutions. Use PySide.QtCore.QThread.sleep() for full second resolution, PySide.QtCore.QThread.msleep() for millisecond resolution, and PySide.QtCore.QThread.usleep() for microsecond resolution.

##QtCore.QMutex
http://srinikom.github.io/pyside-docs/PySide/QtCore/QMutex.html

    The PySide.QtCore.QMutex class provides access serialization between threads.

    The purpose of a PySide.QtCore.QMutex is to protect an object, data structure or section of code so that only one thread can access it at a time (this is similar to the Java synchronized keyword). It is usually best to use a mutex with a PySide.QtCore.QMutexLocker since this makes it easy to ensure that locking and unlocking are performed consistently.

    For example, say there is a method that prints a message to the user on two lines:

        number = 6

        def method1():
            number *= 5
            number /= 4

        def method2():
            number *= 3
            number /= 2

    If these two methods are called in succession, the following happens:

        # method1()
        number *= 5        # number is now 30
        number /= 4        # number is now 7

        # method2()
        number *= 3        # number is now 21
        number /= 2        # number is now 10

    If these two methods are called simultaneously from two threads then the following sequence could result:

        # Thread 1 calls method1()
        number *= 5        # number is now 30

        # Thread 2 calls method2().
        #
        # Most likely Thread 1 has been put to sleep by the operating
        # system to allow Thread 2 to run.
        number *= 3        # number is now 90
        number /= 2        # number is now 45

        # Thread 1 finishes executing.
        number /= 4        # number is now 11, instead of 10

    If we add a mutex, we should get the result we want:

        mutex = QMutex()
        number = 6

        def method1():
            mutex.lock()
            number *= 5
            number /= 4
            mutex.unlock()

        def method2():
            mutex.lock()
            number *= 3
            number /= 2
            mutex.unlock()

    Then only one thread can modify number at any given time and the result is correct. This is a trivial example, of course, but applies to any other case where things need to happen in a particular sequence.
