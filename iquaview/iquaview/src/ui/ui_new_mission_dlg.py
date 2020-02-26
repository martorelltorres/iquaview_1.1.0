# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_new_mission_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewMissionDlg(object):
    def setupUi(self, NewMissionDlg):
        NewMissionDlg.setObjectName("NewMissionDlg")
        NewMissionDlg.resize(400, 103)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewMissionDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nameLabel = QtWidgets.QLabel(NewMissionDlg)
        self.nameLabel.setObjectName("nameLabel")
        self.horizontalLayout.addWidget(self.nameLabel)
        self.nameText = QtWidgets.QLineEdit(NewMissionDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameText.sizePolicy().hasHeightForWidth())
        self.nameText.setSizePolicy(sizePolicy)
        self.nameText.setObjectName("nameText")
        self.horizontalLayout.addWidget(self.nameText)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewMissionDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewMissionDlg)
        self.buttonBox.accepted.connect(NewMissionDlg.accept)
        self.buttonBox.rejected.connect(NewMissionDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(NewMissionDlg)

    def retranslateUi(self, NewMissionDlg):
        _translate = QtCore.QCoreApplication.translate
        NewMissionDlg.setWindowTitle(_translate("NewMissionDlg", "New Mission"))
        self.nameLabel.setText(_translate("NewMissionDlg", "Mission Name:"))

