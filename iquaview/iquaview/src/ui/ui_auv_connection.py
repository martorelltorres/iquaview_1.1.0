# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_auv_connection.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AUVConnectionWidget(object):
    def setupUi(self, AUVConnectionWidget):
        AUVConnectionWidget.setObjectName("AUVConnectionWidget")
        AUVConnectionWidget.resize(303, 88)
        AUVConnectionWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(AUVConnectionWidget)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.auv_groupBox = QtWidgets.QGroupBox(AUVConnectionWidget)
        self.auv_groupBox.setMinimumSize(QtCore.QSize(285, 70))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.auv_groupBox.setFont(font)
        self.auv_groupBox.setStyleSheet("QGroupBox {\n"
"    border: 1px solid silver;\n"
"    border-radius: 6px;\n"
"    margin-top: 6px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 7px;\n"
"    padding: 0px 5px 0px 5px;\n"
"}")
        self.auv_groupBox.setFlat(False)
        self.auv_groupBox.setObjectName("auv_groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.auv_groupBox)
        self.horizontalLayout.setContentsMargins(-1, 9, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ip_auv_label = QtWidgets.QLabel(self.auv_groupBox)
        self.ip_auv_label.setObjectName("ip_auv_label")
        self.horizontalLayout.addWidget(self.ip_auv_label)
        self.ip_auv_text = QtWidgets.QLineEdit(self.auv_groupBox)
        self.ip_auv_text.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip_auv_text.sizePolicy().hasHeightForWidth())
        self.ip_auv_text.setSizePolicy(sizePolicy)
        self.ip_auv_text.setObjectName("ip_auv_text")
        self.horizontalLayout.addWidget(self.ip_auv_text)
        self.port_auv_label = QtWidgets.QLabel(self.auv_groupBox)
        self.port_auv_label.setObjectName("port_auv_label")
        self.horizontalLayout.addWidget(self.port_auv_label)
        self.port_auv_text = QtWidgets.QLineEdit(self.auv_groupBox)
        self.port_auv_text.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.port_auv_text.sizePolicy().hasHeightForWidth())
        self.port_auv_text.setSizePolicy(sizePolicy)
        self.port_auv_text.setMaximumSize(QtCore.QSize(55, 16777215))
        self.port_auv_text.setObjectName("port_auv_text")
        self.horizontalLayout.addWidget(self.port_auv_text)
        self.verticalLayout.addWidget(self.auv_groupBox)

        self.retranslateUi(AUVConnectionWidget)
        QtCore.QMetaObject.connectSlotsByName(AUVConnectionWidget)

    def retranslateUi(self, AUVConnectionWidget):
        _translate = QtCore.QCoreApplication.translate
        AUVConnectionWidget.setWindowTitle(_translate("AUVConnectionWidget", "AUV Connection"))
        self.auv_groupBox.setTitle(_translate("AUVConnectionWidget", "AUV Connection"))
        self.ip_auv_label.setText(_translate("AUVConnectionWidget", "IP:"))
        self.port_auv_label.setText(_translate("AUVConnectionWidget", "Port:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AUVConnectionWidget = QtWidgets.QWidget()
    ui = Ui_AUVConnectionWidget()
    ui.setupUi(AUVConnectionWidget)
    AUVConnectionWidget.show()
    sys.exit(app.exec_())

