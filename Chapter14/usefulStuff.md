Things that might be useful when working through Chapter 14 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)


#Useful links
##Overview of model/view programming
http://qt-project.org/doc/qt-4.8/model-view-programming.html

##Enumeration of item data roles
http://radekp.github.io/qtmoko/api/qt.html#ItemDataRole-enum

##Itemflags enumeration
http://qt-project.org/doc/qt-4.8/qt.html#ItemFlag-enum

##Nice tutorial on QListWidget
http://www.pythoncentral.io/pyside-pyqt-tutorial-the-qlistwidget/

##Enumeration of selection modes
http://github.io/docs/pyside/PySide/QtGui/QAbstractItemView.html#QtGui.QtGui.QAbstractItemView.SelectionMode

##Enumeration of drag and drop modes
http://github.io/docs/pyside/PySide/QtGui/QAbstractItemView.html#QtGui.QtGui.QAbstractItemView.DragDropMode

##Example of how Qt docs are better than pyside docs:
http://qt-project.org/doc/qt-4.8/qabstracttablemodel.html

##QStyleOption docs are better in pyqt:
http://pyqt.sourceforge.net/Docs/PyQt4/qstyleoption.html

#Useful Documentation

##QListWidget
http://github.io/docs/pyside/PySide/QtGui/QListWidget.html

    The QtGui.QListWidget class provides an item-based list widget.

    QtGui.QListWidget is a convenience class that provides a list view similar to the one supplied by QtGui.QListView. For a more flexible list view widget, use the QtGui.QListView class with a standard model.

    List widgets are constructed in the same way as other widgets:

        listWidget = QListWidget(self)

    The QtGui.QAbstractItemView.selectionMode() of a list widget determines how many of the items in the list can be selected at the same time, and whether complex selections of items can be created. This can be set with the QtGui.QAbstractItemView.setSelectionMode() function (see useful links, above, for link to enumeration of different modes).

    There are two ways to add items to the list: they can be constructed with the list widget as their parent widget, or they can be constructed with no parent widget and added to the list later. If a list widget already exists when the items are constructed, the first method is easier to use:

        QListWidgetItem(tr("Oak"), listWidget)
        QListWidgetItem(tr("Fir"), listWidget)
        QListWidgetItem(tr("Pine"), listWidget)

    If you need to insert a new item into the list at a particular position, then the item should be constructed without a parent widget. The QtGui.QListWidget.insertItem() function should then be used to place it within the list. The list widget will take ownership of the item.

        newItem = QListWidgetItem()
        newItem.setText(itemText)
        listWidget.insertItem(row, newItem)

    For multiple items, QtGui.QListWidget.insertItems() can be used instead. The number of items in the list is found with the QtGui.QListWidget.count() function. To remove items from the list, use QtGui.QListWidget.takeItem(), because 'removeItem' or 'deleteItem' would be too obvious and make learning Qt much too simple.
    
    Probably the easiest way to add item or items: QListWidget.addItem() or QListWidget.addItems().

    The current (selected) item in the list can be found with QtGui.QListWidget.currentItem(), and changed with QtGui.QListWidget.setCurrentItem(). The user can also change the current item by navigating with the keyboard or clicking on a different item. When the current item changes, the QtGui.QListWidget.currentItemChanged() signal is emitted with the new current item and the item that was previously current.

