# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_timeoutwidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Timeout(object):
    def setupUi(self, Timeout):
        Timeout.setObjectName("Timeout")
        Timeout.resize(94, 37)
        self.gridLayout = QtWidgets.QGridLayout(Timeout)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.timeout_label = QtWidgets.QLabel(Timeout)
        self.timeout_label.setText("")
        self.timeout_label.setObjectName("timeout_label")
        self.horizontalLayout.addWidget(self.timeout_label)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Timeout)
        QtCore.QMetaObject.connectSlotsByName(Timeout)

    def retranslateUi(self, Timeout):
        _translate = QtCore.QCoreApplication.translate
        Timeout.setWindowTitle(_translate("Timeout", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Timeout = QtWidgets.QWidget()
    ui = Ui_Timeout()
    ui.setupUi(Timeout)
    Timeout.show()
    sys.exit(app.exec_())

