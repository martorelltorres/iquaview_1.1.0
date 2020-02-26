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
 Dialog to configure AUV parameters, grouped in different sections.
 The dialog is dynamically created according to the items defined under the tag ros_params
 in the auv configuration xml file.
"""

import time
import logging

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QMessageBox, QWidget
from PyQt5.QtGui import QValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp, QEvent, pyqtSignal

from iquaview.src.ui.ui_auvconfigparams import Ui_AUVConfigParamsDlg
from iquaview.src.xmlconfighandler.rosparamsreader import RosParamsReader
from iquaview.src.cola2api import cola2_interface
from iquaview.src.utils.textvalidator import get_custom_double_validator

logger = logging.getLogger(__name__)


class AUVConfigParamsDlg(QDialog, Ui_AUVConfigParamsDlg):
    applied_changes = pyqtSignal()

    def __init__(self, config, vehicle_info, parent=None):
        super(AUVConfigParamsDlg, self).__init__(parent)
        self.setupUi(self)
        self.config = config
        self.vehicle_info = vehicle_info
        self.rosparamsreader = None
        self.sections = None
        self.changes = False
        self.current_index = 0
        self.ip = self.vehicle_info.get_vehicle_ip()
        self.port = 9091
        self.vehicle_namespace = self.vehicle_info.get_vehicle_namespace()
        # install event filter to catch wheel event
        self.section_comboBox.installEventFilter(self)

        self.closeButton.clicked.connect(self.close)
        self.applyButton.clicked.connect(self.apply_params)
        self.saveDefaultButton.clicked.connect(self.save_params)
        self.section_comboBox.currentIndexChanged.connect(self.update_params_form)

    def init(self):
        """
        Initialize RosParamsReader and load multiple sections
        """
        self.changes = False

        self.rosparamsreader = RosParamsReader(self.config,
                                               self.ip,
                                               9091,
                                               self.vehicle_namespace)
        self.load_sections()

    def load_sections(self):
        """
        Read xml configuration and load sections
        """
        self.sections = self.rosparamsreader.read_configuration()
        self.section_comboBox.clear()
        for section in self.sections:
            self.section_comboBox.addItem(section.get_description())

    def update_params_form(self):
        """
        Updates the params form
        """
        success = True
        index = self.section_comboBox.currentIndex()

        if self.changes:
            reply = QMessageBox.question(self, 'Apply changes confirmation',
                                         "Some changes have not been applied. Do you want to apply them?",
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.apply_params()

            else:
                self.changes = False
                self.load_sections()

        if success:
            self.current_index = index
            self.current_section = self.sections[self.current_index]
            self.section_comboBox.setCurrentIndex(self.current_index)
            form_layout = self.scrollAreaWidgetContents.layout()
            # Clear current widgets of the layout
            for i in reversed(range(form_layout.count())):
                widget_to_remove = form_layout.takeAt(i).widget()
                # remove it from the layout list
                form_layout.removeWidget(widget_to_remove)
                # remove it from the iquaview
                widget_to_remove.setParent(None)

            # Put new widgets in the form
            n_param = 0
            for param in self.current_section.get_params():
                label_param = QLabel(self.scrollAreaWidgetContents)
                label_param.setText(param.get_description() + ":")
                if not param.is_array() and param.get_type() == "boolean":
                    combo_box = QComboBox(self.scrollAreaWidgetContents)
                    combo_box.installEventFilter(self)
                    combo_box.setObjectName(str(n_param))
                    combo_box.addItem("true")
                    combo_box.addItem("false")
                    if param.get_value() == "false":
                        combo_box.setCurrentIndex(1)
                    form_layout.addRow(label_param, combo_box)
                    combo_box.currentIndexChanged.connect(self.on_box_changed)
                else:

                    line_edit_param = QLineEdit(self.scrollAreaWidgetContents)
                    line_edit_param.setObjectName(str(n_param))
                    line_edit_param.textChanged.connect(self.on_text_changed)
                    line_edit_param.setText(param.get_value())
                    form_layout.addRow(label_param, line_edit_param)
                n_param = n_param + 1

            self.changes = False

        else:
            self.changes = False
            self.section_comboBox.setCurrentIndex(self.current_index)
            self.changes = True

    def eventFilter(self, source, event):
        # event filter to ignore wheel on combobox
        if (event.type() == QEvent.Wheel and
                isinstance(source, QComboBox)):
            event.ignore()
            return True
        else:
            return QWidget.eventFilter(self, source, event)

    def on_text_changed(self, string):
        """
        Check if 'string' is valid
        :param string: value of the field
        """
        sender = self.sender()
        params = self.current_section.get_params()
        params[int(sender.objectName())].set_value(string)
        # check lines correct

        state = self.check_param(params[int(sender.objectName())])
        if state == QValidator.Acceptable:
            color = ''  # white
        elif state == QValidator.Intermediate:
            color = '#fff79a'  # yellow
        else:
            color = '#f6989d'  # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        self.changes = True

    def on_box_changed(self, i):
        """
        Check if 'i' is valid
        :param i: value of the field
        """
        sender = self.sender()
        params = self.current_section.get_params()
        params[int(sender.objectName())].set_value(sender.itemText(i))
        self.changes = True

    def check_param(self, param):
        """
        Check if 'param' is valid
        :param param: value of the field
        """
        # double
        if not param.is_array() and param.get_type() == "double":
            # double validator
            validator = get_custom_double_validator()

        # double array
        elif param.is_array() and param.get_type() == "double":
            string = ""
            # dinamic regular expresion
            for x in range(0, int(param.get_array_size())):
                if x == int(param.get_array_size()) - 1:
                    string += "-?[\\d\\.]*"
                else:
                    string += "-?[\\d\\.]*,\s*"
            regexp = QRegExp("\\[" + string + "\\]")
            validator = QRegExpValidator(regexp)

            # boolean array
        elif param.is_array() and param.get_type() == "boolean":
            string = ""
            # dinamic regular expresion
            for x in range(0, int(param.get_array_size())):
                if x == int(param.get_array_size()) - 1:
                    string += "(true|false)"
                else:
                    string += "(true|false),\s*"
            regexp = QRegExp("\\[" + string + "\\]")
            validator = QRegExpValidator(regexp)

        state = validator.validate(param.get_value(), 0)[0]
        return state

    def are_values_acceptable(self):
        """
        Check if the values are acceptable
        :return: return True if all the values are acceptable, otherwise False
        """
        is_acceptable = True
        for param in self.current_section.get_params():
            # only check lineedits
            if not (not param.is_array() and param.get_type() == "boolean"):
                # check param in lineEdit
                state = self.check_param(param)
                if state != QValidator.Acceptable:
                    is_acceptable = False
        return is_acceptable

    def apply_params(self):
        """ Apply params"""
        try:
            if self.are_values_acceptable():
                logger.info("Applying parameters")
                for param in self.current_section.get_params():
                    cola2_interface.set_ros_param(self.ip, self.port, self.vehicle_namespace + param.get_name(),
                                                  param.get_value())
                time.sleep(1.0)
                # action_id
                logger.info(
                    "sending action service:  %s Param: %s " % (self.current_section.get_action_id(), param.get_name()))
                result = cola2_interface.send_empty_service(self.ip, self.port,
                                                            self.vehicle_namespace + self.current_section.get_action_id())
                logger.info("Result: %s" % result)
                self.changes = False
                self.applied_changes.emit()
                return True

            else:
                logger.warning("It has not been possible to apply changes")
                raise Exception("It has not been possible to apply changes. \
                                 Please review the values of the parameters.")

        except ConnectionRefusedError:
            logger.error("Applying parameters failed")
            QMessageBox.critical(self,
                                 "Applying parameters failed",
                                 "Connection Refused",
                                 QMessageBox.Close)
        except Exception as e:
            logger.error("Applying parameters failed")
            QMessageBox.critical(self,
                                 "Applying parameters failed",
                                 e.args[0],
                                 QMessageBox.Close)

    def save_params(self):
        """ Save Params"""
        save_msg = "Are you sure you want to save all the parameters as defaults?"
        reply = QMessageBox.question(self, 'Saving Confirmation',
                                     save_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # apply params
                self.apply_params()
                logger.info("Saving parameters as defaults...")
                # TODO: update to new cola2
                string = "/default_param_handler/update_params_in_yamls"
                cola2_interface.send_empty_service(self.ip, self.port,
                                                   self.vehicle_namespace + string)

            except ConnectionRefusedError:
                logger.error("Saving parameters failed")
                QMessageBox.critical(self,
                                     "Saving parameters failed",
                                     "Connection Refused",
                                     QMessageBox.Close)
        else:
            logger.info("Parameters not saved")
