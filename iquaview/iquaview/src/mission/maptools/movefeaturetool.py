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
Map tool for moving a clicked mission track.
"""

import logging
from math import degrees, cos

from qgis.core import (QgsTolerance,
                       QgsRectangle,
                       QgsFeatureRequest,
                       QgsFeature,
                       QgsWkbTypes,
                       QgsPointXY,
                       QgsGeometry,
                       QgsDistanceArea,
                       QgsCoordinateReferenceSystem,
                       QgsProject)
from qgis.gui import QgsMapTool, QgsRubberBand

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from iquaview.src.utils.calcutils import endpoint

logger = logging.getLogger(__name__)


class MoveFeatureTool(QgsMapTool):
    def __init__(self, mission_track, canvas):
        QgsMapTool.__init__(self, canvas)
        self.band = None
        self.feature = None
        self.startcoord = None
        self.mission_track = mission_track
        self.layer = mission_track.get_mission_layer()
        self.clicked_outside_layer = False
        self.mCtrl = False
        self.rot_center = None
        self.rot_center_rb = None
        self.ini_rot_point = None
        self.last_rot_angle = 0.0
        self.curr_angle = 0.0
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')
        self.ini_geom = next(self.layer.dataProvider().getFeatures()).geometry()
        logger.info(mission_track.get_mission_name())

    def canvasMoveEvent(self, event):
        """
        Override of QgsMapTool mouse move event
        """
        if self.band and not self.mCtrl:
            point = self.toMapCoordinates(event.pos())
            offset_x = point.x() - self.startcoord.x()
            offset_y = point.y() - self.startcoord.y()
            self.band.setTranslationOffset(offset_x, offset_y)
            self.band.updatePosition()
            self.band.update()

        if self.band and self.mCtrl:
            end_rot_point = self.toMapCoordinates(event.pos())
            self.curr_angle = self.distance.bearing(self.rot_center, end_rot_point) \
                        - self.distance.bearing(self.rot_center, self.ini_rot_point)\
                        + self.last_rot_angle
            self.rotate_and_project_band(self.curr_angle)

    def canvasPressEvent(self, event):
        """
        Override of QgsMapTool mouse press event
        """

        if event.button() == Qt.LeftButton and not self.mCtrl:

            if self.band:
                self.band.hide()
                self.band = None
            self.feature = None

            logger.info("layer feature count {}".format(self.layer.featureCount()))
            if not self.layer:
                return

            logger.info("Trying to find feature in layer")
            point = self.toLayerCoordinates(self.layer, event.pos())
            search_radius = (QgsTolerance.toleranceInMapUnits(10, self.layer,
                                                              self.canvas().mapSettings(), QgsTolerance.Pixels))

            rect = QgsRectangle()
            rect.setXMinimum(point.x() - search_radius)
            rect.setXMaximum(point.x() + search_radius)
            rect.setYMinimum(point.y() - search_radius)
            rect.setYMaximum(point.y() + search_radius)

            rq = QgsFeatureRequest().setFilterRect(rect)

            f = QgsFeature()
            self.layer.getFeatures(rq).nextFeature(f)
            if f.geometry():
                self.band = self.create_rubber_band()
                self.band.setToGeometry(f.geometry(), self.layer)
                self.band.show()
                self.startcoord = self.toMapCoordinates(event.pos())
                self.feature = f
                self.clicked_outside_layer = False
                return
            else:
                self.clicked_outside_layer = True

    def canvasReleaseEvent(self, event):
        """
        Override of QgsMapTool mouse release event
        """
        if event.button() == Qt.LeftButton and not self.mCtrl:
            if not self.band:
                if self.clicked_outside_layer and len(self.mission_track.find_waypoints_in_mission()) > 0:
                    confirmation_msg = "Do you want to move the mission ? \n\n" \
                                       "First waypoint will set on the marked point."
                    reply = QMessageBox.question(self.parent(), 'Movement Confirmation',
                                                 confirmation_msg, QMessageBox.Yes, QMessageBox.No)

                    if reply == QMessageBox.Yes:
                        feats = self.layer.getFeatures()
                        for f in feats:  # will be only one
                            if self.layer.geometryType() == QgsWkbTypes.LineGeometry:
                                list_wp = f.geometry().asPolyline()
                                self.startcoord = self.toLayerCoordinates(self.layer, list_wp[0])
                            elif self.layer.geometryType() == QgsWkbTypes.PointGeometry:
                                wp = f.geometry().asPoint()
                                self.startcoord = self.toLayerCoordinates(self.layer, wp)
                            self.feature = f
                        self.move_position(event.pos())
                return

            if not self.layer:
                return

            if not self.feature:
                return

            self.move_position(event.pos())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and self.band is None \
                and len(self.mission_track.find_waypoints_in_mission()) > 1:
            self.mCtrl = True
            self.show_rotation_center()
            self.show_rubber_band()
            self.rotate_and_project_band(self.last_rot_angle)
            self.ini_rot_point = self.toMapCoordinates(self.canvas().mouseLastXY())

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control and self.mCtrl:
            self.mCtrl = False
            self.rotate_and_project_mission()
            self.hide_rotation_center()
            self.hide_rubber_band()
            self.last_rot_angle = self.curr_angle

    def move_position(self, pos):
        start_point = self.toLayerCoordinates(self.layer, self.startcoord)
        end_point = self.toLayerCoordinates(self.layer, pos)

        # Find vertical distance to be translated
        a = self.distance.bearing(start_point, end_point)
        d = self.distance.measureLine(start_point, end_point)
        vertical_dist = abs(cos(a) * d)

        # If translating a point or if translation is small,
        # do a simple translation (very small error, proportional to vertical dist)
        if vertical_dist < 9000 or self.layer.geometryType() == QgsWkbTypes.PointGeometry:
            dx = end_point.x() - start_point.x()
            dy = end_point.y() - start_point.y()
            self.layer.startEditing()
            self.layer.translateFeature(self.feature.id(), dx, dy)
            self.layer.commitChanges()

        # If translation is big, translate and project (small and constant error due to approximations in calculations)
        else:
            ini_coords = next(self.layer.dataProvider().getFeatures()).geometry().asPolyline()
            end_coords = []
            if len(ini_coords) > 1:
                dx = end_point.x() - start_point.x()
                dy = end_point.y() - start_point.y()
                end_c = QgsPointXY(ini_coords[0].x() + dx, ini_coords[0].y() + dy)
                end_coords.append(end_c)
                for i in range(1, len(ini_coords)):
                    dist = self.distance.measureLine(ini_coords[i-1], ini_coords[i])
                    angle = self.distance.bearing(ini_coords[i-1], ini_coords[i])
                    end_c = endpoint(end_coords[i-1], dist, degrees(angle))
                    end_coords.append(end_c)

                feature = next(self.layer.dataProvider().getFeatures())
                self.layer.startEditing()
                self.layer.changeGeometry(feature.id(), QgsGeometry.fromPolylineXY(end_coords))
                self.layer.commitChanges()

        if self.band is not None:
            self.band.hide()
            self.band = None

        # get new waypoints and put them into mission structure
        feats = self.layer.getFeatures()
        for f in feats:  # will be only one
            if self.layer.geometryType() == QgsWkbTypes.LineGeometry:
                list_wp = f.geometry().asPolyline()
                for wp in range(0, len(list_wp)):
                    point = list_wp[wp]
                    self.mission_track.change_position(wp, point)
            elif self.layer.geometryType() == QgsWkbTypes.PointGeometry:
                wp = f.geometry().asPoint()
                self.mission_track.change_position(0, wp)

        # rotation center and geometry have changed, set rot_center to none to recalculate when needed
        self.rot_center = None
        self.last_rot_angle = 0.0
        self.ini_geom = next(self.layer.dataProvider().getFeatures()).geometry()

    def deactivate(self):
        """
        Deactive the tool.
        """
        self.hide_rotation_center()
        self.hide_rubber_band()

    def create_rubber_band(self):
        """
        Creates a new rubber band.
        """
        band = QgsRubberBand(self.canvas())
        band.setColor(QColor("green"))
        band.setWidth(2)
        band.setLineStyle(Qt.DashLine)
        return band

    def show_rotation_center(self):
        """
        Shows rotation center of the mission with a point rubber band
        """
        if len(self.mission_track.find_waypoints_in_mission()) > 1:
            feature = next(self.layer.dataProvider().getFeatures())
            list_wp = feature.geometry().asPolyline()
            if self.rot_center is None or self.rot_center_rb is None:
                self.rot_center = self.find_geometric_center(list_wp)
                self.rot_center_rb = QgsRubberBand(self.canvas())
                self.rot_center_rb.setColor(QColor("black"))
                self.rot_center_rb.setWidth(3)
                self.rot_center_rb.setToGeometry(QgsGeometry.fromPointXY(self.rot_center), None)
                self.rot_center_rb.update()
            else:
                self.rot_center_rb.show()

    def hide_rotation_center(self):
        """
        Hides the rotation center of the mission and deletes the point rubber band
        """
        if self.rot_center_rb:
            self.rot_center_rb.hide()
            # self.rot_center_rb = None

    def find_geometric_center(self, list_wp):
        """
        Finds geometric center from a list of waypoints

        :param list_wp: list of waypoints
        :return: geometric center of the list of waypoints
        """
        center = QgsPointXY()
        max_x = None
        min_x = None
        max_y = None
        min_y = None

        # Geometric center
        for i in range(0, len(list_wp)):
            point = list_wp[i]
            if max_x is None or point.x() > max_x:
                max_x = point.x()
            if min_x is None or point.x() < min_x:
                min_x = point.x()
            if max_y is None or point.y() > max_y:
                max_y = point.y()
            if min_y is None or point.y() < min_y:
                min_y = point.y()

        center.setX((max_x + min_x)/2)
        center.setY((max_y + min_y)/2)

        return center

    def show_rubber_band(self):
        """
        Creates and shows a rubber band with the geometry of the mission
        """
        if len(self.mission_track.find_waypoints_in_mission()) > 1:
            self.band = self.create_rubber_band()
            self.band.setToGeometry(self.ini_geom, self.layer)

    def hide_rubber_band(self):
        """
        Hides and deletes the rubber band of the geometry of the mission
        """
        if self.band:
            self.band.hide()
            self.band = None

    def rotate_and_project_band(self, rot_angle=0.0):
        """
        Rebuilds the initial geometry of the mission rotated with the angle defined by rot_angle and it gets stored in
        the geometry of self.band

        :param rot_angle: Angle used to rotate the geometry
        """
        ini_coords = self.ini_geom.asPolyline()
        end_coords = []
        if len(ini_coords) > 1:
            dist = self.distance.measureLine(self.rot_center, ini_coords[0])
            angle = self.distance.bearing(self.rot_center, ini_coords[0]) + rot_angle
            end_first_wp = endpoint(self.rot_center, dist, degrees(angle))
            end_coords.append(end_first_wp)
            for i in range(1, len(ini_coords)):
                dist = self.distance.measureLine(ini_coords[i-1], ini_coords[i])
                angle = self.distance.bearing(ini_coords[i-1], ini_coords[i]) + rot_angle
                end_c = endpoint(end_coords[i-1], dist, degrees(angle))
                end_coords.append(end_c)

            end_band_geom = QgsGeometry().fromPolylineXY(end_coords)
            self.band.setToGeometry(end_band_geom, self.layer)

    def rotate_and_project_mission(self):
        """
        Copy the changes from the rotated and projected rubber band to the geometry of the mission
        """
        list_wp = self.band.asGeometry().asPolyline()
        if len(list_wp) > 1:
            for i in range(0, len(list_wp)):
                point = list_wp[i]
                self.mission_track.change_position(i, point)
            feature = next(self.layer.dataProvider().getFeatures())
            self.layer.startEditing()
            self.layer.changeGeometry(feature.id(), self.band.asGeometry())
            self.layer.commitChanges()
