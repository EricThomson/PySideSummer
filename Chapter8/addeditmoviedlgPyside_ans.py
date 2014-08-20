# -*- coding: utf-8 -*-
"""
addeditmoviedlgPyside_ans.py
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
import moviedataPyside_ans
import ui_addeditmoviedlg_ans


class AddEditMovieDlg(QtGui.QDialog, ui_addeditmoviedlg_ans.Ui_AddEditMovieDlg):

    def __init__(self, movies, movie=None, parent=None):
        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)

        self.movies = movies
        self.movie = movie
        self.acquiredDateEdit.setDisplayFormat(moviedataPyside_ans.DATEFORMAT)
        #How to display edit box
        if movie is not None:
            self.titleLineEdit.setText(movie.title)
            self.yearSpinBox.setValue(movie.year)
            self.minutesSpinBox.setValue(movie.minutes)
            self.acquiredDateEdit.setDate(movie.acquired)
            self.acquiredDateEdit.setEnabled(False)
            self.notesTextEdit.setPlainText(movie.notes)
            self.locationLineEdit.setText(movie.location)
            self.notesTextEdit.setFocus()
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText(
                                  "&Accept")
            self.setWindowTitle("My Movies - Edit Movie")
        else:
            today = QtCore.QDate.currentDate()
            self.acquiredDateEdit.setDateRange(today.addDays(-365),
                                               today)
            self.acquiredDateEdit.setDate(today)
            self.titleLineEdit.setFocus()
        self.on_titleLineEdit_textEdited("")

    #Enable OK button on button box when title is entered (and not deleted)
    @QtCore.Slot(str)
    def on_titleLineEdit_textEdited(self, text):
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(bool(self.titleLineEdit.text()))


    def accept(self):
        title = self.titleLineEdit.text()
        year = self.yearSpinBox.value()
        minutes = self.minutesSpinBox.value()
        notes = self.notesTextEdit.toPlainText()
        location=self.locationLineEdit.text()
        if self.movie is None:
            acquired = self.acquiredDateEdit.date()
            self.movie = moviedataPyside_ans.Movie(title, year, minutes, acquired, notes, location)
            if self.movies == 27705:  #just for the test below...otherwise will get an error
                print "Test success"
            else:
                self.movies.add(self.movie)
                
        else:
            self.movies.updateMovie(self.movie, title, year, minutes, notes, location)
        QtGui.QDialog.accept(self)
        

if __name__ == "__main__":
    #Primitive test to make sure GUI isn't breaking
    import sys
    app = QtGui.QApplication(sys.argv)  
    form = AddEditMovieDlg(27705)
    form.show()
    app.exec_()