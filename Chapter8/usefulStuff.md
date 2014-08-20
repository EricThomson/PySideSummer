Things that might be useful when working through Chapter 8 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
  id() :  https://docs.python.org/2/library/functions.html#id

#Useful Documentation
  **QtGui.QTableWidget**
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QTableWidget.html
    
    The PySide.QtGui.QTableWidget class provides an item-based table view with a default model (model/view framework will be covered in a subsequent chapter of Summerfield's book).Table widgets provide standard table display facilities for applications. The items in a PySide.QtGui.QTableWidget are provided by PySide.QtGui.QTableWidgetItem .

    Table widgets can be constructed with the required numbers of rows and columns:
        tableWidget = QTableWidget(12, 3, self)
    Alternatively, tables can be constructed without a given size and resized later:
        tableWidget = QTableWidget()
        tableWidget.setRowCount(10)
        tableWidget.setColumnCount(5)

    Items are created ouside the table (with no parent widget) and inserted into the table with PySide.QtGui.QTableWidget.setItem() :
        newItem = QTableWidgetItem(tr("%s" % ((row+1)*(column+1))))
        tableWidget.setItem(row, column, newItem)

    If you want to enable sorting in your table widget, do so after you have populated it with items, otherwise sorting may interfere with the insertion order (see PySide.QtGui.QTableWidget.setItem() for details).   

    Tables can be given both horizontal and vertical headers. The simplest way to create the headers is to supply a list of strings to the PySide.QtGui.QTableWidget.setHorizontalHeaderLabels() and PySide.QtGui.QTableWidget.setVerticalHeaderLabels() functions. These will provide simple textual headers for the table’s columns and rows. More sophisticated headers can be created from existing table items that are usually constructed outside the table. For example, we can construct a table item with an icon and aligned text, and use it as the header for a particular column:
        cubesHeaderItem = QTableWidgetItem(tr("Cubes"))
        cubesHeaderItem.setIcon(QIcon(QPixmap(":/Images/cubed.png")))
        cubesHeaderItem.setTextAlignment(Qt::AlignVCenter)

    The number of rows in the table can be found with PySide.QtGui.QTableWidget.rowCount() , and the number of columns with PySide.QtGui.QTableWidget.columnCount() . The table can be cleared with the PySide.QtGui.QTableWidget.clear() function. 
    
  **QtGui.QTableWidgetItem**
  http://srinikom.github.io/pyside-docs/PySide/QtGui/QTableWidgetItem.html
    
    The PySide.QtGui.QTableWidgetItem class provides an item for use with the PySide.QtGui.QTableWidget class. Table items are used to hold pieces of information for table widgets. Items usually contain text, icons, or checkboxes

    By default, items are enabled, editable, selectable, checkable, and can be used both as the source of a drag and drop operation and as a drop target. Each item’s flags can be changed by calling PySide.QtGui.QTableWidgetItem.setFlags() with the appropriate value (see Qt.ItemFlags [see link below]). Checkable items can be checked and unchecked with the PySide.QtGui.QTableWidgetItem.setCheckState() function. The corresponding PySide.QtGui.QTableWidgetItem.checkState() function indicates whether the item is currently checked.

    enumeration of possible flags for an item:
    http://srinikom.github.io/pyside-docs/PySide/QtCore/Qt.html#PySide.QtCore.PySide.QtCore.Qt.ItemFlag
    
    
  **QtCore.QDataStream**
  http://srinikom.github.io/pyside-docs/PySide/QtCore/QDataStream.html
    The PySide.QtCore.QDataStream class provides serialization of binary data to a PySide.QtCore.QIODevice .

    A data stream is a binary stream of encoded information which is 100% independent of the host computer’s operating system, CPU or byte order. For example, a data stream that is written by a PC under Windows can be read by a Sun SPARC running Solaris.You can also use a data stream to read/write raw unencoded binary data . If you want a “parsing” input stream, see PySide.QtCore.QTextStream .

    The PySide.QtCore.QDataStream class implements the serialization of C++’s basic data types, like char , short , int , char * , etc. Serialization of more complex data is accomplished by breaking up the data into primitive units.

    A data stream cooperates closely with a PySide.QtCore.QIODevice . A PySide.QtCore.QIODevice represents an input/output medium one can read data from and write data to.

    Each item written to the stream is written in a predefined binary format that varies depending on the item’s type. Supported Qt types include PySide.QtGui.QBrush , PySide.QtGui.QColor , PySide.QtCore.QDateTime , PySide.QtGui.QFont , PySide.QtGui.QPixmap , PySide.QtCore.QString , PySide.QtCore.QVariant and many others. For the complete list of all Qt types supporting data streaming see Serializing Qt Data Types .

    For integers it is best to always cast to a Qt integer type for writing, and to read back into the same Qt integer type. This ensures that you get integers of the size you want and insulates you from compiler and platform differences.

    PySide.QtCore.QDataStream‘s binary format has evolved since Qt 1.0, and is likely to continue evolving to reflect changes done in Qt. When inputting or outputting complex types, it’s very important to make sure that the same version of the stream ( PySide.QtCore.QDataStream.version()) is used for reading and writing. If you need both forward and backward compatibility, you can hardcode the version number in the application:

    stream.setVersion(QDataStream.Qt_4_0)

    If you are producing a new binary data format, such as a file format for documents created by your application, you could use a PySide.QtCore.QDataStream to write the data in a portable format. Typically, you would write a brief header containing a magic string and a version number to give yourself room for future expansion. 
      
  
  **QtCore.QTextStream**
  http://srinikom.github.io/pyside-docs/PySide/QtCore/QTextStream.html
    The PySide.QtCore.QTextStream class provides a convenient interface for reading and writing text.

    PySide.QtCore.QTextStream can operate on a PySide.QtCore.QIODevice , a PySide.QtCore.QByteArray or a PySide.QtCore.QString . Using PySide.QtCore.QTextStream‘s streaming operators, you can conveniently read and write words, lines and numbers. For generating text, PySide.QtCore.QTextStream supports formatting options for field padding and alignment, and formatting of numbers.

    Besides using PySide.QtCore.QTextStream ‘s constructors, you can also set the device or string PySide.QtCore.QTextStream operates on by calling PySide.QtCore.QTextStream.setDevice() or PySide.QtCore.QTextStream.setString() . You can seek to a position by calling PySide.QtCore.QTextStream.seek() , and PySide.QtCore.QTextStream.atEnd() will return true when there is no data left to be read. If you call PySide.QtCore.QTextStream.flush() , PySide.QtCore.QTextStream will empty all data from its write buffer into the device and call PySide.QtCore.QTextStream.flush() on the device.

    Internally, PySide.QtCore.QTextStream uses a Unicode based buffer, and PySide.QtCore.QTextCodec is used by PySide.QtCore.QTextStream to automatically support different character sets. By default, QTextCodec.codecForLocale() is used for reading and writing, but you can also set the codec by calling PySide.QtCore.QTextStream.setCodec() . Automatic Unicode detection is also supported. When this feature is enabled (the default behavior), PySide.QtCore.QTextStream will detect the UTF-16 or the UTF-32 BOM (Byte Order Mark) and switch to the appropriate UTF codec when reading. PySide.QtCore.QTextStream does not write a BOM by default, but you can enable this by calling setGenerateByteOrderMark(true). When PySide.QtCore.QTextStream operates on a PySide.QtCore.QString directly, the codec is disabled.

    There are three general ways to use PySide.QtCore.QTextStream when reading text files:
    1. Chunk by chunk, by calling PySide.QtCore.QTextStream.readLine() or PySide.QtCore.QTextStream.readAll() .
    2. Word by word. PySide.QtCore.QTextStream supports streaming into QStrings, QByteArrays and char* buffers. Words are delimited by space, and leading white space is automatically skipped.
    3. Character by character, by streaming into PySide.QtCore.QChar or char types. This method is often used for convenient input handling when parsing files, independent of character encoding and end-of-line semantics. To skip white space, call PySide.QtCore.QTextStream.skipWhiteSpace() .

    Since the text stream uses a buffer, you should not read from the stream using the implementation of a superclass. For instance, if you have a PySide.QtCore.QFile and read from it directly using QFile.readLine() instead of using the stream, the text stream’s internal position will be out of sync with the file’s position.

    By default, when reading numbers from a stream of text, PySide.QtCore.QTextStream will automatically detect the number’s base representation. For example, if the number starts with “0x”, it is assumed to be in hexadecimal form. If it starts with the digits 1-9, it is assumed to be in decimal form, and so on. You can set the integer base, thereby disabling the automatic detection, by calling PySide.QtCore.QTextStream.setIntegerBase().

    PySide.QtCore.QTextStream supports many formatting options for generating text. You can set the field width and pad character by calling PySide.QtCore.QTextStream.setFieldWidth() and PySide.QtCore.QTextStream.setPadChar(). Use PySide.QtCore.QTextStream.setFieldAlignment() to set the alignment within each field. 

    For real numbers, call PySide.QtCore.QTextStream.setRealNumberNotation() and PySide.QtCore.QTextStream.setRealNumberPrecision() to set the notation (SmartNotation , ScientificNotation , FixedNotation ) and precision in digits of the generated number. Some extra number formatting options are also available through PySide.QtCore.QTextStream.setNumberFlags() (http://qt-project.org/doc/qt-4.8/qtextstream.html#NumberFlag-enum).
  
  
  **pickle**
  https://docs.python.org/2.7/library/pickle.html

    The pickle module implements a fundamental, but powerful algorithm for serializing and de-serializing a Python object structure. “Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, and “unpickling” is the inverse operation, whereby a byte stream is converted back into an object hierarchy. Pickling (and unpickling) is alternatively known as “serialization”, “marshalling,” [1] or “flattening”, however, to avoid confusion, the terms used here are “pickling” and “unpickling”.

    To serialize an object hierarchy, you first create a pickler, then you call the pickler’s dump() method.  To de-serialize a data stream, you first create an unpickler, then you call the unpickler’s load() method.

  
  **QDomDocument**
  https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/PySide/QtXml/QDomDocument.html

    The PySide.QtXml.QDomDocument class represents an XML document. It represents the entire XML document. Conceptually, it is the root of the document tree, and provides the primary access to the document’s data.

    Since elements, text nodes, comments, processing instructions, etc., cannot exist outside the context of a document, the document class also contains the factory functions needed to create these objects. The DOM classes that will be used most often are PySide.QtXml.QDomNode , PySide.QtXml.QDomDocument , PySide.QtXml.QDomElement and PySide.QtXml.QDomText.

    The parsed XML is represented internally by a tree of objects that can be accessed using the various QDom classes. All QDom classes only reference objects in the internal tree. The internal objects in the DOM tree will get deleted once the last QDom object referencing them and the PySide.QtXml.QDomDocument itself are deleted.

    Creation of elements, text nodes, etc. is done using the various factory functions provided in this class. Using the default constructors of the QDom classes will only result in empty objects that cannot be manipulated or inserted into the Document.

    The PySide.QtXml.QDomDocument class has several functions for creating document data, for example, PySide.QtXml.QDomDocument.createElement(), PySide.QtXml.QDomDocument.createTextNode() , PySide.QtXml.QDomDocument.createComment(), and PySide.QtXml.QDomDocument.createAttribute().

    The entire content of the document is set with PySide.QtXml.QDomDocument.setContent() . This function parses the string it is passed as an XML document and creates the DOM tree that represents the document. The root element is available using PySide.QtXml.QDomDocument.documentElement() . The textual representation of the document can be obtained using PySide.QtXml.QDomDocument.toString() .

    It is possible to insert a node from another document into the document using PySide.QtXml.QDomDocument.importNode() .

    You can obtain a list of all the elements that have a particular tag with PySide.QtXml.QDomDocument.elementsByTagName() or with PySide.QtXml.QDomDocument.elementsByTagNameNS() .

    For further information about the Document Object Model see the Document Object Model (DOM) Level 1 and Level 2 Core Specifications (http://www.w3.org/DOM/DOMTR)
    

  **QDomNode**
  http://pyside.github.io/docs/pyside/PySide/QtXml/QDomNode.html#
    The PySide.QtXml.QDomNode class is the base class for all the nodes in a DOM tree. Many functions in the DOM return a PySide.QtXml.QDomNode. You can find out the type of a node using PySide.QtXml.QDomNode.isAttr() , PySide.QtXml.QDomNode.isDocument() , PySide.QtXml.QDomNode.isDocumentType() , PySide.QtXml.QDomNode.isElement() , PySide.QtXml.QDomNode.isEntityReference() , PySide.QtXml.QDomNode.isText() , 

    A PySide.QtXml.QDomNode can be converted into one of its subclasses using PySide.QtXml.QDomNode.toAttr() , PySide.QtXml.QDomNode.toDocument() , PySide.QtXml.QDomNode.toDocumentType() , PySide.QtXml.QDomNode.toElement(), PySide.QtXml.QDomNode.toText() , PySide.QtXml.QDomNode.toEntity() , PySide.QtXml.QDomNode.toNotation(). You can convert a node to a null node with PySide.QtXml.QDomNode.clear() .

    Copies of the PySide.QtXml.QDomNode class share their data using explicit sharing. This means that modifying one node will change all copies. This is especially useful in combination with functions which return a PySide.QtXml.QDomNode , e.g. PySide.QtXml.QDomNode.firstChild() . You can make an independent copy of the node with PySide.QtXml.QDomNode.cloneNode() .

    A PySide.QtXml.QDomNode can be null, much like a null pointer. Creating a copy of a null node results in another null node. It is not possible to modify a null node, but it is possible to assign another, possibly non-null node to it. In this case, the copy of the null node will remain null. You can check if a PySide.QtXml.QDomNode is null by calling PySide.QtXml.QDomNode.isNull() . The empty constructor of a PySide.QtXml.QDomNode (or any of the derived classes) creates a null node.

    Nodes are inserted with PySide.QtXml.QDomNode.insertBefore() , PySide.QtXml.QDomNode.insertAfter() or PySide.QtXml.QDomNode.appendChild() . You can replace one node with another using PySide.QtXml.QDomNode.replaceChild() and remove a node with PySide.QtXml.QDomNode.removeChild() .

    To traverse nodes use PySide.QtXml.QDomNode.firstChild() to get a node’s first child (if any), and PySide.QtXml.QDomNode.nextSibling() to traverse. PySide.QtXml.QDomNode also provides PySide.QtXml.QDomNode.lastChild() , and PySide.QtXml.QDomNode.parentNode() . To find the first child node with a particular node name use PySide.QtXml.QDomNode.namedItem() .

    To find out if a node has children use PySide.QtXml.QDomNode.hasChildNodes() and to get a list of all of a node’s children use PySide.QtXml.QDomNode.childNodes() .

    The node’s name and value (the meaning of which varies depending on its type) is returned by PySide.QtXml.QDomNode.nodeName() and PySide.QtXml.QDomNode.nodeValue() respectively. The node’s type is returned by PySide.QtXml.QDomNode.nodeType() . The node’s value can be set with PySide.QtXml.QDomNode.setNodeValue() .

    The document to which the node belongs is returned by PySide.QtXml.QDomNode.ownerDocument() .

    PySide.QtXml.QDomElement nodes have attributes which can be retrieved with PySide.QtXml.QDomNode.attributes() .

    You can write the XML representation of the node to a text stream with PySide.QtXml.QDomNode.save() .

    The following example looks for the first element in an XML document and prints the names of all the elements that are its direct children:
        d = QDomDocument()
        d.setContent(someXML)
        n = d.firstChild()
        while !n.isNull():
            if n.isElement():
                e = n.toElement()
                print "Element name: %s" % e.tagName()
                break
            n = n.nextSibling()

 
  
  **QXmlSimpleReader**
  http://srinikom.github.io/pyside-docs/PySide/QtXml/QXmlSimpleReader.html

    The PySide.QtXml.QXmlSimpleReader class provides an implementation of a simple XML parser. This XML reader is suitable for a wide range of applications. It is able to parse well-formed XML and can report the namespaces of elements to a content handler.

    The easiest pattern of use for this class is to create a reader instance, define an input source, specify the handlers to be used by the reader, and parse the data.    For example, we could use a PySide.QtCore.QFile to supply the input. Here, we create a reader, and define an input source to be used by the reader:

        xmlReader = QXmlSimpleReader()
        source = QXmlInputSource(filename)

    A handler lets us perform actions when the reader encounters certain types of content, or if errors in the input are found. The reader must be told which handler to use for each type of event. For many common applications, we can create a custom handler by subclassing PySide.QtXml.QXmlDefaultHandler , and use this to handle both error and content events:

        handler = Handler()
        xmlReader.setContentHandler(handler)
        xmlReader.setErrorHandler(handler)

    If you don’t set at least the content and error handlers, the parser will fall back on its default behavior—and will do nothing.

    The most convenient way to handle the input is to read it in a single pass using the PySide.QtXml.QXmlSimpleReader.parse() function with an argument that specifies the input source:

        ok = xmlReader.parse(source)

        if not ok:
            print "Parsing failed."

    If you can’t parse the entire input in one go (for example, it is huge, or is being delivered over a network connection), data can be fed to the parser in pieces.