##QListWidgetItem
http://github.io/docs/pyside/PySide/QtGui/QListWidgetItem.html

    The QtGui.QListWidgetItem class provides an item for use with the QtGui.QListWidget item view class.

    A QtGui.QListWidgetItem represents a single item in a QtGui.QListWidget. Each item can hold several pieces of information, and will display them appropriately.

    The item view convenience classes use a classic item-based interface rather than a pure model/view approach. For a more flexible list view widget, consider using the QtGui.QListView class with a standard model.

    List items can be inserted automatically into a list, when they are constructed, by specifying the list widget:

        QListWidgetItem(tr("Hazel"), listWidget)

    Alternatively, list items can also be created without a parent widget, and later inserted into a list using QListWidget.insertItem().

    List items are typically used to display QtGui.QListWidgetItem.text() and an QtGui.QListWidgetItem.icon(). These are set with the QtGui.QListWidgetItem.setText() and QtGui.QListWidgetItem.setIcon() functions. The appearance of the text can be customized with QtGui.QListWidgetItem.setFont(), QtGui.QListWidgetItem.setForeground(), and QtGui.QListWidgetItem.setBackground(). Text in list items can be aligned using the QtGui.QListWidgetItem.setTextAlignment() function. Tooltips, status tips and “What’s This?” help can be added to list items with QtGui.QListWidgetItem.setToolTip(), QtGui.QListWidgetItem.setStatusTip(), and QtGui.QListWidgetItem.setWhatsThis().

    By default, items are enabled, selectable, checkable, and can be the source of drag and drop operations.

    Each item’s flags can be changed by calling QtGui.QListWidgetItem.setFlags() with the appropriate value (see Qt.ItemFlags ). Checkable items can be checked, unchecked and partially checked with the QtGui.QListWidgetItem.setCheckState() function. The corresponding QtGui.QListWidgetItem.checkState() function indicates the item’s current check state.

    The QtGui.QListWidgetItem.isHidden() function can be used to determine whether the item is hidden. To hide an item, use QtGui.QListWidgetItem.setHidden().


##QTableWidget
http://github.io/docs/pyside/PySide/QtGui/QTableWidget.html

    The QtGui.QTableWidget class provides an item-based table view with a default model.
    Table widgets provide standard table display facilities for applications. The items in a QtGui.QTableWidget are provided by QtGui.QTableWidgetItem.

    If you want a table that uses your own data model [what does this mean, exactly?] you should use QtGui.QTableView rather than this class.

    Table widgets can be constructed with the required numbers of rows and columns:

        tableWidget = QTableWidget(12, 3, self)

    Alternatively, tables can be constructed without a given size and resized later:

        tableWidget = QTableWidget()
        tableWidget.setRowCount(10)
        tableWidget.setColumnCount(5)

    Items are created outside the table (with no parent widget) and inserted into the table with QtGui.QTableWidget.setItem() :

        newItem = QTableWidgetItem("stinkbutton")
        tableWidget.setItem(row, column, newItem)

    If you want to enable sorting in your table widget, do so after you have populated it with items, otherwise sorting may interfere with the insertion order (see QtGui.QTableWidget.setItem() for details). 

    [Details: setItem sets the item for the given row and column to item. The table takes ownership of the item. Note that if sorting is enabled (see QtGui.QTableView.sortingEnabled() ) and column is the current sort column, the row will be moved to the sorted position determined by item. If you want to set several items of a particular row (say, by calling QtGui.QTableWidget.setItem() in a loop), you may want to turn off sorting before doing so, and turn it back on afterwards; this will allow you to use the same row argument for all items in the same row (i.e. QtGui.QTableWidget.setItem() will not move the row).]

    Tables can be given both horizontal and vertical headers. The simplest way to create the headers is to supply a list of strings to the QtGui.QTableWidget.setHorizontalHeaderLabels() and QtGui.QTableWidget.setVerticalHeaderLabels() functions. These will provide simple textual headers for the table’s columns and rows. More sophisticated headers can be created from existing table items that are usually constructed outside the table. For example, we can construct a table item with an icon and aligned text, and use it as the header for a particular column:

        cubesHeaderItem = QTableWidgetItem(tr("Cubes"))
        cubesHeaderItem.setIcon(QIcon(QPixmap(":/Images/cubed.png")))
        cubesHeaderItem.setTextAlignment(Qt::AlignVCenter)

    The number of rows in the table can be found with QtGui.QTableWidget.rowCount(), and the number of columns with QtGui.QTableWidget.columnCount(). The table can be cleared with the QtGui.QTableWidget.clear() function.


