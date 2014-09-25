Things that might be useful when working through Chapter 12 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
Excellent graphics view framework overview
http://qt-project.org/doc/qt-4.8/graphicsview.html


#Useful Documentation
##QtGui.QGraphicsScene
http://pyside.github.io/docs/pyside/PySide/QtGui/QGraphicsScene.html

    The PySide.QtGui.QGraphicsScene class provides a surface for managing a large number of 2D graphical items. The class serves as a container for QGraphicsItems. It is used together with PySide.QtGui.QGraphicsView for visualizing graphical items, such as lines, rectangles, text, or even custom items, on a 2D surface. PySide.QtGui.QGraphicsScene is part of the Graphics View Framework .

    PySide.QtGui.QGraphicsScene also provides functionality that lets you efficiently determine both the location of items, and for determining what items are visible within an arbitrary area on the scene. With the PySide.QtGui.QGraphicsView widget, you can either visualize the whole scene, or zoom in and view only parts of the scene.

    Example [note this does not work]
        scene = QGraphicsScene()
        scene.addText("Hello, world!")
        view = QGraphicsView(scene)
        view.show()

    Note that PySide.QtGui.QGraphicsScene has no visual appearance of its own; it only manages the items. You need to create a PySide.QtGui.QGraphicsView widget to visualize the scene.

    To add items to a scene, you start off by constructing a PySide.QtGui.QGraphicsScene object. Then, you have two options: either add your existing PySide.QtGui.QGraphicsItem objects by calling PySide.QtGui.QGraphicsScene.addItem() , or you can call one of the convenience functions PySide.QtGui.QGraphicsScene.addEllipse() , PySide.QtGui.QGraphicsScene.addLine() , PySide.QtGui.QGraphicsScene.addPath() , PySide.QtGui.QGraphicsScene.addPixmap() , PySide.QtGui.QGraphicsScene.addPolygon() , PySide.QtGui.QGraphicsScene.addRect() , or PySide.QtGui.QGraphicsScene.addText() , which all return a pointer to the newly added item. The dimensions of the items added with these functions are relative to the item’s coordinate system, and the items position is initialized to (0, 0) in the scene.

    You can then visualize the scene using PySide.QtGui.QGraphicsView . When the scene changes, (e.g., when an item moves or is transformed) PySide.QtGui.QGraphicsScene emits the PySide.QtGui.QGraphicsScene.changed() signal. To remove an item, call PySide.QtGui.QGraphicsScene.removeItem().
    
    This is awesome, simple, intuitive. 

    The scene’s bounding rect is set by calling PySide.QtGui.QGraphicsScene.setSceneRect() . Items can be placed at any position on the scene, and the size of the scene is by default unlimited. The scene rect is used only for internal bookkeeping, maintaining the scene’s item index. If the scene rect is unset, PySide.QtGui.QGraphicsScene will use the bounding area of all items, as returned by PySide.QtGui.QGraphicsScene.itemsBoundingRect() , as the scene rect. However, PySide.QtGui.QGraphicsScene.itemsBoundingRect() is a relatively time consuming function, as it operates by collecting positional information for every item on the scene. Because of this, you should always set the scene rect when operating on large scenes.

    One of PySide.QtGui.QGraphicsScene ‘s greatest strengths is its ability to efficiently determine the location of items. Even with millions of items on the scene, the PySide.QtGui.QGraphicsScene.items() functions can determine the location of an item within few milliseconds. There are several overloads to PySide.QtGui.QGraphicsScene.items() : one that finds items at a certain position, one that finds items inside or intersecting with a polygon or a rectangle, and more. The list of returned items is sorted by stacking order, with the topmost item being the first item in the list. For convenience, there is also an PySide.QtGui.QGraphicsScene.itemAt() function that returns the topmost item at a given position.

    PySide.QtGui.QGraphicsScene maintains selection information for the scene. To select items, call PySide.QtGui.QGraphicsScene.setSelectionArea() , and to clear the current selection, call PySide.QtGui.QGraphicsScene.clearSelection() . Call PySide.QtGui.QGraphicsScene.selectedItems() to get the list of all selected items.

    ###Event Handling and Propagation

    Another responsibility that PySide.QtGui.QGraphicsScene has, is to propagate events from PySide.QtGui.QGraphicsView . To send an event to a scene, you construct an event that inherits PySide.QtCore.QEvent , and then send it using, for example, QApplication.sendEvent() . PySide.QtGui.QGraphicsScene.event() is responsible for dispatching the event to the individual items. Some common events are handled by convenience event handlers. For example, key press events are handled by PySide.QtGui.QGraphicsScene.keyPressEvent() , and mouse press events are handled by PySide.QtGui.QGraphicsScene.mousePressEvent() .

    Key events are delivered to the focus item . To set the focus item, you can either call PySide.QtGui.QGraphicsScene.setFocusItem() , passing an item that accepts focus, or the item itself can call QGraphicsItem.setFocus() . Call PySide.QtGui.QGraphicsScene.focusItem() to get the current focus item. For compatibility with widgets, the scene also maintains its own focus information. By default, the scene does not have focus, and all key events are discarded. If PySide.QtGui.QGraphicsScene.setFocus() is called, or if an item on the scene gains focus, the scene automatically gains focus. If the scene has focus, PySide.QtGui.QGraphicsScene.hasFocus() will return true, and key events will be forwarded to the focus item, if any. If the scene loses focus, (i.e., someone calls PySide.QtGui.QGraphicsScene.clearFocus() ) while an item has focus, the scene will maintain its item focus information, and once the scene regains focus, it will make sure the last focus item regains focus.

    For mouse-over effects, PySide.QtGui.QGraphicsScene dispatches hover events . If an item accepts hover events (see QGraphicsItem.acceptHoverEvents() ), it will receive a GraphicsSceneHoverEnter event when the mouse enters its area. As the mouse continues moving inside the item’s area, PySide.QtGui.QGraphicsScene will send it GraphicsSceneHoverMove events. When the mouse leaves the item’s area, the item will receive a GraphicsSceneHoverLeave event.

    
