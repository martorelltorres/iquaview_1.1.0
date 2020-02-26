# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_usbl_connection.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_USBLConnectionWidget(object):
    def setupUi(self, USBLConnectionWidget):
        USBLConnectionWidget.setObjectName("USBLConnectionWidget")
        USBLConnectionWidget.resize(303, 125)
        self.verticalLayout = QtWidgets.QVBoxLayout(USBLConnectionWidget)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.usbl_groupBox = QtWidgets.QGroupBox(USBLConnectionWidget)
        self.usbl_groupBox.setMinimumSize(QtCore.QSize(285, 85))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.usbl_groupBox.setFont(font)
        self.usbl_groupBox.setStyleSheet("QGroupBox {\n"
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
        self.usbl_groupBox.setFlat(False)
        self.usbl_groupBox.setObjectName("usbl_groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.usbl_groupBox)
        self.verticalLayout_2.setContentsMargins(-1, 19, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontal_layout_ip_2 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_ip_2.setObjectName("horizontal_layout_ip_2")
        self.ip_usbl_label = QtWidgets.QLabel(self.usbl_groupBox)
        self.ip_usbl_label.setObjectName("ip_usbl_label")
        self.horizontal_layout_ip_2.addWidget(self.ip_usbl_label)
        self.ip_usbl_text = QtWidgets.QLineEdit(self.usbl_groupBox)
        self.ip_usbl_text.setEnabled(True)
        self.ip_usbl_text.setObjectName("ip_usbl_text")
        self.horizontal_layout_ip_2.addWidget(self.ip_usbl_text)
        self.port_usbl_label = QtWidgets.QLabel(self.usbl_groupBox)
        self.port_usbl_label.setObjectName("port_usbl_label")
        self.horizontal_layout_ip_2.addWidget(self.port_usbl_label)
        self.port_usbl_text = QtWidgets.QLineEdit(self.usbl_groupBox)
        self.port_usbl_text.setEnabled(True)
        self.port_usbl_text.setMaximumSize(QtCore.QSize(55, 16777215))
        self.port_usbl_text.setObjectName("port_usbl_text")
        self.horizontal_layout_ip_2.addWidget(self.port_usbl_text)
        self.verticalLayout_2.addLayout(self.horizontal_layout_ip_2)
        self.horizontal_layout_ip_3 = QtWidgets.QHBoxLayout()
        self.horizontal_layout_ip_3.setObjectName("horizontal_layout_ip_3")
        self.id_usbl_label = QtWidgets.QLabel(self.usbl_groupBox)
        self.id_usbl_label.setObjectName("id_usbl_label")
        self.horizontal_layout_ip_3.addWidget(self.id_usbl_label)
        self.id_usbl_text = QtWidgets.QLineEdit(self.usbl_groupBox)
        self.id_usbl_text.setEnabled(True)
        self.id_usbl_text.setObjectName("id_usbl_text")
        self.horizontal_layout_ip_3.addWidget(self.id_usbl_text)
        self.targetid_usbl_label = QtWidgets.QLabel(self.usbl_groupBox)
        self.targetid_usbl_label.setObjectName("targetid_usbl_label")
        self.horizontal_layout_ip_3.addWidget(self.targetid_usbl_label)
        self.targetid_usbl_text = QtWidgets.QLineEdit(self.usbl_groupBox)
        self.targetid_usbl_text.setEnabled(True)
        self.targetid_usbl_text.setMaximumSize(QtCore.QSize(41, 16777215))
        self.targetid_usbl_text.setObjectName("targetid_usbl_text")
        self.horizontal_layout_ip_3.addWidget(self.targetid_usbl_text)
        self.verticalLayout_2.addLayout(self.horizontal_layout_ip_3)
        self.verticalLayout.addWidget(self.usbl_groupBox)

        self.retranslateUi(USBLConnectionWidget)
        QtCore.QMetaObject.connectSlotsByName(USBLConnectionWidget)

    def retranslateUi(self, USBLConnectionWidget):
        _translate = QtCore.QCoreApplication.translate
        USBLConnectionWidget.setWindowTitle(_translate("USBLConnectionWidget", "USBL Connection"))
        self.usbl_groupBox.setTitle(_translate("USBLConnectionWidget", "USBL Connection"))
        self.ip_usbl_label.setText(_translate("USBLConnectionWidget", "IP:"))
        self.port_usbl_label.setText(_translate("USBLConnectionWidget", "Port:"))
        self.id_usbl_label.setText(_translate("USBLConnectionWidget", "USBL Id:"))
        self.targetid_usbl_label.setText(_translate("USBLConnectionWidget", "Target Id:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    USBLConnectionWidget = QtWidgets.QWidget()
    ui = Ui_USBLConnectionWidget()
    ui.setupUi(USBLConnectionWidget)
    USBLConnectionWidget.show()
    sys.exit(app.exec_())

