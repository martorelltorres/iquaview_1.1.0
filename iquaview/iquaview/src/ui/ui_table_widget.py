# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_table_widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName("Table")
        Table.resize(732, 227)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Table.sizePolicy().hasHeightForWidth())
        Table.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Table)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(Table)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(507, 148))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(1, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(2, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("0.0")
        self.tableWidget.setItem(3, 5, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "Form"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Table", "Current Pose"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Table", "Desired Pose"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Table", "Current Twist"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Table", "Desired Twist"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Table", "X"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Table", "Y"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Table", "Z"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Table", "Roll"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Table", "Pitch"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Table", "Yaw"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Table = QtWidgets.QWidget()
    ui = Ui_Table()
    ui.setupUi(Table)
    Table.show()
    sys.exit(app.exec_())

