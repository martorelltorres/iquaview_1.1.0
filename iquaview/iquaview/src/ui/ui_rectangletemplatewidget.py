# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rectangletemplatewidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RectangleTemplateWidget(object):
    def setupUi(self, RectangleTemplateWidget):
        RectangleTemplateWidget.setObjectName("RectangleTemplateWidget")
        RectangleTemplateWidget.resize(304, 555)
        self.verticalLayout = QtWidgets.QVBoxLayout(RectangleTemplateWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.missionAreaGroupBox = QtWidgets.QGroupBox(RectangleTemplateWidget)
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
        self.verticalLayout.addWidget(self.missionAreaGroupBox)
        self.InitialPointgroupBox = QtWidgets.QGroupBox(RectangleTemplateWidget)
        self.InitialPointgroupBox.setMinimumSize(QtCore.QSize(0, 70))
        self.InitialPointgroupBox.setMaximumSize(QtCore.QSize(16777215, 75))
        self.InitialPointgroupBox.setStyleSheet("QGroupBox {\n"
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
        self.InitialPointgroupBox.setObjectName("InitialPointgroupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.InitialPointgroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.initial_point_label = QtWidgets.QLabel(self.InitialPointgroupBox)
        self.initial_point_label.setObjectName("initial_point_label")
        self.horizontalLayout.addWidget(self.initial_point_label)
        self.initial_point_comboBox = QtWidgets.QComboBox(self.InitialPointgroupBox)
        self.initial_point_comboBox.setObjectName("initial_point_comboBox")
        self.initial_point_comboBox.addItem("")
        self.initial_point_comboBox.addItem("")
        self.initial_point_comboBox.addItem("")
        self.initial_point_comboBox.addItem("")
        self.horizontalLayout.addWidget(self.initial_point_comboBox)
        self.verticalLayout.addWidget(self.InitialPointgroupBox)
        self.transectsGroupBox = QtWidgets.QGroupBox(RectangleTemplateWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transectsGroupBox.sizePolicy().hasHeightForWidth())
        self.transectsGroupBox.setSizePolicy(sizePolicy)
        self.transectsGroupBox.setMinimumSize(QtCore.QSize(0, 210))
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
        self.verticalLayout_2.addWidget(self.altitudeButton)
        self.line = QtWidgets.QFrame(self.transectsGroupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
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
        self.verticalLayout.addWidget(self.transectsGroupBox)

        self.retranslateUi(RectangleTemplateWidget)
        QtCore.QMetaObject.connectSlotsByName(RectangleTemplateWidget)

    def retranslateUi(self, RectangleTemplateWidget):
        _translate = QtCore.QCoreApplication.translate
        RectangleTemplateWidget.setWindowTitle(_translate("RectangleTemplateWidget", "Form"))
        self.missionAreaGroupBox.setTitle(_translate("RectangleTemplateWidget", "Mission Area"))
        self.alongTrackLabel.setText(_translate("RectangleTemplateWidget", "Along track"))
        self.acrossTrackLabel.setText(_translate("RectangleTemplateWidget", "Across track"))
        self.automaticExtent.setText(_translate("RectangleTemplateWidget", "Automatic extent"))
        self.fixedExtent.setText(_translate("RectangleTemplateWidget", "Fixed extent "))
        self.centerOnTargetButton.setText(_translate("RectangleTemplateWidget", "Center on Target"))
        self.drawRectangleButton.setText(_translate("RectangleTemplateWidget", "Draw Rectangle"))
        self.InitialPointgroupBox.setTitle(_translate("RectangleTemplateWidget", "Define Initial Point"))
        self.initial_point_label.setText(_translate("RectangleTemplateWidget", "Initial Point:"))
        self.initial_point_comboBox.setItemText(0, _translate("RectangleTemplateWidget", "First Corner"))
        self.initial_point_comboBox.setItemText(1, _translate("RectangleTemplateWidget", "Second Corner"))
        self.initial_point_comboBox.setItemText(2, _translate("RectangleTemplateWidget", "Third Corner"))
        self.initial_point_comboBox.setItemText(3, _translate("RectangleTemplateWidget", "Fourth Corner"))
        self.transectsGroupBox.setTitle(_translate("RectangleTemplateWidget", "Transects"))
        self.altitudeModeLabel.setText(_translate("RectangleTemplateWidget", "Altitude mode:"))
        self.depthButton.setText(_translate("RectangleTemplateWidget", "Depth"))
        self.zLabel.setText(_translate("RectangleTemplateWidget", "z:"))
        self.altitudeButton.setText(_translate("RectangleTemplateWidget", "Altitude"))
        self.speed_label.setText(_translate("RectangleTemplateWidget", "Speed:"))
        self.tolerance_label.setText(_translate("RectangleTemplateWidget", "Tolerance:"))
        self.x_label.setText(_translate("RectangleTemplateWidget", "X:"))
        self.y_label.setText(_translate("RectangleTemplateWidget", "Y:"))
        self.z_label.setText(_translate("RectangleTemplateWidget", "Z:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RectangleTemplateWidget = QtWidgets.QWidget()
    ui = Ui_RectangleTemplateWidget()
    ui.setupUi(RectangleTemplateWidget)
    RectangleTemplateWidget.show()
    sys.exit(app.exec_())

