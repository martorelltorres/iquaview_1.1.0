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
 Dialog to add and landmark point (latitude, longitude)
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QValidator
from PyQt5.Qt import QApplication

from qgis.core import QgsFeature, QgsVectorLayer, QgsPointXY, QgsGeometry, QgsMapLayer

from iquaview.src.ui.ui_point_feature import Ui_PointFeature
from iquaview.src.mapsetup import  addlandmarktool
from iquaview.src.utils.coordinateconverter import (degree_to_degree_minute,
                                                    degree_minute_to_degree,
                                                    degree_to_degree_minute_second,
                                                    degree_minute_second_to_degree)
from iquaview.src.utils.textvalidator import (validate_custom_double,
                                              validate_custom_int,
                                              get_color,
                                              get_custom_int_validator,
                                              get_custom_double_validator)


class PointFeatureDlg(QDialog, Ui_PointFeature):
    map_tool_change_signal = pyqtSignal()
    landmark_added = pyqtSignal(QgsMapLayer)
    landmark_removed = pyqtSignal(QgsMapLayer)
    finish_add_landmark_signal = pyqtSignal()

    def __init__(self, canvas, proj, parent=None):
        super(PointFeatureDlg, self).__init__(parent)
        self.setupUi(self)

        self.point = None
        self.point_layer = None
        self.feat = None
        self.num = 1
        self.canvas = canvas
        self.proj = proj

        self.double_validator = get_custom_double_validator()
        self.int_validator = get_custom_int_validator()

        self.getCoordinatesButton.setIcon(QIcon(":/resources/pickPointInMap.svg"))
        self.getCoordinatesButton.clicked.connect(self.set_point_tool)
        self.getCoordinatesButton.setToolTip("Pick point in map")

        self.copy_to_clipboardButton.setIcon(QIcon(":/resources/mActionCopyClipboard.svg"))
        self.copy_to_clipboardButton.setToolTip("Copy to clipboard")
        self.copy_to_clipboardButton.clicked.connect(self.copy_to_clipboard)

        self.tool_add_landmark = addlandmarktool.AddLandmarkTool(canvas)
        self.tool_add_landmark.point_signal.connect(self.add_new_landmark)
        self.previous_coordinates_format = self.comboBox.currentText()
        self.comboBox.currentIndexChanged.connect(self.set_format)

    def get_coordinates(self):
        """ Return the coordinates (latitude, longitude)
        :return : latitude, longitude
        """
        return self.point.y(), self.point.x()

    def set_point_tool(self):
        """Set the maptool to pointTool"""
        self.map_tool_change_signal.emit() #Emit signal to warn mainwindow that we are changing a maptool
        self.canvas.setMapTool(self.tool_add_landmark)

    def add_new_landmark(self, point):
        """
        create a landmark point
        :param point: Point to add on the canvas
        """
        if self.feat is not None:
            self.point_layer.dataProvider().deleteFeatures([self.feat.id()])
            self.landmark_removed.emit(self.point_layer)

        self.point = point
        name = "LandmarkPoint_" + str(self.num)
        restart_search = True
        # This loops tries to find a free name for the LandmarkPoint_
        while restart_search:
            restart_search = False
            # for every layer
            for layer in self.proj.mapLayers().values():
                # check name
                if layer.name() == name:
                    self.num += 1
                    name = "LandmarkPoint_" + str(self.num)
                    # Set to True to find the next LandmarkPoint
                    restart_search = True

        self.point_layer = QgsVectorLayer(
            "Point?crs=epsg:4326",
            name,
            "memory")

        self.feat = QgsFeature()
        self.feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(self.point.x(), self.point.y())))
        self.point_layer.dataProvider().addFeatures([self.feat])
        self.landmark_added.emit(self.point_layer)

        if self.comboBox.currentText() == "Decimal degrees":
            self.set_degrees_from_point()

        if self.comboBox.currentText() == "Degrees, minutes":
            # convert degree to degreeminute
            self.set_degrees_minutes_from_point()

        if self.comboBox.currentText() == "Degrees, minutes, seconds":
            # convert degree to degminsec
            self.set_degrees_minutes_seconds_from_point()

    def set_format(self):
        """ Set widgets on dialog according with combobox coordinates format"""

        if self.previous_coordinates_format == "Decimal degrees":

            if validate_custom_double(self.lon_degrees_lineedit.text()) == QValidator.Acceptable and \
                    validate_custom_double(self.lat_degrees_lineedit.text()) == QValidator.Acceptable:

                self.point = QgsPointXY(float(self.lon_degrees_lineedit.text()),
                                        float(self.lat_degrees_lineedit.text()))
            else:
                self.point = None

        elif self.previous_coordinates_format == "Degrees, minutes":
            lat_d = self.lat_degrees_lineedit.text()
            lat_m = self.lat_minutes_lineedit.text()
            lon_d = self.lon_degrees_lineedit.text()
            lon_m = self.lon_minutes_lineedit.text()

            if validate_custom_int(lat_d) == QValidator.Acceptable \
                and validate_custom_double(lat_m) == QValidator.Acceptable \
                and validate_custom_int(lon_d) == QValidator.Acceptable \
                and validate_custom_double(lon_m) == QValidator.Acceptable:

                lat_dm = [lat_d, lat_m]
                lon_dm = [lon_d, lon_m]

                # convert degree_minute to degree
                lat_degree, lon_degree = degree_minute_to_degree(lat_dm, lon_dm)
                self.point = QgsPointXY(float(lon_degree),
                                        float(lat_degree))
            else:

                self.point = None

        elif self.previous_coordinates_format == "Degrees, minutes, seconds":
            if validate_custom_int(self.lat_degrees_lineedit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lat_minutes_lineedit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lat_seconds_lineedit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lon_degrees_lineedit.text()) == QValidator.Acceptable \
                    and validate_custom_int(self.lon_minutes_lineedit.text()) == QValidator.Acceptable \
                    and validate_custom_double(self.lon_seconds_lineedit.text()) == QValidator.Acceptable:

                lat = self.lat_degrees_lineedit.text() + 'º' + self.lat_minutes_lineedit.text() + '\'' + self.lat_seconds_lineedit.text() + '\'\''
                lon = self.lon_degrees_lineedit.text() + 'º' + self.lon_minutes_lineedit.text() + '\'' + self.lon_seconds_lineedit.text() + '\'\''

                lat_degree, lon_degree = degree_minute_second_to_degree(lat, lon)
                self.point = QgsPointXY(float(lon_degree),
                                        float(lat_degree))

            else:
                self.point = None

        # delete previous widgets
        self.delete_all(self.latitude_layout)
        self.delete_all(self.longitude_layout)

        lat_label = QLabel(self)
        lat_label.setText("Latitude: ")
        lat_label.setFixedWidth(75)
        lon_label = QLabel(self)
        lon_label.setText("Longitude: ")
        lon_label.setFixedWidth(75)

        self.latitude_layout.addWidget(lat_label)
        self.longitude_layout.addWidget(lon_label)

        if self.comboBox.currentText() == "Decimal degrees" or self.previous_coordinates_format is None:
            self.lat_degrees_lineedit = QLineEdit(self)
            self.lon_degrees_lineedit = QLineEdit(self)

            self.lat_degrees_lineedit.textChanged.connect(self.validate_coordinates_double)
            self.lon_degrees_lineedit.textChanged.connect(self.validate_coordinates_double)

            self.latitude_layout.addWidget(self.lat_degrees_lineedit)
            self.longitude_layout.addWidget(self.lon_degrees_lineedit)

            self.set_degrees_from_point()


        if self.comboBox.currentText() == "Degrees, minutes":

            lat_deg_label = QLabel(self)
            lat_deg_label.setText("º")
            lon_deg_label = QLabel(self)
            lon_deg_label.setText("º")
            lat_min_label = QLabel(self)
            lat_min_label.setText("\'")
            lon_min_label = QLabel(self)
            lon_min_label.setText("\'")
            self.lat_degrees_lineedit = QLineEdit(self)
            self.lon_degrees_lineedit = QLineEdit(self)
            self.lat_minutes_lineedit = QLineEdit(self)
            self.lon_minutes_lineedit = QLineEdit(self)

            self.lat_degrees_lineedit.textChanged.connect(self.validate_coordinates_int)
            self.lon_degrees_lineedit.textChanged.connect(self.validate_coordinates_int)
            self.lat_minutes_lineedit.textChanged.connect(self.validate_coordinates_double)
            self.lon_minutes_lineedit.textChanged.connect(self.validate_coordinates_double)

            self.latitude_layout.addWidget(self.lat_degrees_lineedit)
            self.latitude_layout.addWidget(lat_deg_label)
            self.latitude_layout.addWidget(self.lat_minutes_lineedit)
            self.latitude_layout.addWidget(lat_min_label)

            self.longitude_layout.addWidget(self.lon_degrees_lineedit)
            self.longitude_layout.addWidget(lon_deg_label)
            self.longitude_layout.addWidget(self.lon_minutes_lineedit)
            self.longitude_layout.addWidget(lon_min_label)

            self.set_degrees_minutes_from_point()


        if self.comboBox.currentText() == "Degrees, minutes, seconds":

            lat_deg_label = QLabel(self)
            lat_deg_label.setText("º")
            lon_deg_label = QLabel(self)
            lon_deg_label.setText("º")
            lat_min_label = QLabel(self)
            lat_min_label.setText("\'")
            lon_min_label = QLabel(self)
            lon_min_label.setText("\'")
            lat_sec_label = QLabel(self)
            lat_sec_label.setText("\'\'")
            lon_sec_label = QLabel(self)
            lon_sec_label.setText("\'\'")
            self.lat_degrees_lineedit = QLineEdit(self)
            self.lon_degrees_lineedit = QLineEdit(self)
            self.lat_minutes_lineedit = QLineEdit(self)
            self.lon_minutes_lineedit = QLineEdit(self)
            self.lat_seconds_lineedit = QLineEdit(self)
            self.lon_seconds_lineedit = QLineEdit(self)

            self.lat_degrees_lineedit.textChanged.connect(self.validate_coordinates_int)
            self.lon_degrees_lineedit.textChanged.connect(self.validate_coordinates_int)
            self.lat_minutes_lineedit.textChanged.connect(self.validate_coordinates_int)
            self.lon_minutes_lineedit.textChanged.connect(self.validate_coordinates_int)
            self.lat_seconds_lineedit.textChanged.connect(self.validate_coordinates_double)
            self.lon_seconds_lineedit.textChanged.connect(self.validate_coordinates_double)

            self.latitude_layout.addWidget(self.lat_degrees_lineedit)
            self.latitude_layout.addWidget(lat_deg_label)
            self.latitude_layout.addWidget(self.lat_minutes_lineedit)
            self.latitude_layout.addWidget(lat_min_label)
            self.latitude_layout.addWidget(self.lat_seconds_lineedit)
            self.latitude_layout.addWidget(lat_sec_label)

            self.longitude_layout.addWidget(self.lon_degrees_lineedit)
            self.longitude_layout.addWidget(lon_deg_label)
            self.longitude_layout.addWidget(self.lon_minutes_lineedit)
            self.longitude_layout.addWidget(lon_min_label)
            self.longitude_layout.addWidget(self.lon_seconds_lineedit)
            self.longitude_layout.addWidget(lon_sec_label)

            self.set_degrees_minutes_seconds_from_point()


        self.previous_coordinates_format = self.comboBox.currentText()

    def set_degrees_from_point(self):
        """ From point in degrees, fill degrees QLineEdits"""
        if self.point is not None:

            lat_degrees_text = str(self.point.y())
            lon_degrees_text = str(self.point.x())

            if (validate_custom_double(lat_degrees_text) == QValidator.Acceptable and
                    validate_custom_double(lon_degrees_text) == QValidator.Acceptable):

                self.lat_degrees_lineedit.setText("{:.8F}".format(float(lat_degrees_text)))
                self.lon_degrees_lineedit.setText("{:.8F}".format(float(lon_degrees_text)))

    def set_degrees_minutes_from_point(self):
        """ From point in degrees, fill degrees and minutesQLineEdits"""

        if self.point is not None:

            lat_degrees_text = str(self.point.y())
            lon_degrees_text = str(self.point.x())

            if (validate_custom_double(lat_degrees_text) == QValidator.Acceptable and
                    validate_custom_double(lon_degrees_text) == QValidator.Acceptable):

                lat_dm, lon_dm = degree_to_degree_minute(float(lat_degrees_text), float(lon_degrees_text))

                lat_d, lat_m = str(lat_dm).split('º')
                lat_m, unused = lat_m.split('\'')

                lon_d, lon_m = str(lon_dm).split('º')
                lon_m, unused = lon_m.split('\'')

                self.lat_degrees_lineedit.setText("{:d}".format(int(lat_d)))
                self.lat_minutes_lineedit.setText("{:.8F}".format(float(lat_m)))
                self.lon_degrees_lineedit.setText("{:d}".format(int(lon_d)))
                self.lon_minutes_lineedit.setText("{:.8F}".format(float(lon_m)))

    def set_degrees_minutes_seconds_from_point(self):
        """ From point in degrees, fill degrees, minutes and seconds QLineEdits"""

        if self.point is not None:

            lat_degrees_text = str(self.point.y())
            lon_degrees_text = str(self.point.x())

            if (validate_custom_double(lat_degrees_text) == QValidator.Acceptable and
                    validate_custom_double(lon_degrees_text) == QValidator.Acceptable):

                lat_dms, lon_dms = degree_to_degree_minute_second(float(lat_degrees_text), float(lon_degrees_text))

                lat_deg, lat_ms = str(lat_dms).split('º')
                lat_ms, unused = lat_ms.split('\'\'')
                lat_min, lat_sec = lat_ms.split('\'')

                lon_deg, lon_ms = str(lon_dms).split('º')
                lon_ms, unused = lon_ms.split('\'\'')
                lon_min, lon_sec = lon_ms.split('\'')

                self.lat_degrees_lineedit.setText("{:d}".format(int(lat_deg)))
                self.lat_minutes_lineedit.setText("{:d}".format(int(lat_min)))
                self.lat_seconds_lineedit.setText("{:.8F}".format(float(lat_sec)))
                self.lon_degrees_lineedit.setText("{:d}".format(int(lon_deg)))
                self.lon_minutes_lineedit.setText("{:d}".format(int(lon_min)))
                self.lon_seconds_lineedit.setText("{:.8F}".format(float(lon_sec)))

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

    def reset(self):
        """ Reset params"""
        self.comboBox.setCurrentIndex(0)
        self.point = None
        self.point_layer = None
        self.feat = None
        self.previous_coordinates_format = None

        self.set_format()

    def copy_to_clipboard(self):
        """Copy coordinates to clipboard"""
        cb = QApplication.clipboard()
        cb.clear()
        if self.comboBox.currentText() == "Decimal degrees" :
            cb.setText("{}, {}".format(self.lat_degrees_lineedit.text(),self.lon_degrees_lineedit.text()))
        if self.comboBox.currentText() == "Degrees, minutes":
            cb.setText("{}º {}', {}º {}\'".format(self.lat_degrees_lineedit.text(), self.lat_minutes_lineedit.text(),
                                            self.lon_degrees_lineedit.text(), self.lon_minutes_lineedit.text()))
        if self.comboBox.currentText() == "Degrees, minutes, seconds":
            cb.setText("{}º {}' {}\'\', {}º {}\' {}\'\'".format(self.lat_degrees_lineedit.text(),
                                                  self.lat_minutes_lineedit.text(),
                                                  self.lat_seconds_lineedit.text(),
                                                  self.lon_degrees_lineedit.text(),
                                                  self.lon_minutes_lineedit.text(),
                                                  self.lon_seconds_lineedit.text()))

    def accept(self):
        """ Insert self.pont in the canvas"""
        self.set_format()
        if self.point is not None:
            new_point = QgsPointXY(float(self.get_coordinates()[1]),
                                   float(self.get_coordinates()[0]))
            if self.point_layer is None:
                self.add_new_landmark(self.point)

            self.point_layer.startEditing()
            self.point_layer.beginEditCommand("Move Point")  # for undo
            self.point_layer.moveVertex(new_point.x(), new_point.y(), self.feat.id() + 1, 0)
            self.point_layer.endEditCommand()
            self.point_layer.commitChanges()

            self.finish_add_landmark_signal.emit()
            super(PointFeatureDlg, self).accept()
        else:
            QMessageBox.warning(self,
                                "Invalid Point",
                                "Invalid point, make sure the coordinates are correct.",
                                QMessageBox.Close)

    def reject(self):
        """ reject point insertion"""
        if self.feat is not None:
            # if we are aborting, point is deleted
            self.point_layer.dataProvider().deleteFeatures([self.feat.id()])
            self.landmark_removed.emit(self.point_layer)

        self.finish_add_landmark_signal.emit()
        super(PointFeatureDlg, self).reject()

    def delete_all(self, layout):
        """
        delete all widget from layout
        :param layout: layout is a qt layout
        """
        if layout is not None:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_all(item.layout())
