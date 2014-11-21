#PySide Summer Chapter 15 (Databases)
PySide translation of files in Chapter 15 of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008). Also see `usefulStuff.md` for helpful links and excerpts from the PySide documentation.

##Notes about translation of Chapter 15
A few things.

1. To get the database to open in all of the programs: 

    import site 
    
 And then, before the line `QtSql.QSqlDatabase.addDatabase("QSQLITE")`:

	site_pack_path = site.getsitepackages()[1] 
	QtGui.QApplication.addLibraryPath('{0}\\PySide\\plugins'.format(site_pack_path))
    
2. Replace the single line:

        self.assetView.selectionModel().currentRowChanged.connect(self.assetChanged)
        
 With the two lines:

        selectionModel = self.assetView.selectionModel()
        selectionModel.currentRowChanged.connect(self.assetChanged)
        
 This seems to be due to a bug in PySide.

###Licensing and such
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
