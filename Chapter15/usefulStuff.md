Things that might be useful when working through Chapter 15 of Rapid GUI Programming by Summerfield.
Part of PySideSummer repository (https://github.com/EricThomson/PySideSummer)


#Useful links
Good, simple example of displaying database in table:
http://stackoverflow.com/a/20993806/1886357

Simple widget mapper example:
http://qt-project.org/doc/qt-4.8/itemviews-simplewidgetmapper.html

Enumeration of potential driver features:
http://srinikom.github.io/pyside-docs/PySide/QtSql/QSqlDriver.html#QtSql.QtSql.QSqlDriver.DriverFeature

Enumeration of process event flags:
http://qt-project.org/doc/qt-4.8/qeventloop.html#ProcessEventsFlag-enum

Mapping data to widgets (note this is for C++)--would be really nice to port this documentation to Python!
http://doc.qt.digia.com/qq/qq21-datawidgetmapper.html


#Useful Documentation
##QtSql.QSqlQuery
http://srinikom.github.io/pyside-docs/PySide/QtSql/QSqlQuery.html

    The QtSql.QSqlQuery class provides a means of executing and manipulating SQL statements.

    QtSql.QSqlQuery encapsulates the functionality involved in creating, navigating and retrieving data from SQL queries which are executed on a QtSql.QSqlDatabase. It can be used to execute DML (data manipulation language) statements, such as SELECT, INSERT, UPDATE, and DELETE, as well as DDL (data definition language) statements, such as CREATE TABLE. It can also be used to execute database-specific commands which are not standard SQL (e.g. SET DATESTYLE=ISO for PostgreSQL).

    Successfully executed SQL statements set the query’s state to active so that QtSql.QSqlQuery.isActive() returns true. Otherwise the query’s state is set to inactive. In either case, when executing a new SQL statement, the query is positioned on an invalid record. An active query must be navigated to a valid record (so that QtSql.QSqlQuery.isValid() returns true) before values can be retrieved.

    For some databases, if an active query that is a SELECT statement exists when you call QtSql.QSqlDatabase.commit() or QtSql.QSqlDatabase.rollback(), the commit or rollback will fail. See QtSql.QSqlQuery.isActive() for details.

    Navigating records is performed with the following functions:

        QtSql.QSqlQuery.next()
        QtSql.QSqlQuery.previous()
        QtSql.QSqlQuery.first()
        QtSql.QSqlQuery.last()
        QtSql.QSqlQuery.seek()

    These functions allow the programmer to move forward, backward or arbitrarily through the records returned by the query. If you only need to move forward through the results (e.g., by using QtSql.QSqlQuery.next()), you can use QtSql.QSqlQuery.setForwardOnly(), which will save a significant amount of memory overhead and improve performance on some databases. Once an active query is positioned on a valid record, data can be retrieved using QtSql.QSqlQuery.value(). All data is transferred from the SQL backend using QVariants.

    For example:

    query = QSqlQuery("SELECT country FROM artist")
    while query.next():
        country = query.value(0)
        doSomething(country)

    To access the data returned by a query, use value(int). Each field in the data returned by a SELECT statement is accessed by passing the field’s position in the statement, starting from 0. This makes using SELECT * queries inadvisable because the order of the fields returned is indeterminate.

    For the sake of efficiency, there are no functions to access a field by name (unless you use prepared queries with names, as explained below). To convert a field name into an index, use QtSql.QSqlQuery.record(). QtSql.QSqlRecord.indexOf(), for example:

    query = QSqlQuery("SELECT * FROM artist")
    fieldNo = query.record().indexOf("country")
    while query.next():
        country = query.value(fieldNo)
        doSomething(country)

    QtSql.QSqlQuery supports prepared query execution and the binding of parameter values to placeholders. Some databases don’t support these features, so for those, Qt emulates the required functionality. For example, the Oracle and ODBC drivers have proper prepared query support, and Qt makes use of it; but for databases that don’t have this support, Qt implements the feature itself, e.g. by replacing placeholders with actual values when a query is executed. Use QtSql.QSqlQuery.numRowsAffected() to find out how many rows were affected by a non-SELECT query, and QtSql.QSqlQuery.size() to find how many were retrieved by a SELECT.

    Oracle databases identify placeholders by using a colon-name syntax, e.g :name. ODBC simply uses ? characters. Qt supports both syntaxes, with the restriction that you can’t mix them in the same query.

    You can retrieve the values of all the fields in a single variable (a map) using QtSql.QSqlQuery.boundValues().

	###Approaches to Binding Values

    Below we present the same example using each of the four different binding approaches, as well as one example of binding values to a stored procedure.

    #### binding using named placeholders:

		query = QSqlQuery()
		query.prepare("INSERT INTO person (id, forename, surname) "
					  "VALUES (:id, :forename, :surname)")
		query.bindValue(":id", 1001)
		query.bindValue(":forename", "Bart")
		query.bindValue(":surname", "Simpson")
		query.exec_()

    ####Positional binding using named placeholders:

		query = QSqlQuery()
		query.prepare("INSERT INTO person (id, forename, surname) "
					  "VALUES (:id, :forename, :surname)")
		query.bindValue(0, 1001)
		query.bindValue(1, "Bart")
		query.bindValue(2, "Simpson")
		query.exec_()

    ####Binding values using positional placeholders (version 1):

		query = QSqlQuery()
		query.prepare("INSERT INTO person (id, forename, surname) "
					  "VALUES (?, ?, ?)")
		query.bindValue(0, 1001)
		query.bindValue(1, "Bart")
		query.bindValue(2, "Simpson")
		query.exec_()

    ####Binding values using positional placeholders (version 2):

		query = QSqlQuery()
		query.prepare("INSERT INTO person (id, forename, surname) "
					  "VALUES (?, ?, ?)")
		query.addBindValue(1001)
		query.addBindValue("Bart")
		query.addBindValue("Simpson")
		query.exec_()

    ####Binding values to a stored procedure:

    This code calls a stored procedure called AsciiToInt(), passing it a character through its in parameter, and taking its result in the out parameter.

		query = QSqlQuery()
		query.prepare("CALL AsciiToInt(?, ?)")
		query.bindValue(0, "A")
		query.bindValue(1, 0, QSql.Out)
		query.exec_()
		i = query.boundValue(1) # i is 65

    Note that unbound parameters will retain their values.

    Stored procedures that uses the return statement to return values, or return multiple result sets, are not fully supported. For specific details see SQL Database Drivers.

    ###Warning

    You must load the SQL driver and open the connection before a QtSql.QSqlQuery is created. Also, the connection must remain open while the query exists; otherwise, the behavior of QtSql.QSqlQuery is undefined.

    
##QtSql.QSqlRecord
http://srinikom.github.io/pyside-docs/PySide/QtSql/QSqlRecord.html

    The QtSql.QSqlRecord class encapsulates a database record.

    The QtSql.QSqlRecord class encapsulates the functionality and characteristics of a database record (usually a row in a table or view within the database). QtSql.QSqlRecord supports adding and removing fields as well as setting and retrieving field values.

    The values of a record’s fields’ can be set by name or position with QtSql.QSqlRecord.setValue(); if you want to set a field to null use QtSql.QSqlRecord.setNull(). To find the position of a field by name use QtSql.QSqlRecord.indexOf(), and to find the name of a field at a particular position use QtSql.QSqlRecord.fieldName(). Use QtSql.QSqlRecord.field() to retrieve a QtSql.QSqlField object for a given field. Use QtSql.QSqlRecord.contains() to see if the record contains a particular field name.

    When queries are generated to be executed on the database only those fields for which QtSql.QSqlRecord.isGenerated() is true are included in the generated SQL.

    A record can have fields added with QtSql.QSqlRecord.append() or QtSql.QSqlRecord.insert(), replaced with QtSql.QSqlRecord.replace(), and removed with QtSql.QSqlRecord.remove(). All the fields can be removed with QtSql.QSqlRecord.clear(). The number of fields is given by QtSql.QSqlRecord.count(); all their values can be cleared (to null) using QtSql.QSqlRecord.clearValues().  
    
    
##QSqlDatabase
http://srinikom.github.io/pyside-docs/PySide/QtSql/QSqlDatabase.html

    The QtSql.QSqlDatabase class represents a connection to a database.

    The QtSql.QSqlDatabase class provides an interface for accessing a database through a connection. An instance of QtSql.QSqlDatabase represents the connection. The connection provides access to the database via one of the supported database drivers, which are derived from QtSql.QSqlDriver. Alternatively, you can subclass your own database driver from QtSql.QSqlDriver. See How to Write Your Own Database Driver for more information.

    Create a connection (i.e., an instance of QtSql.QSqlDatabase) by calling one of the static QtSql.QSqlDatabase.addDatabase() functions, where you specify the driver or type of driver to use (i.e., what kind of database will you access?) and a connection name. A connection is known by its own name, not by the name of the database it connects to. You can have multiple connections to one database. QtSql.QSqlDatabase also supports the concept of a default connection, which is the unnamed connection. To create the default connection, don’t pass the connection name argument when you call QtSql.QSqlDatabase.addDatabase(). Subsequently, when you call any static member function that takes the connection name argument, if you don’t pass the connection name argument, the default connection is assumed. The following snippet shows how to create and open a default connection to a PostgreSQL database:

        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName("acidalia")
        db.setDatabaseName("customdb")
        db.setUserName("mojito")
        db.setPassword("J0a1m8")
        ok = db.open()

    Once the QtSql.QSqlDatabase object has been created, set the connection parameters with QtSql.QSqlDatabase.setDatabaseName(), QtSql.QSqlDatabase.setUserName(), QtSql.QSqlDatabase.setPassword(), QtSql.QSqlDatabase.setHostName(), QtSql.QSqlDatabase.setPort(), and QtSql.QSqlDatabase.setConnectOptions(). Then call QtSql.QSqlDatabase.open() to activate the physical connection to the database. The connection is not usable until you open it.

    The connection defined above will be the default connection, because we didn’t give a connection name to QtSql.QSqlDatabase.addDatabase(). Subsequently, you can get the default connection by calling QtSql.QSqlDatabase.database() without the connection name argument:

        db = QSqlDatabase.database()

    QtSql.QSqlDatabase is a value class. Changes made to a database connection via one instance of QtSql.QSqlDatabase will affect other instances of QtSql.QSqlDatabase that represent the same connection. Use QtSql.QSqlDatabase.cloneDatabase() to create an independent database connection based on an existing one.

    If you create multiple database connections, specify a unique connection name for each one, when you call QtSql.QSqlDatabase.addDatabase(). Use QtSql.QSqlDatabase.database() with a connection name to get that connection. Use QtSql.QSqlDatabase.removeDatabase() with a connection name to remove a connection. QtSql.QSqlDatabase outputs a warning if you try to remove a connection referenced by other QtSql.QSqlDatabase objects. Use QtSql.QSqlDatabase.contains() to see if a given connection name is in the list of connections.

    Once a connection is established, you can call QtSql.QSqlDatabase.tables() to get the list of tables in the database, call QtSql.QSqlDatabase.primaryIndex() to get a table’s primary index, and call QtSql.QSqlDatabase.record() to get meta-information about a table’s fields (e.g., field names).

    If the driver supports transactions, use QtSql.QSqlDatabase.transaction() to start a transaction, and QtSql.QSqlDatabase.commit() or QtSql.QSqlDatabase.rollback() to complete it. Use QtSql.QSqlDriver.hasFeature() to ask if the driver supports transactions. Note: When using transactions, you must start the transaction before you create your query.

    If an error occurs, QtSql.QSqlDatabase.lastError() will return information about it.

    Get the names of the available SQL drivers with QtSql.QSqlDatabase.drivers(). Check for the presence of a particular driver with QtSql.QSqlDatabase.isDriverAvailable(). If you have created your own custom driver, you must register it with QtSql.QSqlDatabase.registerSqlDriver().

##QDataWidgetMapper (compare to QSignalMapper)
http://srinikom.github.io/pyside-docs/PySide/QtGui/QDataWidgetMapper.html

    The QtGui.QDataWidgetMapper class provides mapping between a section of a data model to widgets. It can be used to create data-aware widgets by mapping the widgets to a data model. 

    Every time the current index changes, each widget is updated with data from the model via the property specified when its mapping was made. If the user edits the contents of a widget, the changes are read using the same property and written back to the model. By default, each widget’s user property is used to transfer data between the model and the widget. Since Qt 4.3, an additional QtGui.QDataWidgetMapper.addMapping() function enables a named property to be used instead of the default user property.

    It is possible to set an item delegate to support custom widgets. By default, a QtGui.QItemDelegate is used to synchronize the model with the widgets.

    Let us assume that we have an item model named model with the following contents:
        1 	Qt Norway 	Oslo
        2 	Qt Australia 	Brisbane
        3 	Qt USA 	Palo Alto
        4 	Qt China 	Beijing
        5 	Qt Germany 	Berlin

    The following code will map the columns of the model to widgets called mySpinBox, myLineEdit and myCountryChooser :

        mapper = QDataWidgetMapper
        mapper.setModel(model)
        mapper.addMapping(mySpinBox, 0)
        mapper.addMapping(myLineEdit, 1)
        mapper.addMapping(myCountryChooser, 2)
        mapper.toFirst()

    After the call to QtGui.QDataWidgetMapper.toFirst(), mySpinBox displays the value 1, myLineEdit displays Nokia Corporation and/or its subsidiary(-ies) and myCountryChooser displays Oslo. The navigational functions QtGui.QDataWidgetMapper.toFirst(), QtGui.QDataWidgetMapper.toNext(), QtGui.QDataWidgetMapper.toPrevious(), QtGui.QDataWidgetMapper.toLast() and QtGui.QDataWidgetMapper.setCurrentIndex() can be used to navigate in the model and update the widgets with contents from the model.

    The QtGui.QDataWidgetMapper.setRootIndex() function enables a particular item in a model to be specified as the root index - children of this item will be mapped to the relevant widgets in the user interface.

    QtGui.QDataWidgetMapper supports two submit policies, AutoSubmit and ManualSubmit. AutoSubmit will update the model as soon as the current widget loses focus, ManualSubmit will not update the model unless QtGui.QDataWidgetMapper.submit() is called. ManualSubmit is useful when displaying a dialog that lets the user cancel all modifications. Also, other views that display the model won’t update until the user finishes all their modifications and submits.

    Note that QtGui.QDataWidgetMapper keeps track of external modifications. If the contents of the model are updated in another module of the application, the widgets are updated as well.

##QSql.QSqlRelationalTableModel
http://srinikom.github.io/pyside-docs/PySide/QtSql/QSqlRelationalTableModel.html

    The QtSql.QSqlRelationalTableModel class provides an editable data model for a single database table, with foreign key support.

    QtSql.QSqlRelationalTableModel acts like QtSql.QSqlTableModel, but allows columns to be set as foreign keys into other database tables. Foreign keys are resolved into human-readable text strings.

    The following code snippet shows how the QtSql.QSqlRelationalTableModel was set up:

        model.setTable("employee")
        model.setRelation(2, QSqlRelation("city", "id", "name"))
        model.setRelation(3, QSqlRelation("country", "id", "name"))

    The QtSql.QSqlRelationalTableModel.setRelation() function calls establish a relationship between two tables. The first call specifies that column 2 in table employee is a foreign key that maps with field id of table city, and that the view should present the city's name field to the user. The second call does something similar with column 3.

    If you use a read-write QtSql.QSqlRelationalTableModel, you probably want to use QtSql.QSqlRelationalDelegate on the view. Unlike the default delegate, QtSql.QSqlRelationalDelegate provides a combobox for fields that are foreign keys into other tables. To use the class, simply call QAbstractItemView.setItemDelegate() on the view with an instance of QtSql.QSqlRelationalDelegate :

        view =  QTableView()
        view.setModel(model)
        view.setItemDelegate(QSqlRelationalDelegate(view))

    The sql/relationaltablemodel example illustrates how to use QtSql.QSqlRelationalTableModel in conjunction with QtSql.QSqlRelationalDelegate to provide tables with foreign key support.

    Notes:
    -  The table must have a primary key declared.
    -  The table’s primary key may not contain a relation to another table.
    -  If a relational table contains keys that refer to non-existent rows in the referenced table, the rows containing the invalid keys will not be exposed through the model. The user or the database is responsible for keeping referential integrity.
    -  If a relation’s display column name is also used as a column name in the main table, or if it is used as display column name in more than one relation it will be aliased. The alias is is the relation’s table name and display column name joined by an underscore (e.g. tablename_columnname). All occurrences of the duplicate display column name are aliased when duplication is detected, but no aliasing is done to the column names in the main table. The aliasing doesn’t affect QtSql.QSqlRelation, so QSqlRelation.displayColumn() will return the original display column name, but QSqlRecord.fieldName() will return aliases.
    -  When using QtSql.QSqlRelationalTableModel.setData() the role should always be Qt.EditRole, and when using QtSql.QSqlRelationalTableModel.data() the role should always be Qt.DisplayRole. [?]

##QtSql.QSqlTableModel
http://srinikom.github.io/pyside-docs/PySide/QtSql/QSqlTableModel.html

    The QtSql.QSqlTableModel class provides an editable data model for a single database table.

    QtSql.QSqlTableModel is a high-level interface for reading and writing database records from a single table. It is build on top of the lower-level QtSql.QSqlQuery and can be used to provide data to view classes such as QtGui.QTableView. For example:

        model =  QSqlTableModel()
        model.setTable("employee")
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()
        model.removeColumn(0) # don't show the ID
        model.setHeaderData(0, Qt.Horizontal, tr("Name"))
        model.setHeaderData(1, Qt.Horizontal, tr("Salary"))

        view =  QTableView()
        view.setModel(model)
        view.show()

    We set the SQL table’s name and the edit strategy, then we set up the labels displayed in the view header. The edit strategy dictates when the changes done by the user in the view are actually applied to the database. The possible values are OnFieldChange, OnRowChange, and OnManualSubmit.

    QtSql.QSqlTableModel can also be used to access a database programmatically, without binding it to a view:

        model = QSqlQueryModel()
        model.setQuery("SELECT * FROM employee")
        salary = model.record(4).value("salary")

    The code snippet above extracts the salary field from record 4 in the result set of the query SELECT * from employee.

    It is possible to set filters using QtSql.QSqlTableModel.setFilter(), or modify the sort order using QtSql.QSqlTableModel.setSort(). At the end, you must call QtSql.QSqlTableModel.select() to populate the model with data.

    QtSql.QSqlTableModel.select() populates the model with data from the table that was set via QtSql.QSqlTableModel.setTable(), using the specified filter and sort condition, and returns true if successful; otherwise returns false. Note that calling QtSql.QSqlTableModel.select() will revert any unsubmitted changes and remove any inserted columns.

    QtSql.QSqlTableModel provides no direct support for foreign keys. Use the QtSql.QSqlRelationalTableModel and QtSql.QSqlRelationalDelegate if you want to resolve foreign keys.

    
##