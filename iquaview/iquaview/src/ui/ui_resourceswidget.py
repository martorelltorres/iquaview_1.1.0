# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_resourceswidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ResourcesWidget(object):
    def setupUi(self, ResourcesWidget):
        ResourcesWidget.setObjectName("ResourcesWidget")
        ResourcesWidget.resize(134, 80)
        ResourcesWidget.setMaximumSize(QtCore.QSize(160, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(ResourcesWidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.usages_layout = QtWidgets.QGridLayout()
        self.usages_layout.setObjectName("usages_layout")
        self.ram_usage_label = QtWidgets.QLabel(ResourcesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ram_usage_label.sizePolicy().hasHeightForWidth())
        self.ram_usage_label.setSizePolicy(sizePolicy)
        self.ram_usage_label.setObjectName("ram_usage_label")
        self.usages_layout.addWidget(self.ram_usage_label, 1, 1, 1, 1)
        self.cpu_text_label = QtWidgets.QLabel(ResourcesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cpu_text_label.sizePolicy().hasHeightForWidth())
        self.cpu_text_label.setSizePolicy(sizePolicy)
        self.cpu_text_label.setObjectName("cpu_text_label")
        self.usages_layout.addWidget(self.cpu_text_label, 0, 0, 1, 1)
        self.ram_text_label = QtWidgets.QLabel(ResourcesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ram_text_label.sizePolicy().hasHeightForWidth())
        self.ram_text_label.setSizePolicy(sizePolicy)
        self.ram_text_label.setObjectName("ram_text_label")
        self.usages_layout.addWidget(self.ram_text_label, 1, 0, 1, 1)
        self.cpu_usage_label = QtWidgets.QLabel(ResourcesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cpu_usage_label.sizePolicy().hasHeightForWidth())
        self.cpu_usage_label.setSizePolicy(sizePolicy)
        self.cpu_usage_label.setObjectName("cpu_usage_label")
        self.usages_layout.addWidget(self.cpu_usage_label, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.usages_layout, 2, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.battery_layout = QtWidgets.QVBoxLayout()
        self.battery_layout.setObjectName("battery_layout")
        self.gridLayout.addLayout(self.battery_layout, 1, 0, 1, 2)

        self.retranslateUi(ResourcesWidget)
        QtCore.QMetaObject.connectSlotsByName(ResourcesWidget)

    def retranslateUi(self, ResourcesWidget):
        _translate = QtCore.QCoreApplication.translate
        ResourcesWidget.setWindowTitle(_translate("ResourcesWidget", "Form"))
        self.ram_usage_label.setText(_translate("ResourcesWidget", "    %"))
        self.cpu_text_label.setText(_translate("ResourcesWidget", "CPU usage:"))
        self.ram_text_label.setText(_translate("ResourcesWidget", "RAM usage:"))
        self.cpu_usage_label.setText(_translate("ResourcesWidget", "    %"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ResourcesWidget = QtWidgets.QWidget()
    ui = Ui_ResourcesWidget()
    ui.setupUi(ResourcesWidget)
    ResourcesWidget.show()
    sys.exit(app.exec_())

