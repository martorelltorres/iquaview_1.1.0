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
 Class to periodically check for thrusters activation state.
"""

from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class ThrustersStatus(QObject):
    thrusters_signal = pyqtSignal()

    def __init__(self, vehicledata):
        super(ThrustersStatus, self).__init__()
        self.vehicle_data = vehicledata
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_thrusters_status)
        self.status = None
        self.subscribed = False

    def update_thrusters_status(self):
        """ Set subscribed state to True and start Timer"""
        self.subscribed = True
        self.timer.start(1000)

    def refresh_thrusters_status(self):
        """Refresh thrusters status. Timer to get every second thrusters status. """
        if self.subscribed:
            thrusters_status = self.vehicle_data.get_thrusters_status()
            if thrusters_status is not None:
                # if new status is different that old status
                if thrusters_status != self.status:
                    self.status = thrusters_status
                    # send signal to notify that thrusters status
                    self.thrusters_signal.emit()

    def get_thrusters_enabled(self):
        return self.status

    def disconnect(self):
        self.subscribed = False
        self.status = None
        self.timer.stop()
