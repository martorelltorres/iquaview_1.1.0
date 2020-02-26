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
 Helper classes to get a valid xml file
"""

import os.path
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import QFileInfo
from iquaview.src.ui.ui_auvconfigxml import Ui_AUVconfigDialog


class ConfigCheckXML(QDialog, Ui_AUVconfigDialog):
    def __init__(self, config):
        super(ConfigCheckXML, self).__init__()
        self.setupUi(self)
        self.config = config
        self.config_filename = config.csettings['configs_path'] + '/' + config.csettings['last_auv_config_xml']
        self.auv_config_lineEdit.setText(config.csettings['last_auv_config_xml'])

        self.auv_config_pushButton.clicked.connect(self.load_auv_config)
        self.buttonBox.accepted.connect(self.on_accept)

    def exists(self):
        """Check if config file exists."""
        exists = os.path.exists(self.config_filename)
        return exists

    def load_auv_config(self):
        """ Open dialog to lad an auv config file."""
        configuration_filename, __ = QFileDialog.getOpenFileName(self, 'AUV configuration',
                                                                 self.config.csettings['last_auv_config_xml'],
                                                                 "AUV configuration(*.xml) ;; All files (*.*)")
        if configuration_filename:
            file_info = QFileInfo(configuration_filename)
            filename = file_info.fileName()

            self.auv_config_lineEdit.setText(str(filename))

    def on_accept(self):
        """ On accept config check xml"""
        exists = os.path.exists(self.config.csettings['configs_path'] + '/' + self.auv_config_lineEdit.text())
        if exists:

            # update config
            self.config.settings['last_auv_config_xml'] = self.auv_config_lineEdit.text()
            self.config.csettings['last_auv_config_xml'] = self.config.settings['last_auv_config_xml']

            self.config.save()
            self.accept()

        else:
            QMessageBox.critical(self.parent(),
                                 "AUV configuration XML Error",
                                 "AUV configuration: " + self.auv_config_lineEdit.text() + " no exist.",
                                 QMessageBox.Close)
