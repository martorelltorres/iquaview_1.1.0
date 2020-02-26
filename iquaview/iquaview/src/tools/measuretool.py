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
Map tool for measuring a distance in the map canvas.
"""
from math import degrees, sqrt, atan2, sin, cos
from qgis.core import (QgsDistanceArea,
                       QgsWkbTypes,
                       QgsProject,
                       QgsCoordinateReferenceSystem,
                       QgsGeometry,
                       QgsCircularString,
                       QgsPoint,
                       QgsUnitTypes)
from qgis.gui import QgsMapTool, QgsRubberBand
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox


class MeasureDistanceTool(QgsMapTool):
    finished = pyqtSignal()

    def __init__(self, canvas, msglog):
        super().__init__(canvas)
        self.canvas = canvas
        self.msglog = msglog
        self.start_point = self.end_point = None
        self.rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.setColor(QColor(255, 0, 0, 100))
        self.rubber_band.setWidth(3)
        self.rubber_band_points = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.rubber_band_points.setIconSize(10)
        self.rubber_band_points.setColor(QColor(255, 0, 0, 150))
        crs = self.canvas.mapSettings().destinationCrs()
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())
        self.reset()

    def reset(self):
        self.msglog.logMessage("")
        self.start_point = self.end_point = None
        self.rubber_band.reset(QgsWkbTypes.LineGeometry)
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)

    def canvasPressEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        transform = self.canvas.getCoordinateTransform()
        point = transform.toMapCoordinates(event.pos().x(), event.pos().y())
        if self.start_point:
            self.end_point = point
            self.rubber_band.addPoint(self.end_point)
            self.rubber_band_points.addPoint(self.end_point)
            distance = self.distance_calc.measureLine([self.start_point, self.end_point])
            bearing = self.distance_calc.bearing(self.start_point, point)
            distancemsg = QMessageBox(self.parent())
            distancemsg.finished.connect(self.deactivate)
            distancemsg.setWindowTitle("Measure tool")
            distancemsg.setText("Distance: {:.3F} m. Bearing: {:.3F} º".format(distance, degrees(bearing)))
            distancemsg.exec()
            self.finish()

        else:
            self.start_point = point
            self.rubber_band.addPoint(self.start_point)
            self.rubber_band_points.addPoint(self.start_point)

    def canvasMoveEvent(self, e):
        if self.start_point and not self.end_point:
            transform = self.canvas.getCoordinateTransform()
            point = transform.toMapCoordinates(e.pos().x(), e.pos().y())
            self.rubber_band.movePoint(point)
            distance = self.distance_calc.measureLine([self.start_point, point])
            bearing = self.distance_calc.bearing(self.start_point, point)
            self.msglog.logMessage("")
            self.msglog.logMessage("Current distance: {:.3F} m. Bearing: {:.3F} º".format(distance, degrees(bearing)), "Measure distance:", 0)

    def keyPressEvent(self, event):
        """
        When escape key is pressed, line is restarted
        """
        if event.key() == Qt.Key_Escape:
            self.reset()

    def finish(self):
        self.reset()
        self.finished.emit()


class MeasureAngleTool(QgsMapTool):
    finished = pyqtSignal()

    def __init__(self, canvas, msglog):
        super().__init__(canvas)
        self.canvas = canvas
        self.msglog = msglog
        self.start_point = self.middle_point = self.end_point = None
        self.rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.setColor(QColor(255, 0, 0, 100))
        self.rubber_band.setWidth(3)
        self.rubber_band_points = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.rubber_band_points.setIconSize(10)
        self.rubber_band_points.setColor(QColor(255, 0, 0, 150))
        self.rubber_band_curve = QgsRubberBand(self.canvas)
        self.rubber_band_curve.setWidth(2)
        self.rubber_band_curve.setColor(QColor(255, 153, 0, 100))

        crs = self.canvas.mapSettings().destinationCrs()
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())
        self.reset()

    def reset(self):
        self.msglog.logMessage("")
        self.start_point = self.middle_point = self.end_point = None
        self.rubber_band.reset(QgsWkbTypes.LineGeometry)
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
        self.rubber_band_curve.reset()

    def canvasPressEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        transform = self.canvas.getCoordinateTransform()
        point = transform.toMapCoordinates(event.pos().x(), event.pos().y())
        if self.start_point and self.middle_point:
            angle_start_to_middle = self.distance_calc.bearing(self.middle_point, self.start_point)
            angle_end_to_middle = self.distance_calc.bearing(self.middle_point, point)
            angle = degrees(angle_end_to_middle - angle_start_to_middle)
            if angle < -180:
                angle = 360 + angle
            elif angle > 180:
                angle = angle - 360

            anglemsg = QMessageBox(self.parent())
            anglemsg.finished.connect(self.deactivate)
            anglemsg.setWindowTitle("Measure angle tool")
            anglemsg.setText("Angle: {:.3F} º".format(abs(angle)))
            anglemsg.exec()
            self.finish()

        elif self.start_point:
            self.middle_point = point
            self.rubber_band.addPoint(self.middle_point)
            self.rubber_band_points.addPoint(self.middle_point)

        else:
            self.start_point = point
            self.rubber_band.addPoint(self.start_point)
            self.rubber_band_points.addPoint(self.start_point)

    def canvasMoveEvent(self, e):
        if self.start_point and not self.end_point:
            transform = self.canvas.getCoordinateTransform()
            point = transform.toMapCoordinates(e.pos().x(), e.pos().y())
            self.rubber_band.movePoint(point)

        if self.start_point and self.middle_point and not self.end_point:
            angle_start_to_middle = self.distance_calc.bearing(self.middle_point, self.start_point)
            angle_end_to_middle = self.distance_calc.bearing(self.middle_point, point)
            angle = degrees(angle_end_to_middle - angle_start_to_middle)

            if angle < -180:
                angle = 360 + angle
            elif angle > 180:
                angle = angle - 360

            self.msglog.logMessage("")
            self.msglog.logMessage("Current angle: {:.3F} º".format(abs(angle)), "Measure angle:", 0)

            self.rubber_band_curve.reset()

            # get the distance from center to point
            dist_mid_to_p = sqrt((point.x() - self.middle_point.x())*(point.x() - self.middle_point.x()) +
                                     (point.y() - self.middle_point.y())*(point.y() - self.middle_point.y()))
            dist_mid_to_start = sqrt((self.start_point.x() - self.middle_point.x())*(self.start_point.x() - self.middle_point.x()) +
                                     (self.start_point.y() - self.middle_point.y())*(self.start_point.y() - self.middle_point.y()))

            # get angle
            angle_start = atan2(self.start_point.y() - self.middle_point.y(), self.start_point.x() - self.middle_point.x())
            angle_p = atan2(point.y() - self.middle_point.y(), point.x() - self.middle_point.x())

            # smaller distance
            if dist_mid_to_p < dist_mid_to_start:
                dist = dist_mid_to_p
            else:
                dist = dist_mid_to_start

            y_p = dist * sin(angle_p)
            x_p = dist * cos(angle_p)
            y_start = dist * sin(angle_start)
            x_start = dist * cos(angle_start)

            circular_ring = QgsCircularString()
            circular_ring = circular_ring.fromTwoPointsAndCenter(
                                     QgsPoint(self.middle_point.x() + x_start / 2,
                                              self.middle_point.y() + y_start / 2),
                                     QgsPoint(self.middle_point.x() + x_p / 2,
                                              self.middle_point.y() + y_p / 2),
                                     QgsPoint(self.middle_point.x(),
                                              self.middle_point.y()),
                                     True)

            circular_geometry = QgsGeometry(circular_ring)

            self.rubber_band_curve.addGeometry(circular_geometry,
                                               QgsCoordinateReferenceSystem(4326,
                                                                            QgsCoordinateReferenceSystem.EpsgCrsId))

    def keyPressEvent(self, event):
        """
        When escape key is pressed, line is restarted
        """
        if event.key() ==  Qt.Key_Escape:
            self.reset()

    def finish(self):
        self.reset()
        self.finished.emit()


class MeasureAreaTool(QgsMapTool):
    finished = pyqtSignal()

    def __init__(self, canvas, msglog):
        super().__init__(canvas)
        self.canvas = canvas
        self.msglog = msglog
        self.start_point = self.middle_point = self.end_point = None
        self.rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.rubber_band.setColor(QColor(255, 0, 0, 100))
        self.rubber_band.setWidth(3)
        self.rubber_band_points = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.rubber_band_points.setIconSize(10)
        self.rubber_band_points.setColor(QColor(255, 0, 0, 150))

        crs = self.canvas.mapSettings().destinationCrs()
        self.area_calc = QgsDistanceArea()
        self.area_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.area_calc.setEllipsoid(crs.ellipsoidAcronym())
        self.reset()

    def reset(self):
        """ Reset log message and rubber band"""
        self.msglog.logMessage("")
        self.start_point = self.end_point = None
        self.rubber_band.reset(QgsWkbTypes.PolygonGeometry)
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)

    def canvasPressEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        transform = self.canvas.getCoordinateTransform()
        point = transform.toMapCoordinates(event.pos().x(), event.pos().y())

        if self.start_point and event.button() == Qt.RightButton:
            multipoint = self.rubber_band.asGeometry()
            area = self.area_calc.measureArea(multipoint)
            anglemsg = QMessageBox(self.parent())
            anglemsg.finished.connect(self.deactivate)
            anglemsg.setWindowTitle("Measure area tool")
            anglemsg.setText("Area: {} ".format(self.area_calc.formatArea(area, 3, QgsUnitTypes.AreaSquareMeters, True)))
            anglemsg.exec()
            self.finish()
        elif self.start_point:
            self.rubber_band.addPoint(point)
            self.rubber_band_points.addPoint(point)

        else:
            self.start_point = point
            self.rubber_band.addPoint(self.start_point)
            self.rubber_band_points.addPoint(self.start_point)

    def canvasMoveEvent(self, e):
        if self.start_point and not self.end_point:
            transform = self.canvas.getCoordinateTransform()
            point = transform.toMapCoordinates(e.pos().x(), e.pos().y())
            self.rubber_band.movePoint(point)

            multipoint = self.rubber_band.asGeometry()
            area = self.area_calc.measureArea(multipoint)
            self.msglog.logMessage("")
            self.msglog.logMessage("Current area: {} ".format(self.area_calc.formatArea(area,
                                                                                        3,
                                                                                        QgsUnitTypes.AreaSquareMeters,
                                                                                        True)), "Measure Area:", 0)

    def keyPressEvent(self, event):
        """
        When escape key is pressed, line is restarted
        """
        if event.key() ==  Qt.Key_Escape:
            self.reset()

    def finish(self):
        self.reset()
        self.finished.emit()
