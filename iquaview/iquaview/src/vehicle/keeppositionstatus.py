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
Class to periodically check the keep position status of the vehicle
by checking the /cola2_control/keep_position_enabled topic
"""

from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class KeepPositionStatus(QObject):
    keep_position_signal = pyqtSignal()

    def __init__(self, vehicledata, msglog):
        super(KeepPositionStatus, self).__init__()
        self.vehicle_data = vehicledata
        self.msglog = msglog
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_keep_position_status)
        self.status = None
        self.subscribed = False

    def update_keep_position_status(self):
        self.subscribed = True
        self.timer.start(1000)

    def refresh_keep_position_status(self):
        """Refresh keep position status. Timer to get every second keep position status. """
        if self.subscribed:
            keep_position_status = self.vehicle_data.get_captain_state()
            #back compatibility
            if keep_position_status is None:
                keep_position_status = self.vehicle_data.get_active_controller()

            if keep_position_status is not None:
                # if new data is different that old data
                if keep_position_status != self.status:
                    self.status = keep_position_status
                    # send signal to notify that keep position status
                    self.keep_position_signal.emit()

                if self.get_keep_position_enabled():
                    if not self.is_old_version() and self.is_safety_keep_position():
                        # self.msglog.logMessage("", "Keep position", 3)
                        self.msglog.logMessage("Safety keep Position Enabled", "Keep position", 3)
                    else:
                        # self.msglog.logMessage("", "Keep position", 3)
                        self.msglog.logMessage("Keep Position Enabled", "Keep position", 3)

    def get_keep_position_enabled(self):
        """ Return keep position status"""
        # 3 is a keep position, 4 is a safety keep position
        # 3 is a park (back compatibility with active controller)

        keep_position_status = self.vehicle_data.get_captain_state()
        if keep_position_status is not None:
            return self.status == 3 or self.status == 4
        else:
            #back compatibility with active controller
            return self.status == 3

    def is_old_version(self):
        """
        back compatible method to check if cola2 architecture is in old or in new version.
        :return: return True if is in old version, otherwise False
        """
        is_old = True
        keep_position_status = self.vehicle_data.get_captain_state()
        if keep_position_status is not None:
            is_old = False

        return is_old

    def is_safety_keep_position(self):
        """
        Return True if  status is a safety keep position, otherwise False
        :return: Return True if status is safety keep position, otherwise False
        """
        return self.status == 4

    def disconnect(self):
        self.subscribed = False
        self.status = None
        self.timer.stop()