##QTableWidgetItem
http://github.io/docs/pyside/PySide/QtGui/QTableWidgetItem.html

    The QtGui.QTableWidgetItem class provides an item for use with the QtGui.QTableWidget class. Table items are used to hold pieces of information for table widgets. Items usually contain text, icons, or checkboxes

    The QtGui.QTableWidgetItem class is a convenience class that provides an item for use with the QtGui.QTableWidget class. Top-level items are constructed without a parent then inserted at the position specified by a pair of row and column numbers:

        newItem = QTableWidgetItem("Do it")
        tableWidget.setItem(row, column, newItem)

    Each item can have its own background brush which is set with the QtGui.QTableWidgetItem.setBackground() function. The current background brush can be found with QtGui.QTableWidgetItem.background(). The text label for each item can be rendered with its own font and brush. These are specified with the QtGui.QTableWidgetItem.setFont() and QtGui.QTableWidgetItem.setForeground() functions, and read with QtGui.QTableWidgetItem.font() and QtGui.QTableWidgetItem.foreground().

    By default, items are enabled, editable, selectable, checkable, and can be used both as the source of a drag and drop operation and as a drop target. Each item’s flags can be changed by calling QtGui.QTableWidgetItem.setFlags() with the appropriate value (see Qt.ItemFlags ). Checkable items can be checked and unchecked with the QtGui.QTableWidgetItem.setCheckState() function. The corresponding QtGui.QTableWidgetItem.checkState() function indicates whether the item is currently checked.
    
 ##QTreeWidget
 http://github.io/docs/pyside/PySide/QtGui/QTreeWidget.html
 
    The QtGui.QTreeWidget class provides a tree view that uses a predefined tree model.

    The QtGui.QTreeWidget class is a convenience class that provides a standard tree widget with a classic item-based interface. This class is based on Qt’s Model/View architecture and uses a default model to hold items, each of which is a QtGui.QTreeWidgetItem.

    Developers who do not need the flexibility of the Model/View framework can use this class to create simple hierarchical lists very easily. A more flexible approach involves combining a QtGui.QTreeView with a standard item model. This allows the storage of data to be separated from its representation.

    In its simplest form, a tree widget can be constructed in the following way:

        treeWidget = QTreeWidget()
        treeWidget.setColumnCount(1)
        items = []
        for i in range(10):
            items.append(QTreeWidgetItem(None, QStringList(QString("item: %1").arg(i))))
        treeWidget.insertTopLevelItems(None, items)

    Before items can be added to the tree widget, the number of columns must be set with QtGui.QTreeWidget.setColumnCount(). This allows each item to have one or more labels or other decorations. The number of columns in use can be found with the QtGui.QTreeWidget.columnCount() function.

    The tree can have a header that contains a section for each column in the widget. It is easiest to set up the labels for each section by supplying a list of strings with QtGui.QTreeWidget.setHeaderLabels(), but a custom header can be constructed with a QtGui.QTreeWidgetItem and inserted into the tree with the QtGui.QTreeWidget.setHeaderItem() function.

    The items in the tree can be sorted by column according to a predefined sort order. If sorting is enabled, the user can sort the items by clicking on a column header. Sorting can be enabled or disabled by calling QtGui.QTreeView.setSortingEnabled(). The QtGui.QTreeView.isSortingEnabled() function indicates whether sorting is enabled.

 
 ##QTreeWidgetItem
 http://github.io/docs/pyside/PySide/QtGui/QTreeWidgetItem.html

    The QtGui.QTreeWidgetItem class is a convenience class that provides an item for use with the QtGui.QTreeWidget convenience class. Tree widget items are used to hold rows of information for tree widgets. Rows usually contain several columns of data, each of which can contain a text label and an icon.

    Items are usually constructed with a parent that is either a QtGui.QTreeWidget (for top-level items) or a QtGui.QTreeWidgetItem (for items on lower levels of the tree). For example, the following code constructs a top-level item to represent cities of the world, and adds a entry for Oslo as a child item:

        cities =  QTreeWidgetItem(treeWidget)
        cities.setText(0, tr("Cities"))
        osloItem =  QTreeWidgetItem(cities)
        osloItem.setText(0, tr("Oslo"))
        osloItem.setText(1, tr("Yes"))

    Items can be added in a particular order by specifying the item they follow when they are constructed:

        planets =  QTreeWidgetItem(treeWidget, cities)
        planets.setText(0, tr("Planets"))

    Each column in an item can have its own background brush which is set with the QtGui.QTreeWidgetItem.setBackground() function. The current background brush can be found with QtGui.QTreeWidgetItem.background(). The text label for each column can be rendered with its own font and brush. These are specified with the QtGui.QTreeWidgetItem.setFont() and QtGui.QTreeWidgetItem.setForeground() functions, and read with QtGui.QTreeWidgetItem.font() and QtGui.QTreeWidgetItem.foreground().

    The main difference between top-level items and those in lower levels of the tree is that a top-level item has no QtGui.QTreeWidgetItem.parent(). This information can be used to tell the difference between items, and is useful to know when inserting and removing items from the tree. Children of an item can be removed with QtGui.QTreeWidgetItem.takeChild() and inserted at a given index in the list of children with the QtGui.QTreeWidgetItem.insertChild() function.

    By default, items are enabled, selectable, checkable, and can be the source of a drag and drop operation. Each item’s flags can be changed by calling QtGui.QTreeWidgetItem.setFlags() with the appropriate value (see Qt.ItemFlags ). Checkable items can be checked and unchecked with the QtGui.QTreeWidgetItem.setCheckState() function. The corresponding QtGui.QTreeWidgetItem.checkState() function indicates whether the item is currently checked.

