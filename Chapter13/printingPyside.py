# -*- coding: utf-8 -*-
"""
printingPyside.py
Annotated PySide port of printing.pyw from Chapter 13
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Notes on translation: 

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
import math
import sys
from PySide import QtGui, QtCore
from xml.sax.saxutils import escape as escape
import resource_rc


DATE_FORMAT = "MMM d, yyyy"


class Statement(object):

    def __init__(self, company, contact, address):
        self.company = company
        self.contact = contact
        self.address = address
        self.transactions = [] # List of (QtCore.QDate, float) two-tuples

    def balance(self):
        return sum([amount for date, amount in self.transactions])


class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.printer = QtGui.QPrinter()
        self.printer.setPageSize(QtGui.QPrinter.Letter)
        self.generateFakeStatements()
        self.table = QtGui.QTableWidget()
        self.populateTable()

        cursorButton = QtGui.QPushButton("Print via Q&Cursor")
        htmlButton = QtGui.QPushButton("Print via &HTML")
        painterButton = QtGui.QPushButton("Print via Q&Painter")
        quitButton = QtGui.QPushButton("&Quit")

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(cursorButton)
        buttonLayout.addWidget(htmlButton)
        buttonLayout.addWidget(painterButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        cursorButton.clicked.connect(self.printViaQCursor)
        htmlButton.clicked.connect(self.printViaHtml)
        painterButton.clicked.connect(self.printViaQPainter)
        quitButton.clicked.connect(self.accept)

        self.setWindowTitle("Printing")


    def generateFakeStatements(self):
        self.statements = []
        statement = Statement("Consality", "Ms S. Royal",
                "234 Rue Saint Hyacinthe, 750201, Paris")
        statement.transactions.append((QtCore.QDate(2007, 8, 11), 2342))
        statement.transactions.append((QtCore.QDate(2007, 9, 10), 2342))
        statement.transactions.append((QtCore.QDate(2007, 10, 9), 2352))
        statement.transactions.append((QtCore.QDate(2007, 10, 17), -1500))
        statement.transactions.append((QtCore.QDate(2007, 11, 12), 2352))
        statement.transactions.append((QtCore.QDate(2007, 12, 10), 2352))
        statement.transactions.append((QtCore.QDate(2007, 12, 20), -7500))
        statement.transactions.append((QtCore.QDate(2007, 12, 20), 250))
        statement.transactions.append((QtCore.QDate(2008, 1, 10), 2362))
        self.statements.append(statement)

        statement = Statement("Demamitur Plc", "Mr G. Brown",
                "14 Tall Towers, Tower Hamlets, London, WC1 3BX")
        statement.transactions.append((QtCore.QDate(2007, 5, 21), 871))
        statement.transactions.append((QtCore.QDate(2007, 6, 20), 542))
        statement.transactions.append((QtCore.QDate(2007, 7, 20), 1123))
        statement.transactions.append((QtCore.QDate(2007, 7, 20), -1928))
        statement.transactions.append((QtCore.QDate(2007, 8, 13), -214))
        statement.transactions.append((QtCore.QDate(2007, 9, 15), -3924))
        statement.transactions.append((QtCore.QDate(2007, 9, 15), 2712))
        statement.transactions.append((QtCore.QDate(2007, 9, 15), -273))
        #statement.transactions.append((QtCore.QDate(2007, 11, 8), -728))
        #statement.transactions.append((QtCore.QDate(2008, 2, 7), 228))
        #statement.transactions.append((QtCore.QDate(2008, 3, 13), -508))
        #statement.transactions.append((QtCore.QDate(2008, 3, 22), -2481))
        #statement.transactions.append((QtCore.QDate(2008, 4, 5), 195))
        self.statements.append(statement)


    def populateTable(self):
        headers = ["Company", "Contact", "Address", "Balance"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.statements))
        for row, statement in enumerate(self.statements):
            self.table.setItem(row, 0,
                    QtGui.QTableWidgetItem(statement.company))
            self.table.setItem(row, 1,
                    QtGui.QTableWidgetItem(statement.contact))
            self.table.setItem(row, 2,
                    QtGui.QTableWidgetItem(statement.address))
            item = QtGui.QTableWidgetItem("$ {:,.2f}".format(
                                    statement.balance()))
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.table.setItem(row, 3, item)
        self.table.resizeColumnsToContents()


    def printViaHtml(self):
        html = ""
        for statement in self.statements:
            date = QtCore.QDate.currentDate().toString(DATE_FORMAT)
            address = escape(statement.address).replace(",", "<br>")
            contact = escape(statement.contact)
            balance = statement.balance()
            html += ("<p align=right><img src=':/logo.png'></p>"
                     "<p align=right>Greasy Hands Ltd."
                     "<br>New Lombard Street"
                     "<br>London<br>WC13 4PX<br>{0}</p>"
                     "<p>{1}</p><p>Dear {2},</p>"
                     "<p>The balance of your account is {3}.").format(
                     date, address, contact, "$ {:,.2f}".format(balance))
            if balance < 0:
                html += (" <p><font color=red><b>Please remit the "
                         "amount owing immediately.</b></font>")
            else:
                html += (" We are delighted to have done business "
                         "with you.")
            html += ("</p><p>&nbsp;</p><p>"
                     "<table border=1 cellpadding=2 "
                     "cellspacing=2><tr><td colspan=3>"
                     "Transactions</td></tr>")
            for date, amount in statement.transactions:
                color, status = "black", "Credit"
                if amount < 0:
                    color, status = "red", "Debit"
                html += ("<tr><td align=right>{0}</td>"
                         "<td>{1}</td><td align=right>"
                         "<font color={2}>{3}</font></td></tr>".format(
                         date.toString(DATE_FORMAT), status, color,
                         "$ {:,.2f}".format(abs(amount))))
            html += ("</table></p><p style='page-break-after:always;'>"
                     "We hope to continue doing "
                     "business with you,<br>Yours sincerely,"
                     "<br><br>K.&nbsp;Longrey, Manager</p>")
        dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QtGui.QTextDocument()
            document.setHtml(html)
            document.print_(self.printer)


    def printViaQCursor(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return
        logo = QtGui.QPixmap(":/logo.png")
        headFormat = QtGui.QTextBlockFormat()
        headFormat.setAlignment(QtCore.Qt.AlignLeft)
        headFormat.setTextIndent(
                self.printer.pageRect().width() - logo.width() - 216)
        bodyFormat = QtGui.QTextBlockFormat()
        bodyFormat.setAlignment(QtCore.Qt.AlignJustify)
        lastParaBodyFormat = QtGui.QTextBlockFormat(bodyFormat)
        lastParaBodyFormat.setPageBreakPolicy(
                QtGui.QTextFormat.PageBreak_AlwaysAfter)
        rightBodyFormat = QtGui.QTextBlockFormat()
        rightBodyFormat.setAlignment(QtCore.Qt.AlignRight)
        headCharFormat = QtGui.QTextCharFormat()
        headCharFormat.setFont(QtGui.QFont("Helvetica", 10))
        bodyCharFormat = QtGui.QTextCharFormat()
        bodyCharFormat.setFont(QtGui.QFont("Times", 11))
        redBodyCharFormat = QtGui.QTextCharFormat(bodyCharFormat)
        redBodyCharFormat.setForeground(QtCore.Qt.red)
        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(2)
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        mainFrame = cursor.currentFrame()
        page = 1
        for statement in self.statements:
            cursor.insertBlock(headFormat, headCharFormat)
            cursor.insertImage(":/logo.png")
            for text in ("Greasy Hands Ltd.", "New Lombard Street",
                         "London", "WC13 4PX",
                         QtCore.QDate.currentDate().toString(DATE_FORMAT)):
                cursor.insertBlock(headFormat, headCharFormat)
                cursor.insertText(text)
            for line in statement.address.split(", "):
                cursor.insertBlock(bodyFormat, bodyCharFormat)
                cursor.insertText(line)
            cursor.insertBlock(bodyFormat)
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("Dear {},".format(statement.contact))
            cursor.insertBlock(bodyFormat)
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            balance = statement.balance()
            cursor.insertText("The balance of your account is $ {:,.2f}."
                    .format(balance))
            if balance < 0:
                cursor.insertBlock(bodyFormat, redBodyCharFormat)
                cursor.insertText("Please remit the amount owing "
                                  "immediately.")
            else:
                cursor.insertBlock(bodyFormat, bodyCharFormat)
                cursor.insertText("We are delighted to have done "
                                  "business with you.")
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("Transactions:")
            table = cursor.insertTable(len(statement.transactions), 3,
                                       tableFormat)
            row = 0
            for date, amount in statement.transactions:
                cellCursor = table.cellAt(row, 0).firstCursorPosition()
                cellCursor.setBlockFormat(rightBodyFormat)
                cellCursor.insertText(date.toString(DATE_FORMAT),
                                      bodyCharFormat)
                cellCursor = table.cellAt(row, 1).firstCursorPosition()
                if amount > 0:
                    cellCursor.insertText("Credit", bodyCharFormat)
                else:
                    cellCursor.insertText("Debit", bodyCharFormat)
                cellCursor = table.cellAt(row, 2).firstCursorPosition()
                cellCursor.setBlockFormat(rightBodyFormat)
                format = bodyCharFormat
                if amount < 0:
                    format = redBodyCharFormat
                cellCursor.insertText("$ {:,.2f}".format(amount), format)
                row += 1
            cursor.setPosition(mainFrame.lastPosition())
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("We hope to continue doing business "
                              "with you,")
            cursor.insertBlock(bodyFormat, bodyCharFormat)
            cursor.insertText("Yours sincerely")
            cursor.insertBlock(bodyFormat)
            if page == len(self.statements):
                cursor.insertBlock(bodyFormat, bodyCharFormat)
            else:
                cursor.insertBlock(lastParaBodyFormat, bodyCharFormat)
            cursor.insertText("K. Longrey, Manager")
            page += 1
        document.print_(self.printer)


    def printViaQPainter(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return
        LeftMargin = 72
        sansFont = QtGui.QFont("Helvetica", 10)
        sansLineHeight = QtGui.QFontMetrics(sansFont).height()
        serifFont = QtGui.QFont("Times", 11)
        fm = QtGui.QFontMetrics(serifFont)
        DateWidth = fm.width(" September 99, 2999 ")
        CreditWidth = fm.width(" Credit ")
        AmountWidth = fm.width(" W999999.99 ")
        serifLineHeight = fm.height()
        logo = QtGui.QPixmap(":/logo.png")
        painter = QtGui.QPainter(self.printer)
        pageRect = self.printer.pageRect()
        page = 1
        for statement in self.statements:
            painter.save()
            y = 0
            x = pageRect.width() - logo.width() - LeftMargin
            painter.drawPixmap(x, 0, logo)
            y += logo.height() + sansLineHeight
            painter.setFont(sansFont)
            painter.drawText(x, y, "Greasy Hands Ltd.")
            y += sansLineHeight
            painter.drawText(x, y, "New Lombard Street")
            y += sansLineHeight
            painter.drawText(x, y, "London")
            y += sansLineHeight
            painter.drawText(x, y, "WC13 4PX")
            y += sansLineHeight
            painter.drawText(x, y,
                    QtCore.QDate.currentDate().toString(DATE_FORMAT))
            y += sansLineHeight
            painter.setFont(serifFont)
            x = LeftMargin
            for line in statement.address.split(", "):
                painter.drawText(x, y, line)
                y += serifLineHeight
            y += serifLineHeight
            painter.drawText(x, y, "Dear {},".format(statement.contact))
            y += serifLineHeight
            balance = statement.balance()
            painter.drawText(x, y, "The balance of your "
                    "account is $ {:,.2f}".format(balance))
            y += serifLineHeight
            if balance < 0:
                painter.setPen(QtCore.Qt.red)
                text = "Please remit the amount owing immediately."
            else:
                text = ("We are delighted to have done business "
                        "with you.")
            painter.drawText(x, y, text)
            painter.setPen(QtCore.Qt.black)
            y += int(serifLineHeight * 1.5)
            painter.drawText(x, y, "Transactions:")
            y += serifLineHeight
            option = QtGui.QTextOption(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            for date, amount in statement.transactions:
                x = LeftMargin
                h = int(fm.height() * 1.3)
                painter.drawRect(x, y, DateWidth, h)
                painter.drawText(
                        QtCore.QRectF(x + 3, y + 3, DateWidth - 6, h - 6),
                        date.toString(DATE_FORMAT), option)
                x += DateWidth
                painter.drawRect(x, y, CreditWidth, h)
                text = "Credit"
                if amount < 0:
                    text = "Debit"
                painter.drawText(
                        QtCore.QRectF(x + 3, y + 3, CreditWidth - 6, h - 6),
                        text, option)
                x += CreditWidth
                painter.drawRect(x, y, AmountWidth, h)
                if amount < 0:
                    painter.setPen(QtCore.Qt.red)
                painter.drawText(
                        QtCore.QRectF(x + 3, y + 3, AmountWidth - 6, h - 6),
                        "$ {:,.2f}".format(amount), option)
                painter.setPen(QtCore.Qt.black)
                y += h
            y += serifLineHeight
            x = LeftMargin
            painter.drawText(x, y, "We hope to continue doing "
                                   "business with you,")
            y += serifLineHeight
            painter.drawText(x, y, "Yours sincerely")
            y += serifLineHeight * 3
            painter.drawText(x, y, "K. Longrey, Manager")
            x = LeftMargin
            y = pageRect.height() - 72
            painter.drawLine(x, y, pageRect.width() - LeftMargin, y)
            y += 2
            font = QtGui.QFont("Helvetica", 9)
            font.setItalic(True)
            painter.setFont(font)
            option = QtGui.QTextOption(QtCore.Qt.AlignCenter)
            option.setWrapMode(QtGui.QTextOption.WordWrap)
            painter.drawText(
                    QtCore.QRectF(x, y, pageRect.width() - 2 * LeftMargin, 31),
                    "The contents of this letter are for information "
                    "only and do not form part of any contract.",
                    option)
            page += 1
            if page <= len(self.statements):
                self.printer.newPage()
            painter.restore()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()

