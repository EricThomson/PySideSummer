# -*- coding: utf-8 -*-
"""
waterqualityPyside.py
Annotated PySide port of waterquality.pyw from Chapter 16
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Requires waterdata.csv.gz

Provides two views of the same model. One standard text tableview (left-hand
splitter), and another more visual representation of the same data (right-
hand splitter).

To do:
1.  When does he actually get back to the 'setfocus' point he says he will get 
back to?

Notes on translation:
1. There is no 'contains' method. Replace with 'in'
    if "unicode" in face: #face.contains("unicode"):
2. Replace obsolete Qt.TextColorRole with Qt.ForegroundRole.
3. Unicode literals...from future...

4. be sure to add difference in signal for custom signals emitting to tutorial translation
notes-- see signalsSlotsRuminations.docx.
------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html

"""
from __future__ import unicode_literals  #for unicode characters in headerData

import gzip
import os
import platform
import sys
from PySide import QtGui, QtCore
        
(TIMESTAMP, TEMPERATURE, INLETFLOW, TURBIDITY, CONDUCTIVITY,
 COAGULATION, RAWPH, FLOCCULATEDPH) = range(8)

      
def displayRole(roleDict, role):
    recastRole = int(role)  #in case sent in like Qt.DisplayRole
    roleDescription = roleDict[recastRole]
    return roleDescription

def displayFlags(flagDict, flags = None):
    if not flags:
        return None
    else:
        flagDescriptions = []
        recastFlags = int(flags)  #all flags, cast to integer
        #print "Number of elements in dict: ", len(flagDict)
        for flagInd in range(len(flagDict)):
            flagVal = flagDict.keys()[flagInd]
            if recastFlags & flagVal:
                flagDescriptions.append(flagDict.values()[flagInd])
        return flagDescriptions
        
dataRoles = {0: 'DisplayRole', 1: 'DecorationRole', 2: 'EditRole', 3: 'ToolTipRole',\
            4: 'StatusTipRole', 5: 'WhatsThisRole', 6: 'FontRole', 7: 'TextAlignmentRole',\
            8: 'BackgroundRole', 9: 'ForegroundRole', 10: 'CheckStateRole', 13: 'SizeHintRole',\
            14: 'InitialSortOrderRole', 32: 'UserRole'}  

itemFlags = {0: 'NoItemFlags', 1: 'ItemIsSelectable', 2: 'ItemIsEditable', 4: 'ItemIsDragEnabled',\
             8: 'ItemIsDropEnabled', 16: 'ItemIsUserCheckable', 32: 'ItemIsEnabled', 64: 'ItemIsTriState'}

dropActionFlags ={0: 'IgnoreAction', 1: 'CopyAction', 2: 'MoveAction',\
                 4: 'LinkAction', 255: 'ActionMask', 32770: 'TargetMoveAction'}
                 
TIMESTAMPFORMAT = "yyyy-MM-dd hh:mm"


class MainForm(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        #Create model
        self.model = WaterQualityModel(os.path.join(
                os.path.dirname(__file__), "waterdata.csv.gz"))
                
        #Create standard text view of model
        self.tableView = QtGui.QTableView()
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setModel(self.model)
        
        #Pictorial view of model
        self.waterView = WaterQualityView()
        self.waterView.setModel(self.model)
        #Set up scroll area for custom view
        scrollArea = QtGui.QScrollArea()
        scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        scrollArea.setWidget(self.waterView) #inserts relevant widget into scrollview
        self.waterView.scrollarea = scrollArea

        #Layout of two views
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.tableView)
        splitter.addWidget(scrollArea)
        splitter.setSizes([600, 230])
        layout = QtGui.QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Water Quality Data")
        QtCore.QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor)) #hourglass while loading
        splash = QtGui.QLabel(self)
        pixmap = QtGui.QPixmap(os.path.join(os.path.dirname(__file__),
                "iss013-e-14802.jpg"))
        splash.setPixmap(pixmap)
        splash.setWindowFlags(QtCore.Qt.SplashScreen)
        splash.move(self.x() + ((self.width() - pixmap.width()) / 2),
                    self.y() + ((self.height() - pixmap.height()) / 2))
        splash.show()
        QtGui.QApplication.processEvents()
        try:
            self.model.load()
        except IOError as e:
            QtGui.QMessageBox.warning(self, "Water Quality - Error", e)
        else:
            self.tableView.resizeColumnsToContents()
        splash.close()
        QtGui.QApplication.processEvents()
        QtGui.QApplication.restoreOverrideCursor()
        

