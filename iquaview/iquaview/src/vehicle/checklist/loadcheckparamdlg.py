"""
Copyright (c) 2018 Iqua Robotics SL

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.
"""

"""
 Classes to load check param dialog
"""

from iquaview.src.ui import ui_param_check
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog


class LoadCheckParamDialog(QDialog, ui_param_check.Ui_Dialog):
    def __init__(self, description, topics, position, ip, port, vehicle_namespace, parent=None):
        super(LoadCheckParamDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Check Parameters")
        self.back_clk = False
        self.back_pushButton.clicked.connect(self.on_click_back)
        self.x_next_pushButton.clicked.connect(self.accept_fail)
        self.x_next_pushButton.setIcon(QtGui.QIcon(":/resources/Red_X.svg"))
        self.tick_next_pushButton.clicked.connect(self.accept_pass)
        self.tick_next_pushButton.setIcon(QtGui.QIcon(":/resources/Green_tick.svg"))
        self.correct_values = False
        self.description.setText(description)
        # self.name.setText(topic_name + ":")
        for topic in topics:
            group_box = QtWidgets.QGroupBox(self)
            group_box.setTitle(topic.name.text)
            group_box.setMinimumSize(QtCore.QSize(285, 150))
            font = QtGui.QFont()
            font.setBold(False)
            font.setWeight(50)
            group_box.setFont(font)
            group_box.setStyleSheet("QGroupBox {\n"
                                    "    border: 1px solid silver;\n"
                                    "    border-radius: 6px;\n"
                                    "    margin-top: 6px;\n"
                                    "}\n"
                                    "\n"
                                    "QGroupBox::title {\n"
                                    "    subcontrol-origin: margin;\n"
                                    "    left: 7px;\n"
                                    "    padding: 0px 5px 0px 5px;\n"
                                    "}")
            group_box.setFlat(False)
            group_box.setObjectName("groupBox")
            vertical_layout = QtWidgets.QVBoxLayout(group_box)
            minimumheight = 50
            fields = topic.get_ct_topic(ip, port, vehicle_namespace)
            for field in fields:
                horizontal_layout_value = QtWidgets.QHBoxLayout()
                horizontal_layout_value.setObjectName("horizontalLayoutValue")
                field_desc = QtWidgets.QLabel(group_box)
                field_desc.setObjectName("field_desc")
                field_desc.setText(field.field_description.text)
                horizontal_layout_value.addWidget(field_desc)
                spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Minimum)
                horizontal_layout_value.addItem(spacer_item)
                line_edit = QtWidgets.QLineEdit(group_box)
                line_edit.setObjectName("lineEdit")
                line_edit.setReadOnly(True)
                line_edit.setMinimumWidth(180)
                if isinstance(field.field_value, float):
                    line_edit.setText("%.9f" % field.field_value)
                elif isinstance(field.field_value, int):
                    line_edit.setText(str(field.field_value))
                else:
                    line_edit.setText(field.field_value)
                horizontal_layout_value.addWidget(line_edit)
                vertical_layout.addLayout(horizontal_layout_value)
                minimumheight += line_edit.height()
            group_box.updateGeometry()
            group_box.setMinimumHeight(minimumheight)
            self.verticalGroupLayout.addWidget(group_box)

        # first dialog
        if position == 0:
            self.back_pushButton.setEnabled(False)
        else:
            self.back_pushButton.setEnabled(True)

    def accept_pass(self):
        self.correct_values = True
        self.accept()

    def accept_fail(self):
        self.correct_values = False
        self.accept()

    def isChecked(self):
        return self.correct_values

    def on_click_back(self):
        self.back_clk = True
        self.accept()

    def back_clicked(self):
        return self.back_clk
