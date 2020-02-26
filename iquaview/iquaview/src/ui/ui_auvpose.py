# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_auvpose.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AUVPosewidget(object):
    def setupUi(self, AUVPosewidget):
        AUVPosewidget.setObjectName("AUVPosewidget")
        AUVPosewidget.resize(302, 220)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AUVPosewidget.sizePolicy().hasHeightForWidth())
        AUVPosewidget.setSizePolicy(sizePolicy)
        AUVPosewidget.setMinimumSize(QtCore.QSize(302, 220))
        self.verticalLayout = QtWidgets.QVBoxLayout(AUVPosewidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connectButton = QtWidgets.QPushButton(AUVPosewidget)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        self.trackwidget = TrackWidget(AUVPosewidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trackwidget.sizePolicy().hasHeightForWidth())
        self.trackwidget.setSizePolicy(sizePolicy)
        self.trackwidget.setMinimumSize(QtCore.QSize(290, 100))
        self.trackwidget.setObjectName("trackwidget")
        self.verticalLayout.addWidget(self.trackwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status_label = QtWidgets.QLabel(AUVPosewidget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout.addWidget(self.status_label)
        self.auv_status_label = QtWidgets.QLabel(AUVPosewidget)
        self.auv_status_label.setMinimumSize(QtCore.QSize(230, 0))
        self.auv_status_label.setText("")
        self.auv_status_label.setObjectName("auv_status_label")
        self.horizontalLayout.addWidget(self.auv_status_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.recovery_action_status_label = QtWidgets.QLabel(AUVPosewidget)
        self.recovery_action_status_label.setText("")
        self.recovery_action_status_label.setObjectName("recovery_action_status_label")
        self.horizontalLayout_3.addWidget(self.recovery_action_status_label)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.depth_label = QtWidgets.QLabel(AUVPosewidget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.depth_label.setFont(font)
        self.depth_label.setObjectName("depth_label")
        self.horizontalLayout_2.addWidget(self.depth_label)
        self.auv_depth_label = QtWidgets.QLabel(AUVPosewidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auv_depth_label.sizePolicy().hasHeightForWidth())
        self.auv_depth_label.setSizePolicy(sizePolicy)
        self.auv_depth_label.setMinimumSize(QtCore.QSize(140, 0))
        self.auv_depth_label.setText("")
        self.auv_depth_label.setObjectName("auv_depth_label")
        self.horizontalLayout_2.addWidget(self.auv_depth_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(AUVPosewidget)
        QtCore.QMetaObject.connectSlotsByName(AUVPosewidget)

    def retranslateUi(self, AUVPosewidget):
        _translate = QtCore.QCoreApplication.translate
        AUVPosewidget.setWindowTitle(_translate("AUVPosewidget", "AUV Pose"))
        self.connectButton.setText(_translate("AUVPosewidget", "Connect"))
        self.status_label.setText(_translate("AUVPosewidget", "Status:"))
        self.depth_label.setText(_translate("AUVPosewidget", "Depth/Altitude:"))

from canvastracks.trackwidget import TrackWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AUVPosewidget = QtWidgets.QWidget()
    ui = Ui_AUVPosewidget()
    ui.setupUi(AUVPosewidget)
    AUVPosewidget.show()
    sys.exit(app.exec_())