##QAbstractTableModel
http://github.io/docs/pyside/PySide/QtCore/QAbstractTableModel.html

    The QtCore.QAbstractTableModel class provides an abstract model that can be subclassed to create table models. QtCore.QAbstractTableModel provides a standard interface for models that represent their data as a two-dimensional array of items. It is not used directly, but must be subclassed.

    Since the model provides a more specialized interface than QtCore.QAbstractItemModel, it is not suitable for use with tree views, although it can be used to provide data to a QtGui.QListView. If you need to represent a simple list of items, and only need a model to contain a single column of data, subclassing the QtCore.QAbstractListModel may be more appropriate.

    The QtCore.QAbstractItemModel.rowCount() and QtCore.QAbstractItemModel.columnCount() functions return the dimensions of the table. To retrieve a model index corresponding to an item in the model, use QtCore.QAbstractTableModel.index() and provide only the row and column numbers.

    ###Subclassing

    When subclassing QtCore.QAbstractTableModel, you must implement QtCore.QAbstractItemModel.rowCount(), QtCore.QAbstractItemModel.columnCount(), and QtCore.QAbstractItemModel.data(). Default implementations of the QtCore.QAbstractTableModel.index() and QtCore.QAbstractTableModel.parent() functions are provided by QtCore.QAbstractTableModel.Most models also implement QtCore.QAbstractItemModel.headerData(). [not required officially though]

    Editable models need to implement QtCore.QAbstractItemModel.setData(), and implement QtCore.QAbstractItemModel.flags() to return a value containing Qt.ItemIsEditable.

    Models that provide interfaces to resizable data structures can provide implementations of QtCore.QAbstractItemModel.insertRows(), QtCore.QAbstractItemModel.removeRows(), QtCore.QAbstractItemModel.insertColumns(), and QtCore.QAbstractItemModel.removeColumns(). 
    
    ###Making all views update correctly
    When implementing these functions, it is important to call the appropriate functions so that all connected views are aware of any changes:

        An QtCore.QAbstractItemModel.insertRows() implementation must call QtCore.QAbstractItemModel.beginInsertRows() before inserting new rows into the data structure, and it must call QtCore.QAbstractItemModel.endInsertRows() immediately afterwards.
        
        An QtCore.QAbstractItemModel.insertColumns() implementation must call QtCore.QAbstractItemModel.beginInsertColumns() before inserting new columns into the data structure, and it must call QtCore.QAbstractItemModel.endInsertColumns() immediately afterwards.
        
        A QtCore.QAbstractItemModel.removeRows() implementation must call QtCore.QAbstractItemModel.beginRemoveRows() before the rows are removed from the data structure, and it must call QtCore.QAbstractItemModel.endRemoveRows() immediately afterwards.
        
        A QtCore.QAbstractItemModel.removeColumns() implementation must call QtCore.QAbstractItemModel.beginRemoveColumns() before the columns are removed from the data structure, and it must call QtCore.QAbstractItemModel.endRemoveColumns() immediately afterwards.

