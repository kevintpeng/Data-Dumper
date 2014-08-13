# This generates the settings window.
# Please run Sanitize_win.py if you want to run the Data Dumper GUI.

from PyQt4 import QtCore, QtGui, Qt


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class SettingsWindow(QtGui.QWidget):
    def __init__(self, preferences, dumper):
        QtGui.QWidget.__init__(self)
        self.preferences = preferences
        self.dumper = dumper

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(450, 425)
        self.verticalLayout_6 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.database_line = QtGui.QLineEdit(Form)
        self.database_line.setObjectName(_fromUtf8("lineEdit_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.database_line)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.username_line = QtGui.QLineEdit(Form)
        self.username_line.setObjectName(_fromUtf8("lineEdit_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.username_line)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_8)
        self.inference_size_line = QtGui.QLineEdit(Form)
        self.inference_size_line.setObjectName(_fromUtf8("lineEdit_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.inference_size_line)
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_9)
        self.confidence_percent_line = QtGui.QLineEdit(Form)
        self.confidence_percent_line.setObjectName(_fromUtf8("lineEdit_7"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.confidence_percent_line)
        self.host_line = QtGui.QLineEdit(Form)
        self.host_line.setObjectName(_fromUtf8("lineEdit_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.host_line)
        self.verticalLayout_4.addLayout(self.formLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_6.addWidget(self.line)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_8.addWidget(self.label_10)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.blacklist_char = QtGui.QLineEdit(Form)
        self.blacklist_char.setObjectName(_fromUtf8("lineEdit_5"))
        self.horizontalLayout_3.addWidget(self.blacklist_char)
        self.button_add_to_list = QtGui.QPushButton(Form)
        self.button_add_to_list.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_3.addWidget(self.button_add_to_list)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addLayout(self.verticalLayout)

        self.button_add_to_list.clicked.connect(self.add_item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Settings", None))
        self.label.setText(_translate("Form", "Server Setting", None))
        self.label_5.setText(_translate("Form", "Host", None))
        self.label_6.setText(_translate("Form", "Database", None))
        self.database_line.setText(_translate("Form", self.preferences.database, None))
        self.label_7.setText(_translate("Form", "Username", None))
        self.username_line.setText(_translate("Form", self.preferences.username, None))
        self.label_8.setText(_translate("Form", "Inference Size", None))
        self.inference_size_line.setText(_translate("Form", str(self.preferences.inference_size), None))
        self.label_9.setText(_translate("Form", "Confidence %", None))
        self.confidence_percent_line.setText(_translate("Form", str(self.preferences.confidence_percent*100), None))
        self.host_line.setText(_translate("Form", str(self.preferences.host), None))
        self.label_3.setText(_translate("Form", "Sanitizing Blacklist of Characters/Phrases", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        for i in range(len(self.preferences.char_blacklist)):
            self.listWidget.addItem(self.preferences.char_blacklist[i])

        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_10.setText(_translate("Form", "Enter a symbol and press Add to\n"
                                                 "add to the character blacklist.\n"
                                                 "To remove characters, edit the\n"
                                                 "variable CHAR_BLACKLIST in the\n"
                                                 "'settings_default.yaml' file.", None))
        self.button_add_to_list.setText(_translate("Form", "Add to List", None))
        self.host_line.textChanged.connect(self.save_preferences)
        self.database_line.textChanged.connect(self.save_preferences)
        self.username_line.textChanged.connect(self.save_preferences)
        self.confidence_percent_line.textChanged.connect(self.save_preferences)
        self.inference_size_line.textChanged.connect(self.save_preferences)

    # Adds an item to the character blacklist, both in GUI and in data
    def add_item(self):
        if len(self.blacklist_char.text()) == 1:
            for i in range(self.listWidget.count()):
                if self.listWidget.item(i).text() == self.blacklist_char.text():
                    return
            self.listWidget.addItem(self.blacklist_char.text())
        else:
            # Show a popup saying it has to be one character long
            pass

        self.save_preferences()

    # updates the settings' values in memory and rewrite the file
    def save_preferences(self):
        char_blacklist = ""

        for i in range(self.listWidget.count()):
            text = str(self.listWidget.item(i).text())
            if text not in char_blacklist:
                char_blacklist += text
        self.preferences.update_settings(str(self.host_line.text()),
                                         str(self.database_line.text()),
                                         str(self.username_line.text()),
                                         float(str(self.confidence_percent_line.text()))/100,
                                         int(str(self.inference_size_line.text())),
                                         char_blacklist)
        self.preferences.write_settings_file()
