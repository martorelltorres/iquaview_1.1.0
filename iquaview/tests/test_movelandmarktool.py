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
from qgis.core import QgsProject, QgsPointXY, QgsWkbTypes
from qgis.gui import QgsMapCanvas

from iquaview.src.mapsetup import movelandmarktool, pointfeaturedlg
from iquaview.src import resources_rc

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
iquaview_root_path = srcpath + '/../'
sys.path.append(iquaview_root_path)


class TestMissionTrack(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.canvas = QgsMapCanvas()
        self.proj = QgsProject.instance()
        self.proj.setFileName("")

        self.point_feature = pointfeaturedlg.PointFeatureDlg(self.canvas, self.proj)
        self.point_feature.reset()
        self.tool_move_landmark = movelandmarktool.MoveLandmarkTool(self.canvas)

        self.point_feature.landmark_added.connect(self.set_layer)

        self.x_pos = 41.77
        self.y_pos = 3.03
        self.point_feature.add_new_landmark(QgsPointXY(self.x_pos, self.y_pos))

    def set_layer(self, layer):
        """
        Sets created layer as current layer in move landmark tool
        :param layer: layer
        """
        self.tool_move_landmark.set_landmark_layer(layer)
        feature_it = self.tool_move_landmark.lm_layer.dataProvider().getFeatures()
        self.tool_move_landmark.lm_feature = next(feature_it)
        self.tool_move_landmark.lm_point = self.tool_move_landmark.lm_feature.geometry().asPoint()

    def test_structure(self):
        layer = self.tool_move_landmark.lm_layer
        self.assertEqual(layer.geometryType(), QgsWkbTypes.PointGeometry)

        feature_it = layer.dataProvider().getFeatures()
        feature = next(feature_it)
        self.assertEqual(feature.geometry().wkbType(), QgsWkbTypes.Point)

        point = feature.geometry().asPoint()
        self.assertEqual(point.x(), self.x_pos)
        self.assertEqual(point.y(), self.y_pos)

    def test_move(self):
        end_point = QgsPointXY(45.005, 4.127)
        self.tool_move_landmark.move_position(end_point)
        self.assert_almost_equal_point(end_point)

        end_point = QgsPointXY(0.0, 0.0)
        self.tool_move_landmark.move_position(end_point)
        self.assert_almost_equal_point(end_point)

        end_point = QgsPointXY(1000, 1000)
        self.tool_move_landmark.move_position(end_point)
        self.assert_almost_equal_point(end_point)

        end_point = QgsPointXY(self.x_pos, self.y_pos)
        self.tool_move_landmark.move_position(end_point)
        self.assert_almost_equal_point(end_point)

    def assert_almost_equal_point(self, point):
        """
        Checks if point is the actual landmark point
        Once checks pass, updates landmark point. This action happens naturally whenever a point is clicked in canvas
        and needs to be done here because there are no clicks in this test.
        :param point:
        """
        layer = self.tool_move_landmark.lm_layer
        feature_it = layer.dataProvider().getFeatures()
        feature = next(feature_it)
        fpoint = feature.geometry().asPoint()

        self.assertAlmostEqual(fpoint.x(), point.x(), 12)  # with 12 decimal precision (0.1mm)
        self.assertAlmostEqual(fpoint.y(), point.y(), 12)

        self.tool_move_landmark.lm_point = point


if __name__ == "__main__":
    unittest.main()
