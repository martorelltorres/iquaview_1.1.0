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
Map tool to manage the addition of waypoints in a mission graphically
using a QGIS rubber band
"""

import math
import logging

from iquaview.src.utils.calcutils import intersect_point_to_line, is_between
from iquaview.src.mission.startendmarker import StartEndMarker
from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY, QgsDistanceArea, QgsProject
from qgis.gui import QgsMapTool, QgsRubberBand, QgsVertexMarker
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

logger = logging.getLogger(__name__)


class EditTool(QgsMapTool):
    wp_clicked = pyqtSignal(int)

    def __init__(self, mission_track, canvas, msglog):
        QgsMapTool.__init__(self, canvas)
        self.setCursor(Qt.CrossCursor)
        self.mission_track = mission_track
        self.msglog = msglog
        self.dragging = False
        self.feature = None
        self.vertex = None
        self.startcoord = None
        self.layer = self.mission_track.get_mission_layer()
        logger.info(self.mission_track.get_mission_name())

        self.rubber_band = QgsRubberBand(self.canvas(), QgsWkbTypes.LineGeometry)
        self.rubber_band.setWidth(2)
        self.rubber_band.setColor(QColor("green"))

        self.point_cursor_band = QgsRubberBand(self.canvas(), QgsWkbTypes.LineGeometry)
        self.point_cursor_band.setWidth(1)
        self.point_cursor_band.setLineStyle(Qt.DashLine)
        self.point_cursor_band.setColor(QColor(255, 0, 0, 100))

        self.mid_point_band = QgsRubberBand(self.canvas(), QgsWkbTypes.PointGeometry)
        self.mid_point_band.setColor(QColor(255, 0, 0, 100))
        self.mid_point_band.setIconSize(18)

        self.rubber_band_points = QgsRubberBand(self.canvas(), QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setColor(QColor("green"))
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.rubber_band_points.setIconSize(10)

        self.mission_track.mission_changed.connect(self.update_rubber_bands)

        self.vertex_marker = QgsVertexMarker(self.canvas())
        self.start_end_marker = StartEndMarker(canvas, self.mission_track.find_waypoints_in_mission(), QColor("green"))

        self.layer.startEditing()

        self.wp = []
        self.mCtrl = False
        # handler for mission feature
        self.update_rubber_bands(0)

        crs = canvas.mapSettings().destinationCrs()
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())

    def update_rubber_bands(self, current_wp):
        self.rubber_band.reset(QgsWkbTypes.LineGeometry)
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
        self.wp = self.mission_track.find_waypoints_in_mission()

        self.start_end_marker.update_markers(self.wp)

        if len(self.wp) > 0:

            for v in self.wp:
                pc = self.toLayerCoordinates(self.layer, QgsPointXY(v))
                self.rubber_band.addPoint(pc)
                self.rubber_band_points.addPoint(pc)
            logger.debug("MISSION UPDATE: now we have {} waypoints".format(len(self.wp)))

            self.vertex_marker.setCenter(QgsPointXY(self.wp[current_wp].x(), self.wp[current_wp].y()))
            self.vertex_marker.setColor(QColor(25, 255, 0))
            self.vertex_marker.setIconSize(7)
            self.vertex_marker.setIconType(QgsVertexMarker.ICON_X)  # ICON_BOX, ICON_CROSS, ICON_X
            self.vertex_marker.setPenWidth(2)
            self.vertex_marker.show()

            self.set_geometry()
        else:

            self.vertex_marker.hide()

    def set_control_state(self, state):
        self.mCtrl = state

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and not self.dragging:
            self.mCtrl = True
            pos = self.canvas().mouseLastXY()
            if not self.find_on_feature(pos, self.calc_tolerance()):
                self.show_dist_and_bearing_to_point()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False
            pos = self.canvas().mouseLastXY()
            if not self.find_on_feature(pos, self.calc_tolerance()) and not self.dragging:
                self.show_dist_and_bearing_to_point()
        return

    def canvasDoubleClickEvent(self, event):
        self.canvasPressEvent(event)

    def canvasPressEvent(self, event):
        if self.dragging:
            self.canvasReleaseEvent(event)

        map_pt, layer_pt = self.transform_coordinates(event.pos())
        tolerance = self.calc_tolerance()

        if not self.find_on_feature(event.pos(), tolerance):
            if event.button() == Qt.LeftButton:
                # we have clicked outside the track
                logger.debug("We have clicked outside the track")
                self.point_cursor_band.reset(QgsWkbTypes.LineGeometry)
                if not self.mCtrl:
                    # add step to mission at the end
                    self.mission_track.add_step(len(self.wp), layer_pt)
                    self.show_waypoint_distances(len(self.wp)-1)
                else:
                    self.mission_track.add_step(0, layer_pt)
                    self.show_waypoint_distances(0)
        else:

            logger.debug("We have clicked on the track")
            vertex = self.find_vertex_at(event.pos(), tolerance)

            if event.button() == Qt.LeftButton:
                if vertex is None:
                    logger.debug("We have clicked between vertexs")
                    # we have clicked in between vertex, add intermediate point
                    initial_vertex = self.find_segment_at(event.pos())
                    # self.mission_track.add_step(initial_vertex + 1, layerPt)

                    intersection = intersect_point_to_line(self.toLayerCoordinates(self.layer, event.pos()),
                                                           QgsPointXY(self.wp[initial_vertex]),
                                                           QgsPointXY(self.wp[initial_vertex + 1]))
                    logger.debug("intersection point: {} {}".format(str(intersection.x()), str(intersection.y())))
                    logger.debug("{} {} {} {}".format(self.wp[initial_vertex].x(), self.wp[initial_vertex].y(),
                                 self.wp[initial_vertex + 1].x(), self.wp[initial_vertex + 1].y()))
                    # layerPtIntersection = self.toLayerCoordinates(self.layer,intersection)
                    self.mission_track.add_step(initial_vertex + 1, intersection)
                    self.mid_point_band.reset(QgsWkbTypes.PointGeometry)
                    self.show_waypoint_distances(initial_vertex+1)
                else:
                    logger.debug("We have clicked on vertex {}".format(vertex))
                    # we have clicked on a vertex

                    # Left click -> move vertex.
                    self.dragging = True
                    self.vertex = vertex
                    self.startcoord = event.pos()
                    # self.moveVertexTo(layerPt)

            elif event.button() == Qt.RightButton:
                if vertex is not None and not self.dragging:
                    # Right click -> delete vertex.
                    self.delete_vertex(vertex)

                    if self.find_on_feature(event.pos(), tolerance):  # If cursor still over track
                        vertex = self.find_vertex_at(event.pos(), tolerance)
                        if vertex is None:  # Cursor is between vertexes
                            self.show_mid_point(event.pos())
                        else:  # Cursor is over a vertex
                            self.show_waypoint_distances(vertex)
                    else:
                        self.show_dist_and_bearing_to_point()

    def transform_coordinates(self, canvas_pt):
        return (self.toMapCoordinates(canvas_pt),
                self.toLayerCoordinates(self.layer, canvas_pt))

    def canvasMoveEvent(self, event):
        if self.dragging:
            self.move_vertex_to(self.toLayerCoordinates(self.layer, event.pos()))
            self.mission_track.hide_start_end_markers()
            self.vertex_marker.hide()
            self.start_end_marker.hide_markers()
            self.show_waypoint_distances(self.vertex)

        else:
            tolerance = self.calc_tolerance()
            if self.find_on_feature(event.pos(), tolerance):  # if mouse is over the track
                self.point_cursor_band.reset(QgsWkbTypes.LineGeometry)
                self.mid_point_band.reset(QgsWkbTypes.PointGeometry)
                vertex = self.find_vertex_at(event.pos(), tolerance)

                if vertex is None:  # Cursor is between vertexes
                    self.show_mid_point(event.pos())
                else:  # Cursor is over a vertex
                    self.show_waypoint_distances(vertex)

            else:
                self.mid_point_band.reset(QgsWkbTypes.PointGeometry)
                self.show_dist_and_bearing_to_point()

    def show_dist_and_bearing_to_point(self):
        """
        Finds distance and bearing from the last point (first if pressing ctrl) to the specified point and shows them
        in the message log. Also draws a line between the points.
        """
        bearing = 0.0

        self.point_cursor_band.reset(QgsWkbTypes.LineGeometry)
        point = self.canvas().mouseLastXY()
        if len(self.wp) > 0:
            cursor_point = self.toMapCoordinates(point)
            if self.mCtrl:
                anchor_point = QgsPointXY(self.wp[0])
            else:
                anchor_point = QgsPointXY(self.wp[len(self.wp) - 1])
            self.point_cursor_band.addPoint(cursor_point)
            self.point_cursor_band.addPoint(anchor_point)
            distance = self.distance_calc.measureLine([anchor_point, cursor_point])
            if distance != 0.0:
                bearing = self.distance_calc.bearing(anchor_point, cursor_point)
            self.msglog.logMessage("")
            if self.mCtrl:
                msg = "Distance to next point: "
            else:
                msg = "Distance to previous point: "
            self.msglog.logMessage(msg + "{:.3F} m.  Bearing: {:.3F} º.".format(distance, math.degrees(bearing)),
                                   "Distance and bearing", 0)
        else:
            self.msglog.logMessage("")

    def show_mid_point(self, cursor):
        """
        Finds the projection of the cursor over the track and draws a circle in that point.
        Finds the distances between this projection point and the previous and next points in the mission
        and shows them in the message log.
        :param cursor: position to be projected over the track
        """
        prev_vertex = self.find_segment_at(cursor)
        prev_point = QgsPointXY(self.wp[prev_vertex])
        next_point = QgsPointXY(self.wp[prev_vertex + 1])
        cursor_point = self.toMapCoordinates(cursor)
        intersection = intersect_point_to_line(cursor_point, prev_point, next_point)
        self.mid_point_band.addPoint(intersection)
        distance1 = self.distance_calc.measureLine([prev_point, intersection])
        distance2 = self.distance_calc.measureLine([intersection, next_point])
        self.msglog.logMessage("")
        self.msglog.logMessage("Distance to previous point: {:.3F} m.  Distance to next point: {:.3F} m."
                               .format(distance1, distance2), "Distance between points", 0)

    def show_waypoint_distances(self, vertex):
        """
        Finds the distances to adjacent waypoints of vertex and shows them in the message log
        :param vertex: index of the waypoint from the mission
        """
        curr_point = self.rubber_band_points.getPoint(QgsWkbTypes.PointGeometry, vertex)
        if vertex == 0:
            if len(self.wp) > 1:
                next_point = QgsPointXY(self.wp[vertex+1])
                distance = self.distance_calc.measureLine([curr_point, next_point])
                bearing = self.distance_calc.bearing(next_point, curr_point)
                msg = "Distance to next point: {:.3F} m.  Bearing: {:.3F} º.".format(distance, math.degrees(bearing))
            else:
                msg = ""
            self.msglog.logMessage("")
            self.msglog.logMessage(msg+" (Waypoint {}) ".format(vertex+1), "Vertex distances", 0)
        elif vertex == len(self.wp) - 1:
            prev_point = QgsPointXY(self.wp[vertex-1])
            distance = self.distance_calc.measureLine([prev_point, curr_point])
            bearing = self.distance_calc.bearing(prev_point, curr_point)
            msg = "Distance to previous point: {:.3F} m.  Bearing: {:.3F} º.".format(distance, math.degrees(bearing))
            self.msglog.logMessage("")
            self.msglog.logMessage(msg+" (Waypoint {})".format(vertex+1), "Vertex distances", 0)
        else:
            prev_point = QgsPointXY(self.wp[vertex-1])
            next_point = QgsPointXY(self.wp[vertex+1])
            distance1 = self.distance_calc.measureLine(prev_point, curr_point)
            distance2 = self.distance_calc.measureLine(curr_point, next_point)
            msg = "Distance to previous point: {:.3F} m.  Distance to next point: {:.3F} m."\
                .format(distance1, distance2)
            self.msglog.logMessage("")
            self.msglog.logMessage(msg+" (Waypoint {})".format(vertex+1), "Vertex distances", 0)

    def hide_point_cursor_band(self):
        """
        Hides the rubber band drawn from last (or first) point to cursor
        """
        self.point_cursor_band.reset(QgsWkbTypes.LineGeometry)

    def canvasReleaseEvent(self, event):
        if self.dragging and event.button() == Qt.LeftButton:
            self.dragging = False
            self.vertex_marker.show()
            mapPt, layerPt = self.transform_coordinates(event.pos())
            # Check distance with initial point
            dist = math.sqrt(
                (self.startcoord.x() - event.pos().x()) ** 2 + (self.startcoord.y() - event.pos().y()) ** 2)
            tolerance = self.calc_tolerance()
            if dist > tolerance:
                self.move_vertex_to(layerPt)
                self.mission_track.change_position(self.vertex, layerPt)
                self.wp_clicked.emit(self.vertex)
                self.feature = None
                self.vertex = None
                self.layer.updateExtents()
            else:
                # If release point is the same, has been just a click
                self.move_vertex_to(self.toLayerCoordinates(self.layer, QgsPointXY(self.wp[self.vertex])))
                self.wp_clicked.emit(self.vertex)
                self.feature = None
                self.vertex = None

    def calc_tolerance(self):
        """
        Compute the tolerance on canvas

        :return: tolerance
        """
        # 2% of tolerance
        width_tolerance = 0.02 * self.canvas().width()
        height_tolerance =  0.02 * self.canvas().height()
        if width_tolerance < height_tolerance:
            tolerance = width_tolerance
        else:
            tolerance = height_tolerance
        return tolerance

    def move_vertex_to(self, layerPt):
        """
        Move current vertex to layerPt position.

        :param layerPt: layer point
        :type: QgsPointXY
        """
        if len(self.wp) > 1:
            self.rubber_band.movePoint(self.vertex, layerPt)
            self.rubber_band_points.movePoint(self.vertex, layerPt)
        elif len(self.wp) == 1:
            # A rubber band with PointGeometry and only 1 point acts as if it had 2 points, we need to reset it in
            # order to move the point.
            self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
            self.rubber_band_points.addPoint(layerPt)


    def delete_vertex(self, vertex):
        """
        Delete step 'vertex'.
        :param vertex: step

        """
        self.mission_track.remove_step(vertex)
        self.dragging = False
        self.vertex = None

    def find_on_feature(self, pos, tolerance):
        """
        if clicked point has some segment at a smaller distance than tolerance means that we've clicked on the track

        :param pos: The point that we've clicked
        :param tolerance: The tolerance of pos
        :return: bool
        """
        if len(self.wp) > 1:
            dist_to_segment = []
            for v in range(0, len(self.wp) - 1):
                # convert layer coordinates to canvas coordinates
                a1 = self.toCanvasCoordinates(QgsPointXY(self.wp[v]))
                b1 = self.toCanvasCoordinates(QgsPointXY(self.wp[v + 1]))

                dist_to_segment.append(
                    self.dist_to_segment(a1.x(),
                                         a1.y(),
                                         b1.x(),
                                         b1.y(),
                                         pos.x(),
                                         pos.y()))
                logger.debug("dist to segment: {}".format(dist_to_segment))
                if dist_to_segment[v] < tolerance:
                    return True

            return False
        else:
            # last waypoint
            vertex = self.find_vertex_at(pos, tolerance)
            if vertex is None:
                return False
            else:
                return True

    def find_segment_at(self, pos):
        """
        get the segment that is closer to the clicked point and return its initial vertex

        :param pos: the point that we've clicked
        :return: initial vertex of the segment
        """
        dist_to_segment = []
        for v in range(0, len(self.wp) - 1):
            a1 = self.toCanvasCoordinates(QgsPointXY(self.wp[v]))
            b1 = self.toCanvasCoordinates(QgsPointXY(self.wp[v + 1]))
            dist_to_segment.append(self.dist_to_segment(a1.x(),
                                                        a1.y(),
                                                        b1.x(),
                                                        b1.y(),
                                                        pos.x(),
                                                        pos.y()))

        vertex = dist_to_segment.index(min(dist_to_segment))
        return vertex

    def find_vertex_at(self, pos, tolerance):
        """
        get the vertex that is closer to the clicked point


        :param pos: The point that we've clicked
        :param tolerance: The tolerance of pos
        :return: vertex or None
        """
        if len(self.wp) > 0:
            dist_to_vertex = []
            logger.debug("tolerance {}".format(tolerance))
            for v in range(0, len(self.wp)):
                a1 = self.toCanvasCoordinates(QgsPointXY(self.wp[v]))
                dist_to_vertex.append(math.sqrt((pos.x() - a1.x()) ** 2 + (pos.y() - a1.y()) ** 2))
                logger.debug("dist to vertex: {}".format(dist_to_vertex))

            vertex = dist_to_vertex.index(min(dist_to_vertex))
            if min(dist_to_vertex) > tolerance:
                return None
            else:
                logger.debug("ON VERTEX")
                return vertex
        else:
            return None

    def dist_to_segment(self, ax, ay, bx, by, cx, cy):
        """
        Computes the minimum distance between a point (cx, cy) and a line segment with endpoints (ax, ay) and (bx, by).
        :param ax: endpoint 1, x-coordinate
        :param ay: endpoint 1, y-coordinate
        :param bx: endpoint 2, x-coordinate
        :param by: endpoint 2, y-coordinate
        :param cx: point, x-coordinate
        :param cy: point, x-coordinate
        :return: minimum distance between point and line segment
        """
        # calculate tolerance
        tolerance = self.calc_tolerance()
        # get distance between points c-a and c-b
        dist_to_a = math.sqrt((cx - ax) ** 2 + (cy - ay) ** 2)
        dist_to_b = math.sqrt((cx - bx) ** 2 + (cy - by) ** 2)
        # if distance to point a or distance to point b is smaller than tolerance, return -1
        if (dist_to_a < tolerance) or (dist_to_b < tolerance):
            return -1

        # if one coordinate are between a coordinates or b coordinates
        if is_between(ax, ay, bx, by, cx, cy):

            y = (by - ay)
            x = (bx - ax)

            # line defined by two points formula
            num = abs((y * cx) - (x * cy) + (bx * ay) - (by * ax))
            den = math.sqrt(y ** 2 + x ** 2)
            dl = num / den
            return dl

        else:
            return tolerance + 1

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

    def close_band(self):
        self.start_end_marker.close_markers()
        self.vertex_marker.hide()
        self.canvas().scene().removeItem(self.vertex_marker)
        self.vertex_marker = None
        self.mission_track.mission_changed.disconnect()
        self.layer.commitChanges()
        self.rubber_band.hide()
        self.mid_point_band.hide()
        self.rubber_band_points.hide()
        self.point_cursor_band.hide()
        self.canvas().scene().removeItem(self.rubber_band)
        self.canvas().scene().removeItem(self.mid_point_band)
        self.canvas().scene().removeItem(self.rubber_band_points)
        self.canvas().scene().removeItem(self.point_cursor_band)
        self.rubber_band = None
        self.mid_point_band = None
        self.rubber_band_points = None
        self.point_cursor_band = None
        self.msglog.logMessage("")
