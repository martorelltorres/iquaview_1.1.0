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
Widget to display the general timeout of the vehicle software architecture and allow to reset it.
"""
import logging

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal
from iquaview.src.ui.ui_timeoutwidget import Ui_Timeout
from iquaview.src.cola2api.cola2_interface import send_empty_service, get_ros_param

logger = logging.getLogger(__name__)

class TimeoutWidget(QWidget, Ui_Timeout):

    timeout_warning = pyqtSignal()
    def __init__(self, vehicle_info, vehicle_data, parent=None):
        super(TimeoutWidget, self).__init__(parent)
        self.setupUi(self)
        self.vehicle_info = vehicle_info
        self.vehicle_data = vehicle_data

        self.timeout_warning.connect(self.show_warning)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_timeout)

        self.connected = False
        self.timer_on = False

        self.time = 0
        self.timeout = 0

    def connect(self):
        """ set connected state to True and start timer"""
        self.connected = True
        self.set_timeout()
        self.timer.start(1000)

    def refresh_timeout(self):
        """ Refresh timeout"""
        if self.connected:
            #back compatibility
            data = self.vehicle_data.get_total_time()
            if data is not None and data['valid_data'] == 'new_data':
                # timeout - total_time
                self.time = int(data['timeout']) - data['total_time']
                self.set_time()
            else:
                data = self.vehicle_data.get_watchdog()
                if data is not None and data['valid_data'] == 'new_data':

                   self.time = int(self.timeout) - data['data']
                   self.set_time()

        else:
            self.time -= 1
            self.set_time()

    def set_time(self):
        """ set time to timeout_label"""
        if self.timeout_label:
            # set color
            if self.time < 0:
                self.timeout_label.setStyleSheet('font:italic; color:red')
            elif self.time <= 300:
                if(self.time >0 and self.time%60 == 0):
                    self.timeout_warning.emit()
                self.timeout_label.setStyleSheet('font:italic; color:orange')
            else:
                self.timeout_label.setStyleSheet('font:italic; color:black')

            # set time
            self.timeout_label.setText(str(self.time))

    def set_timeout(self):
        self.timeout = (get_ros_param(self.vehicle_info.get_vehicle_ip(), 9091,
                                 self.vehicle_info.get_vehicle_namespace()+'/safety/timeout')['value'])

    def show_warning(self):
        logger.warning( "Less than {} seconds for timeout expiration. You might want to restart it.".format(str(self.time)))
        QMessageBox.warning(self.parent(),
                                "Timeout",
                                "Less than {} seconds for timeout expiration. You might want to restart it.".format(str(self.time)),
                                QMessageBox.Close)

    def disconnect(self):
        """ Set connected state to False"""
        self.connected = False

    def cancel_timer(self):
        """ Stop timer"""
        self.timer.stop()
        self.time = 0
        self.timeout_label.setText('')
        self.timer_on = False

    def reset_timeout(self):
        """ Send service that reset timeout"""
        if self.connected:
            reset_timeout = self.vehicle_data.get_reset_timeout_service()
            if reset_timeout is not None:
                send_empty_service(self.vehicle_info.get_vehicle_ip(), 9091,
                                   self.vehicle_info.get_vehicle_namespace()+reset_timeout)
                self.set_timeout()
                logger.info("Reset timeout")
            else:
                logger.error("The service 'Reset Timeout' could not be sent.")
                QMessageBox.critical(self,
                                     "Reset timeout error",
                                     "The service 'Reset Timeout' could not be sent.",
                                     QMessageBox.Close)