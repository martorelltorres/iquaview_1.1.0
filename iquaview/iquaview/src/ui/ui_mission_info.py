# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mission_info.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_missionInfo(object):
    def setupUi(self, missionInfo):
        missionInfo.setObjectName("missionInfo")
        missionInfo.resize(376, 127)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(missionInfo.sizePolicy().hasHeightForWidth())
        missionInfo.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(missionInfo)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(missionInfo)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.last_waypoint_onsurface = QtWidgets.QLabel(missionInfo)
        self.last_waypoint_onsurface.setObjectName("last_waypoint_onsurface")
        self.gridLayout.addWidget(self.last_waypoint_onsurface, 2, 1, 1, 1)
        self.first_waypoint_onsurface = QtWidgets.QLabel(missionInfo)
        self.first_waypoint_onsurface.setObjectName("first_waypoint_onsurface")
        self.gridLayout.addWidget(self.first_waypoint_onsurface, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(missionInfo)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.estimated_time = QtWidgets.QLabel(missionInfo)
        self.estimated_time.setObjectName("estimated_time")
        self.gridLayout.addWidget(self.estimated_time, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(missionInfo)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(missionInfo)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.n_waypoints = QtWidgets.QLabel(missionInfo)
        self.n_waypoints.setObjectName("n_waypoints")
        self.gridLayout.addWidget(self.n_waypoints, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(missionInfo)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.total_distance = QtWidgets.QLabel(missionInfo)
        self.total_distance.setObjectName("total_distance")
        self.gridLayout.addWidget(self.total_distance, 3, 1, 1, 1)

        self.retranslateUi(missionInfo)
        QtCore.QMetaObject.connectSlotsByName(missionInfo)

    def retranslateUi(self, missionInfo):
        _translate = QtCore.QCoreApplication.translate
        missionInfo.setWindowTitle(_translate("missionInfo", "Form"))
        self.label_5.setText(_translate("missionInfo", "Total distance:"))
        self.last_waypoint_onsurface.setText(_translate("missionInfo", "-"))
        self.first_waypoint_onsurface.setText(_translate("missionInfo", "-"))
        self.label_2.setText(_translate("missionInfo", "First waypoint on surface:"))
        self.estimated_time.setText(_translate("missionInfo", "-"))
        self.label.setText(_translate("missionInfo", "No. of waypoints:"))
        self.label_3.setText(_translate("missionInfo", "Estimated total time:"))
        self.n_waypoints.setText(_translate("missionInfo", "-"))
        self.label_4.setText(_translate("missionInfo", "Last waypoint on surface:"))
        self.total_distance.setText(_translate("missionInfo", "-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    missionInfo = QtWidgets.QWidget()
    ui = Ui_missionInfo()
    ui.setupUi(missionInfo)
    missionInfo.show()
    sys.exit(app.exec_())

