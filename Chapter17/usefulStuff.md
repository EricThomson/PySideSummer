Things that I found useful when working through Chapter 17 of Rapid GUI Programming by Summerfield.
Part of Summer repository (https://github.com/EricThomson/Summer)


#Useful links
##Web site to get translations, e.g., English to French:
http://www.microsoft.com/language/en-us/Search.aspx?sString=lock&langID=fr-fr

##Qt Linguist Manual
http://qt-project.org/doc/qt-4.8/linguist-manual.html

##Internationalization with Qt
http://qt-project.org/doc/qt-4.8/internationalization.html

 
#Useful Documentation
##QtGui.QTextBrowser
http://srinikom.github.io/-docs//QtGui/QTextBrowser.html

    The .QtGui.QTextBrowser class provides a rich text browser with hypertext navigation.

    This class extends .QtGui.QTextEdit (in read-only mode), adding some navigation functionality so that users can follow links in hypertext documents. If you want to provide your users with an editable rich text editor, use .QtGui.QTextEdit. If you want a text browser without hypertext navigation use .QtGui.QTextEdit, and use QTextEdit.setReadOnly() to disable editing. If you just need to display a small piece of rich text use .QtGui.QLabel.

    ###Document Source and Contents

    The contents of .QtGui.QTextEdit are set with .QtGui.QTextEdit.setHtml() or .QtGui.QTextEdit.setPlainText(), but .QtGui.QTextBrowser also implements the .QtGui.QTextBrowser.setSource() function, making it possible to use a named document as the source text. The name is looked up in a list of search paths and in the directory of the current document factory.

    If a document name ends with an anchor (for example, “#anchor" ), the text browser automatically scrolls to that position (using .QtGui.QTextEdit.scrollToAnchor() ). When the user clicks on a hyperlink, the browser will call .QtGui.QTextBrowser.setSource() itself with the link’s href value as argument. You can track the current source by connecting to the .QtGui.QTextBrowser.sourceChanged() signal.

    ###Navigation

    .QtGui.QTextBrowser provides .QtGui.QTextBrowser.backward() and .QtGui.QTextBrowser.forward() slots which you can use to implement Back and Forward buttons. The .QtGui.QTextBrowser.home() slot sets the text to the very first document displayed. The .QtGui.QTextBrowser.anchorClicked() signal is emitted when the user clicks an anchor. To override the default navigation behavior of the browser, call the .QtGui.QTextBrowser.setSource() function to supply new document text in a slot connected to this signal.

    If you want to load documents stored in the Qt resource system use qrc as the scheme in the URL to load. For example, for the document resource path :/docs/index.html use qrc:/docs/index.html as the URL with .QtGui.QTextBrowser.setSource().
    

##QtCore.QTranslator
http://srinikom.github.io/pyside-docs/PySide/QtCore/QTranslator.html

    The PySide.QtCore.QTranslator class provides internationalization support for text output.

    An object of this class contains a set of translations from a source language to a target language. PySide.QtCore.QTranslator provides functions to look up translations in a translation file. Translation files are created using Qt Linguist.

    The most common use of PySide.QtCore.QTranslator is to: load a translation file, install it using QApplication.installTranslator() , and use it via QObject.tr() . Here’s the main() function from the `Hello tr()` example that comes with pyside:

        def main(args):
            app = QApplication(args)
            translator = QTranslator()
            translator.load("hellotr_la")
            app.installTranslator(translator)
            hello = QPushButton(QPushButton.tr("Hello world!"))
            hello.resize(100, 30)
            hello.show()
            return app.exec_()

    Note that the translator must be created before the application’s widgets.

    Most applications will never need to do anything else with this class. The other functions provided by this class are useful for applications that work on translator files.

    ###Looking up Translations
    It is possible to look up a translation using PySide.QtCore.QTranslator.translate() (as tr() and QApplication.translate() do). The PySide.QtCore.QTranslator.translate() function takes up to three parameters:
        The context - usually the class name for the tr() caller.
        The source text - usually the argument to tr() .
        The disambiguation - an optional string that helps disambiguate different uses of the same text in the same context.
    For example, the “Cancel” in a dialog might have “Anuluj” when the program runs in Polish (in this case the source text would be “Cancel”). The context would (normally) be the dialog’s class name; there would normally be no comment, and the translated text would be “Anuluj”.

    But it’s not always so simple. The Spanish version of a printer dialog with settings for two-sided printing and binding would probably require both “Activado” and “Activada” as translations for “Enabled”. In this case the source text would be “Enabled” in both cases, and the context would be the dialog’s class name, but the two items would have disambiguations such as “two-sided printing” for one and “binding” for the other. The disambiguation enables the translator to choose the appropriate gender for the Spanish version, and enables Qt to distinguish between translations.

    ###Using Multiple Translations

    Multiple translation files can be installed in an application. Translations are searched for in the reverse order in which they were installed, so the most recently installed translation file is searched for translations first and the earliest translation file is searched last. The search stops as soon as a translation containing a matching string is found.

    This mechanism makes it possible for a specific translation to be “selected” or given priority over the others; simply uninstall the translator from the application by passing it to the QApplication.removeTranslator() function and reinstall it with QApplication.installTranslator() . It will then be the first translation to be searched for matching strings.