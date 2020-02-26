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
 Widget for converting lat lon coordinates between
 decimal degrees/degrees decimal minutes/degrees minutes seconds
"""
import logging

from iquaview.src.ui.ui_coordinateconverterwidget import Ui_CoordinateConverterDialog
from iquaview.src.utils.coordinateconverter import (degree_to_degree_minute,
                                                    degree_minute_to_degree,
                                                    degree_to_degree_minute_second,
                                                    degree_minute_second_to_degree)
from iquaview.src.utils.textvalidator import (validate_custom_double,
                                              validate_custom_int,
                                              get_color,
                                              get_custom_double_validator,
                                              get_custom_int_validator)

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QValidator
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QDialog, QLineEdit, QSizePolicy

logger = logging.getLogger(__name__)


class CoordinateConverterDialog(QDialog, Ui_CoordinateConverterDialog):

    def __init__(self, parent=None):
        super(CoordinateConverterDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Coordinate Converter")
        self.convert_pushButton.clicked.connect(self.convert)
        self.convert_pushButton.setFocus()
        self.edited = 1  # 0: no changes, 1: DDD.DDDDº changed, 2: DDDºMM.MM' changed, 3: DDDºMM'SS.SSS''changed
        self.copyClipboard_pushButton.setIcon(QIcon(":/resources/mActionCopyClipboard.svg"))
        self.copyClipboard_pushButton_2.setIcon(QIcon(":/resources/mActionCopyClipboard.svg"))
        self.copyClipboard_pushButton_3.setIcon(QIcon(":/resources/mActionCopyClipboard.svg"))
        self.copyClipboard_pushButton.setToolTip("Copy to Clipboard")
        self.copyClipboard_pushButton_2.setToolTip("Copy to Clipboard")
        self.copyClipboard_pushButton_3.setToolTip("Copy to Clipboard")

        int_validator = get_custom_int_validator()
        double_validator = get_custom_double_validator()

        self.lat_degree_lineEdit = CcLineEdit(str(0.0), 1)
        self.lat_degree_lineEdit.textChanged.connect(self.validate_coordinates_double)
        self.lat_d_horizontalLayout.insertWidget(1, self.lat_degree_lineEdit)

        self.lon_degree_lineEdit = CcLineEdit(str(0.0), 1)
        self.lon_degree_lineEdit.textChanged.connect(self.validate_coordinates_double)
        self.lon_d_horizontalLayout.addWidget(self.lon_degree_lineEdit)

        self.lat_dm_degree_lineEdit = CcLineEdit(str(0), 2)
        self.lat_dm_degree_lineEdit.textChanged.connect(self.validate_coordinates_int)
        self.lat_dm_horizontalLayout.addWidget(self.lat_dm_degree_lineEdit)

        self.lat_dm_minute_lineEdit = CcLineEdit(str(0.0), 2)
        self.lat_dm_minute_lineEdit.textChanged.connect(self.validate_coordinates_double)
        self.lat_dm_horizontalLayout.addWidget(self.lat_dm_minute_lineEdit)

        self.lon_dm_degree_lineEdit = CcLineEdit(str(0), 2)
        self.lon_dm_degree_lineEdit.textChanged.connect(self.validate_coordinates_int)
        self.lon_dm_horizontalLayout.addWidget(self.lon_dm_degree_lineEdit)

        self.lon_dm_minute_lineEdit = CcLineEdit(str(0.0), 2)
        self.lon_dm_minute_lineEdit.textChanged.connect(self.validate_coordinates_double)
        self.lon_dm_horizontalLayout.addWidget(self.lon_dm_minute_lineEdit)

        self.lat_dms_degree_lineEdit = CcLineEdit(str(0), 3)
        self.lat_dms_degree_lineEdit.textChanged.connect(self.validate_coordinates_int)
        self.lat_dms_horizontalLayout.addWidget(self.lat_dms_degree_lineEdit)

        self.lat_dms_minute_lineEdit = CcLineEdit(str(0), 3)
        self.lat_dms_minute_lineEdit.textChanged.connect(self.validate_coordinates_int)
        self.lat_dms_horizontalLayout.addWidget(self.lat_dms_minute_lineEdit)

        self.lat_dms_second_lineEdit = CcLineEdit(str(0.0), 3)
        self.lat_dms_second_lineEdit.textChanged.connect(self.validate_coordinates_double)
        self.lat_dms_horizontalLayout.addWidget(self.lat_dms_second_lineEdit)

        self.lon_dms_degree_lineEdit = CcLineEdit(str(0), 3)
        self.lon_dms_degree_lineEdit.textChanged.connect(self.validate_coordinates_int)
        self.lon_dms_horizontalLayout.addWidget(self.lon_dms_degree_lineEdit)

        self.lon_dms_minute_lineEdit = CcLineEdit(str(0), 3)
        self.lon_dms_minute_lineEdit.textChanged.connect(self.validate_coordinates_int)
        self.lon_dms_horizontalLayout.addWidget(self.lon_dms_minute_lineEdit)

        self.lon_dms_second_lineEdit = CcLineEdit(str(0.0), 3)
        self.lon_dms_second_lineEdit.textChanged.connect(self.validate_coordinates_double)
        self.lon_dms_horizontalLayout.addWidget(self.lon_dms_second_lineEdit)

        # connect signal to function change_edit
        self.lat_degree_lineEdit.mousePressed.connect(self.change_edit)
        self.lon_degree_lineEdit.mousePressed.connect(self.change_edit)
        self.lat_dm_degree_lineEdit.mousePressed.connect(self.change_edit)
        self.lat_dm_minute_lineEdit.mousePressed.connect(self.change_edit)
        self.lon_dm_degree_lineEdit.mousePressed.connect(self.change_edit)
        self.lon_dm_minute_lineEdit.mousePressed.connect(self.change_edit)
        self.lat_dms_degree_lineEdit.mousePressed.connect(self.change_edit)
        self.lat_dms_minute_lineEdit.mousePressed.connect(self.change_edit)
        self.lat_dms_second_lineEdit.mousePressed.connect(self.change_edit)
        self.lon_dms_degree_lineEdit.mousePressed.connect(self.change_edit)
        self.lon_dms_minute_lineEdit.mousePressed.connect(self.change_edit)
        self.lon_dms_second_lineEdit.mousePressed.connect(self.change_edit)

        self.copyClipboard_pushButton.clicked.connect(self.copy_to_clipboard_degree)
        self.copyClipboard_pushButton_2.clicked.connect(self.copy_to_clipboard_degree_minute)
        self.copyClipboard_pushButton_3.clicked.connect(self.copy_to_clipboard_degree_minute_second)

    def convert(self):
        """Convert current coordinate format to others coordinate formats.
        example:
            DDD.DDDDº       -> DDDºMM.MM' and DDDºMM'SS.SSS''
            DDDºMM.MM'      -> DDD.DDDDº and DDDºMM'SS.SSS''
            DDDºMM'SS.SSS'' -> DDD.DDDDº and DDDºMM.MM'
        """
        # Check if format is correct
        if not self.is_correct():
            return

        # DDD.DDDDº changed
        if self.edited == 1:
            # get text
            lat_degree = self.lat_degree_lineEdit.text()
            lon_degree = self.lon_degree_lineEdit.text()

            logger.debug("lat: " + lat_degree + " lon:" + lon_degree)

            # convert degree to degreeminute
            lat_dm, lon_dm = degree_to_degree_minute(lat_degree, lon_degree)
            logger.debug("lat: " + str(lat_dm) + " lon:" + str(lon_dm))

            lat_d, lat_m = str(lat_dm).split('º ')
            lat_m, unused = lat_m.split('\'')

            self.lat_dm_degree_lineEdit.setText(str(lat_d))
            self.lat_dm_minute_lineEdit.setText(str(lat_m))

            lon_d, lon_m = str(lon_dm).split('º ')
            lon_m, unused = lon_m.split('\'')

            self.lon_dm_degree_lineEdit.setText(str(lon_d))
            self.lon_dm_minute_lineEdit.setText(str(lon_m))

            # convert degree to degminsec
            lat_dms, lon_dms = degree_to_degree_minute_second(float(lat_degree), float(lon_degree))
            logger.debug("lat: " + str(lat_dms) + " lon:" + str(lon_dms))

            lat_deg, lat_ms = str(lat_dms).split('º ')
            lat_ms, unused = lat_ms.split('\'\'')
            lat_min, lat_sec = lat_ms.split('\' ')

            self.lat_dms_degree_lineEdit.setText(str(lat_deg))
            self.lat_dms_minute_lineEdit.setText(str(lat_min))
            self.lat_dms_second_lineEdit.setText(str(lat_sec))

            lon_deg, lon_ms = str(lon_dms).split('º ')
            lon_ms, unused = lon_ms.split('\'\'')
            lon_min, lon_sec = lon_ms.split('\' ')

            self.lon_dms_degree_lineEdit.setText(str(lon_deg))
            self.lon_dms_minute_lineEdit.setText(str(lon_min))
            self.lon_dms_second_lineEdit.setText(str(lon_sec))

        # DDDºMM.MM' changed
        elif self.edited == 2:

            # get text
            lat_d = self.lat_dm_degree_lineEdit.text()
            lat_m = self.lat_dm_minute_lineEdit.text()
            lon_d = self.lon_dm_degree_lineEdit.text()
            lon_m = self.lon_dm_minute_lineEdit.text()

            lat_dm = [lat_d, lat_m]
            lon_dm = [lon_d, lon_m]

            # convert degree_minute to degree
            lat_degree, lon_degree = degree_minute_to_degree(lat_dm, lon_dm)
            logger.debug("lat: " + str(lat_degree) + " lon:" + str(lon_degree))
            self.lat_degree_lineEdit.setText(str(lat_degree))
            self.lon_degree_lineEdit.setText(str(lon_degree))

            # convert degree to degree_minute_second
            lat_dms, lon_dms = degree_to_degree_minute_second(float(lat_degree), float(lon_degree))
            logger.debug("lat: " + str(lat_dms) + " lon:" + str(lon_dms))

            lat_deg, lat_ms = str(lat_dms).split('º ')
            lat_ms, unused = lat_ms.split('\'\'')
            lat_min, lat_sec = lat_ms.split('\' ')

            self.lat_dms_degree_lineEdit.setText(str(lat_deg))
            self.lat_dms_minute_lineEdit.setText(str(lat_min))
            self.lat_dms_second_lineEdit.setText(str(lat_sec))

            lon_deg, lon_ms = str(lon_dms).split('º ')
            lon_ms, unused = lon_ms.split('\'\'')
            lon_min, lon_sec = lon_ms.split('\' ')

            self.lon_dms_degree_lineEdit.setText(str(lon_deg))
            self.lon_dms_minute_lineEdit.setText(str(lon_min))
            self.lon_dms_second_lineEdit.setText(str(lon_sec))

        # DDDºMM'SS.SSS''
        elif self.edited == 3:
            lat = self.lat_dms_degree_lineEdit.text() + 'º' + self.lat_dms_minute_lineEdit.text() + '\'' + self.lat_dms_second_lineEdit.text() + '\'\''
            lon = self.lon_dms_degree_lineEdit.text() + 'º' + self.lon_dms_minute_lineEdit.text() + '\'' + self.lon_dms_second_lineEdit.text() + '\'\''

            lat_degree, lon_degree = degree_minute_second_to_degree(lat, lon)
            logger.debug("lat: " + str(lat_degree) + " lon:" + str(lat_degree))
            self.lat_degree_lineEdit.setText(str(lat_degree))
            self.lon_degree_lineEdit.setText(str(lon_degree))

            lat_dm, lon_dm = degree_to_degree_minute(lat_degree, lon_degree)
            logger.debug("lat: " + str(lat_dm) + " lon:" + str(lon_dm))

            lat_d, lat_m = str(lat_dm).split('º ')
            lat_m, unused = lat_m.split('\'')

            self.lat_dm_degree_lineEdit.setText(str(lat_d))
            self.lat_dm_minute_lineEdit.setText(str(lat_m))

            lon_d, lon_m = str(lon_dm).split('º ')
            lon_m, unused = lon_m.split('\'')

            self.lon_dm_degree_lineEdit.setText(str(lon_d))
            self.lon_dm_minute_lineEdit.setText(str(lon_m))

    def change_edit(self, edit):
        """
        change the focus to edit
        :param edit:
        """
        self.edited = edit

    def copy_to_clipboard_degree(self):
        """Copy degrees to clipboard."""
        cb = QApplication.clipboard()
        cb.clear()
        cb.setText(self.lat_degree_lineEdit.text() + ", " + self.lon_degree_lineEdit.text())

    def copy_to_clipboard_degree_minute(self):
        """Copy degree_minute to clipboard."""
        cb = QApplication.clipboard()
        cb.clear()
        cb.setText(self.lat_dm_degree_lineEdit.text() + "º "
                   + self.lat_dm_minute_lineEdit.text() + "\'"
                   + ", "
                   + self.lon_dm_degree_lineEdit.text() + "º "
                   + self.lon_dm_minute_lineEdit.text() + "\'")

    def copy_to_clipboard_degree_minute_second(self):
        """Copy degree_minute_second to clipboard."""
        cb = QApplication.clipboard()
        cb.clear()
        cb.setText(self.lat_dms_degree_lineEdit.text() + "º "
                   + self.lat_dms_minute_lineEdit.text() + "'"
                   + self.lat_dms_second_lineEdit.text() + "\" "
                   + ", "
                   + self.lon_dms_degree_lineEdit.text() + "º "
                   + self.lon_dms_minute_lineEdit.text() + "'"
                   + self.lon_dms_second_lineEdit.text() + "\" ")

    def validate_coordinates_double(self):
        """validate line edit coordinates with double"""
        sender = self.sender()
        state = validate_custom_double(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def validate_coordinates_int(self):
        """validate line edit coordinates with int"""
        sender = self.sender()
        state = validate_custom_int(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def is_correct(self):
        """Checks if last edited coordinates have the correct format"""
        if self.edited == 1:
            if validate_custom_double(self.lat_degree_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lon_degree_lineEdit.text()) == QValidator.Acceptable:
                return True

        elif self.edited == 2:
            if validate_custom_int(self.lat_dm_degree_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lon_dm_degree_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lat_dm_minute_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lon_dm_minute_lineEdit.text()) == QValidator.Acceptable:
                return True

        elif self.edited == 3:
            if validate_custom_int(self.lat_dms_degree_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lon_dms_degree_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lat_dms_minute_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lon_dms_minute_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lat_dms_second_lineEdit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lon_dms_second_lineEdit.text()) == QValidator.Acceptable:
                return True

        return False


# coordinate converter LineEdit
class CcLineEdit(QLineEdit):
    mousePressed = pyqtSignal(float)

    def __init__(self, value, cc_type):
        super(CcLineEdit, self).__init__(value)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.type = cc_type  # 1: degree, 2: degree_minute, 3: degree_minute_second

    def mousePressEvent(self, event):
        self.mousePressed.emit(self.type)
