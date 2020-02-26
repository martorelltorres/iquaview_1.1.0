# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_summary_checklist.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Summary(object):
    def setupUi(self, Summary):
        Summary.setObjectName("Summary")
        Summary.resize(913, 814)
        self.verticalLayout = QtWidgets.QVBoxLayout(Summary)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_summary = QtWidgets.QVBoxLayout()
        self.verticalLayout_summary.setObjectName("verticalLayout_summary")
        self.summary = QtWidgets.QLabel(Summary)
        self.summary.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.summary.setObjectName("summary")
        self.verticalLayout_summary.addWidget(self.summary)
        self.verticalLayout.addLayout(self.verticalLayout_summary)
        self.scrollArea = QtWidgets.QScrollArea(Summary)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollContents = QtWidgets.QWidget()
        self.scrollContents.setGeometry(QtCore.QRect(0, 0, 893, 497))
        self.scrollContents.setObjectName("scrollContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.line = QtWidgets.QFrame(Summary)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.comments_label = QtWidgets.QLabel(Summary)
        self.comments_label.setAlignment(QtCore.Qt.AlignCenter)
        self.comments_label.setObjectName("comments_label")
        self.verticalLayout.addWidget(self.comments_label)
        self.comments_textEdit = QtWidgets.QTextEdit(Summary)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comments_textEdit.sizePolicy().hasHeightForWidth())
        self.comments_textEdit.setSizePolicy(sizePolicy)
        self.comments_textEdit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.comments_textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.comments_textEdit.setLineWidth(5)
        self.comments_textEdit.setObjectName("comments_textEdit")
        self.verticalLayout.addWidget(self.comments_textEdit)
        self.line_2 = QtWidgets.QFrame(Summary)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.save_pushButton = QtWidgets.QPushButton(Summary)
        self.save_pushButton.setObjectName("save_pushButton")
        self.verticalLayout.addWidget(self.save_pushButton)

        self.retranslateUi(Summary)
        QtCore.QMetaObject.connectSlotsByName(Summary)

    def retranslateUi(self, Summary):
        _translate = QtCore.QCoreApplication.translate
        Summary.setWindowTitle(_translate("Summary", "Dialog"))
        self.summary.setText(_translate("Summary", "Summary"))
        self.comments_label.setText(_translate("Summary", "Comments"))
        self.save_pushButton.setText(_translate("Summary", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Summary = QtWidgets.QDialog()
    ui = Ui_Summary()
    ui.setupUi(Summary)
    Summary.show()
    sys.exit(app.exec_())

