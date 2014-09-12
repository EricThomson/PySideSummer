Things that might be useful when working through Chapter 11 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
Great stuff on painting, from Qt:
http://qt-project.org/doc/qt-4.8/paintsystem.html

Lots of examples, maybe some of those that are not there now will be put there in the future:
https://github.com/PySide/Examples

On size policies:
http://qt-project.org/doc/qt-5/qsizepolicy.html#Policy-enum

Color roles:
http://pyside.github.io/docs/pyside/PySide/QtGui/QPalette.html#PySide.QtGui.PySide.QtGui.QPalette.ColorRole

#Useful documentation
##QtGui.QWidget
http://github.io/docs/pyside/PySide/QtGui/QWidget.html

    The QtGui.QWidget class is the base class of all user interface objects.

    The widget is the atom of the user interface: it receives mouse, keyboard and other events from the window system, and paints a representation of itself on the screen. Every widget is rectangular, and they are sorted in a Z-order. A widget is clipped by its parent and by the widgets in front of it.

    A widget that is not embedded in a parent widget is called a window. Usually, windows have a frame and a title bar, although it is also possible to create windows without such decoration using suitable window flags ). In Qt, QtGui.QMainWindow and the various subclasses of QtGui.QDialog are the most common window types.

    Every widget’s constructor accepts one or two standard arguments:
		1. parent = 0 is the parent of the new widget. If it is 0 (the default), the new widget will be a window. If not, it will be a child of parent, and be constrained by parent's geometry (unless you specify Qt.Window as window flag).
		
		2. Qt.WindowFlags f = 0 (where available) sets the window flags; the default is suitable for almost all widgets, but to get, for example, a window without a window system frame, you must use special flags.
	
    QtGui.QWidget has many member functions, but some of them have little direct functionality; for example, QtGui.QWidget has a font property, but never uses this itself. There are many subclasses which provide real functionality, such as QtGui.QLabel, QtGui.QPushButton, QtGui.QListWidget, and QtGui.QTabWidget.

	###Top-Level and Child Widgets

    A widget without a parent widget is always an independent window (top-level widget). For these widgets, QtGui.QWidget.setWindowTitle() and QtGui.QWidget.setWindowIcon() set the title bar and icon respectively.

    Non-window widgets are child widgets, displayed within their parent widgets. Most widgets in Qt are mainly useful as child widgets. For example, it is possible to display a button as a top-level window, but most people prefer to put their buttons inside other widgets, such as QtGui.QDialog [for diagram see web page].

    If you want to use a QtGui.QWidget to hold child widgets you will usually want to add a layout to the parent QtGui.QWidget. See Layout Management for more information.

	###Composite Widgets

    When a widget is used as a container to group a number of child widgets, it is known as a composite widget. These can be created by constructing a widget with the required visual properties - a QtGui.QFrame, for example - and adding child widgets to it, usually managed by a layout [see diagram].

    Composite widgets can also be created by subclassing a standard widget, such as QtGui.QWidget or QtGui.QFrame, and adding the necessary layout and child widgets in the constructor of the subclass. Many of the examples provided with Qt use this approach, and it is also covered in the Qt Tutorials.

	###Custom Widgets and Painting

    Since QtGui.QWidget is a subclass of QtGui.QPaintDevice, subclasses can be used to display custom content that is composed using a series of painting operations with an instance of the QtGui.QPainter class. This approach contrasts with the canvas-style approach used by the Graphics View Framework where items are added to a scene by the application and are rendered by the framework itself.

    Each widget performs all painting operations from within its QtGui.QWidget.paintEvent() function. This is called whenever the widget needs to be redrawn, either as a result of some external change or when requested by the application.

	###Size Hints and Size Policies

    When implementing a new widget, it is almost always useful to reimplement QtGui.QWidget.sizeHint() to provide a reasonable default size for the widget and to set the correct size policy with QtGui.QWidget.setSizePolicy().

    By default, composite widgets which do not provide a size hint will be sized according to the space requirements of their child widgets.

    The size policy lets you supply good default behavior for the layout management system, so that other widgets can contain and manage yours easily. The default size policy indicates that the size hint represents the preferred size of the widget, and this is often good enough for many widgets.

    The size of top-level widgets are constrained to 2/3 of the desktop’s height and width. You can QtGui.QWidget.resize() the widget manually if these bounds are inadequate.

	###Events

    Widgets respond to events that are typically caused by user actions. Qt delivers events to widgets by calling specific event handler functions with instances of QtCore.QEvent subclasses containing information about each event.

    If your widget only contains child widgets, you probably do not need to implement any event handlers. If you want to detect a mouse click in a child widget call the child’s QtGui.QWidget.underMouse() function inside the widget’s QtGui.QWidget.mousePressEvent().

    The Scribble example implements a wider set of events to handle mouse movement, button presses, and window resizing.

    You will need to supply the behavior and content for your own widgets, but here is a brief overview of the events that are relevant to QtGui.QWidget, starting with the most common ones:

        QtGui.QWidget.paintEvent() is called whenever the widget needs to be repainted. Every widget displaying custom content must implement it. Painting using a QtGui.QPainter can only take place in a QtGui.QWidget.paintEvent() or a function called by a QtGui.QWidget.paintEvent().
		
        QtGui.QWidget.resizeEvent() is called when the widget has been resized.
		
        QtGui.QWidget.mousePressEvent() is called when a mouse button is pressed while the mouse cursor is inside the widget, or when the widget has grabbed the mouse using QtGui.QWidget.grabMouse(). Pressing the mouse without releasing it is effectively the same as calling QtGui.QWidget.grabMouse().
		
        QtGui.QWidget.mouseReleaseEvent() is called when a mouse button is released. A widget receives mouse release events when it has received the corresponding mouse press event. This means that if the user presses the mouse inside your widget, then drags the mouse somewhere else before releasing the mouse button, your widget receives the release event. There is one exception: if a popup menu appears while the mouse button is held down, this popup immediately steals the mouse events.
		
        QtGui.QWidget.mouseDoubleClickEvent() is called when the user double-clicks in the widget. If the user double-clicks, the widget receives a mouse press event, a mouse release event and finally this event instead of a second mouse press event. (Some mouse move events may also be received if the mouse is not held steady during this operation.) It is not possible to distinguish a click from a double-click until the second click arrives. (This is one reason why most GUI books recommend that double-clicks be an extension of single-clicks, rather than trigger a different action.)

    Widgets that accept keyboard input need to reimplement a few more event handlers:

        QtGui.QWidget.keyPressEvent() is called whenever a key is pressed, and again when a key has been held down long enough for it to auto-repeat. The Tab and Shift+Tab keys are only passed to the widget if they are not used by the focus-change mechanisms. To force those keys to be processed by your widget, you must reimplement QWidget.event().
		
        QtGui.QWidget.focusInEvent() is called when the widget gains keyboard focus (assuming you have called QtGui.QWidget.setFocusPolicy() ). Well-behaved widgets indicate that they own the keyboard focus in a clear but discreet way.
		
        QtGui.QWidget.focusOutEvent() is called when the widget loses keyboard focus.

    You may be required to also reimplement some of the less common event handlers:

        QtGui.QWidget.mouseMoveEvent() is called whenever the mouse moves while a mouse button is held down. This can be useful during drag and drop operations. If you call QtGui.QWidget.setMouseTracking() (true), you get mouse move events even when no buttons are held down. (See also the Drag and Drop guide.)
		
        QtGui.QWidget.keyReleaseEvent() is called whenever a key is released and while it is held down (if the key is auto-repeating). In that case, the widget will receive a pair of key release and key press event for every repeat. The Tab and Shift+Tab keys are only passed to the widget if they are not used by the focus-change mechanisms. To force those keys to be processed by your widget, you must reimplement QWidget.event().
		
        QtGui.QWidget.wheelEvent() is called whenever the user turns the mouse wheel while the widget has the focus.
		
        QtGui.QWidget.enterEvent() is called when the mouse enters the widget’s screen space. (This excludes screen space owned by any of the widget’s children.)
		
        QtGui.QWidget.leaveEvent() is called when the mouse leaves the widget’s screen space. If the mouse enters a child widget it will not cause a QtGui.QWidget.leaveEvent().
		
        QtGui.QWidget.moveEvent() is called when the widget has been moved relative to its parent.
        QtGui.QWidget.closeEvent() is called when the user closes the widget (or when QtGui.QWidget.close() is called).

    There are also some rather obscure events described in the documentation for QEvent.Type. To handle these events, you need to reimplement QtGui.QWidget.event() directly.

    The default implementation of QtGui.QWidget.event() handles Tab and Shift+Tab (to move the keyboard focus), and passes on most of the other events to one of the more specialized handlers above.

    Events and the mechanism used to deliver them are covered in The Event System.

	###Groups of Functions and Properties

    Window functions 	
	QtGui.QWidget.show(), QtGui.QWidget.hide(), raise(), QtGui.QWidget.lower(), QtGui.QWidget.close().
	
    Top-level windows 	
	windowModified(), QtGui.QWidget.windowTitle(), QtGui.QWidget.windowIcon(), QtGui.QWidget.windowIconText(), QtGui.QWidget.isActiveWindow(), QtGui.QWidget.activateWindow(), minimized(), QtGui.QWidget.showMinimized(), maximized(), QtGui.QWidget.showMaximized(), fullScreen(), QtGui.QWidget.showFullScreen(), QtGui.QWidget.showNormal().
	
    Window contents 	
	QtGui.QWidget.update(), QtGui.QWidget.repaint(), QtGui.QWidget.scroll().
	
    Geometry 	QtGui.QWidget.pos(), QtGui.QWidget.x(), QtGui.QWidget.y(), QtGui.QWidget.rect(), QtGui.QWidget.size(), QtGui.QWidget.width(), QtGui.QWidget.height(), QtGui.QWidget.move(), QtGui.QWidget.resize(), QtGui.QWidget.sizePolicy(), QtGui.QWidget.sizeHint(), QtGui.QWidget.minimumSizeHint(), QtGui.QWidget.updateGeometry(), QtGui.QWidget.layout(), QtGui.QWidget.frameGeometry(), QtGui.QWidget.geometry(), QtGui.QWidget.childrenRect(), QtGui.QWidget.childrenRegion(), QtGui.QWidget.adjustSize(), QtGui.QWidget.mapFromGlobal(), QtGui.QWidget.mapToGlobal(), QtGui.QWidget.mapFromParent(), QtGui.QWidget.mapToParent(), QtGui.QWidget.maximumSize(), QtGui.QWidget.minimumSize(), QtGui.QWidget.sizeIncrement(), QtGui.QWidget.baseSize(), QtGui.QWidget.setFixedSize()
	
    Mode 	
	visible(), QtGui.QWidget.isVisibleTo(), enabled(), QtGui.QWidget.isEnabledTo(), modal(), QtGui.QWidget.isWindow(), mouseTracking(), QtGui.QWidget.updatesEnabled(), QtGui.QWidget.visibleRegion().
	
    Look and feel 	
	QtGui.QWidget.style(), QtGui.QWidget.setStyle(), QtGui.QWidget.styleSheet(), QtGui.QWidget.cursor(), QtGui.QWidget.font(), QtGui.QWidget.palette(), QtGui.QWidget.backgroundRole(), QtGui.QWidget.setBackgroundRole(), QtGui.QWidget.fontInfo(), QtGui.QWidget.fontMetrics().
	
    Keyboard focus functions
 	focus(), QtGui.QWidget.focusPolicy(), QtGui.QWidget.setFocus(), QtGui.QWidget.clearFocus(), QtGui.QWidget.setTabOrder(), QtGui.QWidget.setFocusProxy(), QtGui.QWidget.focusNextChild(), QtGui.QWidget.focusPreviousChild().
	
    Mouse and keyboard grabbing 
	QtGui.QWidget.grabMouse(), QtGui.QWidget.releaseMouse(), QtGui.QWidget.grabKeyboard(), QtGui.QWidget.releaseKeyboard(), QtGui.QWidget.mouseGrabber(), QtGui.QWidget.keyboardGrabber().
	
    Event handlers 	
	QtGui.QWidget.event(), QtGui.QWidget.mousePressEvent(), QtGui.QWidget.mouseReleaseEvent(), QtGui.QWidget.mouseDoubleClickEvent(), QtGui.QWidget.mouseMoveEvent(), QtGui.QWidget.keyPressEvent(), QtGui.QWidget.keyReleaseEvent(), QtGui.QWidget.focusInEvent(), QtGui.QWidget.focusOutEvent(), QtGui.QWidget.wheelEvent(), QtGui.QWidget.enterEvent(), QtGui.QWidget.leaveEvent(), QtGui.QWidget.paintEvent(), QtGui.QWidget.moveEvent(), QtGui.QWidget.resizeEvent(), QtGui.QWidget.closeEvent(), QtGui.QWidget.dragEnterEvent(), QtGui.QWidget.dragMoveEvent(), QtGui.QWidget.dragLeaveEvent(), QtGui.QWidget.dropEvent(), QtCore.QObject.childEvent(), QtGui.QWidget.showEvent(), QtGui.QWidget.hideEvent(), QtCore.QObject.customEvent(). QtGui.QWidget.changeEvent().
	
    System functions 	
	QtGui.QWidget.parentWidget(), QtGui.QWidget.window(), QtGui.QWidget.setParent(), QtGui.QWidget.winId(), find(), QtGui.QWidget.metric().
	
    Interactive help 	
	QtGui.QWidget.setToolTip(), QtGui.QWidget.setWhatsThis()

	###Widget Style Sheets

    In addition to the standard widget styles for each platform, widgets can also be styled according to rules specified in a style sheet. This feature enables you to customize the appearance of specific widgets to provide visual cues to users about their purpose. For example, a button could be styled in a particular way to indicate that it performs a destructive action.

    The use of widget style sheets is described in more detail in the Qt Style Sheets document.

    To rapidly update custom widgets with simple background colors, such as real-time plotting or graphing widgets, it is better to define a suitable background color (using QtGui.QWidget.setBackgroundRole() with the QPalette.Window role), set the QtGui.QWidget.autoFillBackground() property, and only implement the necessary drawing functionality in the widget’s QtGui.QWidget.paintEvent().
	
	
	
