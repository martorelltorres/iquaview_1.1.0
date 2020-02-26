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
 Class for validating user input fields
"""

from PyQt5.QtGui import QValidator, QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp


def validate_ip(text):
    validator = get_ip_validator()
    state = validator.validate(text, 0)[0]
    return state


def validate_int(text, min=None, max=None):
    validator = get_int_validator(min, max)
    state = validator.validate(text, 0)[0]
    return state


def validate_port(text):
    validator = get_port_validator()
    state = validator.validate(text, 0)[0]
    return state


def validate_custom_double(text):
    validator = get_custom_double_validator()
    state = validator.validate(text, 0)[0]
    return state


def validate_custom_int(text):
    validator = get_custom_int_validator()
    state = validator.validate(text, 0)[0]
    return state


def get_color(state):
    """
    Get a hexadecimal color according with state
    :param state: Qvalidator state
    :return: return a color
    """
    if state == QValidator.Acceptable:
        color = ''  # white
    elif state == QValidator.Intermediate:
        color = '#fff79a'  # yellow
    else:
        color = '#f6989d'  # red
    return color


def get_ip_validator():
    string = "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    regexp = QRegExp(string)
    validator = QRegExpValidator(regexp)
    return validator


def get_port_validator():
    string = "(6553[0-5]|655[0-2][0-9]\d|65[0-4](\d){2}|6[0-4](\d){3}|[1-5](\d){4}|[1-9](\d){0,3})"
    regexp = QRegExp(string)
    validator = QRegExpValidator(regexp)
    return validator


def get_int_validator(min=None, max=None):
    validator = QIntValidator()
    if min is not None:
        validator.setBottom(min)
    if max is not None:
        validator.setTop(max)
    return validator


def get_custom_int_validator(only_positive_numbers=False):
    if only_positive_numbers:
        string = "[+]?\\d*"
    else:
        string = "[+-]?\\d*"
    regexp = QRegExp(string)
    validator = QRegExpValidator(regexp)
    return validator


def get_custom_double_validator():
    string = "[+-]?\\d*[\\.]?\\d+"
    regexp = QRegExp(string)
    validator = QRegExpValidator(regexp)
    return validator