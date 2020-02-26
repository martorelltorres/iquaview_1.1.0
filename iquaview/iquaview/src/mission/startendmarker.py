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

Class that shows start and end vertex marker of the mission on the canvas
"""

from qgis.core import QgsPointXY
from qgis.gui import QgsVertexMarker


class StartEndMarker(object):

    def __init__(self, canvas, waypoints, color):

        self.canvas = canvas
        self.color = color
        self.start_vertex_marker = QgsVertexMarker(self.canvas)
        self.end_vertex_marker = QgsVertexMarker(self.canvas)

        self.update_markers(waypoints)

    def update_markers(self, steps):
        """
        Update start and end vertex markers on canvas.
        :param steps: waypoints in the mission
        :type: list
        """

        if len(steps) > 1:
            self.start_vertex_marker.setCenter(QgsPointXY(steps[0].x(), steps[0].y()))
            self.start_vertex_marker.setColor(self.color)
            self.start_vertex_marker.setIconSize(14)
            self.start_vertex_marker.setIconType(QgsVertexMarker.ICON_CIRCLE)  # ICON_BOX, ICON_CROSS, ICON_X
            self.start_vertex_marker.setPenWidth(2)

            self.start_vertex_marker.show()

            self.end_vertex_marker.setCenter(QgsPointXY(steps[-1].x(), steps[-1].y()))
            self.end_vertex_marker.setColor(self.color)
            self.end_vertex_marker.setIconSize(14)
            self.end_vertex_marker.setIconType(QgsVertexMarker.ICON_BOX)  # ICON_BOX, ICON_CROSS, ICON_X
            self.end_vertex_marker.setPenWidth(2)
            self.end_vertex_marker.show()

        else:

            self.start_vertex_marker.hide()
            self.end_vertex_marker.hide()

    def hide_markers(self):
        """ hide vertex markers. """
        self.start_vertex_marker.hide()
        self.end_vertex_marker.hide()

    def close_markers(self):
        """ Remove vertex markers from canvas."""
        self.hide_markers()
        self.canvas.scene().removeItem(self.start_vertex_marker)
        self.canvas.scene().removeItem(self.end_vertex_marker)
        self.start_vertex_marker = None
        self.end_vertex_marker = None
