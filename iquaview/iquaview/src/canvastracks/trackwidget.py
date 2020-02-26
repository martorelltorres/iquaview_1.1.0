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
 Widget to configure track appearance (color) and allow to clear track
 history and center track on the map.
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog

from qgis.core import (QgsRectangle,
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsFeature,
                       QgsVectorFileWriter,
                       QgsCoordinateReferenceSystem)
from qgis.gui import QgsRubberBand, QgsColorButton

from iquaview.src.ui.ui_track import Ui_Track

logger = logging.getLogger(__name__)


class TrackWidget(QWidget, Ui_Track):

    def __init__(self, parent=None):
        super(TrackWidget, self).__init__(parent)
        self.setupUi(self)
        self.title = "Display track"
        self.canvas = None
        self.band = None
        self.color_btn = None
        self.center = False
        self.position = None
        self.geom_type = None
        self.marker = None
        self.hidden = False
        self.centerButton.setEnabled(False)
        icon = QIcon(":/resources/mActionSave.svg")
        self.save_track_pushButton.setIcon(icon)
        self.save_track_pushButton.setToolTip("Save Track")
        self.save_track_pushButton.clicked.connect(self.save_track)

    def init(self, title, canvas, default_color, geom_type, marker):
        self.canvas = canvas
        self.geom_type = geom_type
        self.track_groupBox.setTitle(title)
        if marker:
            # Add marker
            self.marker = marker
            self.with_marker = True
        else:
            self.with_marker = False
        # Add rubber band
        self.band = QgsRubberBand(self.canvas, self.geom_type)
        if self.geom_type == QgsWkbTypes.PointGeometry:
            self.band.setIcon(QgsRubberBand.ICON_CIRCLE)
            self.band.setIconSize(12)
        else:
            self.band.setWidth(3)
        # Add color button widget for picking color
        self.color_btn = QgsColorButton()
        self.horizontal_layout_color.insertWidget(1, self.color_btn, 0, Qt.AlignLeft)
        self.color_btn.colorChanged.connect(self.color_changed)
        self.color_btn.setDefaultColor(default_color)
        self.color_btn.setColor(default_color)
        # Set signals
        self.centerButton.clicked.connect(self.center_to_location)
        self.clearTrackButton.clicked.connect(self.clear_track)

    def color_changed(self):
        transparent_color = QColor(self.color_btn.color())
        transparent_color.setAlpha(80)
        self.band.setColor(transparent_color)
        if self.with_marker:
            self.marker.set_color(QColor(self.color_btn.color()))

    def add_position(self, position):
        self.band.addPoint(position)

    def track_update_canvas(self, position, heading):
        self.centerButton.setEnabled(True)
        self.position = position
        self.add_position(position)
        if self.with_marker:
            self.marker.set_center(position, heading)
        if self.isHidden():
            if self.with_marker:
                self.marker.hide()
            self.band.hide()
        else:
            if self.with_marker:
                self.marker.show()
            self.band.show()

    def center_to_location(self):
        """
        Center to last received position on the map.
        """
        rect = QgsRectangle(self.position, self.position)
        self.canvas.setExtent(rect)
        self.canvas.zoomScale(400)
        self.canvas.refresh()

    def hide_band(self):
        self.band.hide()

    def hide_marker(self):
        if self.with_marker:
            self.marker.hide()

    def clear_track(self):
        self.band.reset(self.geom_type)

    def save_track(self):
        """
        Save the track to disk
        """
        layer_name, selected_filter = QFileDialog.getSaveFileName(None, 'Save Track', "",
                                                                  'Shapefile (*.shp);;KML (*.kml);;GPX (*.gpx)')

        if layer_name != '':

            if self.geom_type == QgsWkbTypes.PointGeometry:
                geometric_object = "MultiPoint?crs=epsg:4326"
            else:
                geometric_object = "LineString?crs=epsg:4326"

            layer = QgsVectorLayer(
                geometric_object,
                layer_name,
                "memory")
            feature = QgsFeature()
            feature.setGeometry(self.band.asGeometry())
            layer.dataProvider().addFeatures([feature])

            if selected_filter == "Shapefile (*.shp)":

                if not layer_name.endswith('.shp'):
                    layer_name = layer_name + '.shp'
                ret = QgsVectorFileWriter.writeAsVectorFormat(layer, layer_name, "utf-8",
                                                              QgsCoordinateReferenceSystem(4326,
                                                                                           QgsCoordinateReferenceSystem.EpsgCrsId),
                                                              "ESRI Shapefile")
                if ret == QgsVectorFileWriter.NoError:
                    logger.info(layer.name() + " saved to " + layer_name)

            elif selected_filter == "KML (*.kml)":

                if not layer_name.endswith('.kml'):
                    layer_name = layer_name + '.kml'

                QgsVectorFileWriter.writeAsVectorFormat(layer, layer_name, "utf-8",
                                                        QgsCoordinateReferenceSystem(4326,
                                                                                     QgsCoordinateReferenceSystem.EpsgCrsId),
                                                        "KML")
            elif selected_filter == "GPX (*.gpx)":

                if not layer_name.endswith('.gpx'):
                    layer_name = layer_name + '.gpx'
                ds_options = list()
                ds_options.append("GPX_USE_EXTENSIONS=TRUE")
                QgsVectorFileWriter.writeAsVectorFormat(layer, layer_name, "utf-8",
                                                        QgsCoordinateReferenceSystem(4326,
                                                                                     QgsCoordinateReferenceSystem.EpsgCrsId),
                                                        "GPX",
                                                        datasourceOptions=ds_options)

    def close(self):
        self.hide_band()
        self.hide_marker()
        # self.canvas.scene().removeItem(self.band)
        # self.canvas.scene().removeItem(self.marker)