##QtGui.GraphicsView
http://pyside.github.io/docs/pyside/PySide/QtGui/QGraphicsView.html

    The PySide.QtGui.QGraphicsView class provides a widget for displaying the contents of a PySide.QtGui.QGraphicsScene .

    PySide.QtGui.QGraphicsView visualizes the contents of a PySide.QtGui.QGraphicsScene in a scrollable viewport. To create a scene with geometrical items, see PySide.QtGui.QGraphicsScene ‘s documentation. PySide.QtGui.QGraphicsView is part of the Graphics View Framework .

    To visualize a scene, you start by constructing a PySide.QtGui.QGraphicsView object, passing the address of the scene you want to visualize to PySide.QtGui.QGraphicsView ‘s constructor. Alternatively, you can call PySide.QtGui.QGraphicsView.setScene() to set the scene at a later point. After you call PySide.QtGui.QWidget.show() , the view will by default scroll to the center of the scene and display any items that are visible at this point.

    You can explicitly scroll to any position on the scene by using the scroll bars, or by calling PySide.QtGui.QGraphicsView.centerOn() . By passing a point to PySide.QtGui.QGraphicsView.centerOn() , PySide.QtGui.QGraphicsView will scroll its viewport to ensure that the point is centered in the view. An overload is provided for scrolling to a PySide.QtGui.QGraphicsItem , in which case PySide.QtGui.QGraphicsView will see to that the center of the item is centered in the view. If all you want is to ensure that a certain area is visible, (but not necessarily centered,) you can call PySide.QtGui.QGraphicsView.ensureVisible() instead.

    PySide.QtGui.QGraphicsView can be used to visualize a whole scene, or only parts of it. The visualized area is by default detected automatically when the view is displayed for the first time (by calling QGraphicsScene.itemsBoundingRect() ). To set the visualized area rectangle yourself, you can call PySide.QtGui.QGraphicsView.setSceneRect() . This will adjust the scroll bars’ ranges appropriately. Note that although the scene supports a virtually unlimited size, the range of the scroll bars will never exceed the range of an integer (INT_MIN, INT_MAX).

    PySide.QtGui.QGraphicsView visualizes the scene by calling PySide.QtGui.QGraphicsView.render() . By default, the items are drawn onto the viewport by using a regular PySide.QtGui.QPainter , and using default render hints. To change the default render hints that PySide.QtGui.QGraphicsView passes to PySide.QtGui.QPainter when painting items, you can call PySide.QtGui.QGraphicsView.setRenderHints() .

    PySide.QtGui.QGraphicsView supports affine transformations, using PySide.QtGui.QTransform . You can either pass a matrix to PySide.QtGui.QGraphicsView.setTransform() , or you can call one of the convenience functions PySide.QtGui.QGraphicsView.rotate() , PySide.QtGui.QGraphicsView.scale() , PySide.QtGui.QGraphicsView.translate() or PySide.QtGui.QGraphicsView.shear() . The most two common transformations are scaling, which is used to implement zooming, and rotation. PySide.QtGui.QGraphicsView keeps the center of the view fixed during a transformation. Because of the scene alignment (setAligment()), translating the view will have no visual impact.

    You can interact with the items on the scene by using the mouse and keyboard. PySide.QtGui.QGraphicsView translates the mouse and key events into scene events, (events that inherit PySide.QtGui.QGraphicsSceneEvent), and forward them to the visualized scene. In the end, it’s the individual item that handles the events and reacts to them. For example, if you click on a selectable item, the item will typically let the scene know that it has been selected, and it will also redraw itself to display a selection rectangle. Similiary, if you click and drag the mouse to move a movable item, it’s the item that handles the mouse moves and moves itself. Item interaction is enabled by default, and you can toggle it by calling PySide.QtGui.QGraphicsView.setInteractive() .




