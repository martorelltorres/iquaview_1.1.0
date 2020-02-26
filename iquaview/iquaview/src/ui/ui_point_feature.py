# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_point_feature.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PointFeature(object):
    def setupUi(self, PointFeature):
        PointFeature.setObjectName("PointFeature")
        PointFeature.resize(670, 126)
        self.verticalLayout = QtWidgets.QVBoxLayout(PointFeature)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(PointFeature)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(PointFeature)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMaximumSize(QtCore.QSize(225, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.coordinates_vboxlayout = QtWidgets.QVBoxLayout()
        self.coordinates_vboxlayout.setObjectName("coordinates_vboxlayout")
        self.latitude_layout = QtWidgets.QHBoxLayout()
        self.latitude_layout.setObjectName("latitude_layout")
        self.coordinates_vboxlayout.addLayout(self.latitude_layout)
        self.longitude_layout = QtWidgets.QHBoxLayout()
        self.longitude_layout.setObjectName("longitude_layout")
        self.coordinates_vboxlayout.addLayout(self.longitude_layout)
        self.horizontalLayout.addLayout(self.coordinates_vboxlayout)
        self.getCoordinatesButton = QtWidgets.QPushButton(PointFeature)
        self.getCoordinatesButton.setMaximumSize(QtCore.QSize(27, 16777215))
        self.getCoordinatesButton.setText("")
        self.getCoordinatesButton.setObjectName("getCoordinatesButton")
        self.horizontalLayout.addWidget(self.getCoordinatesButton)
        self.copy_to_clipboardButton = QtWidgets.QPushButton(PointFeature)
        self.copy_to_clipboardButton.setMaximumSize(QtCore.QSize(27, 16777215))
        self.copy_to_clipboardButton.setText("")
        self.copy_to_clipboardButton.setObjectName("copy_to_clipboardButton")
        self.horizontalLayout.addWidget(self.copy_to_clipboardButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(PointFeature)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PointFeature)
        self.buttonBox.accepted.connect(PointFeature.accept)
        self.buttonBox.rejected.connect(PointFeature.reject)
        QtCore.QMetaObject.connectSlotsByName(PointFeature)

    def retranslateUi(self, PointFeature):
        _translate = QtCore.QCoreApplication.translate
        PointFeature.setWindowTitle(_translate("PointFeature", "Point Feature"))
        self.label.setText(_translate("PointFeature", "Enter New Coordinates as \'latitude, longitude\'"))
        self.comboBox.setItemText(0, _translate("PointFeature", "Decimal degrees"))
        self.comboBox.setItemText(1, _translate("PointFeature", "Degrees, minutes"))
        self.comboBox.setItemText(2, _translate("PointFeature", "Degrees, minutes, seconds"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PointFeature = QtWidgets.QDialog()
    ui = Ui_PointFeature()
    ui.setupUi(PointFeature)
    PointFeature.show()
    sys.exit(app.exec_())

