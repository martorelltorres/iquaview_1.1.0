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
 Widget to define the ip and port to establish the connection to the AUV
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QValidator

from iquaview.src.ui.ui_auv_connection import Ui_AUVConnectionWidget
from iquaview.src.utils.textvalidator import (validate_ip,
                                              validate_port,
                                              get_color,
                                              get_ip_validator,
                                              get_int_validator)


class AUVConnectionWidget(QWidget, Ui_AUVConnectionWidget):

    def __init__(self, parent=None):
        super(AUVConnectionWidget, self).__init__(parent)
        self.setupUi(self)
        self.ip = None
        self.port = None

        # set validators
        self.ip_auv_text.setValidator(get_ip_validator())
        self.port_auv_text.setValidator(get_int_validator(0, 65535))

        # set signals
        self.ip_auv_text.textChanged.connect(self.ip_validator)
        self.port_auv_text.textChanged.connect(self.port_validator)

    @property
    def ip(self):
        self.__ip = self.ip_auv_text.text()
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip
        self.ip_auv_text.setText(ip)

    @property
    def port(self):
        self.__port = int(self.port_auv_text.text())
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port
        self.port_auv_text.setText(str(port))

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

    def is_auv_valid(self):
        return (validate_ip(self.ip_auv_text.text()) == QValidator.Acceptable and
                validate_port(self.port_auv_text.text()) == QValidator.Acceptable)
