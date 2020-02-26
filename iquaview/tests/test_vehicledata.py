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

import sys
import os
import unittest

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
iquaview_root_path = srcpath + '/../'
sys.path.append(iquaview_root_path)

from PyQt5.QtWidgets import QApplication

from iquaview.src.vehicle.vehicledata import VehicleData
from iquaview.src.vehicle.vehicleinfo import VehicleInfo
from iquaview.src.config import Config


class TestVehicleData(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        #sparus2 default
        self.config = Config()
        self.config.load()
        self.config.csettings = self.config.settings

        vinfo = VehicleInfo(self.config)

        self.vd = VehicleData(self.config,vinfo)


    def test_subscribed(self):
        self.assertEqual(self.vd.is_subscribed(),False)

    def test_gets(self):
        #empty none gets
        self.assertEqual(self.vd.get_total_time(), None)
        self.assertEqual(self.vd.get_watchdog(), None)
        self.assertEqual(self.vd.get_goto_status(), None)
        self.assertEqual(self.vd.get_thrusters_status(), None)
        self.assertEqual(self.vd.get_active_controller(), None)
        self.assertEqual(self.vd.get_captain_state(), None)
        self.assertEqual(self.vd.get_battery_charge(), None)
        self.assertEqual(self.vd.get_cpu_usage(), None)
        self.assertEqual(self.vd.get_ram_usage(), None)
        self.assertEqual(self.vd.get_thruster_setpoints(), None)
        self.assertEqual(self.vd.get_mission_active(), None)
        self.assertEqual(self.vd.get_total_steps(), None)
        self.assertEqual(self.vd.get_status_code(), None)
        self.assertEqual(self.vd.get_error_code(), None)
        self.assertEqual(self.vd.get_recovery_action(), None)
        self.assertEqual(self.vd.get_rosout(), None)


        self.assertEqual(self.vd.get_calibrate_magnetometer_service(), "/imu_angle_estimator/calibrate_magnetometer")
        self.assertEqual(self.vd.get_stop_magnetometer_calibration_service(), "/imu_angle_estimator/stop_magnetometer_calibration")
        self.assertEqual(self.vd.get_keep_position_service(), "/captain/enable_keep_position_non_holonomic")
        self.assertEqual(self.vd.get_disable_keep_position_service(), "/captain/disable_keep_position")
        self.assertEqual(self.vd.get_disable_all_keep_positions_service(), "/captain/disable_all_keep_positions")
        self.assertEqual(self.vd.get_reset_timeout_service(), "/cola2_watchdog/reset_timeout")
        self.assertEqual(self.vd.get_goto_service(), "/captain/enable_goto")
        self.assertEqual(self.vd.get_disable_goto_service(), "/captain/disable_goto")
        self.assertEqual(self.vd.get_enable_thrusters_service(), "/controller/enable_thrusters")
        self.assertEqual(self.vd.get_disable_thrusters_service(), "/controller/disable_thrusters")
        self.assertEqual(self.vd.get_enable_mission_service(), "/captain/enable_default_mission_non_block")
        self.assertEqual(self.vd.get_disable_mission_service(), "/captain/disable_mission")
        self.assertEqual(self.vd.get_teleoperation_launch(), "roslaunch cola2_sparus2 sparus2_teleoperation.launch")

if __name__ == "__main__":
    unittest.main()
