# -*- coding: utf-8 -*-
"""
moviedataPyside_ans.py
Part of solution to Exercise from Chapter 8
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Imported by mymoviesPyside_ans.py

To do:
Make old and new file format variable in moviecontainer. 
Test out as he suggests (different file types, locations, etc)

------            
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer

Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
from xml.sax.saxutils import escape as escape
import bisect
from PySide import QtCore
from PySide import QtXml #https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/PySide/QtXml/index.html

CODEC = "utf-8"
NEWPARA = unichr(0x2029) #(https://docs.python.org/2/library/functions.html#unichr 
NEWLINE = unichr(0x2028)  #like <p> versus <br />
DATEFORMAT = "ddd MMM d, yyyy"

#Replace paragraphs (two newlines replaced by NEWPARA, then \n by NEWLINE
#On replace: http://www.tutorialspoint.com/python/string_replace.htm
def encodedNewlines(text):
    return text.replace("\n\n", NEWPARA).replace("\n", NEWLINE)

def decodedNewlines(text):  
    return text.replace(NEWPARA, "\n\n").replace(NEWLINE, "\n")  
    
    
class Movie(object):
    """A Movie object holds the details of a movie.
    
    The data held are the title, year, minutes length, date acquired,
    and notes. If the year is unknown it is set to 1890. If the minutes
    are unknown they are set to 0. The title and notes are held as strings,
    and the notes may contain embedded newlines. Both are plain text,
    and can contain any Unicode characters. The title cannot contain
    newlines or tabs, but the notes can contain both. The date acquired
    is held as a QDate.
    """
    UNKNOWNYEAR = 1890
    UNKNOWNMINUTES = 0
    
    def __init__(self, title=None, year=UNKNOWNYEAR,
                 minutes=UNKNOWNMINUTES, acquired=None, notes=None, location=None):
        self.title = title
        self.year = year
        self.minutes = minutes
        self.acquired = (acquired if acquired is not None
                                  else QtCore.QDate.currentDate())
        self.notes = notes
        self.location=location


class MovieContainer(object):
    """A MovieContainer holds a set of Movie objects.

    The movies are held in a canonicalized order based on their title
    and year, so if either of these fields is changed the movies must be
    re-sorted. For this reason (and to maintain the dirty flag), all
    updates to movies should be made through this class's updateMovie()
    method.
    """

    #MAGIC_NUMBER and FILE_VERSION are used for saving/loading QDataStream class
    MAGIC_NUMBER = 0x3051E
    NEW_FILE_VERSION = 101
    OLD_FILE_VERSION=100

    def __init__(self):
        self.__fname = ""
        #Each element of the movies list is a two-element list. The first
        #element is a sort key, the second a Movie instance.;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        self.__movies = []
        #Dictionary. For movie i, key is id(Movie(i)) and value is Movie(i)
        #(or at least, a reference to the Movie).
        self.__movieFromId = {}
        self.__dirty = False  #unsaved changes?

    #Make the container iterable
    #On yield: http://www.jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
    def __iter__(self):
        for pair in iter(self.__movies):
            yield pair[1]  #returns just the second element in the pair (the movie)

    #how many movies?
    def __len__(self):
        return len(self.__movies)
        

    def setFilename(self, fname):
        self.__fname = fname

    def filename(self):
        return self.__fname
        
    def isDirty(self):
        return self.__dirty

    def setDirty(self, dirty=True):
        self.__dirty = dirty

    #Clear all data in the container
    #this doesn't clear notes does it? Yes, __movies is set to []
    def clear(self, clearFilename=True):
        self.__movies = []
        self.__movieFromId = {}
        if clearFilename:
            self.__fname = ""
        self.__dirty = False
        
    #add Movie object to container
    def add(self, movie):
        """Adds the given movie to the list if it isn't already
        present. Returns True if added; otherwise returns False."""
        if id(movie) in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        bisect.insort_left(self.__movies, [key, movie])
        self.__movieFromId[id(movie)] = movie
        self.__dirty = True
        return True
        
    #key string created. It is used for sorting movies
    def key(self, title, year):
        text = title.lower()
        if text.startswith("a "):
            text = text[2:]
        elif text.startswith("an "):
            text = text[3:]
        elif text.startswith("the "):
            text = text[4:]
        parts = text.split(" ", 1)  #https://docs.python.org/2/library/stdtypes.html#str.split
        if parts[0].isdigit():
            text = "{0:08d} ".format(int(parts[0]))
            if len(parts) > 1:
                text += parts[1]
        return "{}\t{}".format(text.replace(" ", ""), year)
    
    def delete(self, movie):
        """Deletes the given Movie object from the list and returns True;
        returns False if the movie isn't in the list."""
        if id(movie) not in self.__movieFromId:
            return False
        key = self.key(movie.title, movie.year)
        i = bisect.bisect_left(self.__movies, [key, movie])
        #To remove a movie, must remove it from the movies list as well as the
        #movieFromId dictionary
        del self.__movies[i]
        del self.__movieFromId[id(movie)]
        self.__dirty = True
        return True
        
        
    def updateMovie(self, movie, title, year, minutes=None, notes=None, location=None):
        if minutes is not None:
            movie.minutes = minutes
        if notes is not None:
            movie.notes = notes
        if location is not None:
            movie.location=location
        if title != movie.title or year != movie.year:
            key = self.key(movie.title, movie.year)
            i = bisect.bisect_left(self.__movies, [key, movie])
            self.__movies[i][0] = self.key(title, year)
            movie.title = title
            movie.year = year
            self.__movies.sort()
        self.__dirty = True
        
    @staticmethod
    def formats():
        #mqb: qt binary (uses qdatastream class)
        return "*.mqb"
        
    def save(self, fname=""):
        if fname:
            self.__fname = fname
        if self.__fname.endswith(".mqb"):
            return self.saveQDataStream()
        return False, "Failed to save: invalid file extension"
        
    def load(self, fname=""):
        if fname:
            self.__fname = fname
        if self.__fname.endswith(".mqb"):
            return self.loadQDataStream()
        return False, "Failed to load: invalid file extension"
        
    def movieFromId(self, id):
        """Returns the movie with the given Python ID."""
        return self.__movieFromId[id]


    def movieAtIndex(self, index):
        """Returns the index-th movie."""
        return self.__movies[index][1]
        
    def saveQDataStream(self):
        error = None
        file = None
        
        try:
            file = QtCore.QFile(self.__fname)  #qfile: chapter 6
            if not file.open(QtCore.QIODevice.WriteOnly): #http://srinikom.github.io/pyside-docs/PySide/QtCore/QIODevice.html
                raise IOError(file.errorString())
            stream = QtCore.QDataStream(file)
            #Magic number in case you have same extension for different file format
            stream.writeInt32(MovieContainer.MAGIC_NUMBER)
            #File version in case you end up with a modified format
            stream.writeInt32(MovieContainer.NEW_FILE_VERSION)
            stream.setVersion(QtCore.QDataStream.Qt_4_6)
            for key, movie in self.__movies:
                stream.writeQString(movie.title)
                stream.writeInt16(movie.year)
                stream.writeInt16(movie.minutes)
                stream.writeQString(
                        movie.acquired.toString(QtCore.Qt.ISODate))
                stream.writeQString(movie.notes)
                stream.writeQString(movie.location)
        except EnvironmentError as e:
            error = "Failed to save Qt binary: {0}".format(e)
            print error
        except Exception as e:
            error = "Fail to save Qt binary: {0}".format(e)
            print error
        finally:
            if file is not None:
                file.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Saved {} movie records to {}".format(
                    len(self.__movies),
                    QtCore.QFileInfo(self.__fname).fileName()) 


    def loadQDataStream(self):
        error = None
        file = None
        try:
            file = QtCore.QFile(self.__fname)
            if not file.open(QtCore.QIODevice.ReadOnly):
                raise IOError(file.errorString())
            stream = QtCore.QDataStream(file)
            magic = stream.readInt32()
            #Using the magic number to check file type
            if magic != MovieContainer.MAGIC_NUMBER:
                raise IOError("unrecognized file type")
            #Pull out version number to check for compatability
            version = stream.readInt32()
            #print version
            if version < MovieContainer.OLD_FILE_VERSION:
                raise IOError("old and unreadable file format")
            elif version > MovieContainer.NEW_FILE_VERSION:
                raise IOError("new and unreadable file format")
            stream.setVersion(QtCore.QDataStream.Qt_4_6)
            self.clear(False)  #Set to false-->don't clear filename
            while not stream.atEnd():
                title = stream.readQString()
                year = stream.readInt16()
                minutes = stream.readInt16()
                acquired = QtCore.QDate.fromString(stream.readQString(),
                                            QtCore.Qt.ISODate)
                notes = stream.readQString()
                if version==MovieContainer.NEW_FILE_VERSION:
                    location=stream.readQString()
                    self.add(Movie(title, year, minutes, acquired, notes, location))
                else:
                    self.add(Movie(title, year, minutes, acquired, notes))
        except EnvironmentError as e:
            error = "Failed to load Qt binary: {}".format(e)
        except Exception as e:
            error = "Failed to load Qt binary: {}".format(e)
        finally:
            if file is not None:
                file.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Loaded {} movie records from {}".format(
                    len(self.__movies),
                    QtCore.QFileInfo(self.__fname).fileName())
                    
        
    #on escaping xml:
    #https://wiki.python.org/moin/EscapingXml
    def exportXml(self, fname):
        error = None
        fh = None
        try:
            #print "Fname in method: ", fname, " of type: ", type(fname)
            fh = QtCore.QFile(fname)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setCodec(CODEC)
            stream << unicode(("<?xml version='1.0' encoding='{}'?>\n"
                       "<!DOCTYPE MOVIES>\n"
                       "<MOVIES VERSION='1.1'>\n".format(CODEC)))
            for key, movie in self.__movies:
                stream << unicode(("<MOVIE YEAR='{}' MINUTES='{}' ACQUIRED='{}'>\n".\
                        format(movie.year, movie.minutes, movie.acquired.toString(QtCore.Qt.ISODate))))
                stream << u"<TITLE>" << escape(movie.title) << u"</TITLE>\n<NOTES>"
                if movie.notes is not None:
                    stream << "\n" << escape(encodedNewlines(movie.notes)) << "\n"
                stream << "</NOTES>\n<LOCATION>"
                if movie.location is not None:
                    stream << escape(encodedNewlines(movie.location))
                stream << "\n" << "</LOCATION>\n</MOVIE>\n"
            stream << "\n</MOVIES>\n"
        except EnvironmentError as e:
            error = "Failed to export: {}".format(e)
            print error
        except Exception as e:
            error = "Failed to export with error {0}".format(e)
            print error
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__dirty = False
            return True, "Exported {} movie records to {}".format(
                    len(self.__movies),
                    QtCore.QFileInfo(fname).fileName())
                    


    def importDOM(self, fname):
        dom = QtXml.QDomDocument()
        error = None
        fh = None
        try:
            fh = QtCore.QFile(fname)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            if not dom.setContent(fh):
                raise ValueError("could not parse XML")
        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        except Exception as e:
            error = "Failed to import DOM: {0}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
        try:
            self.populateFromDOM(dom)
        except ValueError as e:
            return False, "Failed to import: {}".format(e)
        self.__fname = ""
        self.__dirty = True
        return True, "Imported {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(fname).fileName())


    def populateFromDOM(self, dom):
        root = dom.documentElement()
        if root.tagName() != "MOVIES":
            raise ValueError("not a Movies XML file")
        self.clear(False)
        ##Getting version number from root node
        #Ended up not using this...
        #if root.hasAttributes():
        #    print "We've got attributes!"
        #    rootAts = root.attributes()
        #    #print rootAts.length()
        #    #print type(rootAts)
        #    attItem=rootAts.item(0)
        #    attr=attItem.toAttr()
        #    print attr.name()
        #    print attr.value()
        #    if attr.name()=="VERSION":
        #        print type(attr.value())
        node = root.firstChild()
        #cycle through siblings of first child (MOVIE node)
        while not node.isNull():
            if node.toElement().tagName() == "MOVIE":
                self.readMovieNode(node.toElement())
            node = node.nextSibling()


    def readMovieNode(self, element):
        #pull text from a node (used below)
        def getText(node):
            child = node.firstChild()
            text = ""
            while not child.isNull():
                if child.nodeType() == QtXml.QDomNode.TextNode:
                    text += child.toText().data()
                child = child.nextSibling()
            return text.strip()

        year = int(element.attribute("YEAR"))
        minutes = int(element.attribute("MINUTES"))
        ymd = element.attribute("ACQUIRED").split("-")
        if len(ymd) != 3:
            raise ValueError("invalid acquired date {}".format(
                    element.attribute("ACQUIRED")))
        acquired = QtCore.QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        title = notes = location = None
        node = element.firstChild()       
        
        #not sure about this way to make it backward compatible by not adding 
        #the additional disjunct: `or location is None`
        while title is None or notes is None: 
            if node.isNull():
                raise ValueError("missing title or location or notes")
            if node.toElement().tagName() == "TITLE":
                title = getText(node)
                #print title
            elif node.toElement().tagName() == "LOCATION":
                location = getText(node)
            elif node.toElement().tagName() == "NOTES":
                notes = getText(node)
            node = node.nextSibling()
        if not title:
            raise ValueError("missing title")
        self.add(Movie(title, year, minutes, acquired,
                       decodedNewlines(notes), location))              
                       
    def importSAX(self, fname):
        error = None
        fh = None
        try:
            handler = SaxMovieHandler(self)
            parser = QtXml.QXmlSimpleReader()
            parser.setContentHandler(handler)
            parser.setErrorHandler(handler)
            fh = QtCore.QFile(fname)
            input = QtXml.QXmlInputSource(fh)
            self.clear(False)
            if not parser.parse(input):
                raise ValueError(handler.error)
        except (IOError, OSError, ValueError) as e:
            error = "Failed to import: {}".format(e)
        except Exception as e:
            error = "Failed to import SAX: {0}".format(e)
        finally:
            if fh is not None:
                fh.close()
            if error is not None:
                return False, error
            self.__fname = ""
            self.__dirty = True
            return True, "Imported {} movie records from {}".format(
                    len(self.__movies), QtCore.QFileInfo(fname).fileName())


