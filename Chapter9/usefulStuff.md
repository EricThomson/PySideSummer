Things that might be useful when working through Chapter 9 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
On setvisible versus show:

http://stackoverflow.com/questions/12177801/whats-the-difference-in-qt-between-setvisible-setshown-and-show-hide

Great discussion of MDI versus SDI versus TDI:
http://stackoverflow.com/questions/486020/is-there-still-a-place-for-mdi


#Useful Documentation

##QTabWidget
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTabWidget.html 

	The QtGui.QTabWidget class provides a stack of tabbed widgets.

	A tab widget provides a tab bar (see QtGui.QTabBar ) and a “page area” that is used to display pages related to each tab. By default, the tab bar is shown above the page area, but different configurations are available (see QTabWidget.TabPosition enum at http://qt-project.org/doc/qt-4.8/qtabwidget.html#TabPosition-enum). 

	Each tab is associated with a different widget (called a page). Only the current page is shown in the page area; all the other pages are hidden. The user can show a different page by clicking on its tab or by pressing its Alt+*letter* shortcut if it has one.

	The normal way to use QtGui.QTabWidget is to do the following:

	The position of the tabs is defined by QtGui.QTabWidget.tabPosition() (enum link above) , their shape by QtGui.QTabWidget.tabShape() (http://qt-project.org/doc/qt-4.8/qtabwidget.html#TabShape-enum).

	The signal QtGui.QTabWidget.currentChanged() is emitted when the user selects a page.

	The current page index is available as QtGui.QTabWidget.currentIndex() , the current page widget with QtGui.QTabWidget.currentWidget() . You can retrieve a pointer to a page widget with a given index using QtGui.QTabWidget.widget() , and can find the index position of a widget with QtGui.QTabWidget.indexOf() . Use QtGui.QTabWidget.setCurrentWidget() or QtGui.QTabWidget.setCurrentIndex() to show a particular page.

	You can change a tab’s text and icon using QtGui.QTabWidget.setTabText() or QtGui.QTabWidget.setTabIcon() . A tab and its associated page can be removed with QtGui.QTabWidget.removeTab() .

	Each tab is either enabled or disabled at any given time (see QtGui.QTabWidget.setTabEnabled() ). If a tab is enabled, the tab text is drawn normally and the user can select that tab. If it is disabled, the tab is drawn in a different way and the user cannot select that tab. Note that even if a tab is disabled, the page can still be visible, for example if all of the tabs happen to be disabled.

	Tab widgets can be a very good way to split up a complex dialog. An alternative is to use a QtGui.QStackedWidget for which you provide some means of navigating between pages, for example, a QtGui.QToolBar or a QtGui.QListWidget .

	Most of the functionality in QtGui.QTabWidget is provided by a QtGui.QTabBar (at the top, providing the tabs) and a QtGui.QStackedWidget (most of the area, organizing the individual pages).


##QTabBar
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTabBar.html

	The QtGui.QTabBar class provides a tab bar, e.g. for use in tabbed dialogs. QtGui.QTabBar is straightforward to use; it draws the tabs using one of the predefined shapes , and emits a signal when a tab is selected. It can be subclassed to tailor the look and feel. 

	Each tab has a QtGui.QTabBar.tabText() , an optional QtGui.QTabBar.tabIcon() , an optional QtGui.QTabBar.tabToolTip() , optional QtGui.QTabBar.tabWhatsThis() and optional QtGui.QTabBar.tabData() . The tabs’s attributes can be changed with QtGui.QTabBar.setTabText() , QtGui.QTabBar.setTabIcon() , QtGui.QTabBar.setTabToolTip() , setTabWhatsThis and QtGui.QTabBar.setTabData() . Each tabs can be enabled or disabled individually with QtGui.QTabBar.setTabEnabled() .

	Each tab can display text in a distinct color. The current text color for a tab can be found with the QtGui.QTabBar.tabTextColor() function. Set the text color for a particular tab with QtGui.QTabBar.setTabTextColor() .

	Tabs are added using QtGui.QTabBar.addTab() , or inserted at particular positions using QtGui.QTabBar.insertTab() . The total number of tabs is given by QtGui.QTabBar.count() . Tabs can be removed from the tab bar with QtGui.QTabBar.removeTab() . Combining QtGui.QTabBar.removeTab() and QtGui.QTabBar.insertTab() allows you to move tabs to different positions.

	The QtGui.QTabBar.shape() property defines the tabs’ appearance. The choice of shape is a matter of taste, although tab dialogs (for preferences and similar) invariably use RoundedNorth . Tab controls in windows other than dialogs almost always use either RoundedSouth or TriangularSouth . Many spreadsheets and other tab controls in which all the pages are essentially similar use TriangularSouth , whereas RoundedSouth is used mostly when the pages are different (e.g. a multi-page tool palette). The default in QtGui.QTabBar is RoundedNorth .

	The most important part of QtGui.QTabBar ‘s API is the QtGui.QTabBar.currentChanged() signal. This is emitted whenever the current tab changes (even at startup, when the current tab changes from ‘none’). There is also a slot, QtGui.QTabBar.setCurrentIndex() , which can be used to select a tab programmatically. The function QtGui.QTabBar.currentIndex() returns the index of the current tab, QtGui.QTabBar.count() holds the number of tabs.

	QtGui.QTabBar creates automatic mnemonic keys in the manner of QtGui.QAbstractButton ; e.g. if a tab’s label is “&Graphics”, Alt+G becomes a shortcut key for switching to that tab.

	The following virtual functions may need to be reimplemented in order to tailor the look and feel or store extra data with each tab:

		QtGui.QTabBar.tabSizeHint() calcuates the size of a tab.
		QtGui.QTabBar.tabInserted() notifies that a new tab was added.
		QtGui.QTabBar.tabRemoved() notifies that a tab was removed.
		QtGui.QTabBar.tabLayoutChange() notifies that the tabs have been re-laid out.
		QtGui.QTabBar.paintEvent() paints all tabs.

	For subclasses, you might also need the QtGui.QTabBar.tabRect() functions which returns the visual geometry of a single tab.

	
##QFrame
http://srinikom.github.io/pyside-docs/PySide/QtGui/QFrame.html

	Note: especially cool at that link is a depiction of the look of different combinations of QFrame property styles and such. 

	The QtGui.QFrame class is the base class of widgets that can have a frame.
	QtGui.QMenu uses this to “raise” the menu above the surrounding screen. QtGui.QProgressBar has a “sunken” look. QtGui.QLabel has a flat look. The frames of widgets like these can be changed.

		label = QLabel()
		label.setFrameStyle(QFrame.Panel | QFrame.Raised)
		label.setLineWidth(2)

		pbar = QProgressBar()
		label.setFrameStyle(QFrame.NoFrame)

	The QtGui.QFrame class can also be used directly for creating simple placeholder frames without any contents.

	The frame style is specified by a frame shape and a shadow style that is used to visually separate the frame from surrounding widgets. These properties can be set together using the QtGui.QFrame.setFrameStyle() function and read with QtGui.QFrame.frameStyle() .

	The frame shapes are NoFrame , Box , Panel , StyledPanel , HLine and VLine ; the shadow styles are Plain , Raised and Sunken .

	A frame widget has three attributes that describe the thickness of the border: 
	1. QtGui.QFrame.lineWidth(): The line width is the width of the frame border. It can be modified to customize the frame’s appearance.
	2. QtGui.QFrame.midLineWidth(): The mid-line width specifies the width of an extra line in the middle of the frame, which uses a third color to obtain a special 3D effect. Notice that a mid-line is only drawn for Box , HLine and VLine frames that are raised or sunken.
	3. QtGui.QFrame.frameWidth(): The frame width is determined by the frame style, and the QtGui.QFrame.frameWidth() function is used to obtain the value defined for the style used.

	The margin between the frame and the contents of the frame can be customized with the QWidget.setContentsMargins() function.
	  
 
##QWidget.setVisible
http://srinikom.github.io/pyside-docs/PySide/QtGui/QWidget.html#QtGui.QtGui.QWidget.setVisible

    QtGui.QWidget.setVisible(visible)
    Parameters:	visible – QtCore.bool

    This property determines whether the widget is visible. Calling setVisible(true) or QtGui.QWidget.show() sets the widget to visible status if all its parent widgets up to the window are visible. If an ancestor is not visible, the widget won’t become visible until all its ancestors are shown. If its size or position has changed, Qt guarantees that a widget gets move and resize events just before it is shown. If the widget has not been resized yet, Qt will adjust the widget’s size to a useful default using QtGui.QWidget.adjustSize() .

    Calling setVisible(false) or QtGui.QWidget.hide() hides a widget explicitly. An explicitly hidden widget will never become visible, even if all its ancestors become visible, unless you show it.

    A widget receives show and hide events when its visibility status changes. Between a hide and a show event, there is no need to waste CPU cycles preparing or displaying information to the user. A video application, for example, might simply stop generating new frames.
    
##QtGui.QSplitter
http://srinikom.github.io/pyside-docs/PySide/QtGui/QSplitter.html

    The QtGui.QSplitter class implements a splitter widget. A splitter lets the user control the size of child widgets by dragging the boundary between the children. Any number of widgets may be controlled by a single splitter. The typical use of a QtGui.QSplitter is to create several widgets and add them using QtGui.QSplitter.insertWidget() or QtGui.QSplitter.addWidget() .

    The following example will show a QtGui.QListView , QtGui.QTreeView , and QtGui.QTextEdit side by side, with two splitter handles:

        splitter =  QSplitter(parent)
        listview =  QListView()
        treeview =  QTreeView()
        textedit =  QTextEdit()
        splitter.addWidget(listview)
        splitter.addWidget(treeview)
        splitter.addWidget(textedit)

    If a widget is already inside a QtGui.QSplitter when QtGui.QSplitter.insertWidget() or QtGui.QSplitter.addWidget() is called, it will move to the new position. This can be used to reorder widgets in the splitter later. You can use QtGui.QSplitter.indexOf() , QtGui.QSplitter.widget() , and QtGui.QSplitter.count() to get access to the widgets inside the splitter.

    A default QtGui.QSplitter lays out its children horizontally (side by side); you can use setOrientation( Qt.Vertical ) to lay its children out vertically.

    By default, all widgets can be as large or as small as the user wishes, between the QtGui.QSplitter.minimumSizeHint() (or QtGui.QWidget.minimumSize() ) and QtGui.QWidget.maximumSize() of the widgets.

    QtGui.QSplitter resizes its children dynamically by default. If you would rather have QtGui.QSplitter resize the children only at the end of a resize operation, call setOpaqueResize(false).

    The initial distribution of size between the widgets is determined by multiplying the initial size with the stretch factor. You can also use QtGui.QSplitter.setSizes() to set the sizes of all the widgets. The function QtGui.QSplitter.sizes() returns the sizes set by the user. Alternatively, you can save and restore the sizes of the widgets from a QtCore.QByteArray using QtGui.QSplitter.saveState() and QtGui.QSplitter.restoreState() respectively.

    When you QtGui.QWidget.hide() a child its space will be distributed among the other children. It will be reinstated when you QtGui.QWidget.show() it again.

	
##QTextEdit
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTextEdit.html

    The QtGui.QTextEdit class provides a widget that is used to edit and display both plain and rich text.

	###Introduction and Concepts
    QtGui.QTextEdit is an advanced WYSIWYG viewer/editor supporting rich text formatting using HTML-style tags. It is optimized to handle large documents and to respond quickly to user input.

    QtGui.QTextEdit works on paragraphs and characters. A paragraph is a formatted string which is word-wrapped to fit into the width of the widget. By default when reading plain text, one newline signifies a paragraph. A document consists of zero or more paragraphs. The words in the paragraph are aligned in accordance with the paragraph’s alignment. Paragraphs are separated by hard line breaks. Each character within a paragraph has its own attributes, for example, font and color.

    QtGui.QTextEdit can display images, lists and tables. If the text is too large to view within the text edit’s viewport, scroll bars will appear. The text edit can load both plain text and HTML files (a subset of HTML 3.2 and 4).

    If you just need to display a small piece of rich text, instead of QTextEdit, use QtGui.QLabel .

    The rich text support in Qt is designed to provide a fast, portable and efficient way to add reasonable online help facilities to applications, and to provide a basis for rich text editors. If you find the HTML support insufficient for your needs you may consider the use of QtWebKit , which provides a full-featured web browser widget for your desktop.

    The shape of the mouse cursor on a QtGui.QTextEdit is Qt.IBeamCursor by default. It can be changed through the QtGui.QAbstractScrollArea.viewport()‘s cursor property.

	###Using QTextEdit as a Display Widget

    QtGui.QTextEdit can display a large HTML subset, including tables and images.

    The text is set or replaced using QtGui.QTextEdit.setHtml() which deletes any existing text and replaces it with the text passed in the QtGui.QTextEdit.setHtml() call. If you call QtGui.QTextEdit.setHtml() with legacy HTML, and then call QtGui.QTextEdit.toHtml() , the text that is returned may have different markup, but will render the same. The entire text can be deleted with QtGui.QTextEdit.clear() .

    Text itself can be inserted using the QtGui.QTextCursor class or using the convenience functions QtGui.QTextEdit.insertHtml() , QtGui.QTextEdit.insertPlainText() , QtGui.QTextEdit.append() or QtGui.QTextEdit.paste() . QtGui.QTextCursor is also able to insert complex objects like tables or lists into the document, and it deals with creating selections and applying changes to selected text.

    By default the text edit wraps words at whitespace to fit within the text edit widget. The QtGui.QTextEdit.setLineWrapMode() function is used to specify the kind of line wrap you want, or NoWrap if you don’t want any wrapping. Call QtGui.QTextEdit.setLineWrapMode() to set a fixed pixel width FixedPixelWidth , or character column (e.g. 80 column) FixedColumnWidth with the pixels or columns specified with QtGui.QTextEdit.setLineWrapColumnOrWidth() . If you use word wrap to the widget’s width WidgetWidth , you can specify whether to break on whitespace or anywhere with QtGui.QTextEdit.setWordWrapMode() .

    The QtGui.QTextEdit.find() function can be used to find and select a given string within the text.

    If you want to limit the total number of paragraphs in a QtGui.QTextEdit , as it is for example often useful in a log viewer, then you can use QtGui.QTextDocument‘s maximumBlockCount property for that.

	###Using QTextEdit as an Editor

    All the information about using QtGui.QTextEdit as a display widget also applies here.

    The current char format’s attributes are set with QtGui.QTextEdit.setFontItalic() , QtGui.QTextEdit.setFontWeight() , QtGui.QTextEdit.setFontUnderline() , QtGui.QTextEdit.setFontFamily() , QtGui.QTextEdit.setFontPointSize() , QtGui.QTextEdit.setTextColor() and QtGui.QTextEdit.setCurrentFont() . The current paragraph’s alignment is set with QtGui.QTextEdit.setAlignment() .

    Selection of text is handled by the QtGui.QTextCursor class, which provides functionality for creating selections, retrieving the text contents or deleting selections. You can retrieve the object that corresponds with the user-visible cursor using the QtGui.QTextEdit.textCursor() method. If you want to set a selection in QtGui.QTextEdit just create one on a QtGui.QTextCursor object and then make that cursor the visible cursor using QtGui.QTextEdit.setTextCursor() . The selection can be copied to the clipboard with QtGui.QTextEdit.copy() , or cut to the clipboard with QtGui.QTextEdit.cut() . The entire text can be selected using QtGui.QTextEdit.selectAll() .

    When the cursor is moved and the underlying formatting attributes change, the QtGui.QTextEdit.currentCharFormatChanged() signal is emitted to reflect the new attributes at the new cursor position.

    QtGui.QTextEdit holds a QtGui.QTextDocument object which can be retrieved using the QtGui.QTextEdit.document() method. You can also set your own document object using QtGui.QTextEdit.setDocument() . QtGui.QTextDocument emits a QtGui.QTextEdit.textChanged() signal if the text changes and it also provides a isModified() function which will return true if the text has been modified since it was either loaded or since the last call to setModified with false as argument. In addition it provides methods for undo and redo.

	###Drag and Drop

    QtGui.QTextEdit also supports custom drag and drop behavior. By default, QtGui.QTextEdit will insert plain text, HTML and rich text when the user drops data of these MIME (multipurpose internet mail extensions) types onto a document. Reimplement QtGui.QTextEdit.canInsertFromMimeData() and QtGui.QTextEdit.insertFromMimeData() to add support for additional MIME types.


	###Editing Key Bindings
    A [partial, curated] list of key bindings which are implemented for editing:
		Backspace 	Deletes the character to the left of the cursor.
		Delete 	Deletes the character to the right of the cursor.
		Ctrl+C 	Copy the selected text to the clipboard.
		Ctrl+Insert 	Copy the selected text to the clipboard.
		Ctrl+K 	Deletes to the end of the line.
		Ctrl+V 	Pastes the clipboard text into text edit.
		Shift+Insert 	Pastes the clipboard text into text edit.
		Ctrl+X 	Deletes the selected text and copies it to the clipboard.
		Shift+Delete 	Deletes the selected text and copies it to the clipboard.
		Ctrl+Z 	Undoes the last operation.
		Ctrl+Y 	Redoes the last operation.
		Ctrl+Home 	Moves the cursor to the beginning of the text.
		End 	Moves the cursor to the end of the line.
		Ctrl+End 	Moves the cursor to the end of the text.
		Alt+Wheel 	Scrolls the page horizontally (the Wheel is the mouse wheel).

    To select (mark) text hold down the Shift key whilst pressing one of the movement keystrokes, for example, Shift+Right will select the character to the right, and Shift+Ctrl+Right will select the word to the right, etc.
    
    
  ##QtGui.QMdiArea
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QMdiArea.html
  
    The QtGui.QMdiArea widget provides an area in which MDI windows are displayed.

    QtGui.QMdiArea functions, essentially, like a window manager for MDI windows. For instance, it draws the windows it manages on itself and arranges them in a cascading or tile pattern. QtGui.QMdiArea is commonly used as the center widget in a QtGui.QMainWindow to create MDI applications, but can also be placed in any layout. 

    Subwindows in QtGui.QMdiArea are instances of QtGui.QMdiSubWindow . They are added to an MDI area with QtGui.QMdiArea.addSubWindow() . It is common to pass a QtGui.QWidget, which is set as the internal widget, to this function, but it is also possible to pass a QtGui.QMdiSubWindow directly.The class inherits QtGui.QWidget , and you can use the same API as with a normal top-level window when programming. QtGui.QMdiSubWindow also has behavior that is specific to MDI windows. See the QtGui.QMdiSubWindow class description for more details.

    A subwindow becomes active when it gets the keyboard focus, or when QtGui.QWidget.setFocus() is called. The user activates a window by moving focus in the usual ways. The MDI area emits the QtGui.QMdiArea.subWindowActivated() signal when the active window changes, and the QtGui.QMdiArea.activeSubWindow() function returns the active subwindow.

    The convenience function QtGui.QMdiArea.subWindowList() returns a list of all subwindows. This information could be used in a popup menu containing a list of windows, for example.

    The subwindows are sorted by the current QMdiArea.WindowOrder . This is used for the QtGui.QMdiArea.subWindowList() and for QtGui.QMdiArea.activateNextSubWindow() and acivatePreviousSubWindow(). Also, it is used when cascading or tiling the windows with QtGui.QMdiArea.cascadeSubWindows() and QtGui.QMdiArea.tileSubWindows() .

    QtGui.QMdiArea provides two built-in layout strategies for subwindows: QtGui.QMdiArea.cascadeSubWindows() and QtGui.QMdiArea.tileSubWindows() . Both are slots and are easily connected to menu entries.


  ##QtGui.QMdiSubWindow
  http://github.io/docs/pyside/PySide/QtGui/QMdiSubWindow.html
  
    The QtGui.QMdiSubWindow class provides a subwindow class for QtGui.QMdiArea .

    QtGui.QMdiSubWindow represents a top-level window in a QtGui.QMdiArea , and consists of a title bar with window decorations, an internal widget, and (depending on the current style) a window frame and a size grip. QtGui.QMdiSubWindow has its own layout, which consists of the title bar and a center area for the internal widget.

    The most common way to construct a QtGui.QMdiSubWindow is to call QMdiArea.addSubWindow() with the internal widget as the argument. You can also create a subwindow yourself, and set an internal widget by calling QtGui.QMdiSubWindow.setWidget() .

    You use the same API when programming with subwindows as with regular top-level windows (e.g., you can call functions such as QtGui.QWidget.show() , QtGui.QWidget.hide() , QtGui.QWidget.showMaximized() , and QtGui.QWidget.setWindowTitle() ).

    ###Subwindow Handling

    QtGui.QMdiSubWindow also supports behavior specific to subwindows in an MDI area.

    By default, each QtGui.QMdiSubWindow is visible inside the MDI area viewport when moved around, but it is also possible to specify transparent window movement and resizing behavior, where only the outline of a subwindow is updated during these operations. The QtGui.QMdiSubWindow.setOption() function is used to enable this behavior.

    The QtGui.QMdiSubWindow.isShaded() function detects whether the subwindow is currently shaded (i.e., the window is collapsed so that only the title bar is visible). To enter shaded mode, call QtGui.QMdiSubWindow.showShaded() [huh?] . QtGui.QMdiSubWindow emits the QtGui.QMdiSubWindow.windowStateChanged() signal whenever the window state has changed (e.g., when the window becomes minimized, or is restored). It also emits QtGui.QMdiSubWindow.aboutToActivate() before it is activated.

    You can also change the active window with the keyboard. By pressing the control and tab keys at the same time, the next (using the current QMdiArea.WindowOrder ) subwindow will be activated. By pressing control, shift, and tab, you will activate the previous window. This is equivalent to calling QtGui.QMdiArea.activateNextSubWindow() and QtGui.QMdiArea.activatePreviousSubWindow() .
    
##QtextEdit (review of functions that are useful for this chapter)
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTextEdit.html
  
    QtGui.QTextEdit holds a QtGui.QTextDocument object which can be retrieved using the QtGui.QTextEdit.document() method. QtGui.QTextEdit.textChanged() signal if the text changes and it also provides a isModified() function which will return true if the text has been modified since it was either loaded or since the last call to setModified with false as argument. 
  
##QtCore.QSignalMapper
http://srinikom.github.io/pyside-docs/PySide/QtCore/QSignalMapper.html

    The QtCore.QSignalMapper class bundles signals from identifiable senders.

    This class collects a set of parameterless signals, and re-emits them with integer, string or widget parameters corresponding to the object that sent the signal.

    The class supports the mapping of particular strings or integers with particular objects using QtCore.QSignalMapper.setMapping(). The objects’ signals can then be connected to the QtCore.QSignalMapper.map() slot which will emit the QtCore.QSignalMapper.mapped() signal with the string or integer associated with the original signalling object. Mappings can be removed later using QtCore.QSignalMapper.removeMappings() .

    Suppose we want to create a custom widget that contains a group of buttons. One approach is to connect each button’s clicked() signal to its own custom slot; but in this example we want to connect all the buttons to a single slot and parameterize the slot by the button that was clicked.

    We connect each button’s clicked() signal to the signal mapper’s QtCore.QSignalMapper.map() slot, and create a mapping in the signal mapper from each button to the button’s text. Finally we connect the signal mapper’s QtCore.QSignalMapper.mapped() signal to the custom widget’s clicked() signal. When the user clicks a button, the custom widget will emit a single clicked() signal whose argument is the text of the button the user clicked.
        button = QPushButton(text)
        signalMapper = QSignalMapper(self)
        signalMapper.setMapping(button, text)
        button.clicked.connect(signalMapper.map)
        signalMapper.mapped[str].connect(mySlot)

##QTextCursor
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTextCursor.html

    The QtGui.QTextCursor class offers an API to access and modify QTextDocuments.

    Text cursors are objects that are used to access and modify the contents and underlying structure of text documents via a programming interface that mimics the behavior of a cursor in a text editor. QtGui.QTextCursor contains information about both the cursor’s position within a QtGui.QTextDocument and any selection that it has made.

    QtGui.QTextCursor is modeled on the way a text cursor behaves in a text editor, providing a programmatic means of performing standard actions through the user interface. A document can be thought of as a single string of characters. The cursor’s current QtGui.QTextCursor.position() then is always either between two consecutive characters in the string, or else before the very first character or after the very last character in the string. Documents can also contain tables, lists, images, and other objects in addition to text but, from the developer’s point of view, the document can be treated as one long string. Some portions of that string can be considered to lie within particular blocks (e.g. paragraphs), or within a table’s cell, or a list’s item, or other structural elements. When we refer to “current character” we mean the character immediately before the cursor QtGui.QTextCursor.position() in the document. Similarly, the “current block” is the block that contains the cursor QtGui.QTextCursor.position() .

    The cursor position can be changed programmatically using QtGui.QTextCursor.setPosition() and QtGui.QTextCursor.movePosition() ; the latter can also be used to select text. For selections see QtGui.QTextCursor.selectionStart() , QtGui.QTextCursor.selectionEnd() , QtGui.QTextCursor.hasSelection() , QtGui.QTextCursor.clearSelection() , and QtGui.QTextCursor.removeSelectedText() .

    If the QtGui.QTextCursor.position() is at the start of a block QtGui.QTextCursor.atBlockStart() returns true; and if it is at the end of a block QtGui.QTextCursor.atBlockEnd() returns true. The format of the current character is returned by QtGui.QTextCursor.charFormat() , and the format of the current block is returned by QtGui.QTextCursor.blockFormat() .

    Formatting can be applied to the current text document using the QtGui.QTextCursor.setCharFormat() , QtGui.QTextCursor.mergeCharFormat() , QtGui.QTextCursor.setBlockFormat() and QtGui.QTextCursor.mergeBlockFormat() functions. 

    Deletions can be achieved using QtGui.QTextCursor.deleteChar() , QtGui.QTextCursor.deletePreviousChar() , and QtGui.QTextCursor.removeSelectedText(). Text strings can be inserted into the document with the QtGui.QTextCursor.insertText() function, blocks (representing new paragraphs) can be inserted with QtGui.QTextCursor.insertBlock() .

    Existing fragments of text can be inserted with QtGui.QTextCursor.insertFragment() but, if you want to insert pieces of text in various formats, it is usually still easier to use QtGui.QTextCursor.insertText() and supply a character format.

    Various types of higher-level structure can also be inserted into the document with the cursor:

    * Lists are ordered sequences of block elements that are decorated with bullet points or symbols. These are inserted in a specified format with QtGui.QTextCursor.insertList().  
    * Tables are inserted with the QtGui.QTextCursor.insertTable() function, and can be given an optional format. These contain an array of cells that can be traversed using the cursor.
    * Inline images are inserted with QtGui.QTextCursor.insertImage() . The image to be used can be specified in an image format, or by name.
    * Frames are inserted by calling QtGui.QTextCursor.insertFrame() with a specified format.

    Cursor movements are limited to valid cursor positions. In Latin writing this is between any two consecutive characters in the text, before the first character, or after the last character. Functions such as QtGui.QTextCursor.movePosition() and QtGui.QTextCursor.deleteChar() limit cursor movement to these valid positions.

