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
 Widget to setup the connection to a USBL device,
 specifying the ip, port, own usbl id and transponder id.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QValidator

from iquaview.src.ui.ui_usbl_connection import Ui_USBLConnectionWidget
from iquaview.src.utils.textvalidator import (validate_ip,
                                              validate_int,
                                              validate_port,
                                              get_color,
                                              get_ip_validator,
                                              get_int_validator,
                                              get_custom_int_validator)


class USBLConnectionWidget(QWidget, Ui_USBLConnectionWidget):

    def __init__(self, parent=None):
        super(USBLConnectionWidget, self).__init__(parent)
        self.setupUi(self)
        self.ip = ""
        self.port = ""
        self.ownid = ""
        self.targetid = ""

        # set validators
        self.ip_usbl_text.setValidator(get_ip_validator())
        int_port_validator = get_int_validator(0, 65535)
        int_id_validator = get_custom_int_validator(only_positive_numbers=True)
        self.port_usbl_text.setValidator(int_port_validator)
        self.id_usbl_text.setValidator(int_id_validator)
        self.targetid_usbl_text.setValidator(int_id_validator)

        # signals
        self.ip_usbl_text.textChanged.connect(self.ip_validator)
        self.port_usbl_text.textChanged.connect(self.port_validator)
        self.id_usbl_text.textChanged.connect(self.int_validator)
        self.targetid_usbl_text.textChanged.connect(self.int_validator)

    @property
    def ip(self):
        self.__ip = self.ip_usbl_text.text()
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip
        self.ip_usbl_text.setText(ip)

    @property
    def port(self):
        self.__port = int(self.port_usbl_text.text())
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port
        self.port_usbl_text.setText(str(port))

    @property
    def ownid(self):
        self.__ownid = int(self.id_usbl_text.text())
        return self.__ownid

    @ownid.setter
    def ownid(self, ownid):
        self.__ownid = ownid
        self.id_usbl_text.setText(str(ownid))

    @property
    def targetid(self):
        self.__targetid = int(self.targetid_usbl_text.text())
        return self.__targetid

    @targetid.setter
    def targetid(self, targetid):
        self.__targetid = targetid
        self.targetid_usbl_text.setText(str(targetid))

    def ip_validator(self):
        sender = self.sender()
        state = validate_ip(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def int_validator(self):
        sender = self.sender()
        state = validate_int(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def port_validator(self):
        sender = self.sender()
        state = validate_port(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def is_usbl_valid(self):
        return (validate_ip(self.ip_usbl_text.text()) == QValidator.Acceptable and
                validate_int(self.port_usbl_text.text()) == QValidator.Acceptable and
                validate_int(self.id_usbl_text.text()) == QValidator.Acceptable and
                validate_int(self.targetid_usbl_text.text()) == QValidator.Acceptable)
