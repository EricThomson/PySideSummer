Things that might be useful when working through Chapter 5 of PySideSummer repository (https://github.com/EricThomson/PySideSummer)

#Useful links
Excellent tutorial on dialogs/message boxes. Great place to start.
http://www.blog.pythonlibrary.org/2013/04/16/pyside-standard-dialogs-and-message-boxes/



#Useful Documentation
##QtGui.QMessageBox
http://srinikom.github.io/pyside-docs/PySide/QtGui/QMessageBox.html

    The QtGui.QMessageBox class provides a modal dialog for informing the user or for asking the user a question and receiving an answer.

    A message box displays a primary QtGui.QMessageBox.text() to alert the user to a situation, an informative text to further explain the alert or to ask the user a question, and an optional detailed text to provide even more data if the user requests it. A message box can also display an QtGui.QMessageBox.icon() and standard buttons for accepting a user response.

    Two APIs for using QtGui.QMessageBox are provided, the property-based API, and the static functions. Calling one of the static functions is the simpler approach, but it is less flexible than using the property-based API, and the result is less informative. Using the property-based API is recommended.

    ###The Property-based API

    To use the property-based API, construct an instance of QtGui.QMessageBox, set the desired properties, and call exec_() to show the message. The simplest configuration is to set only the message text property.

        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.exec_()

    The user must click the OK button to dismiss the message box. The rest of the GUI is blocked until the message box is dismissed.

    A better approach than just alerting the user to an event is to also ask the user what to do about it. Store the question in the informative text property, and set the standard buttons property to the set of buttons you want as the set of user responses. The buttons are specified by combining values from StandardButtons using the bitwise OR operator. The display order for the buttons is platform-dependent. For example, on Windows, Save is displayed to the left of Cancel, whereas on Mac OS, the order is reversed.

    Mark one of your standard buttons to be your default button.

        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()

    The exec() slot returns the StandardButtons value of the button that was clicked.

        if ret == QMessageBox.Save:
            # Save was clicked
        elif ret == QMessageBox.Discard:
            # Don't save was clicked
        elif ret == QMessageBox.Cancel:
            # cancel was clicked
        else:
            # should never be reached

    To give the user more information to help him answer the question, set the detailed text property. If the detailed text property is set, the 'Show Details...' button will be shown, and clicking the 'Show Details...' button displays the detailed text.

    ####Severity Levels and the Icon and Pixmap Properties

    QtGui.QMessageBox supports four predefined message severity levels, or message types, which really only differ in the predefined icon they each show. Specify one of the four predefined message types by setting the QtGui.QMessageBox.icon() property to one of the predefined icons. The following rules are guidelines:
    
        Question 	    For asking a question during normal operations.
        Information 	For reporting information about normal operations.
        Warning 	    For reporting non-critical errors.
        Critical        For reporting critical errors.

    The default value is No Icon. The message boxes are otherwise the same for all cases. When using a standard icon, use the one recommended in the table, or use the one recommended by the style guidelines for your platform. If none of the standard icons is right for your message box, you can use a custom icon by setting the icon pixmap property instead of setting the QtGui.QMessageBox.icon() property.

    In summary, to set an icon, use eitherQtGui.QMessageBox.setIcon() for one of the standard icons, orQtGui.QMessageBox.setIconPixmap() for a custom icon.

    ###The Static Functions API

    Building message boxes with the static functions API, although convenient, is less flexible than using the property-based API, because the static function signatures lack parameters for setting the informative text and detailed text properties. 
    Static functions are available for creating QtGui.QMessageBox.information(), QtGui.QMessageBox.question(), QtGui.QMessageBox.warning(), and QtGui.QMessageBox.critical() message boxes.

    ret = QMessageBox.warning(self, self.tr("My Application"),
                                   self.tr("The document has been modified.\n" + \
                                      "Do you want to save your changes?"),
                                   QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                   QMessageBox.Save)

    The Standard Dialogs example shows how to use QtGui.QMessageBox and the other built-in Qt dialogs.

    ###Custom buttons
    If the standard buttons are not flexible enough for your message box, you can use the QtGui.QMessageBox.addButton() overload that takes a text and a ButtonRole to to add custom buttons. The QMessageBox.ButtonRole is used by QtGui.QMessageBox to determine the ordering of the buttons on screen (which varies according to the platform). You can test the value of QtGui.QMessageBox.clickedButton() after calling exec(). For example,

        msgBox = QMessageBox()
        connectButton = msgBox.addButton("connect", QMessageBox.ActionRole)
        abortButton = msgBox.addButton(QMessageBox.Abort)

        msgBox.exec_()

        if msgBox.clickedButton() == connectButton:
            # connect
        elif msgBox.clickedButton() == abortButton:
            # abort
           
    ###Default and Escape Keys

    The default button (i.e., the button activated when Enter is pressed) can be specified using QtGui.QMessageBox.setDefaultButton(). If a default button is not specified, QtGui.QMessageBox tries to find one based on the button roles of the buttons used in the message box.

    The escape button (the button activated when Esc is pressed) can be specified using QtGui.QMessageBox.setEscapeButton(). If an escape button is not specified, QtGui.QMessageBox tries to find one using these rules:

        1. If there is only one button, it is the button activated when Esc is pressed.
        2. If there is a Cancel button, it is the button activated when Esc is pressed.
        3. If there is exactly one button having either the Reject role or the the No role, it is the button activated when Esc is pressed.
   
    When an escape button can’t be determined using these rules, pressing Esc has no effect.
    
 
    ###QMessageBox.ButtonRole enumeration
    This enum describes the roles that can be used to describe buttons in the button box. Combinations of these roles act as flags used to describe different aspects of their behavior.

    Constant 		            Value   Description
    QMessageBox.InvalidRole      -1     The button is invalid.
    QMessageBox.AcceptRole 	      0     Causes dialog to be accepted (e.g. OK).
    QMessageBox.RejectRole 	      1     Causes dialog to be rejected (e.g. Cancel).
    QMessageBox.DestructiveRole   2     Causes destructive change (e.g. discards changes), closes the dialog.
    QMessageBox.ActionRole 	      3     Causes changes to the elements within the dialog.
    QMessageBox.HelpRole 	      4     Click to request help.
    QMessageBox.YesRole 	      5	    Button is a "Yes"-like button.
    QMessageBox.NoRole 	          6	    Button is a "No"-like button.
    QMessageBox.ApplyRole 	      8	    The button applies current changes.
    QMessageBox.ResetRole 	      7	    The button resets the dialog's fields to default values.

    ###QMessageBox.StandardButton enumeration
    These enums describe flags for standard buttons. Each button has a defined ButtonRole. To use on msgBox using property-based API, setStandardButtons with something like `msgBox.setStandardButtons(x | y | z)`, where x, y, z are the standard buttons. E.g., x = QtGui.QMessageBox.Apply

    Constant 		             Value (hex/dec)	      Description
    QMessageBox.Ok 		         0x00000400 (1024) 	      An "OK" button defined using the AcceptRole.
    QMessageBox.Open 	         0x00002000 (8192)	      A "Open" button : AcceptRole.
    QMessageBox.Save 	         0x00000800 (2048)        A "Save" button : AcceptRole.
    QMessageBox.SaveAll 	     0x00001000 (4096) 	      A "Save All" button : AcceptRole.
    QMessageBox.Retry 	         0x00080000 (524288)      A "Retry" button : AcceptRole.
    QMessageBox.Ignore 	         0x00100000 (1048576)     An "Ignore" button : AcceptRole.
    QMessageBox.Cancel 	         0x00400000 (4194304)     A "Cancel" button : RejectRole.
    QMessageBox.Close 	         0x00200000 (2097152)     A "Close" button : RejectRole.
    QMessageBox.Abort 	         0x00040000 (262144)      An "Abort" button : RejectRole. 
    QMessageBox.Discard 	     0x00800000 (8388608)     Discard or Dont Save (platform dep):DestructiveRole 
    QMessageBox.Apply 	         0x02000000 (33554432)    An "Apply" button : ApplyRole.
    QMessageBox.Reset 	         0x04000000 (67108864)    A "Reset" button : ResetRole.
    QMessageBox.RestoreDefaults  0x08000000 (134217728)   A "Restore Defaults" button : ResetRole.
    QMessageBox.Help 	         0x01000000 (16777216)    A "Help" button : HelpRole.
    QMessageBox.Yes 	         0x00004000 (16384)	      A "Yes" button : YesRole.
    QMessageBox.YesToAll 	     0x00008000 (32768)       A "Yes to All" button : YesRole.
    QMessageBox.No 		         0x00010000 (65536)	      A "No" button : NoRole.
    QMessageBox.NoToAll 	     0x00020000 (131072)      A "No to All" button : NoRole.
    QMessageBox.NoButton 	     0x00000000 (0)	          An invalid button.   
    
    
##QtGui.QDialogButtonBox
http://srinikom.github.io/pyside-docs/PySide/QtGui/QDialogButtonBox.html

    The QtGui.QDialogButtonBox class is a widget that presents buttons in a layout that is appropriate to the current widget style.Dialogs and message boxes typically present buttons in a layout that conforms to the interface guidelines for that platform. Invariably, different platforms have different layouts for their dialogs. QtGui.QDialogButtonBox allows a developer to add buttons to it and will automatically use the appropriate layout for the user’s desktop environment.

    Most buttons for a dialog follow certain roles. Such roles include:

        Accepting or rejecting the dialog.
        Asking for help.
        Performing actions on the dialog itself (such as resetting fields or applying changes).

    There can also be alternate ways of dismissing the dialog which may cause destructive results (such as discarding changes).

    ###Using QDialogButtonBox
    There are a couple ways of using QtGui.QDialogButtonBox. One way is to create the buttons (or button texts) yourself and add them to the button box, specifying their role.

        findButton = QPushButton(self.tr("&Find"))
        moreButton = QPushButton(self.tr("&More"))
        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(findButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(moreButton, QDialogButtonBox.ActionRole)

    Alternatively, QtGui.QDialogButtonBox provides several standard buttons (e.g. OK, Cancel, Save) that you can use. They exist as flags so you can OR them together in the constructor.

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    You can mix and match normal buttons and standard buttons.

    When a button is clicked in the button box, the QtGui.QDialogButtonBox.clicked() signal is emitted for the actual button  that is pressed. For convenience, if the button has an AcceptRole, RejectRole, or HelpRole, the QtGui.QDialogButtonBox.accepted(), QtGui.QDialogButtonBox.rejected(), or QtGui.QDialogButtonBox.helpRequested() signals are emitted respectively.

    If you want a specific button to be default you need to call QPushButton.setDefault() on it yourself. However, if there is no default button set and to preserve which button is the default button across platforms when using the QPushButton.autoDefault property, the first push button with the accept role is made the default button when the QtGui.QDialogButtonBox is shown.

    Contains same enumerations as QMessageBox, but with qdialogbuttonbox attribute.
