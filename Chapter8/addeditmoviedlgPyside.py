# -*- coding: utf-8 -*-
"""
addeditmoviedlgPyside.py
Annotated PySide adaptation of addeditmoviedlg.py from Chapter 8
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Imports dialog ui_addedetmoviedlgPyside to build dialog for adding/editing movies

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
from PySide import QtGui, QtCore
import moviedataPyside
import ui_addeditmoviedlgPyside


class AddEditMovieDlg(QtGui.QDialog, ui_addeditmoviedlgPyside.Ui_AddEditMovieDlg):

    def __init__(self, movies, movie=None, parent=None):
        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)

        self.movies = movies
        self.movie = movie
        self.acquiredDateEdit.setDisplayFormat(moviedataPyside.DATEFORMAT)
        if movie is not None:
            self.titleLineEdit.setText(movie.title)
            self.yearSpinBox.setValue(movie.year)
            self.minutesSpinBox.setValue(movie.minutes)
            self.acquiredDateEdit.setDate(movie.acquired)
            self.acquiredDateEdit.setEnabled(False)
            self.notesTextEdit.setPlainText(movie.notes)
            self.notesTextEdit.setFocus()
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText(
                                  "&Accept")
            self.setWindowTitle("My Movies - Edit Movie")
        else:
            today = QtCore.QDate.currentDate()
            self.acquiredDateEdit.setDateRange(today.addDays(-5),
                                               today)
            self.acquiredDateEdit.setDate(today)
            self.titleLineEdit.setFocus()
        self.on_titleLineEdit_textEdited("")


    @QtCore.Slot(str)
    def on_titleLineEdit_textEdited(self, text):
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(bool(self.titleLineEdit.text()))


    def accept(self):
        title = self.titleLineEdit.text()
        year = self.yearSpinBox.value()
        minutes = self.minutesSpinBox.value()
        notes = self.notesTextEdit.toPlainText()
        if self.movie is None:
            acquired = self.acquiredDateEdit.date()
            self.movie = moviedataPyside.Movie(title, year, minutes, acquired, notes)

            if self.movies == 27705:  #just for the test below...otherwise will get an error
                print "Test success"
            else:
                self.movies.add(self.movie)
                
        else:
            self.movies.updateMovie(self.movie, title, year, minutes, notes)
        QtGui.QDialog.accept(self)
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    form = AddEditMovieDlg(27705)
    form.show()
    app.exec_()

