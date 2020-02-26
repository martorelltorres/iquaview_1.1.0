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
 Class to define canvas markers to display positions in the map
"""

import math
from iquaview.src.utils.calcutils import endpoint, magnitude
from qgis.core import QgsPointXY, QgsDistanceArea, QgsProject
from qgis.gui import QgsMapCanvasItem
from PyQt5.QtCore import Qt, QRectF, QLine, QPoint
from PyQt5.QtGui import QBrush, QPen, QPainter, QPolygonF, QPainterPath
from PyQt5.QtSvg import QSvgRenderer


class CanvasMarker(QgsMapCanvasItem):
    def __init__(self, canvas, color, svg=None, width=0.0, length=0.0, orientation=True, marker_mode=False, config=None):
        super(CanvasMarker, self).__init__(canvas)
        self.canvas = canvas
        self.config = config
        self.size = 20
        self.changing_scale = 400
        self.marker_mode = marker_mode
        self.color = color
        self.pointbrush = QBrush(self.color)
        self.pointpen = QPen(Qt.black)
        self.pointpen.setWidth(1)
        self.map_pos = QgsPointXY(0.0, 0.0)
        self.heading = 0
        self.width = width
        self.length = length
        self.orientation = orientation
        if svg is not None:
            # set crs and ellipsoid
            crs = self.canvas.mapSettings().destinationCrs()
            self.distance_calc = QgsDistanceArea()
            self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
            self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())

            self.svg = QSvgRenderer(svg)
        else:
            self.svg = None

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def set_marker_mode(self, canvas_marker_mode):
        self.marker_mode = canvas_marker_mode

    def paint(self, painter, xxx, xxx2):
        pos = self.toCanvasCoordinates(self.map_pos)
        self.setPos(pos)

        if self.marker_mode:
            mode = self.config.csettings["canvas_marker_mode"]

            if mode == 'auto':
                self.set_size(20)
                transform = self.canvas.getCoordinateTransform()
                start_point = transform.toMapCoordinates(pos.x(), pos.y())
                map_end_point_width = endpoint(start_point, self.width, 90 + math.degrees(self.heading))
                map_end_point_length = endpoint(start_point, self.length, math.degrees(self.heading))

                # to canvas coordinates
                canvas_end_point_width = self.toCanvasCoordinates(map_end_point_width)
                canvas_end_point_length = self.toCanvasCoordinates(map_end_point_length)

                width = magnitude(self.toCanvasCoordinates(start_point), QgsPointXY(canvas_end_point_width))
                height = magnitude(self.toCanvasCoordinates(start_point), QgsPointXY(canvas_end_point_length))

                if width < self.size and height < self.size:
                    self.changing_scale = self.canvas.scale()
                else:
                    self.changing_scale = self.canvas.scale() * 2

            elif mode == 'manual':
                self.changing_scale = self.config.csettings["canvas_marker_scale"]
        else:
            self.changing_scale = 400

        if self.svg is None or self.canvas.scale() >= self.changing_scale:
            self.set_size(20)
            half_size = self.size / 2.0
            rect = QRectF(0 - half_size, 0 - half_size, self.size, self.size)
            painter.setRenderHint(QPainter.Antialiasing)

            self.pointpen.setColor(Qt.black)
            self.pointpen.setWidth(2)
            self.pointbrush.setColor(self.color)

            painter.setBrush(self.pointbrush)
            painter.setPen(self.pointpen)
            y = 0 - half_size
            x = rect.width() / 2 - half_size
            line = QLine(x, y, x, rect.height() - half_size)
            y = rect.height() / 2 - half_size
            x = 0 - half_size
            line2 = QLine(x, y, rect.width() - half_size, y)

            # Arrow
            p = QPolygonF()
            p.append(QPoint(0 - half_size, 0))
            p.append(QPoint(0, -self.size))
            x = rect.width() - half_size
            p.append(QPoint(x, 0))
            p.append(QPoint(0, 0))

            offsetp = QPolygonF()
            offsetp.append(QPoint(0 - half_size, 0))
            offsetp.append(QPoint(0, -self.size))
            x = rect.width() - half_size
            offsetp.append(QPoint(x, 0))
            offsetp.append(QPoint(0, 0))

            painter.save()
            painter.rotate(math.degrees(self.heading) + self.canvas.rotation())
            if self.orientation:
                path = QPainterPath()
                path.addPolygon(p)
                painter.drawPath(path)
            painter.restore()
            painter.drawEllipse(rect)
            painter.drawLine(line)
            painter.drawLine(line2)

        # svg valid
        elif self.svg is not None and self.svg.isValid():

            # get rotation
            rotation = self.canvas.rotation()

            painter.save()

            transform = self.canvas.getCoordinateTransform()
            start_point = transform.toMapCoordinates(pos.x(), pos.y())
            map_end_point_width = endpoint(start_point, self.width, 90 + math.degrees(self.heading))
            map_end_point_length = endpoint(start_point, self.length, math.degrees(self.heading))

            # to canvas coordinates
            canvas_end_point_width = self.toCanvasCoordinates(map_end_point_width)
            canvas_end_point_length = self.toCanvasCoordinates(map_end_point_length)

            width = magnitude(self.toCanvasCoordinates(start_point), QgsPointXY(canvas_end_point_width))
            height = magnitude(self.toCanvasCoordinates(start_point), QgsPointXY(canvas_end_point_length))

            if width > height:
                self.set_size(width)
            else:
                self.set_size(height)

            if width != 0 and height != 0:
                center_x = width / 2.0
                center_y = height / 2.0
                # work out how to shift the image so that it rotates
                #           properly about its center
                # ( x cos a + y sin a - x, -x sin a + y cos a - y)
                myradians = math.radians(rotation + math.degrees(self.heading))
                xshift = int(((center_x * math.cos(myradians)) +
                              (center_y * math.sin(myradians)))
                             - center_x)
                yshift = int(((-center_x * math.sin(myradians)) +
                              (center_y * math.cos(myradians)))
                             - center_y)

                painter.translate(-width / 2, -height / 2)
                painter.rotate(math.degrees(self.heading) + self.canvas.rotation())
                self.svg.render(painter, QRectF(xshift, yshift, width, height))
            painter.restore()

    def boundingRect(self):
        size = self.size * 2
        return QRectF(-size, -size, 2.0 * size, 2.0 * size)

    def updatePosition(self):
        self.set_center(self.map_pos, self.heading)

    def set_center(self, map_pos, heading):
        self.heading = heading
        self.map_pos = map_pos
        self.setPos(self.toCanvasCoordinates(self.map_pos))

    def set_width(self, width):
        self.width = width

    def set_length(self, length):
        self.length = length