##QtGui.QGraphicsItem
http://pyside.github.io/docs/pyside/PySide/QtGui/QGraphicsItem.html

    The PySide.QtGui.QGraphicsItem class is the base class for all graphical items in a PySide.QtGui.QGraphicsScene .

    It provides a light-weight foundation for writing your own custom items. This includes defining the item’s geometry, collision detection, its painting implementation and item interaction through its event handlers. PySide.QtGui.QGraphicsItem is part of the Graphics View Framework

    For convenience, Qt provides a set of standard graphics items for the most common shapes. These are:

        PySide.QtGui.QGraphicsEllipseItem provides an ellipse item
        PySide.QtGui.QGraphicsLineItem provides a line item
        PySide.QtGui.QGraphicsPathItem provides an arbitrary path item
        PySide.QtGui.QGraphicsPixmapItem provides a pixmap item
        PySide.QtGui.QGraphicsPolygonItem provides a polygon item
        PySide.QtGui.QGraphicsRectItem provides a rectangular item
        PySide.QtGui.QGraphicsSimpleTextItem provides a simple text label item
        PySide.QtGui.QGraphicsTextItem provides an advanced text browser item

    All of an item’s geometric information is based on its local coordinate system. The item’s position, PySide.QtGui.QGraphicsItem.pos() , is the only function that does not operate in local coordinates, as it returns a position in parent coordinates. Graphics View Coordinate System (part of Graphics View Framework doc linked above) describes the coordinate system in detail.

    You can set whether an item should be visible (i.e., drawn, and accepting events), by calling PySide.QtGui.QGraphicsItem.setVisible() . Hiding an item will also hide its children. Similarly, you can enable or disable an item by calling PySide.QtGui.QGraphicsItem.setEnabled() . If you disable an item, all its children will also be disabled. By default, items are both visible and enabled. To toggle whether an item is selected or not, first enable selection by setting the ItemIsSelectable flag, and then call PySide.QtGui.QGraphicsItem.setSelected() . Normally, selection is toggled by the scene, as a result of user interaction.

    To write your own graphics item, you first create a subclass of PySide.QtGui.QGraphicsItem , and then start by implementing its two pure virtual public functions: PySide.QtGui.QGraphicsItem.boundingRect() , which returns an estimate of the area painted by the item, and PySide.QtGui.QGraphicsItem.paint() , which implements the actual painting. For example [I have not tested the following (ET)]:

        class SimpleItem(QGraphicsItem):

            def boundingRect(self):
                penWidth = 1.0
                return QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
                              20 + penWidth, 20 + penWidth)

            def paint(self, painter, option, widget):
                painter.drawRoundedRect(-10, -10, 20, 20, 5, 5)

    The PySide.QtGui.QGraphicsItem.boundingRect() function has many different purposes. PySide.QtGui.QGraphicsScene bases its item index on PySide.QtGui.QGraphicsItem.boundingRect() , and PySide.QtGui.QGraphicsView uses it both for culling invisible items, and for determining the area that needs to be recomposed when drawing overlapping items. In addition, PySide.QtGui.QGraphicsItem ‘s collision detection mechanisms use PySide.QtGui.QGraphicsItem.boundingRect() to provide an efficient cut-off. The fine grained collision algorithm in PySide.QtGui.QGraphicsItem.collidesWithItem() is based on calling PySide.QtGui.QGraphicsItem.shape() , which returns an accurate outline of the item’s shape as a PySide.QtGui.QPainterPath .

    PySide.QtGui.QGraphicsScene expects all items PySide.QtGui.QGraphicsItem.boundingRect() and PySide.QtGui.QGraphicsItem.shape() to remain unchanged unless it is notified. If you want to change an item’s geometry in any way, you must first call PySide.QtGui.QGraphicsItem.prepareGeometryChange() to allow PySide.QtGui.QGraphicsScene to update its bookkeeping.

    Collision detection can be done in two ways:

    The PySide.QtGui.QGraphicsItem.contains() function can be called to determine whether the item contains a point or not. This function can also be reimplemented by the item. The default behavior of PySide.QtGui.QGraphicsItem.contains() is based on calling PySide.QtGui.QGraphicsItem.shape() .

    Items can contain other items, and also be contained by other items. All items can have a parent item and a list of children. Unless the item has no parent, its position is in parent coordinates (i.e., the parent’s local coordinates). Parent items propagate both their position and their transformation to all children.


    ###Transformations

    PySide.QtGui.QGraphicsItem supports projective transformations in addition to its base position, PySide.QtGui.QGraphicsItem.pos() . There are several ways to change an item’s transformation. For simple transformations, you can call either of the convenience functions PySide.QtGui.QGraphicsItem.setRotation() or PySide.QtGui.QGraphicsItem.setScale() , or you can pass any transformation matrix to PySide.QtGui.QGraphicsItem.setTransform() . For advanced transformation control you also have the option of setting several combined transformations by calling PySide.QtGui.QGraphicsItem.setTransformations() .

    Item transformations accumulate from parent to child, so if both a parent and child item are rotated 90 degrees, the child’s total transformation will be 180 degrees. Similarly, if the item’s parent is scaled to 2x its original size, its children will also be twice as large. An item’s transformation does not affect its own local geometry; all geometry functions (e.g., PySide.QtGui.QGraphicsItem.contains() , PySide.QtGui.QGraphicsItem.update() , and all the mapping functions) still operate in local coordinates. For convenience, PySide.QtGui.QGraphicsItem provides the functions PySide.QtGui.QGraphicsItem.sceneTransform() , which returns the item’s total transformation matrix (including its position and all parents’ positions and transformations), and PySide.QtGui.QGraphicsItem.scenePos() , which returns its position in scene coordinates. To reset an item’s matrix, call PySide.QtGui.QGraphicsItem.resetTransform() .

    Certain transformation operations produce a different outcome depending on the order in which they are applied. For example, if you scale an transform, and then rotate it, you may get a different result than if the transform was rotated first. However, the order you set the transformation properties on PySide.QtGui.QGraphicsItem does not affect the resulting transformation; PySide.QtGui.QGraphicsItem always applies the properties in a fixed, defined order:

        The item’s base transform is applied ( PySide.QtGui.QGraphicsItem.transform() )
        The item’s transformations list is applied in order ( PySide.QtGui.QGraphicsItem.transformations() )
        The item is rotated relative to its transform origin point ( PySide.QtGui.QGraphicsItem.rotation() , PySide.QtGui.QGraphicsItem.transformOriginPoint() )
        The item is scaled relative to its transform origin point ( PySide.QtGui.QGraphicsItem.scale() , PySide.QtGui.QGraphicsItem.transformOriginPoint() )

    ###Painting
    The PySide.QtGui.QGraphicsItem.paint() function is called by PySide.QtGui.QGraphicsView to paint the item’s contents. The item has no background or default fill of its own; whatever is behind the item will shine through all areas that are not explicitly painted in this function. You can call PySide.QtGui.QGraphicsItem.update() to schedule a repaint, optionally passing the rectangle that needs a repaint. Depending on whether or not the item is visible in a view, the item may or may not be repainted; there is no equivalent to QWidget.repaint() in PySide.QtGui.QGraphicsItem .

    Items are painted by the view, starting with the parent items and then drawing children, in ascending stacking order. You can set an item’s stacking order by calling PySide.QtGui.QGraphicsItem.setZValue() , and test it by calling PySide.QtGui.QGraphicsItem.zValue() , where items with low z-values are painted before items with high z-values. Stacking order applies to sibling items; parents are always drawn before their children.

    ###Sorting
    All items are drawn in a defined, stable order, and this same order decides which items will receive mouse input first when you click on the scene. Normally you don’t have to worry about sorting, as the items follow a “natural order”, following the logical structure of the scene.

    An item’s children are stacked on top of the parent, and sibling items are stacked by insertion order (i.e., in the same order that they were either added to the scene, or added to the same parent). If you add item A, and then B, then B will be on top of A. If you then add C, the items’ stacking order will be A, then B, then C.

    See the example illustration of the stacking order of all limbs of the robot from the Drag and Drop Robot example. The torso is the root item (all other items are children or descendants of the torso), so it is drawn first. Next, the head is drawn, as it is the first item in the torso’s list of children. Then the upper left arm is drawn. As the lower arm is a child of the upper arm, the lower arm is then drawn, followed by the upper arm’s next sibling, which is the upper right arm, and so on.


    ###Events

    PySide.QtGui.QGraphicsItem receives events from PySide.QtGui.QGraphicsScene through the virtual function PySide.QtGui.QGraphicsItem.sceneEvent() . This function distributes the most common events to a set of convenience event handlers:

        PySide.QtGui.QGraphicsItem.contextMenuEvent() handles context menu events
        PySide.QtGui.QGraphicsItem.focusInEvent() and PySide.QtGui.QGraphicsItem.focusOutEvent() handle focus in and out events
        PySide.QtGui.QGraphicsItem.hoverEnterEvent() , PySide.QtGui.QGraphicsItem.hoverMoveEvent() , and PySide.QtGui.QGraphicsItem.hoverLeaveEvent() handles hover enter, move and leave events
        PySide.QtGui.QGraphicsItem.inputMethodEvent() handles input events, for accessibility support
        PySide.QtGui.QGraphicsItem.keyPressEvent() and PySide.QtGui.QGraphicsItem.keyReleaseEvent() handle key press and release events
        PySide.QtGui.QGraphicsItem.mousePressEvent() , PySide.QtGui.QGraphicsItem.mouseMoveEvent() , PySide.QtGui.QGraphicsItem.mouseReleaseEvent() , and PySide.QtGui.QGraphicsItem.mouseDoubleClickEvent() handles mouse press, move, release, click and doubleclick events


    ###Custom Data
    Sometimes it’s useful to register custom data with an item, be it a custom item, or a standard item. You can call PySide.QtGui.QGraphicsItem.setData() on any item to store data in it using a key-value pair (the key being an integer, and the value is a PySide.QtCore.QVariant ). To get custom data from an item, call PySide.QtGui.QGraphicsItem.data() . This functionality is completely untouched by Qt itself; it is provided for the user’s convenience.
    


