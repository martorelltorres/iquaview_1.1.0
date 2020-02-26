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
 Class to trigger the service to calibrate the vehicle's magnetometer
"""

import threading
import logging

from iquaview.src.cola2api.cola2_interface import send_empty_service
from PyQt5.QtCore import pyqtSignal, QObject

logger = logging.getLogger(__name__)


class CalibrateMagnetometer(QObject):
    calibrate_magnetometer_signal = pyqtSignal(bool)

    def __init__(self, vehicle_info, vehicle_data):
        super(CalibrateMagnetometer, self).__init__()

        self.ip = vehicle_info.get_vehicle_ip()
        self.port = 9091
        self.vehicle_namespace = vehicle_info.get_vehicle_namespace()
        self.vehicle_data = vehicle_data

    def start_calibrate_magnetometer(self):
        """ Start calibrate magnetometer in a new thread"""

        self.threadCalibrateMagnetometer = threading.Thread(target=self.calibrate_magnetometer)
        self.threadCalibrateMagnetometer.daemon = True
        self.threadCalibrateMagnetometer.start()

    def calibrate_magnetometer(self):
        """ Send service to start calibrate magnetometer"""
        try:
            enable_thrusters = self.vehicle_data.get_enable_thrusters_service()
            calibrate_magnetometer = self.vehicle_data.get_calibrate_magnetometer_service()
            thruster = send_empty_service(self.ip, self.port,
                                          self.vehicle_namespace+enable_thrusters)
            result = send_empty_service(self.ip, self.port,
                                        self.vehicle_namespace+calibrate_magnetometer)
            logger.info("result {}".format(result))
            self.calibrate_magnetometer_signal.emit(result)

        except:
            self.calibrate_magnetometer_signal.emit(False)

    def stop_magnetometer_calibration(self):
        """ Stop magnetometer calibration"""
        stop_magnetometer_calibration_service = self.vehicle_data.get_stop_magnetometer_calibration_service()
        result = send_empty_service(self.ip, self.port,
                                    self.vehicle_namespace+stop_magnetometer_calibration_service)
