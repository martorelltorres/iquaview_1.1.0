# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_connection_settings.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_connectionSettingsDialog(object):
    def setupUi(self, connectionSettingsDialog):
        connectionSettingsDialog.setObjectName("connectionSettingsDialog")
        connectionSettingsDialog.resize(333, 487)
        self.verticalLayout = QtWidgets.QVBoxLayout(connectionSettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.auv_connection_widget = AUVConnectionWidget(connectionSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auv_connection_widget.sizePolicy().hasHeightForWidth())
        self.auv_connection_widget.setSizePolicy(sizePolicy)
        self.auv_connection_widget.setMinimumSize(QtCore.QSize(303, 80))
        self.auv_connection_widget.setObjectName("auv_connection_widget")
        self.verticalLayout.addWidget(self.auv_connection_widget)
        self.gps_connection_widget = GPSConnectionWidget(connectionSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gps_connection_widget.sizePolicy().hasHeightForWidth())
        self.gps_connection_widget.setSizePolicy(sizePolicy)
        self.gps_connection_widget.setMinimumSize(QtCore.QSize(303, 225))
        self.gps_connection_widget.setObjectName("gps_connection_widget")
        self.verticalLayout.addWidget(self.gps_connection_widget)
        self.usbl_connection_widget = USBLConnectionWidget(connectionSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usbl_connection_widget.sizePolicy().hasHeightForWidth())
        self.usbl_connection_widget.setSizePolicy(sizePolicy)
        self.usbl_connection_widget.setMinimumSize(QtCore.QSize(303, 110))
        self.usbl_connection_widget.setObjectName("usbl_connection_widget")
        self.verticalLayout.addWidget(self.usbl_connection_widget)
        self.teleoperation_connection_widget = TeleoperationConnectionWidget(connectionSettingsDialog)
        self.teleoperation_connection_widget.setObjectName("teleoperation_connection_widget")
        self.verticalLayout.addWidget(self.teleoperation_connection_widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closeButton = QtWidgets.QPushButton(connectionSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.applyButton = QtWidgets.QPushButton(connectionSettingsDialog)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout.addWidget(self.applyButton)
        self.saveButton = QtWidgets.QPushButton(connectionSettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(connectionSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(connectionSettingsDialog)

    def retranslateUi(self, connectionSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        connectionSettingsDialog.setWindowTitle(_translate("connectionSettingsDialog", "Connection Settings"))
        self.closeButton.setText(_translate("connectionSettingsDialog", "Close"))
        self.applyButton.setText(_translate("connectionSettingsDialog", "Apply"))
        self.saveButton.setText(_translate("connectionSettingsDialog", "Save as Defaults"))

from connection.settings.auvconnectionwidget import AUVConnectionWidget
from connection.settings.gpsconnectionwidget import GPSConnectionWidget
from connection.settings.teleoperationconnectionwidget import TeleoperationConnectionWidget
from connection.settings.usblconnectionwidget import USBLConnectionWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectionSettingsDialog = QtWidgets.QDialog()
    ui = Ui_connectionSettingsDialog()
    ui.setupUi(connectionSettingsDialog)
    connectionSettingsDialog.show()
    sys.exit(app.exec_())