##QTableView
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTableView.html

    The QtGui.QTableView class provides a default model/view implementation of a table view. A QtGui.QTableView implements a table view that displays items from a model. 

    QtGui.QTableView implements the interfaces defined by the QtGui.QAbstractItemView class to allow it to display data provided by models derived from the QtCore.QAbstractItemModel class.

    ###Navigation

    You can navigate the cells in the table by clicking on a cell with the mouse, or by using the arrow keys. Because QtGui.QTableView enables QtGui.QAbstractItemView.tabKeyNavigation() by default, you can also hit Tab and Backtab to move from cell to cell.

    ###Visual Appearance

    The table has a vertical header that can be obtained using the QtGui.QTableView.verticalHeader() function, and a horizontal header that is available through the QtGui.QTableView.horizontalHeader() function. The height of each row in the table can be found by using QtGui.QTableView.rowHeight() ; similarly, the width of columns can be found using QtGui.QTableView.columnWidth() Since both of these are plain widgets, you can hide either of them using their QtGui.QWidget.hide() functions.

    Rows and columns can be hidden and shown with QtGui.QTableView.hideRow(), QtGui.QTableView.hideColumn(), QtGui.QTableView.showRow(), and QtGui.QTableView.showColumn() They can be selected with QtGui.QTableView.selectRow() and QtGui.QTableView.selectColumn() The table will show a grid depending on the QtGui.QTableView.showGrid() property.

    The items shown in a table view, like those in the other item views, are rendered and edited using standard delegates However, for some tasks it is sometimes useful to be able to insert widgets in a table instead. Widgets are set for particular indexes with the QtGui.QAbstractItemView.setIndexWidget() function, and later retrieved with QtGui.QAbstractItemView.indexWidget()

    To distribute the available space according to the space requirement of each column or row, call the view’s QtGui.QTableView.resizeColumnsToContents() or QtGui.QTableView.resizeRowsToContents() functions.

    ###Coordinate Systems

    For some specialized forms of tables it is useful to be able to convert between row and column indexes and widget coordinates. The QtGui.QTableView.rowAt() function provides the y-coordinate within the view of the specified row; the row index can be used to obtain a corresponding y-coordinate with QtGui.QTableView.rowViewportPosition() The QtGui.QTableView.columnAt() and QtGui.QTableView.columnViewportPosition() functions provide the equivalent conversion operations between x-coordinates and column indexes.

