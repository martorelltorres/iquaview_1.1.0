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
 Dialog to configure app.config parameters.
 It includes last_auv_config_xml, remote_missions_path, user, coordinate display.
"""

import sys
import os
import os.path
import logging

from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QFileInfo, QDir
from iquaview.src.ui.ui_options import Ui_OptionsDialog

logger = logging.getLogger(__name__)


class OptionsDlg(QDialog, Ui_OptionsDialog):
    def __init__(self, config, vehicle_info):
        super(OptionsDlg, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Options")
        self.config = config
        self.vehicle_info = vehicle_info

        self.auv_config_pushButton.clicked.connect(self.load_auv_config)
        self.buttonBox.accepted.connect(self.on_accept)

        self.auv_config_lineEdit.setText(self.config.csettings['last_auv_config_xml'])
        self.path_rm_lineEdit.setText(self.vehicle_info.get_remote_mission_path())
        self.user_rm_lineEdit.setText(self.vehicle_info.get_vehicle_user())
        self.ip_rm_label.setText("@" + self.vehicle_info.get_vehicle_ip() + ":")

        self.set_coordinate_combobox()
        self.set_vessel_canvas_marker_mode()

    def set_vessel_canvas_marker_mode(self):
        """
        Set canvas marker mode

        """
        canvas_marker_mode = self.config.csettings['canvas_marker_mode']
        if canvas_marker_mode == "auto":
            self.auto_canvasmarker_radioButton.setChecked(True)
        else:
            self.manual_canvasmarker_radioButton.setChecked(True)

        canvas_marker_scale = self.config.csettings['canvas_marker_scale']
        self.changingscale_spinBox.setValue(canvas_marker_scale)

    def set_coordinate_combobox(self):
        """
        Set coordinate format on coordinate combobox
        """
        coordinate_format = self.config.csettings['coordinate_format']
        if coordinate_format == "degree":
            self.coordinate_comboBox.setCurrentIndex(0)
        elif coordinate_format == "degree_minute":
            self.coordinate_comboBox.setCurrentIndex(1)
        else:
            self.coordinate_comboBox.setCurrentIndex(2)

    def load_auv_config(self):
        """Open dialog to load auv config"""
        configuration_filename, __ = QFileDialog.getOpenFileName(self, 'AUV configuration',
                                                                 QDir.homePath(),
                                                                 "AUV configuration(*.xml) ;; All files (*.*)",
                                                                 QDir.homePath())
        if configuration_filename:
            file_info = QFileInfo(configuration_filename)
            filename = file_info.fileName()

            self.auv_config_lineEdit.setText(str(filename))

    def on_accept(self):

        exists = os.path.exists(self.config.csettings['configs_path'] + '/' + self.auv_config_lineEdit.text())
        if exists:
            reply = QMessageBox.No
            if self.auv_config_lineEdit.text() != self.config.settings['last_auv_config_xml']:
                message = "AUV configuration xml changed. Do you want to restart Iquaview?"
                reply = QMessageBox.question(self, 'Restart Confirmation', message, QMessageBox.Yes, QMessageBox.No)

            # update config
            self.config.settings['last_auv_config_xml'] = self.auv_config_lineEdit.text()
            if self.coordinate_comboBox.currentIndex() == 0:
                self.config.settings['coordinate_format'] = 'degree'
            elif self.coordinate_comboBox.currentIndex() == 1:
                self.config.settings['coordinate_format'] = 'degree_minute'
            else:
                self.config.settings['coordinate_format'] = 'degree_minute_second'

            self.config.csettings['last_auv_config_xml'] = self.config.settings['last_auv_config_xml']
            self.config.csettings['coordinate_format'] = self.config.settings['coordinate_format']

            if self.auto_canvasmarker_radioButton.isChecked():
                self.config.settings['canvas_marker_mode'] = 'auto'
            else:
                self.config.settings['canvas_marker_mode'] = 'manual'
                self.config.settings['canvas_marker_scale'] = int(self.changingscale_spinBox.value())

            self.config.csettings['canvas_marker_mode'] = self.config.settings['canvas_marker_mode']
            self.config.csettings['canvas_marker_scale'] = self.config.settings['canvas_marker_scale']

            self.config.save()

            self.vehicle_info.read_xml()
            # update vehicle info
            self.vehicle_info.set_remote_mission_path(self.path_rm_lineEdit.text())
            self.vehicle_info.set_user(self.user_rm_lineEdit.text())

            self.vehicle_info.save()

            if reply == QMessageBox.Yes:
                logger.info("argv was {}".format(sys.argv))
                logger.info("sys.executable was {}".format(sys.executable))
                logger.info("restart now")

                os.execv(sys.executable, ['python3'] + sys.argv)

            self.accept()

        else:
            QMessageBox.critical(self.parent(),
                                 "AUV configuration XML Error",
                                 "AUV configuration: " + self.auv_config_lineEdit.text() + " no exist.",
                                 QMessageBox.Close)
