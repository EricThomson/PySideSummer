Things that might be useful when working through Chapter 4 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
##List of supported style sheet properties:  
http://qt-project.org/doc/qt-4.8/stylesheet-reference.html#list-of-properties

##Similar example using new-style signals/slots:
http://www.blog.pythonlibrary.org/2013/04/10/pyside-connecting-multiple-widgets-to-the-same-slot/

##On partial functions:
http://www.learnpython.org/en/Partial_functions
http://www.techrepublic.com/article/partial-function-application-in-python/

##On lambda functions:
http://www.diveintopython.net/power_of_introspection/lambda_functions.html
http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/

##On currency converters
http://www.blog.pythonlibrary.org/2013/04/09/pyside-creating-a-currency-converter/


#Useful Documentation

##QtCore.QTimer
http://srinikom.github.io/pyside-docs/PySide/QtCore/QTimer.html

    The PySide.QtCore.QTimer class provides repetitive and single-shot timers.

    The PySide.QtCore.QTimer class provides a high-level programming interface for timers. To use it, create a PySide.QtCore.QTimer , connect its PySide.QtCore.QTimer.timeout() signal to the appropriate slots, and call PySide.QtCore.QTimer.start() . From then on it will emit the PySide.QtCore.QTimer.timeout() signal at constant intervals.

    Example for a one second (1000 millisecond) timer (from the Analog Clock example):

        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.update)
        timer.start(1000)

    From then on, the update() slot is called every second.

    You can set a timer to time out only once by calling setSingleShot(true). You can also use the static QTimer.singleShot() function to call a slot after a specified interval:

        QTimer.singleShot(200, self.updateCaption)

    In multithreaded applications, you can use PySide.QtCore.QTimer in any thread that has an event loop. To start an event loop from a non-GUI thread, use QThread.exec() . Qt uses the timer’s thread affinity to determine which thread will emit the PySide.QtCore.QTimer.timeout() signal. Because of this, you must start and stop the timer in its thread; it is not possible to start a timer from another thread.

    As a special case, a PySide.QtCore.QTimer with a timeout of 0 will time out as soon as all the events in the window system’s event queue have been processed. This can be used to do heavy work while providing a snappy user interface:

        timer = QTimer(self)
        timer.timeout.connect(self.processOneThing)
        timer.start()

    processOneThing() will from then on be called repeatedly. It should be written in such a way that it always returns quickly (typically after processing one data item) so that Qt can deliver events to widgets and stop the timer as soon as it has done all its work. This is the traditional way of implementing heavy work in GUI applications; multithreading is now becoming available on more and more platforms, and we expect that zero-millisecond QTimers will gradually be replaced by PySide.QtCore.QThread s.

    ###Accuracy and Timer Resolution

    Timers will never time out earlier than the specified timeout value and they are not guaranteed to time out at the exact value specified. In many situations, they may time out late by a period of time that depends on the accuracy of the system timers.

    The accuracy of timers depends on the underlying operating system and hardware. Most platforms support a resolution of 1 millisecond, though the accuracy of the timer will not equal this resolution in many real-world situations.

    If Qt is unable to deliver the requested number of timer clicks, it will silently discard some.

    ###Alternatives to QTimer

    An alternative to using PySide.QtCore.QTimer is to call QObject.startTimer() for your object and reimplement the QObject.timerEvent() event handler in your class (which must inherit PySide.QtCore.QObject ). The disadvantage is that PySide.QtCore.QTimer.timerEvent() does not support such high-level features as single-shot timers or signals.

    Another alternative to using PySide.QtCore.QTimer is to use PySide.QtCore.QBasicTimer . It is typically less cumbersome than using QObject.startTimer() directly. See Timers for an overview of all three approaches.

    Some operating systems limit the number of timers that may be used; Qt tries to work around these limitations.