class SaxMovieHandler(QtXml.QXmlDefaultHandler):

    def __init__(self, movies):
        QtXml.QXmlDefaultHandler.__init__(self)
        self.movies = movies
        self.text = ""
        self.error = None


    def clear(self):
        self.year = None
        self.minutes = None
        self.acquired = None
        self.title = None
        self.notes = None
        self.location = None


    def startElement(self, namespaceURI, localName, qName, attributes):
        if qName == "MOVIE":
            self.clear()
            self.year = int(attributes.value("YEAR"))
            self.minutes = int(attributes.value("MINUTES"))
            ymd = attributes.value("ACQUIRED").split("-")
            if len(ymd) != 3:
                raise ValueError("invalid acquired date {}".format(
                        attributes.value("ACQUIRED")))
            self.acquired = QtCore.QDate(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        elif qName in ("TITLE", "NOTES", "LOCATION"):
            self.text = ""
        return True


    def characters(self, text):
        self.text += text
        return True


    def endElement(self, namespaceURI, localName, qName):
        if qName == "MOVIE":
            #as with DOM, leaving off self.location here for backwards compatability
            if (self.year is None or self.minutes is None or
                self.acquired is None or self.title is None or
                self.notes is None):
                raise ValueError("incomplete movie record")
            self.movies.add(Movie(self.title, self.year,
                    self.minutes, self.acquired,
                    decodedNewlines(self.notes), self.location))
            self.clear()
        elif qName == "TITLE":
            self.title = self.text.strip()
        elif qName == "NOTES":
            self.notes = self.text.strip()
        elif qName == "LOCATION":
            self.location = self.text.strip()
        return True


    def fatalError(self, exception):
        self.error = "parse error at line {} column {}: {}".format(
                exception.lineNumber(), exception.columnNumber(),
                exception.message())
        return False


##
      

        
        
##
        
#Testing different components of the program
if __name__=="__main__":
    testMovieClass=0
    testContainer=1     
    if testMovieClass:
            print "*" * 40
            print "**Testing Movie class**"
            firstMovie=Movie("Frozen", 2013, 117, notes="Ella's favorite!", location="Lock box")
            print "\n{0} ({1})\nNote: {2}\nLocation: {3}".\
                format(firstMovie.title, firstMovie.year, firstMovie.notes, firstMovie.location)  
            secondMovie=Movie("Jaws", 1975, 108, notes="Good movie.")
            print "\n{0} ({1})\nNote: {2}\nLocation: {3}".\
                format(secondMovie.title, secondMovie.year, secondMovie.notes, secondMovie.location)
            print "*" * 40 + "\n"

    print "*" * 40
    if testContainer:
        firstMovie=Movie("Frozen", 2013, 117, notes="Ella's favorite!", location="Lock box")  
        secondMovie=Movie("Jaws", 1975, 108, notes="Good movie.")
        print "**Testing movieContainer**"
        firstContainer = MovieContainer()
        if firstContainer.add(firstMovie):
            print "Got in movie 1"
        else:
            print "Movie 1 fail"   
        if firstContainer.add(secondMovie):
            print "Got in movie 2"
        else:
            print "Movie 2 fail"
    
        print firstContainer.movieAtIndex(0).title, ":", firstContainer.movieAtIndex(0).location
        print firstContainer.movieAtIndex(1).title, ":", firstContainer.movieAtIndex(1).location
        #print dir(firstContainer)
        print "*" * 40
        
        
        #Test save operation
        #Binary Qt
        print "\n", "*" * 40, "\n", "**Testing save**"
        saveToQData="test_ans.mqb"
        successQData, saveMsgQData=firstContainer.save(saveToQData)
        if successQData:
            print "Successfully saved as qt binary:\n", saveMsgQData
        else:
            print "\nSaving as qt binary failed"
        print "*" * 40,

        #Easier to test XML using mymoviesPyside_ans.py file menu options