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
Class to draw a north arrow in the map canvas
"""

from PyQt5.QtCore import QSize, QRectF
from PyQt5.QtSvg import QSvgRenderer
from qgis.gui import QgsMapCanvasItem
from qgis.core import QgsBearingUtils, QgsPointXY


class NorthArrow(QgsMapCanvasItem):
    def __init__(self, proj, canvas):
        super(NorthArrow, self).__init__(canvas)
        self.proj = proj
        self.canvas = canvas
        self.map_pos = QgsPointXY(0.0, 0.0)
        self.svg = QSvgRenderer(":/resources/arrow.svg")
        self.size = QSize(42, 64)
        self.corner = 1

    def paint(self, painter, xxx, xxx2):
        """Paint north arrow on painter"""
        if self.svg.isValid():
            pos = self.set_position(self.corner, painter.device().width(), painter.device().height())

            rotation = QgsBearingUtils.bearingTrueNorth(self.canvas.mapSettings().destinationCrs(),
                                                        self.canvas.mapSettings().transformContext(),
                                                        self.canvas.extent().center())
            rotation += self.canvas.rotation()

            painter.save()
            painter.rotate(-rotation)  # To translate correctly
            painter.translate(pos.x(), pos.y())
            painter.rotate(rotation)  # To rotate north arrow along with canvas, always pointing north

            # do the drawing, and draw a smooth north arrow even when rotated
            rectangle = QRectF(-self.size.width()/2, -self.size.height()/2, self.size.width(), self.size.height())
            self.svg.render(painter, rectangle)

            painter.restore()

    def set_position(self, corner, width, height):
        """
        Returns the position of the specified corner with a concrete width and height
        :param corner: can be 1, 2, 3 or 4. top left, top right, bot left and bot right respectively
        :param width: width of the paint space
        :param height: height of the paint space
        :return: QgsPointXY of the specified corner
        """
        if corner == 1:  # top left corner
            return QgsPointXY(0 + self.size.height() / 2, 0 + self.size.height() / 2)
        elif corner == 2:  # top right corner
            return QgsPointXY(width - self.size.height() / 2, 0 + self.size.height() / 2)
        elif corner == 3:  # bottom left corner
            return QgsPointXY(0 + self.size.height() / 2, height - self.size.height() / 2)
        elif corner == 4:  # bottom right corner
            return QgsPointXY(width - self.size.height() / 2, height - self.size.height() / 2)
