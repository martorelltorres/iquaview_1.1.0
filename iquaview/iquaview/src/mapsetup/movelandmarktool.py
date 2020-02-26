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
from qgis.core import QgsPointXY, QgsTolerance, QgsDataProvider
from qgis.gui import QgsMapTool, QgsRubberBand
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class MoveLandmarkTool(QgsMapTool):

    def __init__(self, canvas):
        super().__init__(canvas)
        self.lm_layer = None
        self.lm_point = None
        self.clicked_on_landmark = False
        self.band = None

    def set_landmark_layer(self, layer):
        """Sets current land mark layer"""
        self.lm_layer = layer

    def canvasPressEvent(self, event):
        """
        If pressEvent point is near the layer point, enable dragging. Else show msg box
        """

        if event.button() == Qt.LeftButton:
            click_point = self.toLayerCoordinates(self.lm_layer, event.pos())
            if self.lm_layer.featureCount() == 1:
                feature_list = self.lm_layer.dataProvider().getFeatures() #Returns iterator to a list of one feature
                self.lm_feature = next(feature_list) #get first and only element in the list
                self.lm_point = self.lm_feature.geometry().asPoint()
                dist = QgsPointXY.distance(click_point, self.lm_point)
                tolerance = (QgsTolerance.toleranceInMapUnits(15, self.lm_layer,
                                                              self.canvas().mapSettings(), QgsTolerance.Pixels))

                if dist < tolerance:
                    #Clicked on a landmark
                    self.clicked_on_landmark = True
                    self.create_ghost_point()

                else:
                    #Not clicked on a landmark
                    confirmation_msg = "Do you want to move {} here? \n\n".format(self.lm_layer.name())
                    reply = QMessageBox.question(self.parent(), 'Movement Confirmation',
                                                 confirmation_msg, QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.move_position(click_point)

    def canvasReleaseEvent(self, event):
        """
        If dragging, stop and move landmark position to the release event point
        Also destroy rubberband (ghost point)
        """
        if (event.button() == Qt.LeftButton
                and self.lm_layer
                and self.clicked_on_landmark):
            release_point = self.toLayerCoordinates(self.lm_layer, event.pos())
            self.move_position(release_point)
            self.clicked_on_landmark = False
            if self.band:
                self.band.hide()
                self.band = None

    def move_position(self, end_point):
        """
        Translates landmark layer to end_point
        :param end_point: Where to move the landmark point
        """
        # If layer is not stored in memory, change its datasource to memory
        if self.lm_layer.source()[0] == "/":
            temp_feature = next(self.lm_layer.dataProvider().getFeatures())  # iterator with only 1 feature in list
            options = QgsDataProvider.ProviderOptions()
            self.lm_layer.setDataSource("Point?crs=epsg:4326",
                                        self.lm_layer.name(),
                                        "memory",
                                        options)
            self.lm_layer.dataProvider().addFeatures([temp_feature])
            self.lm_feature = next(self.lm_layer.dataProvider().getFeatures())

        dx = end_point.x() - self.lm_point.x()
        dy = end_point.y() - self.lm_point.y()
        self.lm_layer.startEditing()
        self.lm_layer.translateFeature(self.lm_feature.id(), dx, dy)
        self.lm_layer.commitChanges()

    def create_ghost_point(self):
        """
        Creates rubber band as a ghost image of the landmark point
        """
        if self.band is not None:
            self.band.hide()
            self.band = None
        self.band = QgsRubberBand(self.canvas())
        self.band.setColor(QColor("green"))
        self.band.setToGeometry(self.lm_feature.geometry(), self.lm_layer)
        self.band.show()

    def canvasMoveEvent(self, event):
        """
        If dragging, move ghost point
        """
        if self.clicked_on_landmark:
            point = self.toLayerCoordinates(self.lm_layer, event.pos())
            self.move_ghost_point(point)

    def move_ghost_point(self, point):
        """
        Translates ghost point to point
        :param point:  where the rubber band is going to be translated
        """
        if self.band:
            offset_x = point.x() - self.lm_point.x()
            offset_y = point.y() - self.lm_point.y()
            self.band.setTranslationOffset(offset_x, offset_y)
            self.band.updatePosition()
            self.band.update()
