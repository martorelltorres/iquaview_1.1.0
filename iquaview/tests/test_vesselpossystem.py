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
from pathlib import Path

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
iquaview_root_path = srcpath + '/../'
sys.path.append(iquaview_root_path)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from iquaview.src.tools.vesselpossystem import VesselPositionSystem
from iquaview.src.config import Config


class TestVesselPosSystem(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)

        self.config = Config()
        self.config.load()
        self.config.csettings = self.config.settings

        self.vps = VesselPositionSystem(self.config)

    def test_spinbox(self):
        self.assertEqual(type(self.vps.vessel_width_doubleSpinBox.value()), type(0.0))
        self.assertEqual(type(self.vps.vessel_length_doubleSpinBox.value()), type(0.0))
        self.assertEqual(type(self.vps.gps_x_offset_doubleSpinBox.value()), type(0.0))
        self.assertEqual(type(self.vps.gps_y_offset_doubleSpinBox.value()), type(0.0))
        self.assertEqual(type(self.vps.usbl_x_offset_doubleSpinBox.value()), type(0.0))
        self.assertEqual(type(self.vps.usbl_y_offset_doubleSpinBox.value()), type(0.0))
        self.assertEqual(type(self.vps.usbl_z_offset_doubleSpinBox.value()), type(0.0))

    def test_buttons(self):

        okwidget = self.vps.buttonBox.button(self.vps.buttonBox.Ok)
        cancelwidget = self.vps.buttonBox.button(self.vps.buttonBox.Ok)

        QTest.mouseClick(okwidget, Qt.LeftButton)
        QTest.mouseClick(cancelwidget, Qt.LeftButton)


if __name__ == "__main__":
    unittest.main()