##QStyledItemDelegate
http://srinikom.github.io/pyside-docs/PySide/QtGui/QStyledItemDelegate.html

    The QtGui.QStyledItemDelegate class is one of the Model/View Classes and is part of Qt’s model/view framework The delegate allows the display and editing of items to be developed independently from the model and view.
        
    The QtGui.QStyledItemDelegate class is applied to a view. It provides display and editing facilities for data items from a model.

    When displaying data from models in Qt item views, e.g., a QtGui.QTableView, the individual items are drawn by a delegate. Also, when an item is edited, the delegate provides an editor widget that is placed on top of the item view while editing takes place. QtGui.QStyledItemDelegate is the default delegate for all Qt item views.

    The data of items in models are assigned an Qt.ItemDataRole; each item can store appropriate data types for each role (see enumeration below). QtGui.QStyledItemDelegate implements display and editing for the most common datatypes expected by users, including booleans, integers, and strings.

    The data will be drawn differently depending on which role they have in the model. The following table describes the roles and the data types the delegate can handle for each of them. It is often sufficient to ensure that the model returns appropriate data for each of the roles to determine the appearance of items in views.
    
    Role 	                Accepted Types
    Qt.BackgroundRole 	    QtGui.QBrush
    Qt.CheckStateRole 	    Qt.CheckState
    Qt.DecorationRole 	    QtGui.QIcon, QtGui.QPixmap, QtGui.QImage and QtGui.QColor
    Qt.DisplayRole 	        QtCore.QString and types with a string representation
    Qt.EditRole 	        See QtGui.QItemEditorFactory for details
    Qt.FontRole 	        QtGui.QFont
    Qt.SizeHintRole 	    QtCore.QSize
    Qt.TextAlignmentRole 	Qt.Alignment
    Qt.ForegroundRole 	    QtGui.QBrush

    Editors are created with a QtGui.QItemEditorFactory ; a default static instance provided by QtGui.QItemEditorFactory is installed on all item delegates. You can set a custom factory using QtGui.QStyledItemDelegate.setItemEditorFactory() or set a new default factory with QItemEditorFactory.setDefaultFactory() It is the data stored in the item model with the EditRole that is edited. See the QtGui.QItemEditorFactory class for a more high-level introduction to item editor factories. The Color Editor Factory example shows how to create custom editors with a factory.

    ###Subclassing QStyledItemDelegate

    If the delegate does not support painting of the data types you need or you want to customize the drawing of items, you need to subclass QtGui.QStyledItemDelegate, and reimplement QtGui.QStyledItemDelegate.paint() and possibly QtGui.QStyledItemDelegate.sizeHint() The QtGui.QStyledItemDelegate.paint() function is called individually for each item, and with QtGui.QStyledItemDelegate.sizeHint(), you can specify the hint for each of them.

    When reimplementing QtGui.QStyledItemDelegate.paint(), one would typically handle the data types one would like to draw and use the superclass implementation for other types.

    The painting of check box indicators are performed by the current style. The style also specifies the size and the bounding rectangles in which to draw the data for the different data roles. The bounding rectangle of the item itself is also calculated by the style. When drawing already supported data types, it is therefore a good idea to ask the style for these bounding rectangles. The QtGui.QStyle class description describes this in more detail.

    If you wish to change any of the bounding rectangles calculated by the style or the painting of check box indicators, you can subclass QtGui.QStyle. Note, however, that the size of the items can also be affected by reimplementing QtGui.QStyledItemDelegate.sizeHint()

    It is possible for a custom delegate to provide editors without the use of an editor item factory. In this case, the following virtual functions must be reimplemented:

        QtGui.QStyledItemDelegate.createEditor() returns the widget used to change data from the model and can be reimplemented to customize editing behavior.
        QtGui.QStyledItemDelegate.setEditorData() provides the widget with data to manipulate.
        QtGui.QStyledItemDelegate.updateEditorGeometry() ensures that the editor is displayed correctly with respect to the item view.
        QtGui.QStyledItemDelegate.setModelData() returns updated data to the model.

    The Star Delegate example creates editors by reimplementing these methods.

    ###QStyledItemDelegate vs. QItemDelegate

    Since Qt 4.4, there are two delegate classes: QtGui.QItemDelegate and QtGui.QStyledItemDelegate However, the default delegate is QtGui.QStyledItemDelegate These two classes are independent alternatives to painting and providing editors for items in views. The difference between them is that QtGui.QStyledItemDelegate uses the current style to paint its items. We therefore recommend using QtGui.QStyledItemDelegate as the base class when implementing custom delegates or when working with Qt style sheets. The code required for either class should be equal unless the custom delegate needs to use the style for drawing.

    If you wish to customize the painting of item views, you should implement a custom style. Please see the QtGui.QStyle class documentation for details.