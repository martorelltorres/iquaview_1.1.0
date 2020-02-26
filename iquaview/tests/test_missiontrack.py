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

from PyQt5.QtWidgets import QApplication
from qgis.core import QgsProject, QgsWkbTypes, QgsPointXY
from qgis.gui import QgsMapCanvas


from iquaview.src.config import Config
from iquaview.src.vehicle.vehicleinfo import VehicleInfo
from iquaview.src.mission.missioncontroller import MissionController
from iquaview.src.cola2api.mission_types import (Mission,
                                                 MissionStep,
                                                 Parameter,
                                                 MissionAction,
                                                 MissionPosition,
                                                 MissionTolerance,
                                                 MissionSection,
                                                 MissionPark,
                                                 MissionWaypoint)

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
iquaview_root_path = srcpath + '/../'
sys.path.append(iquaview_root_path)


class TestMissionTrack(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        #sparus2 default
        self.config = Config()
        self.config.load()
        self.config.csettings = self.config.settings

        self.vehicle_info = VehicleInfo(self.config)

        self.proj = QgsProject.instance()
        self.proj.setFileName("")

        self.canvas = QgsMapCanvas()
        self.view = None
        self.wp_dock = None
        self.templates_dock = None
        self.minfo_dock = None
        self.msg_log = None
        self.MISSION_NAME = "temp_mission"

        # self.mt = MissionTrack(mission_filename="mission_test.xml")
        self.mission_ctrl = MissionController(self.config, self.vehicle_info, self.proj, self.canvas, self.view,
                                              self.wp_dock, self.templates_dock, self.minfo_dock, self.msg_log)

    def tearDown(self):
        os.remove("temp_mission.xml")

    def test_structure(self):
        self.write_temp_mission_xml()
        self.mission_ctrl.load_mission(self.MISSION_NAME + ".xml")
        self.mission_track = self.mission_ctrl.mission_list[0]

        self.assertNotEqual(self.mission_track, None)
        self.assertEqual(self.mission_track.get_mission_length(), 3)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)
        self.assertEqual(self.mission_track.get_mission_name(), self.MISSION_NAME)

    def test_remove_step(self):
        self.write_temp_mission_xml()
        self.mission_ctrl.load_mission(self.MISSION_NAME + ".xml")
        self.mission_track = self.mission_ctrl.mission_list[0]

        self.mission_track.remove_step(2)
        self.assertEqual(self.mission_track.get_mission_length(), 2)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)

        self.mission_track.remove_step(1)
        self.assertEqual(self.mission_track.get_mission_length(), 1)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.PointGeometry)

        self.mission_track.remove_step(0)
        self.assertEqual(self.mission_track.get_mission_length(), 0)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)

        self.assertEqual(self.mission_track.is_modified(), True)

    def test_add_step(self):
        self.write_temp_mission_xml()
        self.mission_ctrl.load_mission(self.MISSION_NAME + ".xml")
        self.mission_track = self.mission_ctrl.mission_list[0]

        point = QgsPointXY(40.0032123, 3.0594338)
        point2 = QgsPointXY(40.0032127, 3.0594331)
        point3 = QgsPointXY(40.0032151, 3.0594340)
        self.mission_track.add_step(3, point)
        self.mission_track.add_step(0, point2)
        self.mission_track.add_step(2, point3)

        self.assertEqual(self.mission_track.get_mission_length(), 6)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)

        self.assertEqual(self.mission_track.is_modified(), True)

    def test_change_position(self):
        self.write_temp_mission_xml()
        self.mission_ctrl.load_mission(self.MISSION_NAME + ".xml")
        self.mission_track = self.mission_ctrl.mission_list[0]

        point = QgsPointXY(40.001, 3.002)
        self.mission_track.change_position(0, point)

        position = self.mission_track.get_step(0).get_maneuver().get_position()
        lat = position.get_latitude()
        lon = position.get_longitude()
        self.assertEqual(point.x(), lon)
        self.assertEqual(point.y(), lat)

        self.assertEqual(self.mission_track.is_modified(), True)

    def test_empty_mission(self):
        self.write_temp_mission_xml_empty()
        self.mission_ctrl.load_mission(self.MISSION_NAME + '.xml')
        self.mission_track = self.mission_ctrl.mission_list[0]

        self.assertNotEqual(self.mission_track, None)
        self.assertEqual(self.mission_track.get_mission_length(), 0)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)

        point = QgsPointXY(40.0032123, 3.0594338)
        point2 = QgsPointXY(40.0032127, 3.0594331)

        self.mission_track.add_step(0, point)
        self.assertEqual(self.mission_track.get_mission_length(), 1)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.PointGeometry)

        self.mission_track.add_step(1, point2)
        self.assertEqual(self.mission_track.get_mission_length(), 2)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)

        self.mission_track.remove_step(0)
        self.assertEqual(self.mission_track.get_mission_length(), 1)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.PointGeometry)

        self.mission_track.remove_step(0)
        self.assertEqual(self.mission_track.get_mission_length(), 0)
        self.assertEqual(self.mission_track.mission_layer.geometryType(), QgsWkbTypes.LineGeometry)

    def write_temp_mission_xml(self):
        mission = Mission()
        mission_step = MissionStep()
        param = Parameter("abcd")
        param_2 = Parameter("2")
        parameters = list()
        parameters.append(param)
        parameters.append(param_2)
        action = MissionAction("action1", parameters)
        mission_step.add_action(action)
        wp = MissionWaypoint(MissionPosition(41.777, 3.030, 15.0, False),
                             0.5,
                             MissionTolerance(2.0, 2.0, 1.0))
        mission_step.add_maneuver(wp)
        mission.add_step(mission_step)
        mission_step2 = MissionStep()
        sec = MissionSection(MissionPosition(41.777, 3.030, 15.0, False),
                             MissionPosition(41.787, 3.034, 15.0, False),
                             0.5,
                             MissionTolerance(2.0, 2.0, 1.0))
        mission_step2.add_maneuver(sec)
        mission.add_step(mission_step2)
        mission_step3 = MissionStep()
        park = MissionPark(MissionPosition(41.777, 3.030, 15.0, False),
                           0.5,
                           120,
                           MissionTolerance(2.0, 2.0, 1.0))
        mission_step3.add_maneuver(park)
        mission.add_step(mission_step3)
        mission.write_mission(self.MISSION_NAME+'.xml')

    def write_temp_mission_xml_empty(self):
        mission = Mission()
        mission.write_mission(self.MISSION_NAME+'.xml')

if __name__ == "__main__":
    unittest.main()