class WaterQualityModel(QtCore.QAbstractTableModel):
    'Custom model of water quality'
    def __init__(self, filename):
        super(WaterQualityModel, self).__init__()
        self.filename = filename
        self.results = []


    def load(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            self.results = []
            line_data = gzip.open(self.filename).read()
            for line in line_data.decode("utf-8").splitlines():
                parts = line.rstrip().split(",")
                date = QtCore.QDateTime.fromString(parts[0] + ":00",
                                            QtCore.Qt.ISODate)
                result = [date]
                for part in parts[1:]:
                    result.append(float(part))
                self.results.append(result)
        except (IOError, ValueError) as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            self.reset()
            if exception is not None:
                raise exception

    def data(self, index, role=QtCore.Qt.DisplayRole):
        #print "data role: ", displayRole(dataRoles, role)
        if (not index.isValid() or
            not (0 <= index.row() < len(self.results))):
            return None
        column = index.column()
        result = self.results[index.row()]
        if role == QtCore.Qt.DisplayRole:
            item = result[column]
            if column == TIMESTAMP:
                # TODO set time format
                item = item
            else:
                item = "{:.2f}".format(item)
            return item
        elif role == QtCore.Qt.TextAlignmentRole:
            if column != TIMESTAMP:
                return int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            return int(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        elif role == QtCore.Qt.ForegroundRole and column == INLETFLOW:
            if result[column] < 0:
                return QtGui.QColor(QtCore.Qt.red)
        elif (role == QtCore.Qt.ForegroundRole and
              column in (RAWPH, FLOCCULATEDPH)):
            ph = result[column]
            if ph < 7:
                return QtGui.QColor(QtCore.Qt.red)
            elif ph >= 8:
                return QtGui.QColor(QtCore.Qt.blue)
            else:
                return QtGui.QColor(QtCore.Qt.darkGreen)
        return None                
        
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        #print "header data role: ", displayRole(dataRoles, role)
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return int(QtCore.Qt.AlignCenter)
            return int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            if section == TIMESTAMP:
                return "Timestamp"
            elif section == TEMPERATURE:
                return "\u00B0" + "C"
            elif section == INLETFLOW:
                return "Inflow"
            elif section == TURBIDITY:
                return "NTU"
            elif section == CONDUCTIVITY:
                return "\u03BCS/cm"
            elif section == COAGULATION:
                return "mg/L"
            elif section == RAWPH:
                return "Raw Ph"
            elif section == FLOCCULATEDPH:
                return "Floc Ph"
        return int(section + 1)

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.results)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 8


class WaterQualityView(QtGui.QWidget):
    'Custom pictorial view of water quality'
    FLOWCHARS = (unichr(0x21DC), unichr(0x21DD), unichr(0x21C9))
    
    clicked = QtCore.Signal(QtCore.QModelIndex)
    
    def __init__(self, parent=None):
        super(WaterQualityView, self).__init__(parent)
        self.scrollarea = None
        self.model = None
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.selectedRow = -1
        self.flowfont = self.font()
        size = self.font().pointSize()
        if platform.system() == "Windows":
            fontDb = QtGui.QFontDatabase()
            for face in [face.lower() for face in fontDb.families()]:
                #print "face, type(face):",face, ",", type(face)
                if "unicode" in face: #face.contains("unicode"):
                    self.flowfont = QtGui.QFont(face, size)
                    break
            else:
                self.flowfont = QtGui.QFont("symbol", size)
                WaterQualityView.FLOWCHARS = (chr(0xAC), chr(0xAE),chr(0xDE))
                print "Flowchars: ", WaterQualityView.FLOWCHARS

    #Set model on view, and then connect it to its dataChanged and modelReset
    #signals so the view can be resized to match its available data.
    def setModel(self, model):
        self.model = model
        self.model.dataChanged.connect(self.setNewSize)
        self.model.modelReset.connect(self.setNewSize)
        self.setNewSize()  #is this needed?


    def setNewSize(self):
        #print "new view set new size"
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()

    #is this necessary?
    def minimumSizeHint(self):
        #print "new view minimumsizehint"
        size = self.sizeHint()
        fm = QtGui.QFontMetrics(self.font())
        size.setHeight(fm.height() * 3)
        return size

    #seems to be necessary
    def sizeHint(self):
        #print "new view size hint"
        fm = QtGui.QFontMetrics(self.font())
        size = fm.height()
        return QtCore.QSize(fm.width("9999-99-99 99:99 ") + (size * 4),
                     (size / 4) + (size * self.model.rowCount()))


    def paintEvent(self, event):
        #print "Region/rect:\n", event.region(),"\n", event.rect(),"\n" #region different from rect..how?
        if self.model is None:
            return
        fm = QtGui.QFontMetrics(self.font())
        timestampWidth = fm.width("9999-99-99 99:99 ")
        size = fm.height()
        indicatorSize = int(size * 0.8)
        offset = int(1.5 * (size - indicatorSize))
        minY = event.rect().y()
        maxY = minY + event.rect().height() + size
        minY -= size
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        y = 0
        for row in range(self.model.rowCount()):
            x = 0
            if minY <= y <= maxY:
                painter.save()
                painter.setPen(self.palette().color(QtGui.QPalette.Text))
                if row == self.selectedRow:
                    painter.fillRect(x, y + (offset * 0.8),
                            self.width(), size, self.palette().highlight())
                    painter.setPen(self.palette().color(
                            QtGui.QPalette.HighlightedText))
                timestamp = self.model.data(
                        self.model.index(row, TIMESTAMP))
                painter.drawText(x, y + size,
                        timestamp.toString("yyyy-MM-dd hh:mm"))
                        
                #Temperature        
                x += timestampWidth
                temperature = float(self.model.data(
                        self.model.index(row, TEMPERATURE)))
                if temperature < 20:
                    color = QtGui.QColor(0, 0,
                            int(255 * (20 - temperature) / 20))
                elif temperature > 25:
                    color = QtGui.QColor(int(255 * temperature / 100), 0, 0)
                else:
                    color = QtGui.QColor(0, int(255 * temperature / 100), 0)
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                                    indicatorSize)
                                    
                #pH
                x += size
                rawPh = float(self.model.data(
                        self.model.index(row, RAWPH)))
                if rawPh < 7:
                    color = QtGui.QColor(int(255 * rawPh / 10), 0, 0)
                elif rawPh >= 8:
                    color = QtGui.QColor(0, 0, int(255 * rawPh / 10))
                else:
                    color = QtGui.QColor(0, int(255 * rawPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                                    indicatorSize)
                                    
                #flocculate depth
                x += size
                flocPh = float(self.model.data(
                        self.model.index(row, FLOCCULATEDPH)))
                if flocPh < 7:
                    color = QtGui.QColor(int(255 * flocPh / 10), 0, 0)
                elif flocPh >= 8:
                    color = QtGui.QColor(0, 0, int(255 * flocPh / 10))
                else:
                    color = QtGui.QColor(0, int(255 * flocPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                                    indicatorSize)
                                    
                painter.restore()
                painter.save()
                
                #Flow character check
                x += size
                flow = float(self.model.data(
                        self.model.index(row, INLETFLOW)))
                char = None
                if flow <= 0:
                    char = WaterQualityView.FLOWCHARS[0]
                elif flow < 3:
                    char = WaterQualityView.FLOWCHARS[1]
                elif flow > 5.5:
                    char = WaterQualityView.FLOWCHARS[2]
                if char is not None:
                    painter.setFont(self.flowfont)
                    painter.drawText(x, y + size, char)
                painter.restore()
            y += size
            if y > maxY:
                break


    def mousePressEvent(self, event):
        fm = QtGui.QFontMetrics(self.font())
        self.selectedRow = event.y() // fm.height()
        self.update()
        self.clicked.emit(self.model.index(self.selectedRow, 0))


    def keyPressEvent(self, event):
        if self.model is None:
            return
        row = -1
        if event.key() == QtCore.Qt.Key_Up:
            row = max(0, self.selectedRow - 1)
        elif event.key() == QtCore.Qt.Key_Down:
            row = min(self.selectedRow + 1, self.model.rowCount() - 1)
        if row != -1 and row != self.selectedRow:
            self.selectedRow = row
            if self.scrollarea is not None:
                fm = QtGui.QFontMetrics(self.font())
                y = fm.height() * self.selectedRow
                self.scrollarea.ensureVisible(0, y)
            self.update()
            self.clicked.emit(self.model.index(self.selectedRow, 0))
        else:
            QtGui.QWidget.keyPressEvent(self, event)


app = QtGui.QApplication(sys.argv)
form = MainForm()
form.resize(800, 620)

#pull flags for model
#dropActions = form.model.supportedDropActions()
#print "Drop action flags: ", displayFlags(dropActionFlags, dropActions )
#randIndex = form.model.index(2,2)
#randDataFlags = randIndex.flags()
#print randIndex, randDataFlags
#datFlagsList = displayFlags(itemFlags, randDataFlags)
#print "Data flags: ", datFlagsList
form.show()
app.exec_()

