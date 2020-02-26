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
 Class to periodically check for mission activation state.
"""

from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class MissionActive(QObject):
    mission_signal = pyqtSignal()

    def __init__(self, vehicledata):
        super(MissionActive, self).__init__()
        self.vehicle_data = vehicledata
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_mission_status)
        self.status = None
        self.subscribed = False

    def update_mission_status(self):
        """ set subscribed status to true and start timer"""
        self.subscribed = True
        self.timer.start(1000)

    def refresh_mission_status(self):
        """Refresh mission status. Timer to get every second mission status. """

        if self.subscribed:
            mission_status = self.vehicle_data.get_captain_state()
            #back compatibility
            if mission_status is None:
                mission_status = self.vehicle_data.get_mission_active()

            if mission_status is not None:
                # if new status is different that old status
                if mission_status != self.status:
                    self.status = mission_status
                    # send signal to notify that mission status
                    self.mission_signal.emit()

    def get_mission_active(self):
        """
        :return: mission active state
        :rtype: bool
        """
        is_active = False

        mission_status = self.vehicle_data.get_captain_state()
        #back compatibility
        if mission_status is None:
            is_active = self.status
        else:
            if mission_status == 2:
                is_active = True

        return is_active

    def disconnect(self):
        """ disconnect and stop timer"""
        self.subscribed = False
        self.status = None
        self.mission_signal.emit()  # emit status changed
        self.timer.stop()
