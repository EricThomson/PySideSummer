# -*- coding: utf-8 -*-
"""
countersPyside.py

One solution to exercise in Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

He also has a solution at his site, which is probably better than mine.
----            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""

from PySide import QtGui, QtCore

class CounterMatrix(QtGui.QWidget):
       
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent=None)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding))                  
        self.setMinimumSize(self.minimumSizeHint())

        #location 
        self.highlighted=[1, 1]
        self.coordinates= [(i,j) for j in range(3) for i in range(3)]  #;print self.coordinates
        self.tritoggles=[0]*9 #stores state of things at each location
        
        #self.tritoggle some kind of location array      
        self.layout = QtGui.QGridLayout()
        self.layout.addItem(QtGui.QSpacerItem(10,10), 0, 0)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 0, 1)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 0, 2)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 1, 0)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 1, 1)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 1, 2)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 2, 0)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 2, 1)
        self.layout.addItem(QtGui.QSpacerItem(10,10), 2, 2)
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.resize(150, 150)
        self.update()
        
    def paintEvent(self, event = None):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        winHeight, winWidth, widthStep, heightStep = self.getWinParams()
               
        #print "Overall W, H:", winWidth, winHeight
        #Draw grid lines
        painter.setPen(QtCore.Qt.black)
        for i in range(4):
            #vertical lines
            painter.drawLine(QtCore.QPoint(i*widthStep,0), QtCore.QPoint(i*widthStep, winHeight))
            #horizontal lines
            painter.drawLine(QtCore.QPoint(0,heightStep*i), QtCore.QPoint(winWidth, heightStep*i))

  
        #Draw blue outline around selected box
        boxCoord = self.highlighted
        pen=QtGui.QPen(QtCore.Qt.blue, 4)        
        painter.setPen(pen)
        coordHighlight=[QtCore.QPoint(boxCoord[1]*widthStep, boxCoord[0]*heightStep),\
                        QtCore.QPoint((boxCoord[1]+1)*widthStep ,boxCoord[0]*heightStep),\
                        QtCore.QPoint((boxCoord[1]+1)*widthStep, (boxCoord[0]+1)*heightStep),\
                        QtCore.QPoint(boxCoord[1]*widthStep, (boxCoord[0]+1)*heightStep),\
                        QtCore.QPoint(boxCoord[1]*widthStep, boxCoord[0]*heightStep)]
        painter.drawPolyline(coordHighlight)

        #Draw ellipse in highlighted bit based on 3-state toggle state
        #print self.tritoggles
        for highlightIndex in range(9):
            rectHighlighted=self.layout.cellRect(self.coordinates[highlightIndex][0], self.coordinates[highlightIndex][1])
            rectHighlighted.adjust(4, 4, -4, -4) #so it fits nicely in the highlighting
            #print "Highlighted rectangle: ", rectHighlighted, "\n"
            if self.tritoggles[highlightIndex] == 0:        
                painter.setPen(QtGui.QPen(self.palette().window().color())) #why does this work?
                painter.setBrush(self.palette().brush(QtGui.QPalette.Window)) #If you wanted black gackground: painter.setBrush(QtGui.QColor(0, 0, 0))      
                painter.drawEllipse(rectHighlighted)  #draw rectangle size of QWidget
                
            elif self.tritoggles[highlightIndex] == 1:   
                painter.setBrush(QtCore.Qt.yellow)
                pen=QtGui.QPen(QtCore.Qt.yellow, 1)   
                painter.setPen(pen)
                painter.drawEllipse(rectHighlighted)
            else:
                painter.setBrush(QtCore.Qt.red)
                pen=QtGui.QPen(QtCore.Qt.red, 1)   
                painter.setPen(pen)
                painter.drawEllipse(rectHighlighted)
        

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            if self.highlighted[0] > 0:
                self.highlighted[0] = self.highlighted[0] - 1
            else:
                self.highlighted[0] = 2
                
        elif event.key() == QtCore.Qt.Key_Down:
            if self.highlighted[0] < 2:
                self.highlighted[0] = self.highlighted[0] + 1
            else:
                self.highlighted[0] = 0
                
        elif event.key() == QtCore.Qt.Key_Right:
            if self.highlighted[1] < 2:
                self.highlighted[1] = self.highlighted[1] + 1
            else:
                self.highlighted[1] = 0
                
        elif event.key() == QtCore.Qt.Key_Left:
            if self.highlighted[1] > 0:
                self.highlighted[1] = self.highlighted[1] - 1
            else:
                self.highlighted[1] = 2
        elif event.key() ==  QtCore.Qt.Key_Space:
            highlightIndex = self.highlightedIndex()
            toggleVal=self.tritoggles[highlightIndex]
            if toggleVal < 2:
                self.tritoggles[highlightIndex] += 1
            else:
                self.tritoggles[highlightIndex] = 0   
        else:
            QtGui.QWidget.keyPressEvent(self, event)
                   
        self.update()

   
    def getWinParams(self):
        winHeight = self.size().height()
        winWidth = self.size().width()
        heightStep=winHeight/3
        widthStep=winWidth/3      
        #print "Step H,W: ", heightStep, widthStep
        return winHeight, winWidth, widthStep, heightStep
        
    def minimumSizeHint(self):
        return QtCore.QSize(120,120)
    
    def highlightedIndex(self):
        tupHighlighted=tuple(self.highlighted)
        return self.coordinates.index(tupHighlighted)
        
                             
    def mousePressEvent(self, event):
        self.pullHighlighted(event.pos())
        #print "mousePress highlighted: ", self.highlighted
        highlightIndex = self.highlightedIndex()
        #print "**\nIndex selected: ", highlightIndex
        toggleVal=self.tritoggles[highlightIndex]
        if toggleVal < 2:
            self.tritoggles[highlightIndex] += 1
        else:
            self.tritoggles[highlightIndex] = 0
        self.update()



    def pullHighlighted(self, pos):
        winHeight, winWidth, widthStep, heightStep = self.getWinParams()
        #print "pullHighlighted: ", pos.x()
        self.highlighted = [pos.y()/widthStep, pos.x()/heightStep]
        #print "Highlighted box coordinate: ", self.highlighted
        return 
     


if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    myCounter=CounterMatrix()
    myCounter.setWindowTitle("Color-based counter")
    myCounter.show()
    sys.exit(app.exec_())