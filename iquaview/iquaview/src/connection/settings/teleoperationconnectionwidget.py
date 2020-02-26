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
 Widget to setup the device for the joystick connection
"""

from PyQt5.QtWidgets import QWidget
from iquaview.src.ui.ui_teleop_connection import Ui_TeleopConnectionWidget


class TeleoperationConnectionWidget(QWidget, Ui_TeleopConnectionWidget):

    def __init__(self, parent = None ):
        super(TeleoperationConnectionWidget, self).__init__(parent)
        self.setupUi(self)
        self.joystickdevice = None

    @property
    def joystickdevice(self):
        self.__joystickdevice = self.joystick_device_text.text()
        return self.__joystickdevice

    @joystickdevice.setter
    def joystickdevice(self, joystickdevice):
        self.__joystickdevice = joystickdevice
        self.joystick_device_text.setText(joystickdevice)
