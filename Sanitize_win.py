# This window generates the GUI for the data dumper.
# Created: Wed Jul 09 09:09:09 2014
#      by: Kevin Peng
# See data_dumper_tools and psql_tools for methods that were created for this program

# This is the file that you want to be running to run the data dumper.

from PyQt4 import QtCore, QtGui
import sys

from Settings_win import SettingsWindow
from preferences import Preferences
from data_dumper import DataDumper

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


# GENERATE GUI
# ------------------------------------------------------------------------------------------
# This code creates the GUI and connects the actions to functions in other files and classes


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(613, 370)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.file_in_line = QtGui.QLineEdit(self.centralwidget)
        self.file_in_line.setObjectName(_fromUtf8("file_in_line"))
        self.horizontalLayout.addWidget(self.file_in_line)
        self.open_file_button = QtGui.QPushButton(self.centralwidget)
        self.open_file_button.setObjectName(_fromUtf8("open_file_button"))
        self.horizontalLayout.addWidget(self.open_file_button)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_10)
        self.file_out_line = QtGui.QLineEdit(self.centralwidget)
        self.file_out_line.setObjectName(_fromUtf8("file_out_line"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.file_out_line)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.schema_line = QtGui.QLineEdit(self.centralwidget)
        self.schema_line.setObjectName(_fromUtf8("schema_line"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.schema_line)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.table_line = QtGui.QLineEdit(self.centralwidget)
        self.table_line.setObjectName(_fromUtf8("table_line"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.table_line)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_7)
        self.password_line = QtGui.QLineEdit(self.centralwidget)
        self.password_line.setObjectName(_fromUtf8("password_line"))
        self.password_line.setEchoMode (QtGui.QLineEdit.Password)
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.FieldRole, self.password_line)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.auto_read_checkbox = QtGui.QCheckBox(self.centralwidget)
        self.auto_read_checkbox.setObjectName(_fromUtf8("auto_read_checkbox"))
        self.verticalLayout_2.addWidget(self.auto_read_checkbox)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.read_button = QtGui.QPushButton(self.centralwidget)
        self.read_button.setObjectName(_fromUtf8("read_button"))
        self.verticalLayout_2.addWidget(self.read_button)
        self.sanitize_button = QtGui.QPushButton(self.centralwidget)
        self.sanitize_button.setObjectName(_fromUtf8("sanitize_button"))
        self.verticalLayout_2.addWidget(self.sanitize_button)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_2.addWidget(self.label_8)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 613, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuExport = QtGui.QMenu(self.menuFile)
        self.menuExport.setObjectName(_fromUtf8("menuExport"))
        MainWindow.setMenuBar(self.menubar)
        self.actionSet_Defaults = QtGui.QAction(MainWindow)
        self.actionSet_Defaults.setObjectName(_fromUtf8("actionSet_Defaults"))
        self.actionSave_current_preferences = QtGui.QAction(MainWindow)
        self.actionSave_current_preferences.setObjectName(_fromUtf8("actionSave_current_preferences"))
        self.actionLoad_Preferences = QtGui.QAction(MainWindow)
        self.actionLoad_Preferences.setObjectName(_fromUtf8("actionLoad_Preferences"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionSanitization = QtGui.QAction(MainWindow)
        self.actionSanitization.setObjectName(_fromUtf8("actionSanitization"))
        self.actionPostgreSQL = QtGui.QAction(MainWindow)
        self.actionPostgreSQL.setObjectName(_fromUtf8("actionPostgreSQL"))
        self.actionDjango_Model = QtGui.QAction(MainWindow)
        self.actionDjango_Model.setObjectName(_fromUtf8("actionDjango_Model"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.menuExport.addAction(self.actionPostgreSQL)
        self.menuExport.addAction(self.actionDjango_Model)
        self.menuFile.addAction(self.actionSave_current_preferences)
        self.menuFile.addAction(self.actionLoad_Preferences)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.preferences = Preferences("settings_default.yaml")
        self.file_in_line.setText(self.preferences.file_in)
        self.file_in_line.textChanged.connect(self.update_preferences)
        self.file_out_line.setText(self.preferences.file_in.replace(".csv", "_clean.csv"))
        self.file_out_line.textChanged.connect(self.update_preferences)
        self.password_line.textChanged.connect(self.update_preferences)
        self.schema_line.textChanged.connect(self.update_preferences)
        self.table_line.textChanged.connect(self.update_preferences)

        MainWindow.setWindowTitle(_translate("MainWindow", "THE DATA DUMPER!!!", None))
        self.dumper = DataDumper()
        self.actionDjango_Model.triggered.connect(self.press_django)
        self.actionPostgreSQL.triggered.connect(self.press_postgres)
        self.actionSettings.triggered.connect(self.show_settings)
        self.label.setText(_translate("MainWindow", "File Input", None))
        self.open_file_button.setText(_translate("MainWindow", "Open File", None))
        self.open_file_button.clicked.connect(self.selectFile)
        self.label_10.setText(_translate("MainWindow", "File Output", None))
        self.label_2.setText(_translate("MainWindow", "Schema", None))
        self.label_3.setText(_translate("MainWindow", "Table", None))
        self.label_7.setText(_translate("MainWindow", "Password", None))
        self.auto_read_checkbox.setText(_translate("MainWindow", "Create a mapping if it does not exist.", None))
        self.label_8.setText(_translate("MainWindow", "If there is an error, it will appear here.", None))
        self.sanitize_button.setText(_translate("MainWindow", "Sanitize .csv", None))
        self.sanitize_button.clicked.connect(self.press_sanitize)
        self.read_button.setText(_translate("MainWindow", "Map .csv / Overwrite Current Mapping", None))
        self.read_button.clicked.connect(self.press_csv_map)
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuExport.setTitle(_translate("MainWindow", "Export", None))
        self.actionSet_Defaults.setText(_translate("MainWindow", "Defaults", None))
        self.actionSave_current_preferences.setText(_translate("MainWindow", "Save Preferences", None))
        self.actionLoad_Preferences.setText(_translate("MainWindow", "Load Preferences", None))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences", None))
        self.actionSanitization.setText(_translate("MainWindow", "Sanitization", None))
        self.actionPostgreSQL.setText(_translate("MainWindow", "PostgreSQL", None))
        self.actionDjango_Model.setText(_translate("MainWindow", "Django Model", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))

    # GUI FUNCTIONS
    # ---------------------------------------------------------------------------------------

    # Generates the settings window
    def show_settings(self):
        self.settings = SettingsWindow(self.dumper.preferences,self.dumper)
        self.settings.setupUi(self.settings)
        self.settings.show()

    # This is passed to all the methods in data_dumper, lets the functions change the status.
    def set_status(self, status_string):
        self.label_8.setText(status_string)

    # returns T/F if the checkbox is checked or not
    def checked_is_true(self):
        if self.auto_read_checkbox.isChecked():
            return True
        else:
            return False

    # All of the press_------- functions call the data dumper functions and pass functions to them
    def press_csv_map(self):
        self.dumper.csv_map(self.set_status, self.checked_is_true())

    def press_sanitize(self):
        self.dumper.csv_sanitize(self.set_status, self.checked_is_true())

    def press_django(self):
        self.dumper.create_django_model(self.set_status, self.checked_is_true())

    def press_postgres(self):
        self.dumper.create_postgres(self.set_status, self.checked_is_true())

    # Called every time a text field is changed.
    def update_preferences(self):
        self.dumper.preferences.check_fields(self.file_in_line.text(),
                                        self.file_out_line.text(),
                                        self.schema_line.text(),
                                        self.table_line.text(),
                                        self.password_line.text())

    # Adds functionality to the open button window
    def selectFile(self):
        string = QtGui.QFileDialog.getOpenFileName()
        if string != "":
            self.file_in_line.setText(string)
            self.file_out_line.setText(str(string).replace(".csv", "_clean.csv"))
        self.update_preferences()

'''
This is code that I had to add
from "file name" import "class name"
if it is a main window, change from QWidget to QMainWindow
'''
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QMainWindow()
    ui = MainWindow()
    ui.setupUi(Form)

    Form.show()
    sys.exit(app.exec_())