Things that might be useful when working through Chapter 10 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

# Useful links
Drag and drop Qt
http://qt-project.org/doc/qt-4.8/dnd.html

Enumeration of dropaction    
http://qt-project.org/doc/qt-4.8/qt.html#DropAction-enum
	Qt::CopyAction	        0x1(1)      Copy the data to the target.
	Qt::MoveAction	        0x2(2)	    Move the data from the source to the target.
	Qt::LinkAction	        0x4(4)	    Create a link from the source to the target.
	Qt::ActionMask	        0xff(255)	 
	Qt::IgnoreAction	    0x0 (0)	    Ignore the action (do nothing with the data).
	Qt::TargetMoveAction	0x8002(32770) On Windows, used when ownership of the D&D data should be taken over by the target application, i.e., the source application should not delete the data. On X11 this value is used to do a move. TargetMoveAction is not used on the Mac.

# Useful Documentation
## QtCore.QEvent
http://github.io/docs/pyside/PySide/QtCore/QEvent.html

    The QtCore.QEvent class is the base class of all event classes. Event objects contain event parameters.

    Qt’s main event loop (QtCore.QCoreApplication.exec()) fetches native window system events from the event queue, translates them into QEvents, and sends the translated events to QtCore.QObjects.

    In general, many events come from the underlying window system (for such events, QtCore.QEvent.spontaneous() returns true; i.e., returns True if the event originated outside the application (a system event). But it is also possible to manually send events using QtCore.QCoreApplication.sendEvent() and QtCore.QCoreApplication.postEvent() (in which case, if the event is from the application itself, QtCore.QEvent.spontaneous() returns false).

    QObjects receive events by having their QObject.event() function called. The function can be reimplemented in subclasses to customize event handling and add additional event types; QWidget.event() is a notable example. By default, events are dispatched to event handlers like QWidget.mouseMoveEvent(). 

    The basic QtCore.QEvent contains only an event type parameter and an “accept” flag. The accept flag set with QtCore.QEvent.accept() , and cleared with QtCore.QEvent.ignore() . It is set by default, but don’t rely on this as subclasses may choose to clear it in their constructor.

    Subclasses of QtCore.QEvent contain additional parameters that describe the particular event.

	### QtCore.QEvent.Type
    This enum type defines the valid event types in Qt. The event types and the specialized classes for each type are as follows (prefix of QEvent, so for instance first is QEvent.None)
    Constant 							Description
    None 								Not an event.
    AccessibilityDescription 			Used to query accessibility description texts (QtGui.QAccessibleEvent).
    AccessibilityHelp 					Used to query accessibility help texts (QtGui.QAccessibleEvent).
    AccessibilityPrepare 				Accessibility information is requested.
    ActionAdded 						A new action has been added (QtGui.QActionEvent).
    ActionChanged 						An action has been changed (QtGui.QActionEvent).
    ActionRemoved 						An action has been removed (QtGui.QActionEvent).
    ActivationChange 					A widget’s top-level window activation state has changed.
    ApplicationActivate 				The application has been made available to the user.
    ApplicationFontChange 				The default application font has changed.
    ApplicationLayoutDirectionChange 	The default application layout direction has changed.
    ApplicationPaletteChange 			The default application palette has changed.
    ApplicationWindowIconChange 		The application’s icon has changed.
    ChildAdded 							An object gets a child (QtCore.QChildEvent).
    ChildPolished 						A widget child gets polished (QtCore.QChildEvent).
    ChildRemoved 						An object loses a child (QtCore.QChildEvent).
    Clipboard 							The clipboard contents have changed (QtGui.QClipboardEvent).
    Close 								Widget was closed (QtGui.QCloseEvent).
    ContentsRectChange 					The margins of the widget’s content rect changed.
    ContextMenu 						Context popup menu (QtGui.QContextMenuEvent).
    CursorChange 						The widget’s cursor has changed.
    DeferredDelete 						The object will be deleted after it has cleaned up.
    DragEnter 							Cursor enters widget during drag/drop operation (QtGui.QDragEnterEvent).
    DragLeave 							Cursor leaves widget during drag/drop operation (QtGui.QDragLeaveEvent).
    DragMove 							A drag and drop operation is in progress (QtGui.QDragMoveEvent).
    Drop 								A drag and drop operation is completed (QtGui.QDropEvent).
    EnabledChange 						Widget’s enabled state has changed.
    Enter 								Mouse enters widget’s boundaries.
    EnterEditFocus 						An editor widget gains focus for editing.
    EnterWhatsThisMode 					Send to toplevel widgets when application enters “What’s This?” mode.
    FileOpen 							File open request (QtGui.QFileOpenEvent).
    FocusIn 							Widget gains keyboard focus (QtGui.QFocusEvent).
    FocusOut 	                        Widget loses keyboard focus (QtGui.QFocusEvent).
    FontChange 	                        Widget’s font has changed.
    GrabKeyboard 	                    Item gains keyboard grab (QtGui.QGraphicsItem only).
    GrabMouse 	                        Item gains mouse grab (QtGui.QGraphicsItem only).
    GraphicsSceneContextMenu 	        Context popup menu over a graphics scene (QtGui.QGraphicsSceneContextMenuEvent).
    GraphicsSceneDragEnter 	            Cursor enters a graphics scene during DnD operation (QtGui.QGraphicsSceneDragDropEvent).
    GraphicsSceneDragLeave 	            Cursor leaves a graphics scene during a DnD operation (QtGui.QGraphicsSceneDragDropEvent).
    GraphicsSceneDragMove 	            DnD operation is in progress over a scene (QtGui.QGraphicsSceneDragDropEvent).
    GraphicsSceneDrop 	                DnD operation is completed over a scene (QtGui.QGraphicsSceneDragDropEvent).
    GraphicsSceneHelp 	                The user requests help for a graphics scene (QtGui.QHelpEvent).
    GraphicsSceneHoverEnter 	        The mouse cursor enters a hover item in a graphics scene (QtGui.QGraphicsSceneHoverEvent).
    GraphicsSceneHoverLeave 	        The mouse cursor leaves a hover item in a graphics scene (QtGui.QGraphicsSceneHoverEvent).
    GraphicsSceneHoverMove 	            The mouse cursor moves inside a hover item in a graphics scene (QtGui.QGraphicsSceneHoverEvent).
    GraphicsSceneMouseDoubleClick 	    Mouse press again (double click) in a graphics scene (QtGui.QGraphicsSceneMouseEvent).
    GraphicsSceneMouseMove 	            Move mouse in a graphics scene (QtGui.QGraphicsSceneMouseEvent).
    GraphicsSceneMousePress 	        Mouse press in a graphics scene (QtGui.QGraphicsSceneMouseEvent).
    GraphicsSceneMouseRelease 	        Mouse release in a graphics scene (QtGui.QGraphicsSceneMouseEvent).
    GraphicsSceneMove 	                Widget was moved (QtGui.QGraphicsSceneMoveEvent).
    GraphicsSceneResize 	            Widget was resized (QtGui.QGraphicsSceneResizeEvent).
    GraphicsSceneWheel 	                Mouse wheel rolled in a graphics scene (QtGui.QGraphicsSceneWheelEvent).
    Hide 	                            Widget was hidden (QtGui.QHideEvent).
    HideToParent 	                    A child widget has been hidden.
    HoverEnter 	                        The mouse cursor enters a hover widget (QtGui.QHoverEvent).
    HoverLeave 	                        The mouse cursor leaves a hover widget (QtGui.QHoverEvent).
    HoverMove 	                        The mouse cursor moves inside a hover widget (QtGui.QHoverEvent).
    IconDrag 	                        The main icon of a window has been dragged away (QtGui.QIconDragEvent).
    IconTextChange 	                    Widget’s icon text has been changed.
    InputMethod 	                    An input method is being used (QtGui.QInputMethodEvent).
    KeyPress 	                        Key press (QtGui.QKeyEvent).
    KeyRelease 	                        Key release (QtGui.QKeyEvent).
    LanguageChange 	                    The application translation changed.
    LayoutDirectionChange 	            The direction of layouts changed.
    LayoutRequest 	                    Widget layout needs to be redone.
    Leave 	                            Mouse leaves widget’s boundaries.
    LeaveEditFocus 	                    An editor widget loses focus for editing.
    LeaveWhatsThisMode 	                Send to toplevel widgets when the application leaves “What’s This?” mode.
    LocaleChange 	                    The system locale has changed.
    NonClientAreaMouseButtonDblClick 	A mouse double click occurred outside the client area.
    NonClientAreaMouseButtonPress 	    A mouse button press occurred outside the client area.
    NonClientAreaMouseButtonRelease 	A mouse button release occurred outside the client area.
    NonClientAreaMouseMove 	            A mouse move occurred outside the client area.
    MenubarUpdated 	                    The window’s menu bar has been updated.
    MetaCall 	                        An asynchronous method invocation via QMetaObject.invokeMethod() .
    ModifiedChange 	                    Widgets modification state has been changed.
    MouseButtonDblClick 	            Mouse press again (QtGui.QMouseEvent).
    MouseButtonPress 	                Mouse press (QtGui.QMouseEvent).
    MouseButtonRelease 	                Mouse release (QtGui.QMouseEvent).
    MouseMove 	                        Mouse move (QtGui.QMouseEvent).
    MouseTrackingChange 	            The mouse tracking state has changed.
    Move 	                            Widget’s position changed (QtGui.QMoveEvent).
    Paint 	                            Screen update necessary (QtGui.QPaintEvent).
    PaletteChange 	                    Palette of the widget changed.
    ParentAboutToChange 	            The widget parent is about to change.
    ParentChange 	                    The widget parent has changed.
    PlatformPanel 	                    A platform specific panel has been requested.
    Polish 	                            The widget is polished.
    PolishRequest 	                    The widget should be polished.
    QueryWhatsThis 	                    The widget should accept the event if it has “What’s This?” help.
    RequestSoftwareInputPanel 	        A widget wants to open a software input panel (SIP).
    Resize 	                            Widget’s size changed (QtGui.QResizeEvent).
    Shortcut 	                        Key press in child for shortcut key handling (QtGui.QShortcutEvent).
    ShortcutOverride 	                Key press in child, for overriding shortcut key handling (QtGui.QKeyEvent).
    Show 	                            Widget was shown on screen (QtGui.QShowEvent).
    ShowToParent 	                    A child widget has been shown.
    SockAct 	                        Socket activated, used to implement QtCore.QSocketNotifier .
    StateMachineSignal 	                A signal delivered to a state machine ( QStateMachine.SignalEvent).
    StateMachineWrapped 	            The event is a wrapper for, i.e., contains, another event ( QStateMachine.WrappedEvent).
    StatusTip 	                        A status tip is requested (QtGui.QStatusTipEvent).
    StyleChange 	                    Widget’s style has been changed.
    OkRequest 	                        Ok button in decoration pressed. Supported only for Windows CE.
    Timer 	                            Regular timer events (QtCore.QTimerEvent).
    ToolTip 	                        A tooltip was requested (QtGui.QHelpEvent).
    ToolTipChange 	                    The widget’s tooltip has changed.
    UngrabKeyboard 	                    Item loses keyboard grab (QtGui.QGraphicsItem only).
    UngrabMouse 	                    Item loses mouse grab (QtGui.QGraphicsItem only).
    UpdateLater 	                    The widget should be queued to be repainted at a later time.
    UpdateRequest 	                    The widget should be repainted.
    WhatsThis 	                        The widget should reveal “What’s This?” help (QtGui.QHelpEvent).
    WhatsThisClicked 	                A link in a widget’s “What’s This?” help was clicked.
    Wheel 	                            Mouse wheel rolled (QtGui.QWheelEvent).
    WinEventAct 	                    A Windows-specific activation event has occurred.
    WindowActivate 	                    Window was activated.
    WindowBlocked 	                    The window is blocked by a modal dialog.
    WindowDeactivate 	                Window was deactivated.
    WindowIconChange 	                The window’s icon has changed.
    WindowStateChange 	                The window's state (minimized, maximized or full-screen) has changed (QtGui.QWindowStateChangeEvent).
    WindowTitleChange 	                The window title has changed.
    WindowUnblocked 	                The window is unblocked after a modal dialog exited.
    ZOrderChange 	                    The widget’s z-order has changed. This event is never sent to top level windows.
    KeyboardLayoutChange 	            The keyboard layout has changed.
    DynamicPropertyChange 	            A dynamic property was added, changed or removed from the object.
    TouchBegin 	                        Beginning of a sequence of touch-screen and/or track-pad events (QtGui.QTouchEvent)
    TouchUpdate 	                    Touch-screen event (QtGui.QTouchEvent)
    TouchEnd 	                        End of touch-event sequence (QtGui.QTouchEvent)
    WinIdChange 	                    The window system identifer for this native widget has changed
    Gesture 	                        A gesture was triggered (QtGui.QGestureEvent)
    GestureOverride 	                A gesture override was triggered (QtGui.QGestureEvent)


    For convenience, you can use the QtCore.QEvent.registerEventType() function to register and reserve a custom event type for your application. Doing so will allow you to avoid accidentally re-using a custom event type already in use elsewhere in your application.

    
## QtCore.QMimeData
http://srinikom.github.io/pyside-docs/PySide/QtCore/QMimeData.html

    The QtCore.QMimeData class provides a container for data that records information about its MIME (_Multipurpose Internet Mail Extensions_) type.

    QtCore.QMimeData is used to describe information that can be stored in the clipboard , and transferred via the drag and drop mechanism. QtCore.QMimeData objects associate the data that they hold with the corresponding MIME types to ensure that information can be safely transferred between applications, and copied around within the same application.

    QtCore.QMimeData objects are usually supplied to QtGui.QDrag or QtGui.QClipboard objects. This is to enable Qt to manage the memory that they use.

    A single QtCore.QMimeData object can store the same data using several different formats at the same time. The QtCore.QMimeData.formats() function returns a list of the available formats in order of preference. The QtCore.QMimeData.data() function returns the raw data associated with a MIME type, and QtCore.QMimeData.setData() allows you to set the data for a MIME type.

    For the most common MIME types, QtCore.QMimeData provides convenience functions to access the data:

    Tester 	    Getter 	        Setter 	        MIME Types
    hasText() 	text() 	        setText() 	    text/plain
    hasHtml() 	html() 	        setHtml() 	    text/html
    hasUrls() 	urls() 	        setUrls() 	    text/uri-list
    hasImage() 	imageData()     setImageData() 	image/ *
    hasColor() 	colorData()     setColorData() 	application/x-color
    

    ### Platform-Specific MIME Types

    On Windows, QtCore.QMimeData.formats() will also return custom formats available in the MIME data, using the x-qt-windows-mime subtype to indicate that they represent data in non-standard formats. The formats will take the following form:

        application/x-qt-windows-mime; value = "<custom type>"

    The following are examples of custom MIME types:

        application/x-qt-windows-mime; value = "FileGroupDescriptor"
        application/x-qt-windows-mime; value = "FileContents"

    The value declaration of each format describes the way in which the data is encoded.
    
## QtGui.QClipboard
http://srinikom.github.io/pyside-docs/PySide/QtGui/QClipboard.html

    The QtGui.QClipboard class provides access to the window system clipboard. The clipboard offers a simple mechanism to copy and paste data between applications. QtGui.QClipboard supports the same data types that QtGui.QDrag does, and uses similar mechanisms. See the Drag and Drop Qt page (link is above under Useful Links).

    There is a single QtGui.QClipboard object in an application, accessible as QApplication.clipboard().

    Example:
        clipboard = QApplication.clipboard()
        originalText = clipboard.text()
        clipboard.setText(newText)

    QtGui.QClipboard features some convenience functions to access common data types: QtGui.QClipboard.setText() allows the exchange of Unicode text, and QtGui.QClipboard.setPixmap() and QtGui.QClipboard.setImage() allows the exchange of QPixmaps and QImages between applications. The QtGui.QClipboard.setMimeData() function is the ultimate in flexibility: it allows you to add any QtCore.QMimeData into the clipboard. There are corresponding getters for each of these, e.g. QtGui.QClipboard.text() , QtGui.QClipboard.image() and QtGui.QClipboard.pixmap() . You can clear the clipboard by calling QtGui.QClipboard.clear() .

    A pseudocode example of the use of these functions follows:
        def paste(self):
            clipboard = QtGui.QApplication.clipboard()
            mimeData = clipboard.mimeData()

            if mimeData.hasImage():
                setPixmap(mimeData.imageData())
            elif mimeData.hasHtml():
                setText(mimeData.html())
                setTextFormat(QtCore.Qt.RichText)
            elif (mimeData.hasText():
                setText(mimeData.text())
                setTextFormat(QtCore.Qt.PlainText)
            else:
                setText(u"Cannot display data")


    On Windows, the MIME format does not always map directly to the clipboard formats. Qt provides QWindowsMime to map clipboard formats to open-standard MIME formats. 
    
    
## QtGui.QDrag
http://srinikom.github.io/pyside-docs/PySide/QtGui/QDrag.html

    The QtGui.QDrag class provides support for MIME-based drag and drop data transfer. Drag and drop is an intuitive way for users to copy or move data around in an application, and is used in many desktop environments as a mechanism for copying data between applications. Drag and drop support in Qt is centered around the QtGui.QDrag class that handles most of the details of a drag and drop operation.

    The data to be transferred by the drag and drop operation is contained in a QtCore.QMimeData object. This is specified with the QtGui.QDrag.setMimeData() function in the following way:

        drag =  QDrag(self)
        mimeData =  QMimeData()
        mimeData.setText(commentEdit.toPlainText())
        drag.setMimeData(mimeData)

    Note that QtGui.QDrag.setMimeData() assigns ownership of the QtCore.QMimeData object to the QtGui.QDrag object. The QtGui.QDrag must be constructed on the heap with a parent QtGui.QWidget to ensure that Qt can clean up after the drag and drop operation has been completed.

    A pixmap can be used to represent the data while the drag is in progress, and will move with the cursor to the drop target. This pixmap typically shows an icon that represents the MIME type of the data being transferred, but any pixmap can be set with QtGui.QDrag.setPixmap() . The cursor’s hot spot can be given a position relative to the top-left corner of the pixmap with the QtGui.QDrag.setHotSpot() function. The following code positions the pixmap so that the cursor’s hot spot points to the center of its bottom edge:

        drag.setHotSpot(QPoint(drag.pixmap().width()/2, drag.pixmap().height()))

    The source and target widgets can be found with QtGui.QDrag.source() and QtGui.QDrag.target() . These functions are often used to determine whether drag and drop operations started and finished at the same widget, so that special behavior can be implemented.

    QtGui.QDrag only deals with the drag and drop operation itself. It is up to the developer to decide when a drag operation begins, and how a QtGui.QDrag object should be constructed and used. For a given widget, it is often necessary to reimplement QtGui.QWidget.mousePressEvent() to determine whether the user has pressed a mouse button, and reimplement QtGui.QWidget.mouseMoveEvent() to check whether a QtGui.QDrag is required.


## QtGui.QColor
http://srinikom.github.io/pyside-docs/PySide/QtGui/QColor.html

    The QtGui.QColor class provides colors based on RGB, HSV or CMYK values.

    A color is normally specified in terms of RGB (red, green, and blue) components, but it is also possible to specify it in terms of HSV (hue, saturation, and value) and CMYK (cyan, magenta, yellow and black) components. In addition a color can be specified using a color name. The color name can be any of the SVG 1.0 color names.

    The QtGui.QColor constructor creates the color based on RGB values. To create a QtGui.QColor based on either HSV or CMYK values, use the QtGui.QColor.toHsv() and QtGui.QColor.toCmyk() functions respectively. These functions return a copy of the color using the desired format. In addition the static QtGui.QColor.fromRgb() , QtGui.QColor.fromHsv() and QtGui.QColor.fromCmyk() functions create colors from the specified values. 
    
    Alternatively, a color can be converted to any of the three formats using the QtGui.QColor.convertTo() function (returning a copy of the color in the desired format), or any of the QtGui.QColor.setRgb() , QtGui.QColor.setHsv() and QtGui.QColor.setCmyk() functions altering this color’s format. The QtGui.QColor.spec() function tells how the color was specified.

    A color can be set by passing an RGB string (such as “#112233”), or a color name (such as “blue”), to the QtGui.QColor.setNamedColor() function. The color names are taken from the SVG 1.0 color names. The QtGui.QColor.name() function returns the name of the color in the format “#RRGGBB”. Colors can also be set using QtGui.QColor.setRgb() , QtGui.QColor.setHsv() and QtGui.QColor.setCmyk() . To get a lighter or darker color use the QtGui.QColor.lighter() and QtGui.QColor.darker() functions respectively.

    The QtGui.QColor.isValid() function indicates whether a QtGui.QColor is legal at all. For example, a RGB color with RGB values out of range is illegal. For performance reasons, QtGui.QColor mostly disregards illegal colors, and for that reason, the result of using an invalid color is undefined.

    The color components can be retrieved individually, e.g with QtGui.QColor.red() , QtGui.QColor.hue() and QtGui.QColor.cyan() . The values of the color components can also be retrieved in one go using the QtGui.QColor.getRgb() , QtGui.QColor.getHsv() and QtGui.QColor.getCmyk() functions. Using the RGB color model, the color components can in addition be accessed with QtGui.QColor.rgb() .

    QtGui.QColor is platform and device independent. The QColormap class maps the color to the hardware. For more information about painting in general, see the Paint System documentation.

    ### Integer vs. Floating Point Precision

    QtGui.QColor supports floating point precision and provides floating point versions of all the color components functions, e.g. QtGui.QColor.getRgbF() , QtGui.QColor.hueF() and QtGui.QColor.fromCmykF() . Note that since the components are stored using 16-bit integers, there might be minor deviations between the values set using, for example, QtGui.QColor.setRgbF() and the values returned by the QtGui.QColor.getRgbF() function due to rounding.

    While the integer based functions take values in the range 0-255 (except QtGui.QColor.hue() which must have values within the range 0-359), the floating point functions accept values in the range 0.0 - 1.0.

    ### Alpha-Blended Drawing

    QtGui.QColor also support alpha-blended outlining and filling. The alpha channel of a color specifies the transparency effect, 0 represents a fully transparent color, while 255 represents a fully opaque color. For example:

        # Specify semi-transparent red
        painter.setBrush(QColor(255, 0, 0, 127))
        painter.drawRect(0, 0, self.width()/2, self.height())

        # Specify semi-transparent blue
        painter.setBrush(QColor(0, 0, 255, 127))
        painter.drawRect(0, 0, self.width(), self.height()/2)

    Alpha-blended drawing is supported on Windows, Mac OS X, and on X11 systems that have the X Render extension installed.

    The alpha channel of a color can be retrieved and set using the QtGui.QColor.alpha() and QtGui.QColor.setAlpha() functions if its value is an integer, and QtGui.QColor.alphaF() and QtGui.QColor.setAlphaF() if its value is qreal (double). By default, the alpha-channel is set to 255 (opaque). To retrieve and set all the RGB color components (including the alpha-channel) in one go, use the QtGui.QColor.rgba() and QtGui.QColor.setRgba() functions.

    ### Predefined Colors

    There are 20 predefined QColors described by the Qt.GlobalColor enum, including black, white, primary and secondary colors, darker versions of these colors and three shades of gray. QtGui.QColor also recognizes a variety of color names; the static QtGui.QColor.colorNames() function returns a QtCore.QStringList color names that QtGui.QColor knows about.

    #### Color name enum
    http://qt-project.org/doc/qt-4.8/qt.html#GlobalColor-enum
    white, black, gray, lightGray, darkGray
    red, darkRed, green, darkGreen, yellow, darkYellow, blue, darkBlue,
    cyan, darkCyan, magenta, darkMagenta


    ### The HSV Color Model

    The RGB model is hardware-oriented. Its representation is close to what most monitors show. In contrast, HSV represents color in a way more suited to the human perception of color. For example, the relationships “stronger than”, “darker than”, and “the opposite of” are easily expressed in HSV but are much harder to express in RGB.

    HSV, like RGB, has three components:

        H, for hue, is in the range 0 to 359 (i.e., the circle in degrees) if the color is chromatic (not gray), or meaningless if it is gray. It represents degrees on the color wheel familiar to most people. Red is 0 (degrees), green is 120, and blue is 240.

        S, for saturation, is in the range 0 to 255, and the bigger it is, the stronger the color is. Grayish colors have saturation near 0; very strong colors have saturation near 255.

        V, for value, is in the range 0 to 255 and represents lightness or brightness of the color. 0 is black; 255 is as far from black as possible.

    Here are some examples: pure red is H=0, S=255, V=255; a dark red, moving slightly towards the magenta, could be H=350 (equivalent to -10), S=255, V=180; a grayish light red could have H about 0 (say 350-359 or 0-10), S about 50-100, and S=255.

    Qt returns a hue value of -1 for achromatic colors. If you pass a hue value that is too large, Qt forces it into range. Hue 360 or 720 is treated as 0; hue 540 is treated as 180.

    In addition to the standard HSV model, Qt provides an alpha-channel to feature alpha-blended drawing .

    ### The HSL Color Model

    HSL is similar to HSV. Instead of value parameter from HSV, HSL has the lightness parameter. The lightness parameter goes from black to color and from color to white. If you go outside at the night it's black or dark gray. At day its colorful but if you look in a really strong light a things they are going to white and wash out.

    ### The CMYK Color Model

    While the RGB and HSV color models are used for display on computer monitors, the CMYK model is used in the four-color printing process of printing presses and some hard-copy devices.

    CMYK has four components, all in the range 0-255: cyan (C), magenta (M), yellow (Y) and black (K). Cyan, magenta and yellow are called subtractive colors; the CMYK color model creates color by starting with a white surface and then subtracting color by applying the appropriate components. While combining cyan, magenta and yellow gives the color black, subtracting one or more will yield any other color. When combined in various percentages, these three colors can create the entire spectrum of colors.

    Mixing 100 percent of cyan, magenta and yellow does produce black, but the result is unsatisfactory since it wastes ink, increases drying time, and gives a muddy colour when printing. For that reason, black is added in professional printing to provide a solid black tone; hence the term ‘four color process’.

    In addition to the standard CMYK model, Qt provides an alpha-channel to feature alpha-blended drawing.

