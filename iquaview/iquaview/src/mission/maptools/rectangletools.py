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
 Map tools for drawing Rectangles on the canvas
"""

from math import cos, sin, radians, sqrt, degrees, atan2
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsCoordinateTransform, QgsGeometry, QgsPointXY, \
    QgsMapSettings, QgsCoordinateReferenceSystem, QgsDistanceArea, QgsPoint, QgsProject

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor, QPixmap, QColor

from iquaview.src.utils.calcutils import calc_is_collinear, endpoint


def rotate_point(point, angle):
    # Auxliary function to rotate point by a given angle (in radians)
    x = cos(angle) * point.x() - sin(angle) * point.y()
    y = sin(angle) * point.x() + cos(angle) * point.y()
    return QgsPointXY(x, y)


class Rectangle:
    def __init__(self):
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')

    def get_rect_from_center(self, pc, p2, angle=0.0):
        """
        Creates a rectangle from a center point, a corner point and an angle

        :param pc: center point of the geometry
        :param p2: a corner of the geometry
        :param angle: angle of the geometry, 0 by default. In radians
        :return: 4 points geometry
        """

        if angle == 0:
            x_offset = abs(p2.x() - pc.x())
            y_offset = abs(p2.y() - pc.y())

            pt1 = QgsPointXY(pc.x() - x_offset, pc.y() - y_offset)
            pt2 = QgsPointXY(pc.x() - x_offset, pc.y() + y_offset)
            pt3 = QgsPointXY(pc.x() + x_offset, pc.y() + y_offset)
            pt4 = QgsPointXY(pc.x() + x_offset, pc.y() - y_offset)

            geom = QgsGeometry.fromPolygonXY([[pt1, pt2, pt3, pt4]])

        else:
            x_offset = (cos(angle) * (p2.x() - pc.x()) + sin(angle) * (p2.y() - pc.y()))
            y_offset = -(-sin(angle) * (p2.x() - pc.x()) + cos(angle) * (p2.y() - pc.y()))

            pt1 = QgsPointXY(pc.x() - x_offset, pc.y() - y_offset)
            pt2 = QgsPointXY(pc.x() - x_offset, pc.y() + y_offset)
            pt3 = QgsPointXY(pc.x() + x_offset, pc.y() + y_offset)
            pt4 = QgsPointXY(pc.x() + x_offset, pc.y() - y_offset)

            geom = QgsGeometry.fromPolygonXY([[pt1, pt2, pt3, pt4]])

        return geom

    def get_rect_rotated(self, geom, cp, ep = QgsPointXY(0, 0), ip = QgsPointXY(0, 0), delta = 0):
        """
        Rotates a geometry by some delta + the angle between 2 points and the center point of the geometry

        :param geom: geometry to be rotated
        :param cp: center point of the geometry
        :param ep: point marking the end of the rotation
        :param ip: point marking the beginning of the rotation
        :param delta: extra angle of rotation in radians
        :return: geometry rotated and total angle of rotation
        """

        angle_1 = self.distance.bearing(cp, ep)
        angle_2 = self.distance.bearing(cp, ip)
        angle_rotation = delta + (angle_2 - angle_1)

        coords = []
        ring = []
        for i in geom.asPolygon():
            for k in i:
                ini_point = QgsPointXY(k.x() - cp.x(), k.y() - cp.y())
                end_point = rotate_point(ini_point, angle_rotation)
                p3 = QgsPointXY(cp.x() + end_point.x(), cp.y() + end_point.y())
                ring.append(p3)
            coords.append(ring)
            ring = []

        geom = QgsGeometry().fromPolygonXY(coords)

        return geom, angle_rotation

    def get_rect_by3_points(self, p1, p2, p3, length=0):
        angle_exist = self.distance.bearing(p1, p2)

        side = calc_is_collinear(p1, p2, p3)  # check if x_p2 > x_p1 and inverse side
        if side == 0:
            return None
        if length == 0:
            length = self.distance.measureLine(p2, p3)
        p3 = self.distance.computeSpheroidProject(p2, length, angle_exist + radians(90) * side)
        p4 = self.distance.computeSpheroidProject(p1, length, angle_exist + radians(90) * side)
        geom = QgsGeometry.fromPolygonXY([[p1, p2, p3, p4]])
        return geom

    def get_rect_projection(self, rect_geom, cp, x_length = 0, y_length = 0):
        """
        Transforms the rectangle geometry to its projection on the real world, making all its angles 90º


        :param rect_geom: 4 point geometry
        :param cp: central point of the geometry
        :param x_length: distance between first and second points of the rect_geom
        :param y_length: distance between second and third points of the rect_geom
        :return: geometry projected to map
        """
        if x_length == 0 and y_length == 0:
            proj_geom = self.get_rect_by3_points(rect_geom.asPolygon()[0][0],
                                                 rect_geom.asPolygon()[0][1],
                                                 rect_geom.asPolygon()[0][2])

        else:
            point_two = endpoint(rect_geom.asPolygon()[0][0],
                                 x_length,
                                 degrees(self.distance.bearing(rect_geom.asPolygon()[0][0],
                                                               rect_geom.asPolygon()[0][1])))
            point_three = endpoint(rect_geom.asPolygon()[0][0],
                                   y_length,
                                   degrees(self.distance.bearing(rect_geom.asPolygon()[0][1],
                                                                 rect_geom.asPolygon()[0][3])))

            proj_geom = self.get_rect_by3_points(rect_geom.asPolygon()[0][0],
                                                 point_two,
                                                 point_three,
                                                 y_length)

        if proj_geom is not None:

            p1 = proj_geom.asPolygon()[0][0]
            p2 = proj_geom.asPolygon()[0][1]
            p3 = proj_geom.asPolygon()[0][2]
            p4 = proj_geom.asPolygon()[0][3]

            px = (p1.x() + p3.x()) / 2.0
            py = (p1.y() + p3.y()) / 2.0

            p1 = QgsPointXY(p1.x() - px + cp.x(), p1.y() - py + cp.y())
            p2 = QgsPointXY(p2.x() - px + cp.x(), p2.y() - py + cp.y())
            p3 = QgsPointXY(p3.x() - px + cp.x(), p3.y() - py + cp.y())
            p4 = QgsPointXY(p4.x() - px + cp.x(), p4.y() - py + cp.y())

            proj_geom = QgsGeometry.fromPolygonXY([[p1, p2, p3, p4]])

            return proj_geom

        else:
            return rect_geom


class RectBy3PointsTool(QgsMapTool):
    msgbar = pyqtSignal(str)
    rbFinished = pyqtSignal(object)
    rb_reset_signal = pyqtSignal()

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.nbPoints = 0
        self.rb = None
        self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3, self.x_p4, self.y_p4 = None, None, None, None, None, None, None, None
        self.length = 0
        self.mCtrl = False
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')
        # our own fancy cursor
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                       "      c None",
                                       ".     c #FF0000",
                                       "+     c #1210f3",
                                       "                ",
                                       "       +.+      ",
                                       "      ++.++     ",
                                       "     +.....+    ",
                                       "    +.     .+   ",
                                       "   +.   .   .+  ",
                                       "  +.    .    .+ ",
                                       " ++.    .    .++",
                                       " ... ...+... ...",
                                       " ++.    .    .++",
                                       "  +.    .    .+ ",
                                       "   +.   .   .+  ",
                                       "   ++.     .+   ",
                                       "    ++.....+    ",
                                       "      ++.++     ",
                                       "       +.+      "]))
        self.rectangle = Rectangle()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False
        if event.key() == Qt.Key_Escape:
            self.nbPoints = 0
            self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3 = None, None, None, None, None, None
            if self.rb:
                self.rb.reset(True)
            self.rb = None

            self.canvas.refresh()
            self.rb_reset_signal.emit()
            return

    def canvasPressEvent(self, event):
        layer = self.canvas.currentLayer()
        if self.nbPoints == 0:
            color = QColor(255, 0, 0, 128)
            if self.rb:
                self.rb.reset()
                self.rb = None
            self.rb = QgsRubberBand(self.canvas, True)
            self.rb.setColor(color)
            self.rb.setWidth(1)
            self.msgbar.emit("Define bearing and extent along track")
            self.rb_reset_signal.emit()

        elif self.nbPoints == 2:
            self.canvas.refresh()

        point = self.toLayerCoordinates(layer, event.pos())
        point_map = self.toMapCoordinates(layer, point)

        if self.nbPoints == 0:
            self.x_p1 = point_map.x()
            self.y_p1 = point_map.y()
        elif self.nbPoints == 1:
            self.x_p2 = point_map.x()
            self.y_p2 = point_map.y()
            self.msgbar.emit("Define extent across track")
        else:
            self.x_p3 = point_map.x()
            self.y_p3 = point_map.y()

        self.nbPoints += 1

        if self.nbPoints == 3:
            geom = self.rectangle.get_rect_by3_points(QgsPointXY(self.x_p1, self.y_p1),
                                                      QgsPointXY(self.x_p2, self.y_p2),
                                                      QgsPointXY(self.x_p3, self.y_p3))
            self.nbPoints = 0
            self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3 = None, None, None, None, None, None
            self.rbFinished.emit(geom)

        if self.rb: return

    def canvasMoveEvent(self, event):

        if not self.rb: return
        currpoint = self.toMapCoordinates(event.pos())

        if self.nbPoints == 1:
            self.rb.setToGeometry(QgsGeometry.fromPolyline([QgsPoint(self.x_p1, self.y_p1), QgsPoint(currpoint)]), None)
            curr_dist = self.distance.measureLine(QgsPointXY(self.x_p1, self.y_p1), currpoint)
            curr_bearing = degrees(self.distance.bearing(QgsPointXY(self.x_p1, self.y_p1), currpoint))
            if curr_bearing < 0.0:
                curr_bearing = 360 + curr_bearing
            self.msgbar.emit(
                "Current distance: {:.3F} m, Current bearing: {:.3F} degrees".format(curr_dist, curr_bearing))
        if self.nbPoints >= 2:
            geom = self.rectangle.get_rect_by3_points(QgsPointXY(self.x_p1, self.y_p1),
                                                      QgsPointXY(self.x_p2, self.y_p2),
                                                      currpoint)
            curr_dist = self.distance.measureLine(QgsPointXY(self.x_p2, self.y_p2), currpoint)
            curr_bearing = degrees(
                self.distance.bearing(QgsPointXY(self.x_p2, self.y_p2), QgsPointXY(geom.vertexAt(2))))
            if curr_bearing < 0.0:
                curr_bearing = 360 + curr_bearing
            self.msgbar.emit(
                "Current distance: {:.3F} m, Current bearing: {:.3F} degrees".format(curr_dist, curr_bearing))

            self.rb.setToGeometry(geom, None)

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.nbPoints = 0
        self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3 = None, None, None, None, None, None
        if self.rb:
            self.rb.reset(True)
            self.rb.hide()
        self.rb = None
        self.canvas.refresh()

    def is_zoom_tool(self):
        return False

    def is_transient(self):
        return False

    def is_edit_tool(self):
        return True


# RectByFixedExtentTool with fixed length values for the rectangle sides
# Tool class
class RectByFixedExtentTool(QgsMapTool):
    msgbar = pyqtSignal(str)
    rbFinished = pyqtSignal(object)
    rb_reset_signal = pyqtSignal()

    def __init__(self, canvas, x_length, y_length):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.nbPoints = 0
        self.rb = None
        self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3, self.x_p4, self.y_p4 = None, None, None, None, None, None, None, None
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')
        self.fixed_p2, self.fixed_p3 = QgsPointXY(0, 0), QgsPointXY(0, 0)
        self.length = 0
        self.mCtrl = None
        self.x_length = x_length
        self.y_length = y_length
        self.bearing = 0.0
        # our own fancy cursor
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                       "      c None",
                                       ".     c #FF0000",
                                       "+     c #1210f3",
                                       "                ",
                                       "       +.+      ",
                                       "      ++.++     ",
                                       "     +.....+    ",
                                       "    +.     .+   ",
                                       "   +.   .   .+  ",
                                       "  +.    .    .+ ",
                                       " ++.    .    .++",
                                       " ... ...+... ...",
                                       " ++.    .    .++",
                                       "  +.    .    .+ ",
                                       "   +.   .   .+  ",
                                       "   ++.     .+   ",
                                       "    ++.....+    ",
                                       "      ++.++     ",
                                       "       +.+      "]))
        self.rectangle = Rectangle()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False
        if event.key() == Qt.Key_Escape:
            self.nbPoints = 0
            self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3 = None, None, None, None, None, None
            self.fixed_p2, self.fixed_p3 = None, None
            if self.rb:
                self.rb.reset(True)
            self.rb = None

            self.canvas.refresh()
            self.rb_reset_signal.emit()
            return

    def canvasPressEvent(self, event):
        layer = self.canvas.currentLayer()
        if self.nbPoints == 0:
            color = QColor(255, 0, 0, 128)
            if self.rb:
                self.rb.reset()
                self.rb = None
            self.rb = QgsRubberBand(self.canvas, True)
            self.rb.setColor(color)
            self.rb.setWidth(1)
            self.msgbar.emit("Define bearing along track")
            self.rb_reset_signal.emit()

        elif self.nbPoints == 2:
            self.canvas.refresh()

        point = self.toLayerCoordinates(layer, event.pos())
        point_map = self.toMapCoordinates(layer, point)

        if self.nbPoints == 0:
            self.x_p1 = point_map.x()
            self.y_p1 = point_map.y()

        elif self.nbPoints == 1:
            self.x_p2 = point_map.x()
            self.y_p2 = point_map.y()
            self.bearing = self.distance.bearing(QgsPointXY(self.x_p1, self.y_p1), QgsPointXY(self.x_p2, self.y_p2))
            self.msgbar.emit("Define across track direction")
        else:
            self.x_p3 = point_map.x()
            self.y_p3 = point_map.y()

        self.nbPoints += 1

        if self.nbPoints == 3:
            geom = self.rectangle.get_rect_by3_points(QgsPointXY(self.x_p1, self.y_p1), self.fixed_p2, self.fixed_p3,
                                                      self.y_length)
            self.rb.setToGeometry(geom, None)

            self.nbPoints = 0
            self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3 = None, None, None, None, None, None
            self.fixed_p2, self.fixed_p3 = None, None
            self.msgbar.emit("")
            self.rbFinished.emit(geom)

        if self.rb: return

    def canvasMoveEvent(self, event):

        if not self.rb: return
        currpoint = self.toMapCoordinates(event.pos())

        if self.nbPoints == 1:
            self.bearing = self.distance.bearing(QgsPointXY(self.x_p1, self.y_p1), currpoint)
            self.fixed_p2 = self.distance.computeSpheroidProject(QgsPointXY(self.x_p1, self.y_p1), self.x_length,
                                                                 self.bearing)

            self.rb.setToGeometry(QgsGeometry.fromPolyline([QgsPoint(self.x_p1, self.y_p1), QgsPoint(self.fixed_p2)]),
                                  None)
            curr_bearing = degrees(self.bearing)
            if curr_bearing < 0.0:
                curr_bearing = 360 + curr_bearing
            self.msgbar.emit(
                "Current distance: {:.3F} m, Current bearing: {:.3F} degrees".format(self.x_length, curr_bearing))
        if self.nbPoints >= 2:
            # test if currpoint is left or right of the line defined by p1 and p2
            side = calc_is_collinear(QgsPointXY(self.x_p1, self.y_p1), self.fixed_p2, currpoint)

            if side == 0:
                return None
            self.fixed_p3 = self.distance.computeSpheroidProject(QgsPointXY(self.x_p2, self.y_p2), self.y_length,
                                                                 self.bearing + radians(90) * side)

            geom = self.rectangle.get_rect_by3_points(QgsPointXY(self.x_p1, self.y_p1), self.fixed_p2, self.fixed_p3,
                                                      self.y_length)
            self.rb.setToGeometry(geom, None)

            curr_bearing = degrees(self.bearing + radians(90) * side)
            if curr_bearing < 0.0:
                curr_bearing = 360 + curr_bearing
            self.msgbar.emit(
                "Current distance: {:.3F} m, Current bearing: {:.3F} degrees".format(self.y_length, curr_bearing))

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.nbPoints = 0
        self.x_p1, self.y_p1, self.x_p2, self.y_p2, self.x_p3, self.y_p3 = None, None, None, None, None, None
        self.fixed_p2, self.fixed_p3 = None, None
        if self.rb:
            self.rb.reset(True)
            self.rb.hide()
        self.rb = None

        self.canvas.refresh()

    def is_zoom_tool(self):
        return False

    def is_transient(self):
        return False

    def is_edit_tool(self):
        return True


# Tool class
class RectFromCenterTool(QgsMapTool):
    msgbar = pyqtSignal(str)
    rbFinished = pyqtSignal(object)
    rb_reset_signal = pyqtSignal()

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.nbPoints = 0
        self.rb = None
        self.mCtrl = None
        self.shift = False
        self.xc, self.yc, self.p2 = None, None, None
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')
        self.x_length = 0
        self.y_length = 0
        # our own fancy cursor
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                       "      c None",
                                       ".     c #FF0000",
                                       "+     c #17a51a",
                                       "                ",
                                       "       +.+      ",
                                       "      ++.++     ",
                                       "     +.....+    ",
                                       "    +.  .  .+   ",
                                       "   +.   .   .+  ",
                                       "  +.    .    .+ ",
                                       " ++.    .    .++",
                                       " ... ...+... ...",
                                       " ++.    .    .++",
                                       "  +.    .    .+ ",
                                       "   +.   .   .+  ",
                                       "   ++.  .  .+   ",
                                       "    ++.....+    ",
                                       "      ++.++     ",
                                       "       +.+      "]))
        self.curr_geom = None
        self.last_currpoint = None
        self.curr_angle = 0.0
        self.total_angle = 0.0
        self.rectangle = Rectangle()
        self.angle_ini_rot = 0.0
        self.ini_geom = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True
            self.point_ini_rot = self.toMapCoordinates(self.canvas.mouseLastXY())
            self.angle_ini_rot = self.curr_angle

        if event.key() == Qt.Key_Shift:
            self.shift = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False

        if event.key() == Qt.Key_Escape:
            self.nbPoints = 0
            self.xc, self.yc, self.p2 = None, None, None
            if self.rb:
                self.rb.reset(True)
            self.rb = None
            self.canvas.refresh()
            self.rb_reset_signal.emit()
            return

    def changegeomSRID(self, geom):
        layer = self.canvas.currentLayer()
        layerCRSSrsid = layer.crs().srsid()
        projectCRSSrsid = QgsMapSettings().destinationCrs().srsid()
        if layerCRSSrsid != projectCRSSrsid:
            g = QgsGeometry.fromPoint(geom)
            g.transform(QgsCoordinateTransform(projectCRSSrsid, layerCRSSrsid))
            ret_point = g.asPoint()
        else:
            ret_point = geom

        return ret_point

    def canvasPressEvent(self, event):
        layer = self.canvas.currentLayer()

        if self.nbPoints == 0:
            color = QColor(255, 0, 0, 128)
            if self.rb:
                self.rb.reset()
                self.rb = None
            self.rb = QgsRubberBand(self.canvas, True)
            self.rb.setColor(color)
            self.rb.setWidth(1)
            self.canvas.refresh()
            self.rb_reset_signal.emit()


        point = self.toLayerCoordinates(layer, event.pos())
        point_map = self.toMapCoordinates(layer, point)

        if self.nbPoints == 0:
            self.xc = point_map.x()
            self.yc = point_map.y()
        else:
            self.p2 = point_map

        self.nbPoints += 1

        if self.nbPoints == 2:
            # geom = self.rectangle.getRectFromCenter(QgsPointXY(self.xc, self.yc), self.p2, self.curr_angle)
            self.nbPoints = 0
            self.xc, self.yc, self.p2 = None, None, None
            self.last_currpoint = None
            self.curr_angle = 0.0
            self.total_angle = 0.0

            self.mCtrl = False

            self.rbFinished.emit(self.curr_geom)
            self.curr_geom = None

        if self.rb: return

    def canvasMoveEvent(self, event):
        if not self.rb or not self.xc or not self.yc: return

        currpoint = self.toMapCoordinates(event.pos())
        self.msgbar.emit(
            "Adjust lengths along track and across track. Hold Ctrl to adjust track orientation. Click when finished.")

        if not self.mCtrl:
            self.curr_geom = self.rectangle.get_rect_from_center(QgsPointXY(self.xc, self.yc), currpoint,
                                                                 self.curr_angle)
            self.ini_geom = self.curr_geom

            if self.curr_angle != 0:
                self.curr_geom, self.curr_angle = self.rectangle.get_rect_rotated(self.curr_geom,
                                                                                  QgsPointXY(self.xc, self.yc),
                                                                                  delta=self.curr_angle)


            self.x_length = self.distance.measureLine(self.curr_geom.asPolygon()[0][0],
                                                      self.curr_geom.asPolygon()[0][1])
            self.y_length = self.distance.measureLine(self.curr_geom.asPolygon()[0][1],
                                                      self.curr_geom.asPolygon()[0][2])

            self.curr_geom = self.rectangle.get_rect_projection(self.curr_geom, QgsPointXY(self.xc, self.yc),
                                                                self.x_length, self.y_length)


        elif self.ini_geom is not None:
            if self.last_currpoint is None:
                self.last_currpoint = currpoint

            self.curr_geom, self.curr_angle = self.rectangle.get_rect_rotated(self.ini_geom,
                                                                              QgsPointXY(self.xc, self.yc),
                                                                              currpoint, self.point_ini_rot,
                                                                              self.angle_ini_rot)

            self.last_currpoint = currpoint
            self.curr_geom = self.rectangle.get_rect_projection(self.curr_geom, QgsPointXY(self.xc, self.yc),
                                                                self.x_length, self.y_length)


        if self.curr_geom is not None:
            self.rb.setToGeometry(self.curr_geom, None)

    def show_settings_warning(self):
        pass

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.nbPoints = 0
        self.xc, self.yc, self.p2 = None, None, None
        if self.rb:
            self.rb.reset(True)
            self.rb.hide()
        self.rb = None

        self.canvas.refresh()

    def is_zoom_tool(self):
        return False

    def is_transient(self):
        return False

    def is_edit_tool(self):
        return True


# Tool class
class RectFromCenterFixedTool(QgsMapTool):
    msgbar = pyqtSignal(str)
    rbFinished = pyqtSignal(object)
    rb_reset_signal = pyqtSignal()

    def __init__(self, canvas, x_length=0.0, y_length=0.0):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.nbPoints = 0
        self.rb = None
        self.mCtrl = None
        self.xc, self.yc, self.p2 = None, None, None
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')
        self.x_length = x_length
        self.y_length = y_length
        self.diagonal = sqrt(self.x_length / 2 * self.x_length / 2 + self.y_length / 2 * self.y_length / 2)
        # our own fancy cursor
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                       "      c None",
                                       ".     c #FF0000",
                                       "+     c #17a51a",
                                       "                ",
                                       "       +.+      ",
                                       "      ++.++     ",
                                       "     +.....+    ",
                                       "    +.  .  .+   ",
                                       "   +.   .   .+  ",
                                       "  +.    .    .+ ",
                                       " ++.    .    .++",
                                       " ... ...+... ...",
                                       " ++.    .    .++",
                                       "  +.    .    .+ ",
                                       "   +.   .   .+  ",
                                       "   ++.  .  .+   ",
                                       "    ++.....+    ",
                                       "      ++.++     ",
                                       "       +.+      "]))

        self.curr_geom = None
        self.last_currpoint = None
        self.curr_angle = 0.0
        self.total_angle = 0.0
        self.rectangle = Rectangle()
        self.angle_ini_rot = 0.0
        self.ini_geom = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True
            self.point_ini_rot = self.toMapCoordinates(self.canvas.mouseLastXY())
            self.angle_ini_rot = self.curr_angle

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False

        if event.key() == Qt.Key_Escape:
            self.nbPoints = 0
            self.xc, self.yc, self.p2 = None, None, None
            if self.rb:
                self.rb.reset(True)
            self.rb = None

            self.canvas.refresh()
            self.rb_reset_signal.emit()
            return

    def changegeomSRID(self, geom):
        layer = self.canvas.currentLayer()

        layerCRSSrsid = layer.crs().srsid()
        projectCRSSrsid = QgsMapSettings().destinationCrs().srsid()
        if layerCRSSrsid != projectCRSSrsid:
            g = QgsGeometry.fromPoint(geom)
            g.transform(QgsCoordinateTransform(projectCRSSrsid, layerCRSSrsid))
            retPoint = g.asPoint()
        else:
            retPoint = geom

        return retPoint

    def canvasPressEvent(self, event):
        layer = self.canvas.currentLayer()

        if self.nbPoints == 0:
            color = QColor(255, 0, 0, 128)
            if self.rb:
                self.rb.reset()
                self.rb = None
            self.rb = QgsRubberBand(self.canvas, True)
            self.rb.setColor(color)
            self.rb.setWidth(1)
            self.canvas.refresh()
            self.rb_reset_signal.emit()

        point = self.toLayerCoordinates(layer, event.pos())
        pointMap = self.toMapCoordinates(layer, point)

        if self.nbPoints == 0:
            self.xc = pointMap.x()
            self.yc = pointMap.y()
            if self.x_length != 0:
                self.diagonal = sqrt(self.x_length / 2 * self.x_length / 2 + self.y_length / 2 * self.y_length / 2)
                self.p2 = self.distance.computeSpheroidProject(QgsPointXY(self.xc, self.yc), self.diagonal,
                                                               atan2(self.y_length / 2, self.x_length / 2))
        else:
            self.x_bearing = pointMap.x()
            self.y_bearing = pointMap.y()
            self.bearing = self.distance.bearing(QgsPointXY(self.xc, self.yc), pointMap)

        self.nbPoints += 1

        if self.nbPoints == 2:
            self.nbPoints = 0
            self.xc, self.yc, self.p2 = None, None, None
            self.last_currpoint = None
            self.rbFinished.emit(self.curr_geom)
            self.curr_geom = None
            self.curr_angle = 0.0
            self.total_angle = 0.0

        if self.rb: return

    def canvasMoveEvent(self, event):
        if not self.rb or not self.xc or not self.yc: return
        currpoint = self.toMapCoordinates(event.pos())
        self.msgbar.emit("Hold Ctrl to adjust track orientation. Click when finished.")

        if not self.mCtrl:
            if self.last_currpoint is None:
                self.last_currpoint = self.p2
                self.curr_geom = self.rectangle.get_rect_from_center(QgsPointXY(self.xc, self.yc),
                                                                     self.last_currpoint,)
                self.ini_geom = self.curr_geom

                self.curr_geom = self.rectangle.get_rect_projection(self.curr_geom, QgsPointXY(self.xc, self.yc),
                                                                    self.x_length, self.y_length)

        elif self.ini_geom is not None:
            if self.last_currpoint is None:
                self.last_currpoint = currpoint

            self.curr_geom, self.curr_angle = self.rectangle.get_rect_rotated(self.ini_geom,
                                                                              QgsPointXY(self.xc, self.yc),
                                                                              currpoint, self.point_ini_rot,
                                                                              self.angle_ini_rot)

            self.last_currpoint = currpoint
            self.curr_geom = self.rectangle.get_rect_projection(self.curr_geom, QgsPointXY(self.xc, self.yc),
                                                                self.x_length, self.y_length)

        if self.curr_geom is not None:
            self.rb.setToGeometry(self.curr_geom, None)

    def show_settings_warning(self):
        pass

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.nbPoints = 0
        self.xc, self.yc, self.x_p2, self.y_p2 = None, None, None, None
        if self.rb:
            self.rb.reset(True)
        self.rb = None

        self.canvas.refresh()

    def is_zoom_tool(self):
        return False

    def is_transient(self):
        return False

    def is_edit_tool(self):
        return True
