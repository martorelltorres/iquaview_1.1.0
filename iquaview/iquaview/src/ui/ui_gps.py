# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gps.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GPSwidget(object):
    def setupUi(self, GPSwidget):
        GPSwidget.setObjectName("GPSwidget")
        GPSwidget.resize(302, 165)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GPSwidget.sizePolicy().hasHeightForWidth())
        GPSwidget.setSizePolicy(sizePolicy)
        GPSwidget.setMinimumSize(QtCore.QSize(302, 165))
        GPSwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(GPSwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connectButton = QtWidgets.QPushButton(GPSwidget)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        self.trackwidget = TrackWidget(GPSwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trackwidget.sizePolicy().hasHeightForWidth())
        self.trackwidget.setSizePolicy(sizePolicy)
        self.trackwidget.setMinimumSize(QtCore.QSize(295, 100))
        self.trackwidget.setObjectName("trackwidget")
        self.verticalLayout.addWidget(self.trackwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status_label = QtWidgets.QLabel(GPSwidget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout.addWidget(self.status_label)
        self.gps_status_label = QtWidgets.QLabel(GPSwidget)
        self.gps_status_label.setMinimumSize(QtCore.QSize(240, 0))
        self.gps_status_label.setText("")
        self.gps_status_label.setObjectName("gps_status_label")
        self.horizontalLayout.addWidget(self.gps_status_label)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GPSwidget)
        QtCore.QMetaObject.connectSlotsByName(GPSwidget)

    def retranslateUi(self, GPSwidget):
        _translate = QtCore.QCoreApplication.translate
        GPSwidget.setWindowTitle(_translate("GPSwidget", "GPS"))
        self.connectButton.setText(_translate("GPSwidget", "Connect"))
        self.status_label.setText(_translate("GPSwidget", "Status:"))

from canvastracks.trackwidget import TrackWidget
import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GPSwidget = QtWidgets.QWidget()
    ui = Ui_GPSwidget()
    ui.setupUi(GPSwidget)
    GPSwidget.show()
    sys.exit(app.exec_())

