#PySide Summer Chapter 15 (Databases)
PySide translation of files in Chapter 15 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). Also see `usefulStuff.md` for helpful links and excerpts from the PySide documentation.

##Notes about translation of Chapter 15

Translating his Qt file:
1. To get the database to open in all of the programs: 
    import site #at start of program
And then, before the line `QtSql.QSqlDatabase.addDatabase("QSQLITE")`:
    site_pack_path = site.getsitepackages()[1] 
    QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))
I frankly don't really understand why, it is a hack from Stack Overflow:
http://stackoverflow.com/questions/23312446/pyside-qtsql-cannot-load-database-drivers   
 
2. Don't use pyside version to replace pyqt version there, probably need to use 'qt verion'

3. Needed to replace:

        #following needed to be broken up #Eric
        #self.assetView.selectionModel().currentRowChanged.connect(self.assetChanged)
        smodel = self.assetView.selectionModel()
        print "seleciton model connection"
        smodel.currentRowChanged.connect(self.assetChanged)

This seems to be a bug in pyside. It is discussed here:
https://bugreports.qt-project.org/browse/PYSIDE-79
As of 11/10/14, it has not been fixed.

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
