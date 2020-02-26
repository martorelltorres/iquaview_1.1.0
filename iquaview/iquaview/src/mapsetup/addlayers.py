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
 Dialog to select layer of different type (Vector, Raster or Tiled Web Map).
"""

import logging

from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QFileInfo, QDir
from qgis.core import QgsVectorLayer, QgsRasterLayer
from iquaview.src.ui.ui_addlayer_dlg import Ui_AddLayer

logger = logging.getLogger(__name__)


class AddLayersDlg(QDialog, Ui_AddLayer):

    def __init__(self, proj, canvas, msglog, parent=None):
        super(AddLayersDlg, self).__init__(parent)
        self.proj = proj
        self.canvas = canvas
        self.msglog = msglog
        self.setupUi(self)
        self.setWindowTitle("Add Layer")

        self.vector_filename = None
        self.vector_base_name = None
        self.vector_file_extension = None
        self.raster_filename = None
        self.raster_base_name = None

        self.vector_loadfile_pushButton.clicked.connect(self.vector_load_file)
        self.raster_loadfile_pushButton.clicked.connect(self.raster_load_file)
        self.buttonBox.accepted.connect(self.on_accept)

    def vector_load_file(self):
        """ Open dialog to load vector layer."""
        self.vector_filename, __ = QFileDialog.getOpenFileName(self, 'Vector Layer from File', QDir.homePath(),
                                                               "Vector Layer(*.shp *.kml *.osm *.gpx) ;; All files (*.*)")
        if self.vector_filename:
            file_info = QFileInfo(self.vector_filename)
            self.vector_base_name = file_info.baseName()
            self.vector_file_extension = file_info.suffix()
            self.vector_file_lineEdit.setText(str(self.vector_filename))
            self.vector_name_lineEdit.setText(str(self.vector_base_name))

    def raster_load_file(self):
        """ Open dialog to load raster layer."""

        self.raster_filename, __ = QFileDialog.getOpenFileName(self, 'Vector Layer from File', QDir.homePath(),
                                                               "Raster Layer(*.tif) ;; All files (*.*)")
        if self.raster_filename:
            file_info = QFileInfo(self.raster_filename)
            self.raster_base_name = file_info.baseName()

            self.raster_file_lineEdit.setText(str(self.raster_filename))
            self.raster_name_lineEdit.setText(str(self.raster_base_name))

    def on_accept(self):
        if self.vector_radioButton.isChecked():

            self.add_vector_layer()

        elif self.raster_radioButton.isChecked():

            self.add_raster_layer()

        elif self.tiledwebmap_radioButton.isChecked():

            self.add_tiled_web_map_layer()

    def add_vector_layer(self):
        """ Add vector layer to project."""
        self.vector_filename = self.vector_file_lineEdit.text()
        self.vector_base_name = self.vector_name_lineEdit.text()

        if self.vector_file_extension is not None and self.vector_file_extension.lower() == "gpx":
            vlayer_routes = QgsVectorLayer(self.vector_filename + "?type=route", self.vector_base_name+"_route", "gpx")
            vlayer_tracks = QgsVectorLayer(self.vector_filename + "?type=track", self.vector_base_name+"_track", "gpx")
            vlayer_waypoints = QgsVectorLayer(self.vector_filename + "?type=waypoint", self.vector_base_name+" waypoints", "gpx")

            if not vlayer_routes.isValid() or not vlayer_waypoints.isValid() or not vlayer_tracks.isValid():
                logger.warning("Layer failed to load!")
                QMessageBox.critical(self,
                                     "Add Layer",
                                     "Layer format is not recognised as a supported file format",
                                     QMessageBox.Close)
                self.msglog.logMessage("Failed to load layer " + self.vector_filename, "LoadingLayer", 1)

                self.vector_file_lineEdit.setText('')
                self.vector_name_lineEdit.setText('')

            else:
                if vlayer_routes.dataProvider().featureCount() > 0:
                    self.proj.addMapLayer(vlayer_routes)
                if vlayer_tracks.dataProvider().featureCount() > 0:
                    self.proj.addMapLayer(vlayer_tracks)
                if vlayer_waypoints.dataProvider().featureCount() > 0:
                    self.proj.addMapLayer(vlayer_waypoints)

                self.accept()
        else:
            vlayer = QgsVectorLayer(self.vector_filename, self.vector_base_name, "ogr")
            if not vlayer.isValid():
                logger.warning("Layer failed to load!")
                QMessageBox.critical(self,
                                     "Add Layer",
                                     "Layer format is not recognised as a supported file format",
                                     QMessageBox.Close)
                self.msglog.logMessage("Failed to load layer " + vlayer.name(), "LoadingLayer", 1)

                self.vector_file_lineEdit.setText('')
                self.vector_name_lineEdit.setText('')
            else:
                self.proj.addMapLayer(vlayer)
                self.accept()

    def add_raster_layer(self):
        """ Add raster layer to project."""
        self.raster_filename = self.raster_file_lineEdit.text()
        self.raster_base_name = self.raster_name_lineEdit.text()

        rlayer = QgsRasterLayer(self.raster_filename, self.raster_base_name)
        if not rlayer.isValid():
            logger.error("Failed to load layer!")
            QMessageBox.critical(self,
                                 "Add Layer",
                                 "Layer format is not recognised as a supported file format",
                                 QMessageBox.Close)
            self.msglog.logMessage("Failed to load layer " + rlayer.name(), "LoadingLayer", 1)

            self.raster_file_lineEdit.setText('')
            self.raster_name_lineEdit.setText('')
        else:
            self.proj.addMapLayer(rlayer)
            self.canvas.setExtent(rlayer.extent())
            self.accept()

    def add_tiled_web_map_layer(self):
        """ Add tiled web map layer to project."""
        zmin = "&zmin=0"
        zmax = ""

        if self.mCheckBoxZMax_2.isChecked():
            zmax = "&zmax=" + self.mSpinZMax_2.text()

        if self.url_comboBox.currentText() == "OpenStreetMap":
            # open street map
            url_with_params = 'type=xyz&url=http://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png' + zmax + zmin
        elif self.url_comboBox.currentText() == "Google Hybrid":
            # per google maps
            url_with_params = 'type=xyz&url=https://mt1.google.com/vt/lyrs%3Dy%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D' + zmax + zmin
        elif self.url_comboBox.currentText() == "Google Map":
            # per google maps
            url_with_params = 'type=xyz&url=https://mt1.google.com/vt/lyrs%3Dm%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D' + zmax + zmin
        elif self.url_comboBox.currentText() == "Google Satelite":
            # per google maps
            url_with_params = 'type=xyz&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D' + zmax + zmin

        if self.mEditName_2.text() == "":
            self.mEditName_2.setText(self.url_comboBox.currentText())

        xyz_layer = QgsRasterLayer(url_with_params, self.mEditName_2.text(), 'wms')
        if not xyz_layer.isValid():
            logger.error("Failed to load layer!")
            QMessageBox.critical(self,
                                 "Add Layer",
                                 "Layer format is not recognised as a supported file format",
                                 QMessageBox.Close)
            self.msglog.logMessage("Failed to load layer " + xyz_layer.name(), "LoadingLayer", 1)
        else:
            self.proj.addMapLayer(xyz_layer)
            self.accept()
