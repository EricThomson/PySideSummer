Things that might be useful when working through Chapter 16 of Rapid GUI Programming by Summerfield.
Part of PySideSummer repository (https://github.com/EricThomson/PySideSummer)


#Useful links
Talk on delegates by our own Mark Summerfield:
https://www.youtube.com/watch?v=imIH8QLPVcY
Note it focuses on C++, but if you have made it this far in the book you probably are ok with it.

Enumeration of state flags (e.g., state_selected) 
http://pyqt.sourceforge.net/Docs/PyQt4/qstyle.html#StateFlag-enum

Simple tree model example (written for Qt, but good for PySide too)
http://qt-project.org/doc/qt-4.8/itemviews-simpletreemodel.html

Editable tree model example (to work in Pyside needs a couple of tweaks)
http://qt-project.org/doc/qt-4.8/itemviews-editabletreemodel.html

On the use of 'assert' in Python:
http://stackoverflow.com/questions/5142418/what-is-the-use-of-assert-in-python

#Useful Documentation
##QtCore.QAbstractTableModel
http://srinikom.github.io/pyside-docs/PySide/QtCore/QAbstractTableModel.html

See Chapter14 usefulStuff

##QtCore.QAbstractItemModel
    The PySide.QtCore.QAbstractItemModel class provides the abstract interface for item model classes.

    The PySide.QtCore.QAbstractItemModel class defines the standard interface that item models must use to be able to interoperate with other components in the model/view architecture. It is not supposed to be instantiated directly. Instead, you should subclass it to create new models.

    The PySide.QtCore.QAbstractItemModel class is one of the Model/View Classes and is part of Qt’s model/view framework .

    If you need a model to use with a PySide.QtGui.QListView or a PySide.QtGui.QTableView , you should consider subclassing PySide.QtCore.QAbstractListModel or PySide.QtCore.QAbstractTableModel instead of this class.

    The underlying data model is exposed to views and delegates as a hierarchy of tables. If you do not make use of the hierarchy, then the model is a simple table of rows and columns. Each item has a unique index specified by a PySide.QtCore.QModelIndex .
    ../../_images/modelindex-no-parent.png

    Every item of data that can be accessed via a model has an associated model index. You can obtain this model index using the PySide.QtCore.QAbstractItemModel.index() function. Each index may have a PySide.QtCore.QAbstractItemModel.sibling() index; child items have a PySide.QtCore.QAbstractItemModel.parent() index.

    Each item has a number of data elements associated with it and they can be retrieved by specifying a role (see Qt.ItemDataRole ) to the model’s PySide.QtCore.QAbstractItemModel.data() function. Data for all available roles can be obtained at the same time using the PySide.QtCore.QAbstractItemModel.itemData() function.

    Data for each role is set using a particular Qt.ItemDataRole . Data for individual roles are set individually with PySide.QtCore.QAbstractItemModel.setData() , or they can be set for all roles with PySide.QtCore.QAbstractItemModel.setItemData() .

    Items can be queried with PySide.QtCore.QAbstractItemModel.flags() (see Qt.ItemFlag ) to see if they can be selected, dragged, or manipulated in other ways.

    If an item has child objects, PySide.QtCore.QAbstractItemModel.hasChildren() returns true for the corresponding index.

    The model has a PySide.QtCore.QAbstractItemModel.rowCount() and a PySide.QtCore.QAbstractItemModel.columnCount() for each level of the hierarchy. Rows and columns can be inserted and removed with PySide.QtCore.QAbstractItemModel.insertRows() , PySide.QtCore.QAbstractItemModel.insertColumns() , PySide.QtCore.QAbstractItemModel.removeRows() , and PySide.QtCore.QAbstractItemModel.removeColumns() .

    The model emits signals to indicate changes. For example, PySide.QtCore.QAbstractItemModel.dataChanged() is emitted whenever items of data made available by the model are changed. Changes to the headers supplied by the model cause PySide.QtCore.QAbstractItemModel.headerDataChanged() to be emitted. If the structure of the underlying data changes, the model can emit PySide.QtCore.QAbstractItemModel.layoutChanged() to indicate to any attached views that they should redisplay any items shown, taking the new structure into account.

    The items available through the model can be searched for particular data using the PySide.QtCore.QAbstractItemModel.match() function.

    To sort the model, you can use PySide.QtCore.QAbstractItemModel.sort() .

    Subclassing
    Note

    Some general guidelines for subclassing models are available in the Model Subclassing Reference .

    When subclassing PySide.QtCore.QAbstractItemModel , at the very least you must implement PySide.QtCore.QAbstractItemModel.index() , PySide.QtCore.QAbstractItemModel.parent() , PySide.QtCore.QAbstractItemModel.rowCount() , PySide.QtCore.QAbstractItemModel.columnCount() , and PySide.QtCore.QAbstractItemModel.data() . These functions are used in all read-only models, and form the basis of editable models.

    You can also reimplement PySide.QtCore.QAbstractItemModel.hasChildren() to provide special behavior for models where the implementation of PySide.QtCore.QAbstractItemModel.rowCount() is expensive. This makes it possible for models to restrict the amount of data requested by views, and can be used as a way to implement lazy population of model data.

    To enable editing in your model, you must also implement PySide.QtCore.QAbstractItemModel.setData() , and reimplement PySide.QtCore.QAbstractItemModel.flags() to ensure that ItemIsEditable is returned. You can also reimplement PySide.QtCore.QAbstractItemModel.headerData() and PySide.QtCore.QAbstractItemModel.setHeaderData() to control the way the headers for your model are presented.

    The PySide.QtCore.QAbstractItemModel.dataChanged() and PySide.QtCore.QAbstractItemModel.headerDataChanged() signals must be emitted explicitly when reimplementing the PySide.QtCore.QAbstractItemModel.setData() and PySide.QtCore.QAbstractItemModel.setHeaderData() functions, respectively.

    Custom models need to create model indexes for other components to use. To do this, call PySide.QtCore.QAbstractItemModel.createIndex() with suitable row and column numbers for the item, and an identifier for it, either as a pointer or as an integer value. The combination of these values must be unique for each item. Custom models typically use these unique identifiers in other reimplemented functions to retrieve item data and access information about the item’s parents and children. See the Simple Tree Model Example for more information about unique identifiers.

    It is not necessary to support every role defined in Qt.ItemDataRole . Depending on the type of data contained within a model, it may only be useful to implement the PySide.QtCore.QAbstractItemModel.data() function to return valid information for some of the more common roles. Most models provide at least a textual representation of item data for the Qt.DisplayRole , and well-behaved models should also provide valid information for the Qt.ToolTipRole and Qt.WhatsThisRole . Supporting these roles enables models to be used with standard Qt views. However, for some models that handle highly-specialized data, it may be appropriate to provide data only for user-defined roles.

    Models that provide interfaces to resizable data structures can provide implementations of PySide.QtCore.QAbstractItemModel.insertRows() , PySide.QtCore.QAbstractItemModel.removeRows() , PySide.QtCore.QAbstractItemModel.insertColumns() ,and PySide.QtCore.QAbstractItemModel.removeColumns() . When implementing these functions, it is important to notify any connected views about changes to the model’s dimensions both before and after they occur:

        An PySide.QtCore.QAbstractItemModel.insertRows() implementation must call PySide.QtCore.QAbstractItemModel.beginInsertRows() before inserting new rows into the data structure, and PySide.QtCore.QAbstractItemModel.endInsertRows() immediately afterwards.
        An PySide.QtCore.QAbstractItemModel.insertColumns() implementation must call PySide.QtCore.QAbstractItemModel.beginInsertColumns() before inserting new columns into the data structure, and PySide.QtCore.QAbstractItemModel.endInsertColumns() immediately afterwards.
        A PySide.QtCore.QAbstractItemModel.removeRows() implementation must call PySide.QtCore.QAbstractItemModel.beginRemoveRows() before the rows are removed from the data structure, and PySide.QtCore.QAbstractItemModel.endRemoveRows() immediately afterwards.
        A PySide.QtCore.QAbstractItemModel.removeColumns() implementation must call PySide.QtCore.QAbstractItemModel.beginRemoveColumns() before the columns are removed from the data structure, and PySide.QtCore.QAbstractItemModel.endRemoveColumns() immediately afterwards.

    The private signals that these functions emit give attached components the chance to take action before any data becomes unavailable. The encapsulation of the insert and remove operations with these begin and end functions also enables the model to manage persistent model indexes correctly. If you want selections to be handled properly, you must ensure that you call these functions. If you insert or remove an item with children, you do not need to call these functions for the child items. In other words, the parent item will take care of its child items.

    To create models that populate incrementally, you can reimplement PySide.QtCore.QAbstractItemModel.fetchMore() and PySide.QtCore.QAbstractItemModel.canFetchMore() . If the reimplementation of PySide.QtCore.QAbstractItemModel.fetchMore() adds rows to the model, PySide.QtCore.QAbstractItemModel.beginInsertRows() and PySide.QtCore.QAbstractItemModel.endInsertRows() must be called.
    
    

##QtGui.QTreeView
http://srinikom.github.io/pyside-docs/PySide/QtGui/QTreeView.html

    The QtGui.QTreeView class provides a default model/view implementation of a tree view. It is simple to construct a tree view displaying data from a model. In the following example, the contents of a directory are supplied by a QtGui.QDirModel and displayed as a tree:

        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        tree =  QTreeView()
        tree.setModel(model)

    The model/view architecture ensures that the contents of the tree view are updated if the model changes.

    Items that have children can be in an expanded (children are visible) or collapsed (children are hidden) state. When this state changes a QtGui.QTreeView.collapsed() or QtGui.QTreeView.expanded() signal is emitted with the model index of the relevant item.

    The amount of indentation used to indicate levels of hierarchy is controlled by the QtGui.QTreeView.indentation() property.

    Headers in tree views are constructed using the QtGui.QHeaderView class and can be hidden using header()->hide() . Note that each header is configured with its QtGui.QHeaderView.stretchLastSection() property set to true, ensuring that the view does not waste any of the space assigned to it for its header. If this value is set to true, this property will override the resize mode set on the last section in the header.

    ###Key Bindings

    QtGui.QTreeView supports a set of key bindings that enable the user to navigate in the view and interact with the contents of items:
    Up 	        
        Moves the cursor to the item in the same column on the previous row. If the parent of the current   item has no more rows to navigate to, the cursor moves to the relevant item in the last row of the sibling that precedes the parent.
    Down
        Moves the cursor to the item in the same column on the next row. If the parent of the current item has no more rows to navigate to, the cursor moves to the relevant item in the first row of the sibling that follows the parent.
    Left 	
        Hides the children of the current item (if present) by collapsing a branch.
    Minus
        Same as LeftArrow.
    Right
        Reveals the children of the current item (if present) by expanding a branch.
    Plus
        Same as RightArrow.
    Asterisk
        Expands all children of the current item (if present).
    PageUp
        Moves the cursor up one page.
    PageDown
        Moves the cursor down one page.
    Home 
        Moves the cursor to an item in the same column of the first row of the first top-level item in the model.
    End 	
        Moves the cursor to an item in the same column of the last row of the last top-level item in the model.
    F2 	
        In editable models, this opens the current item for editing. The Escape key can be used to cancel the editing process and revert any changes to the data displayed.


    ###Improving Performance
    It is possible to give the view hints about the data it is handling in order to improve its performance when displaying large numbers of items. One approach that can be taken for views that are intended to display items with equal heights is to set the QtGui.QTreeView.uniformRowHeights() property to true.
    


##QtGui.QWidget.setFocusPolicy
http://srinikom.github.io/pyside-docs/PySide/QtGui/QWidget.html#QtGui.QtGui.QWidget.setFocusPolicy

    This property holds the way the widget accepts keyboard focus. The policy is Qt.TabFocus if the widget accepts keyboard focus by tabbing, Qt.ClickFocus if the widget accepts focus by clicking, Qt.StrongFocus if it accepts both, and Qt.NoFocus (the default) if it does not accept focus at all.

    You must enable keyboard focus for a widget if it processes keyboard events. This is normally done from the widget’s constructor. For instance, the QtGui.QLineEdit constructor calls setFocusPolicy( Qt.StrongFocus ). If the widget has a focus proxy, then the focus policy will be propagated to it.

    ###enum QtCore.Qt.FocusPolicy
    This enum type defines the various policies a widget can have with respect to acquiring keyboard focus.

    Constant	    Value	Description
    Qt::TabFocus	0x1	    the widget accepts focus by tabbing.
    Qt::ClickFocus	0x2	    the widget accepts focus by clicking.
    Qt::StrongFocus	0x8	    the widget accepts focus by both tabbing and clicking (TabFocus | ClickFocus)
    Qt::WheelFocus	0x4	    like Qt::StrongFocus plus the widget accepts focus by using the mouse wheel 
    Qt::NoFocus	    0	    the widget does not accept focus.




