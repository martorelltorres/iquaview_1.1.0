# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_auvconfigparams.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AUVConfigParamsDlg(object):
    def setupUi(self, AUVConfigParamsDlg):
        AUVConfigParamsDlg.setObjectName("AUVConfigParamsDlg")
        AUVConfigParamsDlg.resize(673, 437)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AUVConfigParamsDlg.sizePolicy().hasHeightForWidth())
        AUVConfigParamsDlg.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(AUVConfigParamsDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(AUVConfigParamsDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.section_comboBox = QtWidgets.QComboBox(AUVConfigParamsDlg)
        self.section_comboBox.setObjectName("section_comboBox")
        self.horizontalLayout_2.addWidget(self.section_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(AUVConfigParamsDlg)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 653, 170))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName("formLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closeButton = QtWidgets.QPushButton(AUVConfigParamsDlg)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.applyButton = QtWidgets.QPushButton(AUVConfigParamsDlg)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout.addWidget(self.applyButton)
        self.saveDefaultButton = QtWidgets.QPushButton(AUVConfigParamsDlg)
        self.saveDefaultButton.setObjectName("saveDefaultButton")
        self.horizontalLayout.addWidget(self.saveDefaultButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AUVConfigParamsDlg)
        QtCore.QMetaObject.connectSlotsByName(AUVConfigParamsDlg)

    def retranslateUi(self, AUVConfigParamsDlg):
        _translate = QtCore.QCoreApplication.translate
        AUVConfigParamsDlg.setWindowTitle(_translate("AUVConfigParamsDlg", "AUV Configuration Parameters"))
        self.label.setText(_translate("AUVConfigParamsDlg", "Section:"))
        self.closeButton.setText(_translate("AUVConfigParamsDlg", "Close"))
        self.applyButton.setText(_translate("AUVConfigParamsDlg", "Apply"))
        self.saveDefaultButton.setText(_translate("AUVConfigParamsDlg", "Save as default"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AUVConfigParamsDlg = QtWidgets.QDialog()
    ui = Ui_AUVConfigParamsDlg()
    ui.setupUi(AUVConfigParamsDlg)
    AUVConfigParamsDlg.show()
    sys.exit(app.exec_())

