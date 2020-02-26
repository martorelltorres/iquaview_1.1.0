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

import logging

from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QLabel
from PyQt5.QtGui import QValidator
from iquaview.src.ui.ui_add_actions_dlg import Ui_AddActionDlg
from iquaview.src.mission.missioneditionwidget.definitions import ActionDefinition, ParamDefinition
from iquaview.src.xmlconfighandler.missionactionshandler import MissionActionsHandler
from iquaview.src.utils.textvalidator import (validate_custom_int,
                                              validate_custom_double)
logger = logging.getLogger(__name__)


class Loadaddactiondialog(QDialog, Ui_AddActionDlg):
    def __init__(self, config, parent=None):
        super(Loadaddactiondialog, self).__init__(parent)
        self.setupUi(self)
        self.config = config
        self.action_list = list()
        self.comboBox.currentIndexChanged.connect(self.on_box_changed)
        self.CancelpushButton.clicked.connect(self.on_reject)
        self.OkpushButton.clicked.connect(self.on_accept)
        self.load_mission_actions()

    def get_action_name(self):
        """:return: Get action name."""
        return self.comboBox.currentText()

    def get_description(self):
        """:return: Get description name."""
        return self.descriptionActionlabel.text()

    def get_action_id(self):
        """:return: action id from current action."""
        return self.action_list[self.comboBox.currentIndex()].action_id

    def get_params(self):
        current_action = self.action_list[self.comboBox.currentIndex()]
        for i in range(0, len(current_action.param_list)):
            if isinstance(self.formLayout_2.itemAt(i * 2 + 1).widget(), QLineEdit):
                current_action.param_list[i].value = self.formLayout_2.itemAt(i * 2 + 1).widget().text()
            else:
                current_action.param_list[i].value = self.formLayout_2.itemAt(i * 2 + 1).widget().currentText()

        return current_action.param_list

    def load_mission_actions(self):

        ma_handler = MissionActionsHandler(self.config)
        actions = ma_handler.get_actions()
        self.action_list = list()
        self.comboBox.clear()
        for action in actions:
            act = ActionDefinition()
            logger.debug(action.tag)
            for value in action:
                if value.tag == 'action_name':
                    logger.debug("     {} {}".format(value.tag, value.text))
                    act.action_name = value.text
                elif value.tag == 'action_id':
                    logger.debug("     {} {}".format(value.tag, value.text))
                    act.action_id = value.text
                elif value.tag == 'action_description':
                    logger.debug("     {} {}".format(value.tag, value.text))
                    act.action_description = value.text
                elif value.tag == 'param_list':
                    p_list = list()
                    for param in value:
                        p_name = ma_handler.get_name_from_param(param)
                        p_type = ma_handler.get_type_from_param(param)

                        if p_type == "boolean":
                            p_value = "false"
                        elif p_type == "int":
                            p_value = "0"
                        elif p_type == "unsigned int":
                            p_value = "0"
                        else:
                            p_value = "0.0"
                        p_list.append(ParamDefinition(p_name, p_type, p_value))

                    act.param_list = p_list

            self.action_list.append(act)
            self.comboBox.addItem(act.action_name)

    def on_box_changed(self):
        current_action = self.action_list[self.comboBox.currentIndex()]
        # Clear current widgets of the layout
        for i in reversed(range(self.formLayout_2.count())):
            widget_to_remove = self.formLayout_2.takeAt(i).widget()
            # remove it from the layout list
            self.formLayout_2.removeWidget(widget_to_remove)
            # remove it from the iquaview
            widget_to_remove.setParent(None)

        self.descriptionActionlabel.setText(current_action.action_description)
        if len(current_action.param_list) == 0:
            self.parameterslabel.hide()
        else:
            self.parameterslabel.show()

        for i in range(0, len(current_action.param_list)):
            label = QLabel()
            label.setObjectName("label")
            label.setText(current_action.param_list[i].description)
            # bool
            if current_action.param_list[i].param_type == "boolean":
                combo_box = QComboBox()
                combo_box.setObjectName("comboBox")
                combo_box.addItem("true")
                combo_box.addItem("false")
                if current_action.param_list[i].value == "false":
                    combo_box.setCurrentIndex(1)

                # comboBox.currentIndexChanged.connect(self.onBoxTrueFalseChanged)
                self.formLayout_2.addRow(label, combo_box)
            else:
                line_edit = QLineEdit()
                line_edit.setObjectName("lineEdit")
                line_edit.setText(current_action.param_list[i].value)
                if current_action.param_list[i].param_type == "unsigned int" or current_action.param_list[i].param_type == "int":
                    line_edit.textChanged.connect(self.on_int_text_changed)
                else:
                    line_edit.textChanged.connect(self.on_double_text_changed)
                self.formLayout_2.addRow(label, line_edit)

    def on_double_text_changed(self, string):
        sender = self.sender()
        state = validate_custom_double(sender.text())
        if state == QValidator.Acceptable:
            color = ''  # white
        elif state == QValidator.Intermediate:
            color = '#fff79a'  # yellow
        else:
            color = '#f6989d'  # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def on_int_text_changed(self, string):
        sender = self.sender()
        state = validate_custom_int(sender.text())
        if state == QValidator.Acceptable:
            color = ''  # white
        elif state == QValidator.Intermediate:
            color = '#fff79a'  # yellow
        else:
            color = '#f6989d'  # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def is_acceptable(self):
        is_acceptable = True

        for i in range(0, self.formLayout_2.count(), 2):
            if isinstance(self.formLayout_2.itemAt(i + 1).widget(), QLineEdit):
                state = validate_custom_double(self.formLayout_2.itemAt(i + 1).widget().text())
                if state != QValidator.Acceptable:
                    is_acceptable = False
        return is_acceptable

    def on_accept(self):
        if self.is_acceptable():
            self.accept()

    def on_reject(self):
        self.reject()
