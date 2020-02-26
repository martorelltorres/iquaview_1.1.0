# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_auvconfigxml.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AUVconfigDialog(object):
    def setupUi(self, AUVconfigDialog):
        AUVconfigDialog.setObjectName("AUVconfigDialog")
        AUVconfigDialog.resize(404, 104)
        self.verticalLayout = QtWidgets.QVBoxLayout(AUVconfigDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.auv_config_label = QtWidgets.QLabel(AUVconfigDialog)
        self.auv_config_label.setObjectName("auv_config_label")
        self.horizontalLayout.addWidget(self.auv_config_label)
        self.auv_config_lineEdit = QtWidgets.QLineEdit(AUVconfigDialog)
        self.auv_config_lineEdit.setObjectName("auv_config_lineEdit")
        self.horizontalLayout.addWidget(self.auv_config_lineEdit)
        self.auv_config_pushButton = QtWidgets.QPushButton(AUVconfigDialog)
        self.auv_config_pushButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.auv_config_pushButton.setObjectName("auv_config_pushButton")
        self.horizontalLayout.addWidget(self.auv_config_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AUVconfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AUVconfigDialog)
        self.buttonBox.rejected.connect(AUVconfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AUVconfigDialog)

    def retranslateUi(self, AUVconfigDialog):
        _translate = QtCore.QCoreApplication.translate
        AUVconfigDialog.setWindowTitle(_translate("AUVconfigDialog", "Enter valid AUV Configuration file"))
        self.auv_config_label.setText(_translate("AUVconfigDialog", "AUV configuration xml:"))
        self.auv_config_pushButton.setText(_translate("AUVconfigDialog", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AUVconfigDialog = QtWidgets.QDialog()
    ui = Ui_AUVconfigDialog()
    ui.setupUi(AUVconfigDialog)
    AUVconfigDialog.show()
    sys.exit(app.exec_())

