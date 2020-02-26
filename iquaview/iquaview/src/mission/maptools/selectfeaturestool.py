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
Map tool to select multiple features of a layer graphically
"""
import math
import logging

from qgis.core import QgsGeometry, QgsWkbTypes, QgsPointXY, QgsFeature
from qgis.gui import QgsMapTool, QgsRubberBand
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QColor

logger = logging.getLogger(__name__)


class SelectFeaturesTool(QgsMapTool):
    selection_clicked = pyqtSignal(list)

    def __init__(self, mission_track, canvas):
        QgsMapTool.__init__(self, canvas)
        self.setCursor(Qt.ArrowCursor)
        self.mission_track = mission_track
        self.layer = self.mission_track.get_mission_layer()
        self.rubber_band = None
        self.rubber_band_points = None
        self.selection_polygon = []
        self.indexes_within_list = []
        self.band_finished = True
        self.mCtrl = False
        self.p0, self.p1, self.p2, self.p3 = None, None, None, None
        self.mission_track.mission_changed.connect(self.update_rubber_band)
        self.mission_track.step_removed.connect(self.remove_rubber_band)
        self.wp = self.mission_track.find_waypoints_in_mission()
        self.layer.startEditing()
        self.rubber_band_vs_track_indexes = {}
        self.rubber_band_points = QgsRubberBand(self.canvas(), QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.rubber_band_points.setIconSize(10)
        self.rubber_band_points.setColor(QColor("green"))
        self.rubber_band_vertex_counter = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False
        if event.key() == Qt.Key_Escape:
            self.p0, self.p1, self.p2, self.p3 = None, None, None, None
            if self.rubber_band:
                self.rubber_band.reset(True)
            self.close_polygon_band()
            self.band_finished = True
            self.canvas().refresh()
            return

    def canvasPressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = self.toMapCoordinates(event.pos())
            # check if we have clicked on a vertex
            tolerance = self.calc_tolerance()
            vertex = self.find_vertex_at(event.pos(), tolerance)
            if self.mCtrl and vertex is not None:
                # if we have clicked on a vertex, identify which one
                # check if was already in the selection list
                if vertex not in self.indexes_within_list:
                    # add it
                    self.indexes_within_list.append(vertex)
                    self.update_rubber_band()
                else:
                    # remove it
                    self.indexes_within_list.remove(vertex)
                    self.update_rubber_band()

                self.band_finished = True
            elif vertex is None:
                # if we have not clicked on a vertex and there's no polygon band, start it
                if not len(self.selection_polygon) and self.band_finished and not self.mCtrl:
                    self.selection_clicked.emit(list())
                    self.band_finished = False
                    self.rubber_band = QgsRubberBand(self.canvas(), QgsWkbTypes.PolygonGeometry)
                    self.rubber_band.setWidth(2)
                    select_green = QColor("green")
                    select_green.setAlpha(128)
                    self.rubber_band.setColor(select_green)

                    if event.button() == Qt.LeftButton:
                        # Left click -> add vertex
                        self.p0 = QgsPointXY(point.x(), point.y())
                        self.selection_polygon.append(self.p0)
                elif len(self.selection_polygon) == 1 and not self.mCtrl:
                    if event.button() == Qt.LeftButton:
                        # Left click -> add vertex
                        self.p2 = QgsPointXY(point.x(), point.y())
                        self.p1 = QgsPointXY(self.p2.x(), self.p0.y())
                        self.p3 = QgsPointXY(self.p0.x(), self.p2.y())
                        self.selection_polygon.append(self.p1)
                        self.selection_polygon.append(self.p2)
                        self.selection_polygon.append(self.p3)
                        self.band_finished = True
                        self.set_selection()
                        self.close_polygon_band()

            self.selection_clicked.emit(self.indexes_within_list)

    def find_vertex_at(self, pos, tolerance):
        """
        get the vertex that is closer to the clicked point


        :param pos: The point that we've clicked
        :param tolerance: The tolerance of pos
        :return: vertex or None
        """
        if len(self.wp) > 0:
            dist_to_vertex = []
            for v in range(0, len(self.wp)):
                a1 = self.toCanvasCoordinates(QgsPointXY(self.wp[v]))
                dist_to_vertex.append(math.sqrt((pos.x() - a1.x()) ** 2 + (pos.y() - a1.y()) ** 2))

            vertex = dist_to_vertex.index(min(dist_to_vertex))
            if min(dist_to_vertex) > tolerance:
                return None
            else:
                return vertex
        else:
            return None

    def calc_tolerance(self):
        """
        Compute the tolerance on canvas

        :return: tolerance
        """
        # 2% of tolerance
        width_tolerance = 0.02 * self.canvas().width()
        height_tolerance = 0.02 * self.canvas().height()
        if width_tolerance < height_tolerance:
            tolerance = width_tolerance
        else:
            tolerance = height_tolerance
        return tolerance

    def canvasMoveEvent(self, event):

        if not self.band_finished and not self.mCtrl:
            self.p2 = self.toMapCoordinates(event.pos())
            self.p1 = QgsPointXY(self.p2.x(), self.p0.y())
            self.p3 = QgsPointXY(self.p0.x(), self.p2.y())

            self.selection_polygon.append(self.p1)
            self.selection_polygon.append(self.p2)
            self.selection_polygon.append(self.p3)
            self.rubber_band.setToGeometry(QgsGeometry.fromPolygonXY([self.selection_polygon]), None)
            self.selection_polygon.pop()
            self.selection_polygon.pop()
            self.selection_polygon.pop()

    def set_selection(self):
        """
        Set vertices highlight according to polygon
        """
        # Check which features are within the polygon
        mission_track = self.layer.getFeatures()  # get mission track feature

        for f in mission_track:  # loop although mission layer only has one feature
            vertices_it = f.geometry().vertices()
        polygon_geom = QgsGeometry.fromPolygonXY([self.selection_polygon])
        vertices_within_list = []
        # self.indexes_within_list = []
        vertex_index = 0

        # Highlight them using a point rubber band
        self.rubber_band_vertex_counter = 0
        for v in vertices_it:
            point_geom = QgsGeometry.fromPointXY(QgsPointXY(v.x(), v.y()))
            if point_geom.within(polygon_geom):
                vertices_within_list.append(v)
                if not (vertex_index in self.indexes_within_list):  # only add if not already present
                    self.indexes_within_list.append(vertex_index)
                    self.rubber_band_points.addPoint(QgsPointXY(v.x(), v.y()))
                    self.rubber_band_vertex_counter = self.rubber_band_vertex_counter + 1
                    self.rubber_band_vs_track_indexes[vertex_index] = self.rubber_band_vertex_counter - 1
            vertex_index = vertex_index + 1

    def update_rubber_band(self):
        if self.rubber_band_points:
            self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
            self.rubber_band_vs_track_indexes = {}
            self.rubber_band_vertex_counter = 0
        self.wp = self.mission_track.find_waypoints_in_mission()
        if len(self.indexes_within_list) > 0:

            selected_vertices = self.mission_track.find_waypoints_in_mission(self.indexes_within_list)
            for v in selected_vertices:
                vertex_index = 0
                for point in self.wp:
                    if v == point:
                        pc = self.toLayerCoordinates(self.layer, QgsPointXY(v))
                        self.rubber_band_points.addPoint(pc)
                        self.rubber_band_vertex_counter = self.rubber_band_vertex_counter + 1
                        self.rubber_band_vs_track_indexes[vertex_index] = self.rubber_band_vertex_counter - 1
                    vertex_index = vertex_index + 1

        self.set_geometry()

    def remove_rubber_band(self, wp):
        # if self.rubber_band_points:
        #    self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
        self.indexes_within_list.remove(wp)
        self.update_rubber_band()

    def set_geometry(self):
        """
        Save rubber band to geometry of the layer
        """
        if self.layer.featureCount() == 0:
            # no feature yet created
            f = QgsFeature()
            if len(self.wp) == 1:
                f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(self.wp[0].x(), self.wp[0].y())))
            else:
                f.setGeometry(QgsGeometry.fromPolyline(self.wp))
            # self.layer.dataProvider().addFeatures([f])
            self.layer.addFeatures([f])
        else:
            # mission feature present, edit geometry
            feats = self.layer.getFeatures()
            for f in feats:
                if len(self.wp) == 1:
                    self.layer.changeGeometry(f.id(),
                                              QgsGeometry.fromPointXY(QgsPointXY(self.wp[0].x(), self.wp[0].y())))
                else:
                    self.layer.changeGeometry(f.id(), QgsGeometry.fromPolyline(self.wp))
        self.layer.commitChanges()
        self.layer.startEditing()

    def close_polygon_band(self):
        self.selection_polygon = []
        if self.rubber_band is not None:
            self.rubber_band.reset()
            self.canvas().scene().removeItem(self.rubber_band)
        self.rubber_band = None

    def close_highlight_band(self):
        self.rubber_band_points.reset()
        self.canvas().scene().removeItem(self.rubber_band_points)
        self.rubber_band_points = None

    def deactivate(self):
        if self.rubber_band:
            self.close_polygon_band()
        if self.rubber_band_points:
            self.close_highlight_band()

        try:
            self.mission_track.mission_changed.disconnect(self.update_rubber_band)
            self.mission_track.step_removed.disconnect(self.remove_rubber_band)
        except:
            logger.info("no connected to signal")
        self.layer.commitChanges()
