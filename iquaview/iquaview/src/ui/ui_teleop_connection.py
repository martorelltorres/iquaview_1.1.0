# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_teleop_connection.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TeleopConnectionWidget(object):
    def setupUi(self, TeleopConnectionWidget):
        TeleopConnectionWidget.setObjectName("TeleopConnectionWidget")
        TeleopConnectionWidget.resize(303, 88)
        TeleopConnectionWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(TeleopConnectionWidget)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.auv_groupBox = QtWidgets.QGroupBox(TeleopConnectionWidget)
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
        self.joystick_device_label = QtWidgets.QLabel(self.auv_groupBox)
        self.joystick_device_label.setObjectName("joystick_device_label")
        self.horizontalLayout.addWidget(self.joystick_device_label)
        self.joystick_device_text = QtWidgets.QLineEdit(self.auv_groupBox)
        self.joystick_device_text.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.joystick_device_text.sizePolicy().hasHeightForWidth())
        self.joystick_device_text.setSizePolicy(sizePolicy)
        self.joystick_device_text.setObjectName("joystick_device_text")
        self.horizontalLayout.addWidget(self.joystick_device_text)
        self.verticalLayout.addWidget(self.auv_groupBox)

        self.retranslateUi(TeleopConnectionWidget)
        QtCore.QMetaObject.connectSlotsByName(TeleopConnectionWidget)

    def retranslateUi(self, TeleopConnectionWidget):
        _translate = QtCore.QCoreApplication.translate
        TeleopConnectionWidget.setWindowTitle(_translate("TeleopConnectionWidget", "Teleop Connection"))
        self.auv_groupBox.setTitle(_translate("TeleopConnectionWidget", "Teleoperation Connection"))
        self.joystick_device_label.setText(_translate("TeleopConnectionWidget", "Joystick Device:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TeleopConnectionWidget = QtWidgets.QWidget()
    ui = Ui_TeleopConnectionWidget()
    ui.setupUi(TeleopConnectionWidget)
    TeleopConnectionWidget.show()
    sys.exit(app.exec_())

