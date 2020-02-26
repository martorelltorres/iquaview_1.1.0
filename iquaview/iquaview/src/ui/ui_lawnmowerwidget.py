# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_lawnmowerwidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LawnMowerWidget(object):
    def setupUi(self, LawnMowerWidget):
        LawnMowerWidget.setObjectName("LawnMowerWidget")
        LawnMowerWidget.resize(313, 654)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LawnMowerWidget.sizePolicy().hasHeightForWidth())
        LawnMowerWidget.setSizePolicy(sizePolicy)
        LawnMowerWidget.setMinimumSize(QtCore.QSize(0, 654))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(LawnMowerWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.missionAreaGroupBox = QtWidgets.QGroupBox(LawnMowerWidget)
        self.missionAreaGroupBox.setMinimumSize(QtCore.QSize(0, 245))
        self.missionAreaGroupBox.setMaximumSize(QtCore.QSize(16777215, 245))
        self.missionAreaGroupBox.setStyleSheet("QGroupBox {\n"
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
        self.missionAreaGroupBox.setObjectName("missionAreaGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.missionAreaGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.alongTLength = QtWidgets.QDoubleSpinBox(self.missionAreaGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alongTLength.sizePolicy().hasHeightForWidth())
        self.alongTLength.setSizePolicy(sizePolicy)
        self.alongTLength.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.alongTLength.setMaximum(99999.99)
        self.alongTLength.setObjectName("alongTLength")
        self.gridLayout.addWidget(self.alongTLength, 2, 1, 1, 1)
        self.alongTrackLabel = QtWidgets.QLabel(self.missionAreaGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alongTrackLabel.sizePolicy().hasHeightForWidth())
        self.alongTrackLabel.setSizePolicy(sizePolicy)
        self.alongTrackLabel.setObjectName("alongTrackLabel")
        self.gridLayout.addWidget(self.alongTrackLabel, 2, 0, 1, 1)
        self.acrossTrackLabel = QtWidgets.QLabel(self.missionAreaGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acrossTrackLabel.sizePolicy().hasHeightForWidth())
        self.acrossTrackLabel.setSizePolicy(sizePolicy)
        self.acrossTrackLabel.setObjectName("acrossTrackLabel")
        self.gridLayout.addWidget(self.acrossTrackLabel, 3, 0, 1, 1)
        self.acrossTLength = QtWidgets.QDoubleSpinBox(self.missionAreaGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acrossTLength.sizePolicy().hasHeightForWidth())
        self.acrossTLength.setSizePolicy(sizePolicy)
        self.acrossTLength.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.acrossTLength.setMaximum(99999.99)
        self.acrossTLength.setObjectName("acrossTLength")
        self.gridLayout.addWidget(self.acrossTLength, 3, 1, 1, 1)
        self.automaticExtent = QtWidgets.QRadioButton(self.missionAreaGroupBox)
        self.automaticExtent.setChecked(True)
        self.automaticExtent.setObjectName("automaticExtent")
        self.gridLayout.addWidget(self.automaticExtent, 0, 0, 1, 2)
        self.fixedExtent = QtWidgets.QRadioButton(self.missionAreaGroupBox)
        self.fixedExtent.setObjectName("fixedExtent")
        self.gridLayout.addWidget(self.fixedExtent, 1, 0, 1, 2)
        self.centerOnTargetButton = QtWidgets.QPushButton(self.missionAreaGroupBox)
        self.centerOnTargetButton.setObjectName("centerOnTargetButton")
        self.gridLayout.addWidget(self.centerOnTargetButton, 5, 0, 1, 2)
        self.drawRectangleButton = QtWidgets.QPushButton(self.missionAreaGroupBox)
        self.drawRectangleButton.setObjectName("drawRectangleButton")
        self.gridLayout.addWidget(self.drawRectangleButton, 6, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.missionAreaGroupBox)
        self.transectsGroupBox = QtWidgets.QGroupBox(LawnMowerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transectsGroupBox.sizePolicy().hasHeightForWidth())
        self.transectsGroupBox.setSizePolicy(sizePolicy)
        self.transectsGroupBox.setMinimumSize(QtCore.QSize(0, 390))
        self.transectsGroupBox.setMaximumSize(QtCore.QSize(16777215, 390))
        self.transectsGroupBox.setStyleSheet("QGroupBox {\n"
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
        self.transectsGroupBox.setObjectName("transectsGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.transectsGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.altitudeModeLabel = QtWidgets.QLabel(self.transectsGroupBox)
        self.altitudeModeLabel.setObjectName("altitudeModeLabel")
        self.verticalLayout_2.addWidget(self.altitudeModeLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.depthButton = QtWidgets.QRadioButton(self.transectsGroupBox)
        self.depthButton.setChecked(False)
        self.depthButton.setObjectName("depthButton")
        self.buttonGroup = QtWidgets.QButtonGroup(LawnMowerWidget)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.depthButton)
        self.horizontalLayout_2.addWidget(self.depthButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.zLabel = QtWidgets.QLabel(self.transectsGroupBox)
        self.zLabel.setObjectName("zLabel")
        self.horizontalLayout_2.addWidget(self.zLabel)
        self.depthAltitudeBox = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.depthAltitudeBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.depthAltitudeBox.sizePolicy().hasHeightForWidth())
        self.depthAltitudeBox.setSizePolicy(sizePolicy)
        self.depthAltitudeBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.depthAltitudeBox.setMaximum(9999.99)
        self.depthAltitudeBox.setObjectName("depthAltitudeBox")
        self.horizontalLayout_2.addWidget(self.depthAltitudeBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.altitudeButton = QtWidgets.QRadioButton(self.transectsGroupBox)
        self.altitudeButton.setObjectName("altitudeButton")
        self.buttonGroup.addButton(self.altitudeButton)
        self.verticalLayout_2.addWidget(self.altitudeButton)
        self.alongTrackSpacingLabel = QtWidgets.QLabel(self.transectsGroupBox)
        self.alongTrackSpacingLabel.setObjectName("alongTrackSpacingLabel")
        self.verticalLayout_2.addWidget(self.alongTrackSpacingLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fixedSpace = QtWidgets.QRadioButton(self.transectsGroupBox)
        self.fixedSpace.setObjectName("fixedSpace")
        self.horizontalLayout.addWidget(self.fixedSpace)
        self.alongTSpace = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.alongTSpace.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.alongTSpace.setMaximum(99999.99)
        self.alongTSpace.setObjectName("alongTSpace")
        self.horizontalLayout.addWidget(self.alongTSpace)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.bySensorCoverage = QtWidgets.QRadioButton(self.transectsGroupBox)
        self.bySensorCoverage.setEnabled(False)
        self.bySensorCoverage.setObjectName("bySensorCoverage")
        self.verticalLayout_2.addWidget(self.bySensorCoverage)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.fovLabel = QtWidgets.QLabel(self.transectsGroupBox)
        self.fovLabel.setEnabled(False)
        self.fovLabel.setObjectName("fovLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fovLabel)
        self.fovValue = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.fovValue.setEnabled(False)
        self.fovValue.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.fovValue.setMaximum(99999.99)
        self.fovValue.setObjectName("fovValue")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fovValue)
        self.overlapLabel = QtWidgets.QLabel(self.transectsGroupBox)
        self.overlapLabel.setEnabled(False)
        self.overlapLabel.setObjectName("overlapLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.overlapLabel)
        self.overlapValue = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.overlapValue.setEnabled(False)
        self.overlapValue.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.overlapValue.setMaximum(99999.99)
        self.overlapValue.setObjectName("overlapValue")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.overlapValue)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.acrossTracksLabel = QtWidgets.QLabel(self.transectsGroupBox)
        self.acrossTracksLabel.setObjectName("acrossTracksLabel")
        self.verticalLayout_2.addWidget(self.acrossTracksLabel)
        self.numAcrossTracks = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.numAcrossTracks.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.numAcrossTracks.setMaximum(99999.99)
        self.numAcrossTracks.setObjectName("numAcrossTracks")
        self.verticalLayout_2.addWidget(self.numAcrossTracks)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.speed_label = QtWidgets.QLabel(self.transectsGroupBox)
        self.speed_label.setObjectName("speed_label")
        self.horizontalLayout_4.addWidget(self.speed_label)
        self.speed_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.speed_doubleSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.speed_doubleSpinBox.setSingleStep(0.1)
        self.speed_doubleSpinBox.setProperty("value", 0.5)
        self.speed_doubleSpinBox.setObjectName("speed_doubleSpinBox")
        self.horizontalLayout_4.addWidget(self.speed_doubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tolerance_label = QtWidgets.QLabel(self.transectsGroupBox)
        self.tolerance_label.setObjectName("tolerance_label")
        self.verticalLayout_2.addWidget(self.tolerance_label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.x_label = QtWidgets.QLabel(self.transectsGroupBox)
        self.x_label.setMaximumSize(QtCore.QSize(14, 16777215))
        self.x_label.setObjectName("x_label")
        self.horizontalLayout_3.addWidget(self.x_label)
        self.x_tolerance_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.x_tolerance_doubleSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.x_tolerance_doubleSpinBox.setSingleStep(0.5)
        self.x_tolerance_doubleSpinBox.setProperty("value", 2.0)
        self.x_tolerance_doubleSpinBox.setObjectName("x_tolerance_doubleSpinBox")
        self.horizontalLayout_3.addWidget(self.x_tolerance_doubleSpinBox)
        self.y_label = QtWidgets.QLabel(self.transectsGroupBox)
        self.y_label.setMaximumSize(QtCore.QSize(12, 16777215))
        self.y_label.setObjectName("y_label")
        self.horizontalLayout_3.addWidget(self.y_label)
        self.y_tolerance_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.y_tolerance_doubleSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.y_tolerance_doubleSpinBox.setSingleStep(0.5)
        self.y_tolerance_doubleSpinBox.setProperty("value", 2.0)
        self.y_tolerance_doubleSpinBox.setObjectName("y_tolerance_doubleSpinBox")
        self.horizontalLayout_3.addWidget(self.y_tolerance_doubleSpinBox)
        self.z_label = QtWidgets.QLabel(self.transectsGroupBox)
        self.z_label.setMaximumSize(QtCore.QSize(13, 16777215))
        self.z_label.setObjectName("z_label")
        self.horizontalLayout_3.addWidget(self.z_label)
        self.z_tolerance_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.transectsGroupBox)
        self.z_tolerance_doubleSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.z_tolerance_doubleSpinBox.setSingleStep(0.5)
        self.z_tolerance_doubleSpinBox.setProperty("value", 1.0)
        self.z_tolerance_doubleSpinBox.setObjectName("z_tolerance_doubleSpinBox")
        self.horizontalLayout_3.addWidget(self.z_tolerance_doubleSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.transectsGroupBox)

        self.retranslateUi(LawnMowerWidget)
        QtCore.QMetaObject.connectSlotsByName(LawnMowerWidget)

    def retranslateUi(self, LawnMowerWidget):
        _translate = QtCore.QCoreApplication.translate
        LawnMowerWidget.setWindowTitle(_translate("LawnMowerWidget", "Form"))
        self.missionAreaGroupBox.setTitle(_translate("LawnMowerWidget", "Mission Area"))
        self.alongTrackLabel.setText(_translate("LawnMowerWidget", "Along track"))
        self.acrossTrackLabel.setText(_translate("LawnMowerWidget", "Across track"))
        self.automaticExtent.setText(_translate("LawnMowerWidget", "Automatic extent"))
        self.fixedExtent.setText(_translate("LawnMowerWidget", "Fixed extent "))
        self.centerOnTargetButton.setText(_translate("LawnMowerWidget", "Center on Target"))
        self.drawRectangleButton.setText(_translate("LawnMowerWidget", "Draw Rectangle"))
        self.transectsGroupBox.setTitle(_translate("LawnMowerWidget", "Transects"))
        self.altitudeModeLabel.setText(_translate("LawnMowerWidget", "Altitude mode:"))
        self.depthButton.setText(_translate("LawnMowerWidget", "Depth"))
        self.zLabel.setText(_translate("LawnMowerWidget", "z:"))
        self.altitudeButton.setText(_translate("LawnMowerWidget", "Altitude"))
        self.alongTrackSpacingLabel.setText(_translate("LawnMowerWidget", "Along track spacing:"))
        self.fixedSpace.setText(_translate("LawnMowerWidget", "Fixed space "))
        self.bySensorCoverage.setText(_translate("LawnMowerWidget", "By sensor coverage"))
        self.fovLabel.setText(_translate("LawnMowerWidget", "Sensor field of view:"))
        self.overlapLabel.setText(_translate("LawnMowerWidget", "Desired overlap %"))
        self.acrossTracksLabel.setText(_translate("LawnMowerWidget", "Number of across tracks:"))
        self.speed_label.setText(_translate("LawnMowerWidget", "Speed:"))
        self.tolerance_label.setText(_translate("LawnMowerWidget", "Tolerance:"))
        self.x_label.setText(_translate("LawnMowerWidget", "X:"))
        self.y_label.setText(_translate("LawnMowerWidget", "Y:"))
        self.z_label.setText(_translate("LawnMowerWidget", "Z:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LawnMowerWidget = QtWidgets.QWidget()
    ui = Ui_LawnMowerWidget()
    ui.setupUi(LawnMowerWidget)
    LawnMowerWidget.show()
    sys.exit(app.exec_())

