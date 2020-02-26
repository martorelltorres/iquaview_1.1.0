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
 Dialog to configure all the connections to operate the AUV.
 It includes the setup parameters for theconnections to the
 vehicle, gps, usbl and joystick.
"""
from importlib import util
from PyQt5.QtWidgets import QDialog
from iquaview.src.ui.ui_connection_settings import Ui_connectionSettingsDialog


class ConnectionSettingsDlg(QDialog, Ui_connectionSettingsDialog):

    def __init__(self, config, vehicle_info):
        super(ConnectionSettingsDlg, self).__init__()
        self.setupUi(self)
        self.config = config
        self.vehicle_info = vehicle_info

        # Widgets are promoted from QtDesigner
        # self.auv_connection_widget = AUVConnectionWidget(self)
        # self.gps_connection_widget = GPSConnectionWidget(self)
        # self.usbl_connection_widget = USBLConnectionWidget(self)
        if util.find_spec('usblcontroller') is None:
            self.usbl_connection_widget.hide()
            self.resize(300, 50)

        self.closeButton.clicked.connect(self.close)
        self.applyButton.clicked.connect(self.apply_settings)
        self.saveButton.clicked.connect(self.save)

        self.load_settings()

    def load_settings(self):
        self.auv_connection_widget.ip = self.vehicle_info.get_vehicle_ip()
        self.auv_connection_widget.port = self.vehicle_info.get_vehicle_port()

        if self.config.csettings['gps_serial']:
            self.gps_connection_widget.serial_port_clicked(True)
            self.gps_connection_widget.serialPortRadioButton.setChecked(True)
            self.gps_connection_widget.tcp_ip_clicked(False)
            self.gps_connection_widget.TCPRadioButton.setChecked(False)

        else:
            self.gps_connection_widget.serial_port_clicked(False)
            self.gps_connection_widget.serialPortRadioButton.setChecked(False)
            self.gps_connection_widget.tcp_ip_clicked(True)
            self.gps_connection_widget.TCPRadioButton.setChecked(True)

        self.gps_connection_widget.serial_port = self.config.csettings['gps_serial_port']
        self.gps_connection_widget.serial_baudrate = self.config.csettings['gps_serial_baudrate']

        self.gps_connection_widget.ip = self.config.csettings['gps_ip']
        self.gps_connection_widget.hdt_port = self.config.csettings['gps_hdt_port']
        self.gps_connection_widget.gga_port = self.config.csettings['gps_gga_port']

        self.usbl_connection_widget.ip = self.config.csettings['usbl_ip']
        self.usbl_connection_widget.port = self.config.csettings['usbl_port']
        self.usbl_connection_widget.ownid = self.config.csettings['usbl_own_id']
        self.usbl_connection_widget.targetid = self.config.csettings['usbl_target_id']

        self.teleoperation_connection_widget.joystickdevice = self.config.csettings['joystick_device']

    def apply_settings(self):
        if self.valid_parameters():
            self.vehicle_info.set_vehicle_ip(self.auv_connection_widget.ip)
            self.vehicle_info.set_vehicle_port(self.auv_connection_widget.port)
            self.config.csettings['gps_serial'] = self.gps_connection_widget.is_serial()
            if self.config.csettings['gps_serial']:
                self.config.csettings['gps_serial_port'] = self.gps_connection_widget.serial_port
                self.config.csettings['gps_serial_baudrate'] = self.gps_connection_widget.serial_baudrate
            else:
                self.config.csettings['gps_ip'] = self.gps_connection_widget.ip
                self.config.csettings['gps_hdt_port'] = self.gps_connection_widget.hdt_port
                self.config.csettings['gps_gga_port'] = self.gps_connection_widget.gga_port
            self.config.csettings['usbl_ip'] = self.usbl_connection_widget.ip
            self.config.csettings['usbl_port'] = self.usbl_connection_widget.port
            self.config.csettings['usbl_own_id'] = self.usbl_connection_widget.ownid
            self.config.csettings['usbl_target_id'] = self.usbl_connection_widget.targetid
            self.config.csettings['joystick_device'] = self.teleoperation_connection_widget.joystickdevice
            self.close()

    def save(self):
        if self.valid_parameters():
            self.vehicle_info.set_vehicle_ip(self.auv_connection_widget.ip)
            self.vehicle_info.set_vehicle_port(self.auv_connection_widget.port)

            self.config.settings['gps_serial'] = self.gps_connection_widget.is_serial()
            if self.gps_connection_widget.serialPortRadioButton.isChecked():
                self.config.settings['gps_serial_port'] = self.gps_connection_widget.serial_port
                self.config.settings['gps_serial_baudrate'] = self.gps_connection_widget.serial_baudrate
            else:
                self.config.settings['gps_ip'] = self.gps_connection_widget.ip
                self.config.settings['gps_hdt_port'] = self.gps_connection_widget.hdt_port
                self.config.settings['gps_gga_port'] = self.gps_connection_widget.gga_port
            self.config.settings['usbl_ip'] = self.usbl_connection_widget.ip
            self.config.settings['usbl_port'] = self.usbl_connection_widget.port
            self.config.settings['usbl_own_id'] = self.usbl_connection_widget.ownid
            self.config.settings['usbl_target_id'] = self.usbl_connection_widget.targetid
            self.config.csettings['joystick_device'] = self.teleoperation_connection_widget.joystickdevice

            self.vehicle_info.save()
            self.config.save()
            self.apply_settings()

    def valid_parameters(self):
        return (self.auv_connection_widget.is_auv_valid() and
                self.gps_connection_widget.is_gps_valid() and
                self.usbl_connection_widget.is_usbl_valid())
