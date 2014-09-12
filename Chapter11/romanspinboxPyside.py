# -*- coding: utf-8 -*-
"""
romanspinboxPyside.py
Annotated PySide port of romanspinbox.py from Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Subclassing QSpinbox to make a spinbox that displays roman numerals instead of 
decimal-based numbers.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

import sys
from PySide import QtGui, QtCore


def romanFromInt(integer):
    """
    Code taken from Raymond Hettinger's code in Victor Yang's "Decimal
    to Roman Numerals" recipe in the Python Cookbook.

    >>> r = [romanFromInt(x) for x in range(1, 4000)]
    >>> i = [intFromRoman(x) for x in r]
    >>> i == [x for x in range(1, 4000)]
    True
    """
    coding = zip(
        [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1], 
        ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V",
         "IV", "I"])
    if integer <= 0 or integer >= 4000 or int(integer) != integer:
        raise ValueError("expecting an integer between 1 and 3999")
    result = []
    for decimal, roman in coding:
        while integer >= decimal:
            result.append(roman)
            integer -= decimal
    return "".join(result)


def intFromRoman(roman):
    """
    Code taken from Paul Winkler's "Roman Numerals" recipe in the Python
    Cookbook.
    """
    roman = roman.upper()
    coding = (("M",  1000, 3), ("CM", 900, 1), ("D",  500, 1),
              ("CD", 400, 1), ("C",  100, 3), ("XC", 90, 1),
              ("L",  50, 1), ("XL", 40, 1), ("X",  10, 3),
              ("IX", 9, 1), ("V",  5, 1),  ("IV", 4, 1), ("I",  1, 3))
    integer, index = 0, 0
    for numeral, value, maxrepeat in coding:
        count = 0
        while roman[index: index +len(numeral)] == numeral:
            count += 1
            if count > maxrepeat:
                raise ValueError, "not a valid roman number: {0}".format(
                        roman)
            integer += value
            index += len(numeral)
    if index != len(roman):
        raise ValueError, "not a valid roman number: {0}".format(roman)
    return integer


# Regex adapted from Mark Pilgrim's "Dive Into Python" book
class RomanSpinBox(QtGui.QSpinBox):

    def __init__(self, parent=None):
        QtGui.QSpinBox.__init__(self, parent)
        regex = QtCore.QRegExp(r"^M?M?M?(?:CM|CD|D?C?C?C?)"
                        r"(?:XC|XL|L?X?X?X?)(?:IX|IV|V?I?I?I?)$")
        regex.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.validator = QtGui.QRegExpValidator(regex, self)
        self.setRange(1, 3999)
        self.lineEdit().textEdited.connect(self.fixCase)

    #qspinbox has a lineEdit property to access contents make sure roman numerals are uppercase
    def fixCase(self, text):
        #print "text, type:\n", text, "," , type(text)
        self.lineEdit().setText(text.upper())

    #when subclassing spinbox, we need to implement validate, valueFromText, and textFromValue

    #Ensures user enters a valid number, won't even let them enter invalid one
    #Text is individual character, position is its position in string
    def validate(self, text, pos):
        #print "validate text, pos:\n", text, ",", pos
        return self.validator.validate(text, pos)

    #When user enters text, convert to integer, as spinbox represents it as an integer
    def valueFromText(self, text):
        #print "valueFromText, text: ", text
        return intFromRoman(unicode(text))

    #Used to text for box when integer in spinbox changes from hitting spinbox inc/decrement
    def textFromValue(self, value):
        #print "getting text from value...value: ", value
        return romanFromInt(value)


if __name__ == "__main__":
    
    def report(value):
        print("{0:4d} {1}".format(value, romanFromInt(value)))

    app = QtGui.QApplication(sys.argv)
    spinbox = RomanSpinBox()
    spinbox.show()
    spinbox.resize(150,40)
    spinbox.setWindowTitle("Roman")
    spinbox.valueChanged.connect(report)
    app.exec_()
