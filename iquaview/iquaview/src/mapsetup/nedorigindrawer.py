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
 Class to automatically generate a layer with the NED origin point to display in the map canvas
 The NED origin is retrieved from the navigator ROS params.
 """

from qgis.core import (QgsVectorLayer,
                       QgsSymbol,
                       QgsSingleSymbolRenderer,
                       QgsFeature,
                       QgsGeometry,
                       QgsPointXY,
                       QgsSvgMarkerSymbolLayer)
from iquaview.src.cola2api import cola2_interface
from PyQt5.QtWidgets import QMessageBox


class NEDOriginDrawer:
    def __init__(self, proj, vehicle_info):
        self.proj = proj
        self.vehicle_info = vehicle_info
        self.ned_origin_layer = QgsVectorLayer(
            "Point?crs=epsg:4326",
            "NED Origin",
            "memory")
        self.feat = QgsFeature()
        self.ned_origin_layer.dataProvider().addFeature(self.feat)
        self.ned_origin_layer.setRenderer(self.ned_origin_renderer())
        self.ned_origin_layer.setCustomProperty("ned_origin", "NED Origin")

        self.ned_lat = None
        self.ned_lon = None

    def ned_origin_renderer(self):
        symbol = QgsSymbol.defaultSymbol(self.ned_origin_layer.geometryType())
        svg_style = {'fill': '# 0000ff',
                     'name': ':/resources/Star2.svg',
                     'outline': '#000000',
                     'outline - width': '6.8',
                     'size': '6'}
        # create svg symbol layer
        sym_lyr1 = QgsSvgMarkerSymbolLayer.create(svg_style)
        # Replace the default layer with our custom layer
        symbol.deleteSymbolLayer(0)
        symbol.appendSymbolLayer(sym_lyr1)
        # Replace the renderer of the current layer
        renderer = QgsSingleSymbolRenderer(symbol)
        return renderer

    def update_ned_point(self):
        try:
            self.ned_lat = float(cola2_interface.get_ros_param(self.vehicle_info.get_vehicle_ip(), 9091,
                                                               self.vehicle_info.get_vehicle_namespace() + '/navigator/ned_latitude')[
                                     'value'])
            self.ned_lon = float(cola2_interface.get_ros_param(self.vehicle_info.get_vehicle_ip(), 9091,
                                                               self.vehicle_info.get_vehicle_namespace() + '/navigator/ned_longitude')[
                                     'value'])

            # layer is not yet in the project, add it
            if len(self.proj.mapLayersByName('NED Origin')) == 0:
                self.feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(self.ned_lon, self.ned_lat)))
                self.ned_origin_layer.dataProvider().addFeatures([self.feat])
                self.proj.addMapLayer(self.ned_origin_layer, True)
            else:
                self.ned_origin_layer.startEditing()
                self.ned_origin_layer.moveVertex(self.ned_lon, self.ned_lat, self.feat.id() + 1, 0)
                self.ned_origin_layer.commitChanges()

        except:
            QMessageBox.warning(None,
                                "NED Origin update",
                                "Could not read NED origin topic.",
                                QMessageBox.Close)
