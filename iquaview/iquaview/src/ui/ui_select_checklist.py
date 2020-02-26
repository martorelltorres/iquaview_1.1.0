# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_select_checklist.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChecklistSelector(object):
    def setupUi(self, ChecklistSelector):
        ChecklistSelector.setObjectName("ChecklistSelector")
        ChecklistSelector.resize(301, 80)
        self.verticalLayout = QtWidgets.QVBoxLayout(ChecklistSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkLayout = QtWidgets.QHBoxLayout()
        self.checkLayout.setObjectName("checkLayout")
        self.check_label = QtWidgets.QLabel(ChecklistSelector)
        self.check_label.setObjectName("check_label")
        self.checkLayout.addWidget(self.check_label)
        self.check_list_comboBox = QtWidgets.QComboBox(ChecklistSelector)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_list_comboBox.sizePolicy().hasHeightForWidth())
        self.check_list_comboBox.setSizePolicy(sizePolicy)
        self.check_list_comboBox.setObjectName("check_list_comboBox")
        self.checkLayout.addWidget(self.check_list_comboBox)
        self.verticalLayout.addLayout(self.checkLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChecklistSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ChecklistSelector)
        self.buttonBox.accepted.connect(ChecklistSelector.accept)
        self.buttonBox.rejected.connect(ChecklistSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(ChecklistSelector)

    def retranslateUi(self, ChecklistSelector):
        _translate = QtCore.QCoreApplication.translate
        ChecklistSelector.setWindowTitle(_translate("ChecklistSelector", "Dialog"))
        self.check_label.setText(_translate("ChecklistSelector", "Check List:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChecklistSelector = QtWidgets.QDialog()
    ui = Ui_ChecklistSelector()
    ui.setupUi(ChecklistSelector)
    ChecklistSelector.show()
    sys.exit(app.exec_())

