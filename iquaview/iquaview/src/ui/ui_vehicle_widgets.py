# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_vehicle_widgets.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VehicleWidgets(object):
    def setupUi(self, VehicleWidgets):
        VehicleWidgets.setObjectName("VehicleWidgets")
        VehicleWidgets.resize(789, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(VehicleWidgets)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea_widgets = QtWidgets.QScrollArea(VehicleWidgets)
        self.scrollArea_widgets.setWidgetResizable(True)
        self.scrollArea_widgets.setObjectName("scrollArea_widgets")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 769, 280))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea_widgets.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea_widgets)

        self.retranslateUi(VehicleWidgets)
        QtCore.QMetaObject.connectSlotsByName(VehicleWidgets)

    def retranslateUi(self, VehicleWidgets):
        _translate = QtCore.QCoreApplication.translate
        VehicleWidgets.setWindowTitle(_translate("VehicleWidgets", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VehicleWidgets = QtWidgets.QWidget()
    ui = Ui_VehicleWidgets()
    ui.setupUi(VehicleWidgets)
    VehicleWidgets.show()
    sys.exit(app.exec_())

