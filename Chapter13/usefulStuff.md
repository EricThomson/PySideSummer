Things that might be useful when working through Chapter 13 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
Printing with Qt
http://qt-project.org/doc/qt-4.8/printing.html


#Useful Documentation
##QTextEdit
https://github.io/docs/pyside/PySide/QtGui/QTextEdit.html

	See Chapter 9 usefulStuff.md.


##QTextDocument
https://github.io/docs/pyside/PySide/QtGui/QTextDocument.html
	The QtGui.QTextDocument class holds formatted text that can be viewed and edited using a QtGui.QTextEdit.

	QtGui.QTextDocument is a container for structured rich text documents, providing support for styled text and various types of document elements, such as lists, tables, frames, and images. They can be created for use in a QtGui.QTextEdit, or used independently.

	A QtGui.QTextDocument can be edited programmatically using a QtGui.QTextCursor, and its contents can be examined by traversing the document structure. The entire document structure is stored as a hierarchy of document elements beneath the root frame, found with the QtGui.QTextDocument.rootFrame() function. Alternatively, if you just want to iterate over the textual contents of the document you can use QtGui.QTextDocument.begin(), QtGui.QTextDocument.end(), and QtGui.QTextDocument.findBlock() to retrieve text blocks that you can examine and iterate over.

	The layout of a document is determined by the QtGui.QTextDocument.documentLayout() ; you can create your own QtGui.QAbstractTextDocumentLayout subclass and set it using QtGui.QTextDocument.setDocumentLayout() if you want to use your own layout logic. The document’s title and other meta-information can be obtained by calling the QtGui.QTextDocument.metaInformation() function. For documents that are exposed to users through the QtGui.QTextEdit class, the document title is also available via the QTextEdit.documentTitle() function.

	The QtGui.QTextDocument.toPlainText() and QtGui.QTextDocument.toHtml() convenience functions allow you to retrieve the contents of the document as plain text and HTML. The document’s text can be searched using the QtGui.QTextDocument.find() functions.

	Undo/redo of operations performed on the document can be controlled using the QtGui.QTextDocument.setUndoRedoEnabled() function. The undo/redo system can be controlled by an editor widget through the QtGui.QTextDocument.undo() and QtGui.QTextDocument.redo() slots; the document also provides QtGui.QTextDocument.contentsChanged(), QtGui.QTextDocument.undoAvailable(), and QtGui.QTextDocument.redoAvailable() signals that inform connected editor widgets about the state of the undo/redo system. The following are the undo/redo operations of a QtGui.QTextDocument :

		-Insertion or removal of characters. A sequence of insertions or removals within the same text block are regarded as a single undo/redo operation.
		-Insertion or removal of text blocks. Sequences of insertion or removals in a single operation (e.g., by selecting and then deleting text) are regarded as a single undo/redo operation.
		-Text character format changes.
		-Text block format changes.
		-Text block group format changes.


##QSyntaxHighlighter
http://srinikom.github.io/pyside-docs/PySide/QtGui/QSyntaxHighlighter.html

	The QtGui.QSyntaxHighlighter class allows you to define syntax highlighting rules, and in addition you can use the class to query a document’s current formatting or user data.

	The QtGui.QSyntaxHighlighter class is a base class for implementing QtGui.QTextEdit syntax highlighters. A syntax highligher automatically highlights parts of the text in a QtGui.QTextEdit, or more generally in a QtGui.QTextDocument. Syntax highlighters are often used when the user is entering text in a specific format (for example source code) and help the user to read the text and identify syntax errors.

	To provide your own syntax highlighting, you must subclass QtGui.QSyntaxHighlighter and reimplement QtGui.QSyntaxHighlighter.highlightBlock().

	When you create an instance of your QtGui.QSyntaxHighlighter subclass, pass it the QtGui.QTextEdit or QtGui.QTextDocument that you want the syntax highlighting to be applied to. For example:

		editor = QTextEdit()
		highlighter = MyHighlighter(editor.document())

	After this your QtGui.QSyntaxHighlighter.highlightBlock() function will be called automatically whenever necessary. Use your QtGui.QSyntaxHighlighter.highlightBlock() function to apply formatting (e.g. setting the font and color) to the text that is passed to it. QtGui.QSyntaxHighlighter provides the QtGui.QSyntaxHighlighter.setFormat() function which applies a given QtGui.QTextCharFormat on the current text block.