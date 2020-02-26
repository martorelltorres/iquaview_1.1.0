# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_insert_template_widget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InsertTemplateWidget(object):
    def setupUi(self, InsertTemplateWidget):
        InsertTemplateWidget.setObjectName("InsertTemplateWidget")
        InsertTemplateWidget.resize(316, 230)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InsertTemplateWidget.sizePolicy().hasHeightForWidth())
        InsertTemplateWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(InsertTemplateWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.missionTemplateLabel = QtWidgets.QLabel(InsertTemplateWidget)
        self.missionTemplateLabel.setObjectName("missionTemplateLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.missionTemplateLabel)
        self.templateComboBox = QtWidgets.QComboBox(InsertTemplateWidget)
        self.templateComboBox.setEnabled(True)
        self.templateComboBox.setObjectName("templateComboBox")
        self.templateComboBox.addItem("")
        self.templateComboBox.addItem("")
        self.templateComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.templateComboBox)
        self.insertionPointLabel = QtWidgets.QLabel(InsertTemplateWidget)
        self.insertionPointLabel.setObjectName("insertionPointLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.insertionPointLabel)
        self.insertionPointSpinBox = QtWidgets.QSpinBox(InsertTemplateWidget)
        self.insertionPointSpinBox.setObjectName("insertionPointSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.insertionPointSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.scrollArea = QtWidgets.QScrollArea(InsertTemplateWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.templateWidget = QtWidgets.QWidget()
        self.templateWidget.setGeometry(QtCore.QRect(0, 0, 298, 85))
        self.templateWidget.setObjectName("templateWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.templateWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.templateWidget)
        self.verticalLayout.addWidget(self.scrollArea)
        self.previewTracksButton = QtWidgets.QPushButton(InsertTemplateWidget)
        self.previewTracksButton.setObjectName("previewTracksButton")
        self.verticalLayout.addWidget(self.previewTracksButton)
        self.saveTracksButton = QtWidgets.QPushButton(InsertTemplateWidget)
        self.saveTracksButton.setObjectName("saveTracksButton")
        self.verticalLayout.addWidget(self.saveTracksButton)

        self.retranslateUi(InsertTemplateWidget)
        QtCore.QMetaObject.connectSlotsByName(InsertTemplateWidget)

    def retranslateUi(self, InsertTemplateWidget):
        _translate = QtCore.QCoreApplication.translate
        InsertTemplateWidget.setWindowTitle(_translate("InsertTemplateWidget", "Form"))
        self.missionTemplateLabel.setText(_translate("InsertTemplateWidget", "Mission template:"))
        self.templateComboBox.setItemText(0, _translate("InsertTemplateWidget", "Classic Lawn Mower"))
        self.templateComboBox.setItemText(1, _translate("InsertTemplateWidget", "Spiral Lawn Mower"))
        self.templateComboBox.setItemText(2, _translate("InsertTemplateWidget", "Rectangle Template"))
        self.insertionPointLabel.setText(_translate("InsertTemplateWidget", "Insert before wp:"))
        self.previewTracksButton.setText(_translate("InsertTemplateWidget", "Preview Tracks"))
        self.saveTracksButton.setText(_translate("InsertTemplateWidget", "Save Tracks to Mission"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InsertTemplateWidget = QtWidgets.QWidget()
    ui = Ui_InsertTemplateWidget()
    ui.setupUi(InsertTemplateWidget)
    InsertTemplateWidget.show()
    sys.exit(app.exec_())

