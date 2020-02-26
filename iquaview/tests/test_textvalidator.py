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


from PyQt5.QtGui import QValidator

from iquaview.src.utils.textvalidator import (validate_ip,
                                              validate_int,
                                              validate_port,
                                              validate_custom_double,
                                              validate_custom_int,
                                              get_color)


class TestTextValidator(unittest.TestCase):

    def test_validations(self):
        white = ''
        yellow = '#fff79a'
        red = '#f6989d'

        self.assertEqual(validate_ip("127.0.0.1"), QValidator.Acceptable)
        self.assertEqual(validate_ip("255.255.255.255"), QValidator.Acceptable)
        self.assertEqual(validate_ip("127.0."), QValidator.Intermediate)
        self.assertEqual(validate_ip("127.0...1"), QValidator.Invalid)
        self.assertEqual(validate_ip("300.0.0.1"), QValidator.Invalid)
        self.assertEqual(validate_ip("255.255.255.256"), QValidator.Invalid)
        self.assertEqual(validate_ip("abc"), QValidator.Invalid)

        self.assertEqual(validate_int("1"), QValidator.Acceptable)
        self.assertEqual(validate_int("0"), QValidator.Acceptable)
        self.assertEqual(validate_int("-1"), QValidator.Acceptable)
        self.assertEqual(validate_int("2310234"), QValidator.Acceptable)
        self.assertEqual(validate_int("a"), QValidator.Invalid)
        self.assertEqual(validate_int("3", 0, 5), QValidator.Acceptable)
        self.assertEqual(validate_int("5", 0, 5), QValidator.Acceptable)
        self.assertEqual(validate_int("0", 0, 5), QValidator.Acceptable)
        self.assertEqual(validate_int("-1", 0, 5), QValidator.Invalid)
        self.assertEqual(validate_int("6", 0, 5), QValidator.Invalid)

        self.assertEqual(validate_port("1"), QValidator.Acceptable)
        self.assertEqual(validate_port("8005"), QValidator.Acceptable)
        self.assertEqual(validate_port("65535"), QValidator.Acceptable)
        self.assertEqual(validate_port("0"), QValidator.Invalid)
        self.assertEqual(validate_port("-1"), QValidator.Invalid)
        self.assertEqual(validate_port("-8005"), QValidator.Invalid)
        self.assertEqual(validate_port("65536"), QValidator.Invalid)
        self.assertEqual(validate_port("99999"), QValidator.Invalid)
        self.assertEqual(validate_port("005"), QValidator.Invalid)

        self.assertEqual(validate_custom_double("1.0"), QValidator.Acceptable)
        self.assertEqual(validate_custom_double("a"), QValidator.Invalid)
        self.assertEqual(validate_custom_double("1,000.0"), QValidator.Invalid)
        self.assertEqual(validate_custom_double("1.000,0"), QValidator.Invalid)

        self.assertEqual(validate_custom_int("1"), QValidator.Acceptable)
        self.assertEqual(validate_custom_int("0"), QValidator.Acceptable)
        self.assertEqual(validate_custom_int("-1"), QValidator.Acceptable)
        self.assertEqual(validate_custom_int("1,000"), QValidator.Invalid)
        self.assertEqual(validate_custom_int("1.000"), QValidator.Invalid)

        self.assertEqual(get_color(QValidator.Acceptable), white)
        self.assertEqual(get_color(QValidator.Intermediate), yellow)
        self.assertEqual(get_color(QValidator.Invalid), red)


if __name__ == '__main__':
    unittest.main()