##QtGui.QPainter
http://github.io/docs/pyside/PySide/QtGui/QPainter.html

    The QtGui.QPainter class performs low-level painting on widgets and other paint devices.

    QtGui.QPainter provides highly optimized functions to do most of the drawing GUI programs require. It can draw everything from simple lines to complex shapes like pies and chords. It can also draw aligned text and pixmaps. Normally, it draws in a “natural” coordinate system, but it can also do view and world transformation. QtGui.QPainter can operate on any object that inherits the QtGui.QPaintDevice class.

    The common use of QtGui.QPainter is inside a widget’s paint event: Construct and customize (e.g. set the pen or the brush) the painter. Then draw. For example:

        def paintEvent(self, paintEvent):
            painter = QPainter(self)
            painter.setPen(Qt.blue)
            painter.setFont(QFont("Arial", 30))
            painter.drawText(rect(), Qt.AlignCenter, "Qt")

    The core functionality of QtGui.QPainter is drawing, but the class also provide several functions that allows you to customize QtGui.QPainter‘s settings and its rendering quality, and others that enable clipping. In addition you can control how different shapes are merged together by specifying the painter’s composition mode.

    When the paintdevice is a widget, QtGui.QPainter can only be used inside a paintEvent() function or in a function called by paintEvent().

    ###Settings

    There are several settings that you can customize to make QtGui.QPainter draw according to your preferences:

        QPainter.font() is the font used for drawing text. If the painter QPainter.isActive(), you can retrieve information about the currently set font, and its metrics, using the QPainter.fontInfo() and QPainter.fontMetrics() functions respectively.
        
        QPainter.brush() defines the color or pattern that is used for filling shapes.
        
        QPainter.pen() defines the color or stipple that is used for drawing lines or boundaries.
        
        QPainter.backgroundMode() defines whether there is a QPainter.background() or not, i.e it is either Qt.OpaqueMode or Qt.TransparentMode.
        
        QPainter.background() only applies when QPainter.backgroundMode() is Qt.OpaqueMode and QPainter.pen() is a stipple. In that case, it describes the color of the background pixels in the stipple.
        
        QPainter.brushOrigin() defines the origin of the tiled brushes, normally the origin of widget’s background.
        
        QPainter.viewport(), QPainter.window(), QPainter.worldTransform() make up the painter’s coordinate transformation system. For more information, see the Coordinate Transformations section and the Coordinate System documentation (#?)
               
        QPainter.layoutDirection() defines the layout direction used by the painter when drawing text.
        
        QPainter.worldMatrixEnabled() tells whether world transformation is enabled.
        
        QPainter.viewTransformEnabled() tells whether view transformation is enabled.

    Note that some of these settings mirror settings in some paint devices, e.g. QWidget.font(). The QPainter.begin() function (or equivalently the QtGui.QPainter constructor) copies these attributes from the paint device.

    You can at any time save the QtGui.QPainter‘s state by calling the QtGui.QPainter.save() function which saves all the available settings on an internal stack. The QtGui.QPainter.restore() function pops them back.

    ###Drawing

    QtGui.QPainter provides functions to draw most primitives: 
    
        QtGui.QPainter.drawPoint(), QtGui.QPainter.drawPoints(), QtGui.QPainter.drawLine(), QtGui.QPainter.drawRect(), QtGui.QPainter.drawRoundedRect(), QtGui.QPainter.drawEllipse(), QtGui.QPainter.drawArc(), QtGui.QPainter.drawPie(), QtGui.QPainter.drawChord(), QtGui.QPainter.drawPolyline(), QtGui.QPainter.drawPolygon(), QtGui.QPainter.drawConvexPolygon() and drawCubicBezier(). 
        
    The two convenience functions, QtGui.QPainter.drawRects() and QtGui.QPainter.drawLines(), draw the given number of rectangles or lines in the given array of QRects or QLines using the current pen and brush.

    The QtGui.QPainter class also provides the QtGui.QPainter.fillRect() function which fills the given QtCore.QRect, with the given QtGui.QBrush, and the QtGui.QPainter.eraseRect() function that erases the area inside the given rectangle.

    All of these functions have both integer and floating point versions.

    There are functions to draw pixmaps/images, namely QtGui.QPainter.drawPixmap(), QtGui.QPainter.drawImage() and QtGui.QPainter.drawTiledPixmap(). Both QtGui.QPainter.drawPixmap() and QtGui.QPainter.drawImage() produce the same result, except that QtGui.QPainter.drawPixmap() is faster on-screen while QtGui.QPainter.drawImage() may be faster on a QtGui.QPrinter or other devices.

    Text drawing is done using QtGui.QPainter.drawText(). When you need fine-grained positioning, QtGui.QPainter.boundingRect() tells you where a given QtGui.QPainter.drawText() command will draw.

    There is a QtGui.QPainter.drawPicture() function that draws the contents of an entire QtGui.QPicture. The QtGui.QPainter.drawPicture() function is the only function that disregards all the painter’s settings as QtGui.QPicture has its own settings.
    
    There are some nice demonstrations that come with PySide:
    
    ####Basic Drawing demo
    https://github.com/PySide/Examples/tree/master/examples/painting/basicdrawing
    
    The Basic Drawing example shows how to display basic graphics primitives in a variety of styles using the QtGui.QPainter class. If you need to draw a complex shape, especially if you need to do so repeatedly, consider creating a QtGui.QPainterPath and drawing it using QtGui.QPainter.drawPath().

    ####Painter Paths example
    https://github.com/PySide/Examples/blob/master/examples/painting/painterpaths.py
    
    The QtGui.QPainterPath class provides a container for painting operations, enabling graphical shapes to be constructed and reused. The Painter Paths example shows how painter paths can be used to build complex shapes for rendering.

    QtGui.QPainter also provides the QtGui.QPainter.fillPath() function which fills the given QtGui.QPainterPath with the given QtGui.QBrush, and the QtGui.QPainter.strokePath() function that draws the outline of the given path (i.e. strokes the path).

    ####Vector deformation demo (not ported to PySide)
    Shows how to use advanced vector techniques to draw text using a QtGui.QPainterPath.

    ####Gradients demo (not ported to PySide)
    Shows the different types of gradients that are available in Qt.
    
    ####Path Stroking demo  (not por
    Shows Qt’s built-in dash patterns and shows how custom patterns can be used to extend the range of available patterns.

    ###Rendering Quality

    To get the optimal rendering result using QtGui.QPainter, you should use the platform independent QtGui.QImage as paint device; i.e. using QtGui.QImage will ensure that the result has an identical pixel representation on any platform.

    The QtGui.QPainter class also provides a means of controlling the rendering quality through its QPainter.RenderHint enum and the support for floating point precision: All the functions for drawing primitives has a floating point version. These are often used in combination with the QPainter.Antialiasing render hint.

    The _Concentric Circles Example_ (https://github.com/PySide/Examples/blob/master/examples/painting/concentriccircles.py) is nice to see this in action (link). It shows the improved rendering quality that can be obtained using floating point precision and anti-aliasing when drawing custom widgets.

    The application’s main window displays several widgets which are drawn using the various combinations of precision and anti-aliasing.

    The QPainter.RenderHint enum specifies flags to QtGui.QPainter that may or may not be respected by any given engine. QPainter.Antialiasing indicates that the engine should antialias edges of primitives if possible, QPainter.TextAntialiasing indicates that the engine should antialias text if possible, and the QPainter.SmoothPixmapTransform indicates that the engine should use a smooth pixmap transformation algorithm. HighQualityAntialiasing is an OpenGL-specific rendering hint indicating that the engine should use fragment programs and offscreen rendering for antialiasing.

    The QtGui.QPainter.renderHints() function returns a flag that specifies the rendering hints that are set for this painter. Use the QtGui.QPainter.setRenderHint() function to set or clear the currently set RenderHints.

    ###Coordinate Transformations

    Normally, the QtGui.QPainter operates on the device’s own coordinate system (usually pixels), but QtGui.QPainter has good support for coordinate transformations. The most commonly used transformations are scaling, rotation, translation and shearing. Use the QtGui.QPainter.scale() function to scale the coordinate system by a given offset, the QtGui.QPainter.rotate() function to rotate it clockwise and QtGui.QPainter.translate() to translate it (i.e. adding a given offset to the points). You can also twist the coordinate system around the origin using the QtGui.QPainter.shear() function. See the Affine Transformations demo for a visualization of a sheared coordinate system.

    See also the _Transformations example_ (https://github.com/PySide/Examples/blob/master/examples/painting/transformations.py) which shows how transformations influence the way that QtGui.QPainter renders graphics primitives. In particular it shows how the order of transformations affects the result.

    The Affine Transformations demo (not ported to PySide) show Qt’s ability to perform affine transformations on painting operations. The demo also allows the user to experiment with the transformation operations and see the results immediately.

    All the tranformation operations operate on the transformation QtGui.QPainter.worldTransform(). A matrix transforms a point in the plane to another point. For more information about the transformation matrix, see the Coordinate System and QtGui.QTransform documentation.

    The QtGui.QPainter.setWorldTransform() function can replace or add to the currently set QtGui.QPainter.worldTransform(). The QtGui.QPainter.resetTransform() function resets any transformations that were made using QtGui.QPainter.translate(), QtGui.QPainter.scale(), QtGui.QPainter.shear(), QtGui.QPainter.rotate(), QtGui.QPainter.setWorldTransform(), QtGui.QPainter.setViewport() and QtGui.QPainter.setWindow() functions. The QtGui.QPainter.deviceTransform() returns the matrix that transforms from logical coordinates to device coordinates of the platform dependent paint device. The latter function is only needed when using platform painting commands on the platform dependent handle, and the platform does not do transformations nativly.

    When drawing with QtGui.QPainter, we specify points using logical coordinates which then are converted into the physical coordinates of the paint device. The mapping of the logical coordinates to the physical coordinates are handled by QtGui.QPainter‘s QtGui.QPainter.combinedTransform(), a combination of QtGui.QPainter.viewport() and QtGui.QPainter.window() and QtGui.QPainter.worldTransform(). The QtGui.QPainter.viewport() represents the physical coordinates specifying an arbitrary rectangle, the QtGui.QPainter.window() describes the same rectangle in logical coordinates, and the QtGui.QPainter.worldTransform() is identical with the transformation matrix.

    See also Coordinate System (http://qt-project.org/doc/qt-4.8/coordsys.html)

    ###Clipping

    QtGui.QPainter can clip any drawing operation to a rectangle, a region, or a vector path. The current clip is available using the functions QtGui.QPainter.clipRegion() and QtGui.QPainter.clipPath(). Whether paths or regions are preferred (faster) depends on the underlying QtGui.QPainter.paintEngine(). For example, the QtGui.QImage paint engine prefers paths while the X11 paint engine prefers regions. Setting a clip is done in the painters logical coordinates.

    After QtGui.QPainter‘s clipping, the paint device may also clip. For example, most widgets clip away the pixels used by child widgets, and most printers clip away an area near the edges of the paper. This additional clipping is not reflected by the return value of QtGui.QPainter.clipRegion() or QtGui.QPainter.hasClipping().

    ###Composition Modes

    QtGui.QPainter provides the QPainter.CompositionMode enum which defines the Porter-Duff rules for digital image compositing; it describes a model for combining the pixels in one image, the source, with the pixels in another image, the destination.

    The two most common forms of composition are Source and SourceOver. Source is used to draw opaque objects onto a paint device. In this mode, each pixel in the source replaces the corresponding pixel in the destination. In SourceOver composition mode, the source object is transparent and is drawn on top of the destination.

    Note that composition transformation operates pixelwise. For that reason, there is a difference between using the graphic primitive itself and its bounding rectangle: The bounding rect contains pixels with alpha == 0 (i.e the pixels surrounding the primitive). These pixels will overwrite the other image’s pixels, affectively clearing those, while the primitive only overwrites its own area.

    The Composition Modes demo (not ported to PySide) allows you to experiment with the various composition modes and see the results immediately.

    ###Performance

    QtGui.QPainter is a rich framework that allows developers to do a great variety of graphical operations, such as gradients, composition modes and vector graphics. And QtGui.QPainter can do this across a variety of different hardware and software stacks. Naturally the underlying combination of hardware and software has some implications for performance, and ensuring that every single operation is fast in combination with all the various combinations of composition modes, brushes, clipping, transformation, etc, is close to an impossible task because of the number of permutations. As a compromise we have selected a subset of the QtGui.QPainter API and backends, where performance is guaranteed to be as good as we can sensibly get it for the given combination of hardware and software.

    The backends we focus on as high-performance engines are:

        Raster - This backend implements all rendering in pure software and is always used to render into QImages. For optimal performance only use the format types QImage.Format_ARGB32_Premultiplied, QImage.Format_RGB32 or QImage.Format_RGB16. Any other format, including QImage.Format_ARGB32, has significantly worse performance. This engine is also used by default on Windows and on QWS. It can be used as default graphics system on any OS/hardware/software combination by passing -graphicssystem raster on the command line
        
        OpenGL 2.0 (ES) - This backend is the primary backend for hardware accelerated graphics. It can be run on desktop machines and embedded devices supporting the OpenGL 2.0 or OpenGL/ES 2.0 specification. This includes most graphics chips produced in the last couple of years. The engine can be enabled by using QtGui.QPainter onto a QtOpenGL.QGLWidget or by passing -graphicssystem opengl on the command line when the underlying system supports it.
        
        OpenVG - This backend implements the Khronos standard for 2D and Vector Graphics. It is primarily for embedded devices with hardware support for OpenVG. The engine can be enabled by passing -graphicssystem openvg on the command line when the underlying system supports it.

    These operations are:

        Simple transformations, meaning translation and scaling, pluss 0, 90, 180, 270 degree rotations.
        drawPixmap() in combination with simple transformations and opacity with non-smooth transformation mode (QPainter::SmoothPixmapTransform not enabled as a render hint).
        
        Rectangle fills with solid color, two-color linear gradients and simple transforms.
        Rectangular clipping with simple transformations and intersect clip.
        
        Composition Modes QPainter::CompositionMode_Source and QPainter.CompositionMode_SourceOver
        Rounded rectangle filling using solid color and two-color linear gradients fills.
        3x3 patched pixmaps, via qDrawBorderPixmap.

    This list gives an indication of which features to safely use in an application where performance is critical. For certain setups, other operations may be fast too, but before making extensive use of them, it is recommended to benchmark and verify them on the system where the software will run in the end. There are also cases where expensive operations are ok to use, for instance when the result is cached in a QtGui.QPixmap.
   
Color role
http://pyside.github.io/docs/pyside/PySide/QtGui/QPalette.html#PySide.QtGui.PySide.QtGui.QPalette.ColorRole

##QtGui.QSizePolicy
http://srinikom.github.io/pyside-docs/PySide/QtGui/QSizePolicy.html

	The QtGui.QSizePolicy class is a layout attribute describing horizontal and vertical resizing policy.

	The size policy of a widget is an expression of its willingness to be resized in various ways, and affects how the widget is treated by the layout engine. Each widget returns a QtGui.QSizePolicy that describes the horizontal and vertical resizing policy it prefers when being laid out. You can change this for a specific widget by changing its QWidget.sizePolicy property.

	QtGui.QSizePolicy contains two independent QSizePolicy.Policy values and two stretch factors; one describes the widgets’s horizontal size policy, and the other describes its vertical size policy. It also contains a flag to indicate whether the height and width of its preferred size are related.

	The horizontal and vertical policies can be set in the constructor, and altered using the QtGui.QSizePolicy.setHorizontalPolicy() and QtGui.QSizePolicy.setVerticalPolicy() functions. The stretch factors can be set using the QtGui.QSizePolicy.setHorizontalStretch() and QtGui.QSizePolicy.setVerticalStretch() functions. The flag indicating whether the widget’s QtGui.QWidget.sizeHint() is width-dependent (such as a menu bar or a word-wrapping label) can be set using the QtGui.QSizePolicy.setHeightForWidth() function.

	The current size policies and stretch factors can be retrieved using the QtGui.QSizePolicy.horizontalPolicy(), QtGui.QSizePolicy.verticalPolicy(), QtGui.QSizePolicy.horizontalStretch() and QtGui.QSizePolicy.verticalStretch() functions. Alternatively, use the QtGui.QSizePolicy.transpose() function to swap the horizontal and vertical policies and stretches. The QtGui.QSizePolicy.hasHeightForWidth() function returns the current status of the flag indicating the size hint dependencies.

	Use the QtGui.QSizePolicy.expandingDirections() function to determine whether the associated widget can make use of more space than its QtGui.QWidget.sizeHint() function indicates, as well as find out in which directions it can expand.


##QtGui.QSpinBox
http://github.io/docs/pyside/PySide/QtGui/QSpinBox.html

    The QtGui.QSpinBox class provides a spin box widget. QtGui.QSpinBox is designed to handle integers and discrete sets of values (e.g., month names); use QtGui.QDoubleSpinBox for floating point values.

    QtGui.QSpinBox allows the user to choose a value by clicking the up/down buttons or pressing up/down on the keyboard to increase/decrease the value currently displayed. The user can also type the value in manually. The spin box supports integer values but can be extended to use different strings with QtGui.QSpinBox.validate(), QtGui.QSpinBox.textFromValue() and QtGui.QSpinBox.valueFromText().

    Every time the value changes QtGui.QSpinBox emits the QtGui.QSpinBox.valueChanged() signals. The current value can be fetched with QtGui.QSpinBox.value() and set with QtGui.QSpinBox.setValue().

    Clicking the up/down buttons or using the keyboard accelerator’s up and down arrows will increase or decrease the current value in steps of size QtGui.QSpinBox.singleStep(). If you want to change this behaviour you can reimplement the virtual function QtGui.QAbstractSpinBox.stepBy(). The minimum and maximum value and the step size can be set using one of the constructors, and can be changed later with QtGui.QSpinBox.setMinimum(), QtGui.QSpinBox.setMaximum() and QtGui.QSpinBox.setSingleStep().

    Most spin boxes are directional, but QtGui.QSpinBox can also operate as a circular spin box, i.e. if the range is 0-99 and the current value is 99, clicking “up” will give 0 if QtGui.QAbstractSpinBox.wrapping() is set to true. Use QtGui.QAbstractSpinBox.setWrapping() if you want circular behavior.

    The displayed value can be prepended and appended with arbitrary strings indicating, for example, currency or the unit of measurement. See QtGui.QSpinBox.setPrefix() and QtGui.QSpinBox.setSuffix(). The text in the spin box is retrieved with QtGui.QAbstractSpinBox.text() (which includes any QtGui.QSpinBox.prefix() and QtGui.QSpinBox.suffix() ), or with QtGui.QSpinBox.cleanText() (which has no QtGui.QSpinBox.prefix(), no QtGui.QSpinBox.suffix() and no leading or trailing whitespace).

	###Subclassing QSpinBox
    If using QtGui.QSpinBox.prefix(), QtGui.QSpinBox.suffix(), and QtGui.QAbstractSpinBox.specialValueText() don’t provide enough control, you subclass QtGui.QSpinBox and reimplement QtGui.QSpinBox.valueFromText() and QtGui.QSpinBox.textFromValue().

##QtGui.QValidator
http://srinikom.github.io/pyside-docs/PySide/QtGui/QValidator.html
	
	The QtGui.QValidator class provides validation of input text. The class itself is abstract. Two subclasses, QtGui.QIntValidator and QtGui.QDoubleValidator, provide basic numeric-range checking, and QtGui.QRegExpValidator provides general checking using a custom regular expression.

	If the built-in validators aren’t sufficient, you can subclass QtGui.QValidator. The class has two virtual functions: QtGui.QValidator.validate() and QtGui.QValidator.fixup().

	QtGui.QValidator.validate() must be implemented by every subclass. It returns `Invalid`, `Intermediate` or `Acceptable` depending on whether its argument is valid (for the subclass’s definition of valid).

	These three states require some explanation. An Invalid string is clearly invalid. Intermediate is less obvious: the concept of validity is difficult to apply when the string is incomplete (still being edited). QtGui.QValidator defines Intermediate as the property of a string that is neither clearly invalid nor acceptable as a final result. Acceptable means that the string is acceptable as a final result. One might say that any string that is a plausible intermediate state during entry of an Acceptable string is Intermediate.



##QtGui.QBoxLayout
http://github.io/docs/pyside/PySide/QtGui/QBoxLayout.html

	The QtGui.QBoxLayout class lines up child widgets horizontally or vertically. QtGui.QBoxLayout takes the space it gets (from its parent layout or from the QtGui.QLayout.parentWidget()), divides it up into a row of boxes, and makes each managed widget fill one box.

	If the QtGui.QBoxLayout‘s orientation is Qt.Horizontal the boxes are placed in a row, with suitable sizes. Each widget (or other box) will get at least its minimum size and at most its maximum size. Any excess space is shared according to the stretch factors (more about that below).

	If the QtGui.QBoxLayout‘s orientation is Qt.Vertical, the boxes are placed in a column, again with suitable sizes.

	The easiest way to create a QtGui.QBoxLayout is to use one of the convenience classes, e.g. QtGui.QHBoxLayout (for Qt.Horizontal boxes) or QtGui.QVBoxLayout (for Qt.Vertical boxes). You can also use the QtGui.QBoxLayout constructor directly, specifying its direction as LeftToRight, RightToLeft, TopToBottom, or BottomToTop. 

	If the QtGui.QBoxLayout is not the top-level layout (i.e. it is not managing all of the widget’s area and children), you must add it to its parent layout before you can do anything with it. The normal way to add a layout is by calling parentLayout-> QtGui.QBoxLayout.addLayout().

	Once you have done this, you can add boxes to the QtGui.QBoxLayout using one of four functions:
		QtGui.QBoxLayout.addWidget() to add a widget to the QtGui.QBoxLayout and set the widget’s stretch factor. (The stretch factor is along the row of boxes.)
		QtGui.QBoxLayout.addSpacing() to create an empty box; this is one of the functions you use to create nice and spacious dialogs. See below for ways to set margins.
		QtGui.QBoxLayout.addStretch() to create an empty, stretchable box.
		QtGui.QBoxLayout.addLayout() to add a box containing another QtGui.QLayout to the row and set that layout’s stretch factor.
	Use QtGui.QBoxLayout.insertWidget(), QtGui.QBoxLayout.insertSpacing(), QtGui.QBoxLayout.insertStretch() or QtGui.QBoxLayout.insertLayout() to insert a box at a specified position in the layout.

	QtGui.QBoxLayout also includes two margin widths:
		QtGui.QLayout.setContentsMargins() sets the width of the outer border on each side of the widget. This is the width of the reserved space along each of the QtGui.QBoxLayout‘s four sides.
		QtGui.QBoxLayout.setSpacing() sets the width between neighboring boxes. (You can use QtGui.QBoxLayout.addSpacing() to get more space at a particular spot.)
	The margin default is provided by the style. The default margin most Qt styles specify is 9 for child widgets and 11 for windows. The spacing defaults to the same as the margin width for a top-level layout, or to the same as the parent layout.

	To remove a widget from a layout, call QtGui.QLayout.removeWidget(). Calling QWidget.hide() on a widget also effectively removes the widget from the layout until QWidget.show() is called.

	You will almost always want to use QtGui.QVBoxLayout and QtGui.QHBoxLayout rather than QtGui.QBoxLayout because of their convenient constructors.
	
##bb