##QtGui.QGraphicsTextItem
http://github.io/docs/pyside/PySide/QtGui/QGraphicsTextItem.html

    The QtGui.QGraphicsTextItem class provides a text item that you can add to a QtGui.QGraphicsScene to display formatted text. If you only need to show plain text in an item, consider using QtGui.QGraphicsSimpleTextItem instead.

    To set the item’s text, pass a QtCore.QString to QtGui.QGraphicsTextItem ‘s constructor, or call QtGui.QGraphicsTextItem.setHtml() / QtGui.QGraphicsTextItem.setPlainText() .

    QtGui.QGraphicsTextItem uses the text’s formatted size and the associated font to provide a reasonable implementation of QtGui.QGraphicsTextItem.boundingRect() , QtGui.QGraphicsTextItem.shape() , and QtGui.QGraphicsTextItem.contains() . You can set the font by calling QtGui.QGraphicsTextItem.setFont() .

    It is possible to make the item editable by setting the Qt.TextEditorInteraction flag using QtGui.QGraphicsTextItem.setTextInteractionFlags() .

    The item’s preferred text width can be set using QtGui.QGraphicsTextItem.setTextWidth() and obtained using QtGui.QGraphicsTextItem.textWidth() .

    In order to align HTML text in the center, the item’s text width must be set.
    

