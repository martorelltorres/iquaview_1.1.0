# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_param_check.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(622, 78)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.description = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.gridLayout.addWidget(self.description, 0, 0, 1, 1)
        self.verticalGroupLayout = QtWidgets.QVBoxLayout()
        self.verticalGroupLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalGroupLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalGroupLayout.setObjectName("verticalGroupLayout")
        self.gridLayout.addLayout(self.verticalGroupLayout, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.back_pushButton = QtWidgets.QPushButton(Dialog)
        self.back_pushButton.setObjectName("back_pushButton")
        self.horizontalLayout.addWidget(self.back_pushButton)
        self.x_next_pushButton = QtWidgets.QPushButton(Dialog)
        self.x_next_pushButton.setObjectName("x_next_pushButton")
        self.horizontalLayout.addWidget(self.x_next_pushButton)
        self.tick_next_pushButton = QtWidgets.QPushButton(Dialog)
        self.tick_next_pushButton.setObjectName("tick_next_pushButton")
        self.horizontalLayout.addWidget(self.tick_next_pushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.description.setText(_translate("Dialog", "description"))
        self.back_pushButton.setText(_translate("Dialog", "Back"))
        self.x_next_pushButton.setText(_translate("Dialog", "Fail"))
        self.tick_next_pushButton.setText(_translate("Dialog", "Pass"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

