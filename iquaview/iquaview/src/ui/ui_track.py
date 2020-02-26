# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_track.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Track(object):
    def setupUi(self, Track):
        Track.setObjectName("Track")
        Track.resize(299, 98)
        Track.setMinimumSize(QtCore.QSize(0, 0))
        Track.setMaximumSize(QtCore.QSize(299, 98))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Track)
        self.verticalLayout_2.setContentsMargins(0, 9, 0, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.track_groupBox = QtWidgets.QGroupBox(Track)
        self.track_groupBox.setMinimumSize(QtCore.QSize(281, 80))
        self.track_groupBox.setStyleSheet("QGroupBox {\n"
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
        self.track_groupBox.setObjectName("track_groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.track_groupBox)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontal_layout_color = QtWidgets.QHBoxLayout()
        self.horizontal_layout_color.setObjectName("horizontal_layout_color")
        self.label = QtWidgets.QLabel(self.track_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 27))
        self.label.setObjectName("label")
        self.horizontal_layout_color.addWidget(self.label)
        self.save_track_pushButton = QtWidgets.QPushButton(self.track_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_track_pushButton.sizePolicy().hasHeightForWidth())
        self.save_track_pushButton.setSizePolicy(sizePolicy)
        self.save_track_pushButton.setText("")
        self.save_track_pushButton.setObjectName("save_track_pushButton")
        self.horizontal_layout_color.addWidget(self.save_track_pushButton)
        self.verticalLayout.addLayout(self.horizontal_layout_color)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.centerButton = QtWidgets.QPushButton(self.track_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerButton.sizePolicy().hasHeightForWidth())
        self.centerButton.setSizePolicy(sizePolicy)
        self.centerButton.setObjectName("centerButton")
        self.horizontalLayout.addWidget(self.centerButton)
        self.clearTrackButton = QtWidgets.QPushButton(self.track_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearTrackButton.sizePolicy().hasHeightForWidth())
        self.clearTrackButton.setSizePolicy(sizePolicy)
        self.clearTrackButton.setObjectName("clearTrackButton")
        self.horizontalLayout.addWidget(self.clearTrackButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.track_groupBox)

        self.retranslateUi(Track)
        QtCore.QMetaObject.connectSlotsByName(Track)

    def retranslateUi(self, Track):
        _translate = QtCore.QCoreApplication.translate
        Track.setWindowTitle(_translate("Track", "Track"))
        self.track_groupBox.setTitle(_translate("Track", "Display track"))
        self.label.setText(_translate("Track", "Color:"))
        self.centerButton.setText(_translate("Track", "Center and Zoom to Map"))
        self.clearTrackButton.setText(_translate("Track", "Clear Track"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Track = QtWidgets.QWidget()
    ui = Ui_Track()
    ui.setupUi(Track)
    Track.show()
    sys.exit(app.exec_())

