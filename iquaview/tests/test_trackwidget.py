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
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from qgis.gui import QgsMapCanvas
from qgis.core import QgsWkbTypes, QgsPointXY

from iquaview.src import resources_rc, resources_qgis
from iquaview.src.canvastracks.canvasmarker import CanvasMarker
from iquaview.src.canvastracks.trackwidget import TrackWidget
from iquaview.src.config import Config


class TestCanvasMarker(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)

        self.config = Config()
        self.config.load()
        self.config.csettings = self.config.settings

        self.canvas = QgsMapCanvas()
        self.canvas.setObjectName("canvas")

        self.default_color_auv = Qt.darkGreen

        self.marker = CanvasMarker(self.canvas, self.default_color_auv,
                                   None,
                                   marker_mode=True, config=self.config)

    def test_buttons(self):
        self.trackwidget_auv = TrackWidget()
        self.trackwidget_auv.init("AUV track",
                                  self.canvas,
                                  self.default_color_auv,
                                  QgsWkbTypes.LineGeometry,
                                  self.marker)
        for i in range(0, 10):
            self.trackwidget_auv.track_update_canvas(QgsPointXY(i*10, i*-10), 0)

        QTest.mouseClick(self.trackwidget_auv.centerButton, Qt.LeftButton)
        QTest.mouseClick(self.trackwidget_auv.clearTrackButton, Qt.LeftButton)


if __name__ == "__main__":
    unittest.main()
