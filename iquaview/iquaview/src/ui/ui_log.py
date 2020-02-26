# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_log.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Log(object):
    def setupUi(self, Log):
        Log.setObjectName("Log")
        Log.resize(470, 249)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Log)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Log)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(Log)
        QtCore.QMetaObject.connectSlotsByName(Log)

    def retranslateUi(self, Log):
        _translate = QtCore.QCoreApplication.translate
        Log.setWindowTitle(_translate("Log", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Log = QtWidgets.QWidget()
    ui = Ui_Log()
    ui.setupUi(Log)
    Log.show()
    sys.exit(app.exec_())

