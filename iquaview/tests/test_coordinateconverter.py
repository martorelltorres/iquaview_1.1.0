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

from iquaview.src.utils import coordinateconverter


class TestCoordinateConverter(unittest.TestCase):

    def test_converter(self):

        lat = 41.77785501
        lon = 3.03357015

        lat_dm, lon_dm = coordinateconverter.degree_to_degree_minute(lat, lon)

        lat_d, lat_m = str(lat_dm).split('º')
        lat_m, unused = lat_m.split('\'')

        lon_d, lon_m = str(lon_dm).split('º')
        lon_m, unused = lon_m.split('\'')

        lat_dm = [lat_d, lat_m]
        lon_dm = [lon_d, lon_m]

        lat_degree, lon_degree = coordinateconverter.degree_minute_to_degree(lat_dm, lon_dm)
        lat_dms, lon_dms = coordinateconverter.degree_to_degree_minute_second(float(lat_degree), float(lon_degree))
        lat_deg, lon_deg = coordinateconverter.degree_minute_second_to_degree(lat_dms, lon_dms)

        self.assertEqual(type(lat), type(lat_deg))
        self.assertEqual(type(lon), type(lon_deg))

        self.assertEqual('%.6f'%(lat), '%.6f'%(lat_deg))
        self.assertEqual('%.6f'%(lon), '%.6f'%(lon_deg))

if __name__ == '__main__':
    unittest.main()
