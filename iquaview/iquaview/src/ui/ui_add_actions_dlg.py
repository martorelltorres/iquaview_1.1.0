# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_actions_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddActionDlg(object):
    def setupUi(self, AddActionDlg):
        AddActionDlg.setObjectName("AddActionDlg")
        AddActionDlg.resize(368, 221)
        self.gridLayout = QtWidgets.QGridLayout(AddActionDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.CancelpushButton = QtWidgets.QPushButton(AddActionDlg)
        self.CancelpushButton.setObjectName("CancelpushButton")
        self.horizontalLayout_3.addWidget(self.CancelpushButton)
        self.OkpushButton = QtWidgets.QPushButton(AddActionDlg)
        self.OkpushButton.setObjectName("OkpushButton")
        self.horizontalLayout_3.addWidget(self.OkpushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.actionlabel = QtWidgets.QLabel(AddActionDlg)
        self.actionlabel.setObjectName("actionlabel")
        self.horizontalLayout_2.addWidget(self.actionlabel)
        self.comboBox = QtWidgets.QComboBox(AddActionDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.descriptionActionlabel = QtWidgets.QLabel(AddActionDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionActionlabel.sizePolicy().hasHeightForWidth())
        self.descriptionActionlabel.setSizePolicy(sizePolicy)
        self.descriptionActionlabel.setScaledContents(True)
        self.descriptionActionlabel.setWordWrap(True)
        self.descriptionActionlabel.setObjectName("descriptionActionlabel")
        self.horizontalLayout.addWidget(self.descriptionActionlabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.parameterslabel = QtWidgets.QLabel(AddActionDlg)
        self.parameterslabel.setObjectName("parameterslabel")
        self.horizontalLayout_4.addWidget(self.parameterslabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.verticalLayout.addLayout(self.formLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(AddActionDlg)
        QtCore.QMetaObject.connectSlotsByName(AddActionDlg)

    def retranslateUi(self, AddActionDlg):
        _translate = QtCore.QCoreApplication.translate
        AddActionDlg.setWindowTitle(_translate("AddActionDlg", "Add Action"))
        self.CancelpushButton.setText(_translate("AddActionDlg", "Cancel"))
        self.OkpushButton.setText(_translate("AddActionDlg", "OK"))
        self.actionlabel.setText(_translate("AddActionDlg", "Action:"))
        self.descriptionActionlabel.setText(_translate("AddActionDlg", "Description"))
        self.parameterslabel.setText(_translate("AddActionDlg", "Parameters:"))

