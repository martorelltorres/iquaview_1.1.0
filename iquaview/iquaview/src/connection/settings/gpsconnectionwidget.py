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
 Widget to setup the connection of a GPS device,
 either from a serial port or a TCP/IP connection.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QValidator
from qgis.core import QgsGpsDetector

from iquaview.src.ui.ui_gps_connection import Ui_gpsConnectionWidget
from iquaview.src.utils.textvalidator import (validate_ip,
                                              validate_port,
                                              get_color,
                                              get_ip_validator,
                                              get_int_validator)


class GPSConnectionWidget(QWidget, Ui_gpsConnectionWidget):

    def __init__(self, parent=None):
        super(GPSConnectionWidget, self).__init__(parent)
        self.setupUi(self)
        self.serial_port = None
        self.serial_baudrate = None
        self.ip = None
        self.hdt_port = None
        self.gga_port = None

        # set validators
        self.ip_text.setValidator(get_ip_validator())
        int_port_validator = get_int_validator(0, 65535)
        self.hdt_port_text.setValidator(int_port_validator)
        self.gga_port_text.setValidator(int_port_validator)

        # set signals
        self.serialPortRadioButton.toggled.connect(self.serial_port_clicked)
        self.TCPRadioButton.toggled.connect(self.tcp_ip_clicked)
        self.updateDevicesButton.clicked.connect(self.update_devices)
        self.ip_text.textChanged.connect(self.ip_validator)
        self.hdt_port_text.textChanged.connect(self.port_validator)
        self.gga_port_text.textChanged.connect(self.port_validator)
        self.update_devices()

    def update_devices(self):
        detector = QgsGpsDetector('scan')
        self.deviceComboBox.clear()
        devices_list = []
        for port in detector.availablePorts():
            devices_list.append(port[0])
        self.deviceComboBox.addItems(devices_list)

    def serial_port_clicked(self, enabled):
        if enabled:
            self.deviceComboBox.setEnabled(True)
            self.baudRateComboBox.setEnabled(True)
            self.ip_text.setEnabled(False)
            self.hdt_port_text.setEnabled(False)
            self.gga_port_text.setEnabled(False)

    def tcp_ip_clicked(self, enabled):
        if enabled:
            self.ip_text.setEnabled(True)
            self.hdt_port_text.setEnabled(True)
            self.gga_port_text.setEnabled(True)
            self.deviceComboBox.setEnabled(False)
            self.baudRateComboBox.setEnabled(False)

    def is_serial(self):
        if self.serialPortRadioButton.isChecked():
            return True
        elif self.TCPRadioButton.isChecked():
            return False

    @property
    def serial_port(self):
        self.__serial_port = self.deviceComboBox.currentText()
        return self.__serial_port

    @serial_port.setter
    def serial_port(self, serial_port):
        self.__serial_port = serial_port
        self.deviceComboBox.setCurrentText(serial_port)

    @property
    def serial_baudrate(self):
        self.__serial_baudrate = int(self.baudRateComboBox.currentText())
        return self.__serial_baudrate

    @serial_baudrate.setter
    def serial_baudrate(self, serial_baudrate):
        self.__serial_baudrate = serial_baudrate
        self.baudRateComboBox.setCurrentText(str(serial_baudrate))

    @property
    def ip(self):
        self.__ip = self.ip_text.text()
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip
        self.ip_text.setText(ip)

    @property
    def hdt_port(self):
        self.__hdt_port = int(self.hdt_port_text.text())
        return self.__hdt_port

    @hdt_port.setter
    def hdt_port(self, port):
        self.__hdt_port = port
        self.hdt_port_text.setText(str(port))

    @property
    def gga_port(self):
        self.__gga_port = int(self.gga_port_text.text())
        return self.__gga_port

    @gga_port.setter
    def gga_port(self, port):
        self.__gga_port = port
        self.gga_port_text.setText(str(port))

    def ip_validator(self):
        sender = self.sender()
        state = validate_ip(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def port_validator(self):
        sender = self.sender()
        state = validate_port(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def is_gps_valid(self):
        return (self.serialPortRadioButton.isChecked()
                or (self.TCPRadioButton.isChecked()
                    and validate_ip(self.ip_text.text()) == QValidator.Acceptable
                    and validate_port(self.hdt_port_text.text()) == QValidator.Acceptable
                    and validate_port(self.gga_port_text.text()) == QValidator.Acceptable))
