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
 Rectangle pattern definition
"""

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from iquaview.src.ui.ui_rectangletemplatewidget import Ui_RectangleTemplateWidget
from iquaview.src.mission.maptools.rectangletools import (RectBy3PointsTool,
                                                          RectByFixedExtentTool,
                                                          RectFromCenterTool,
                                                          RectFromCenterFixedTool)
from iquaview.src.cola2api.mission_types import (Mission,
                                                 MissionStep,
                                                 MissionPosition,
                                                 MissionWaypoint,
                                                 MissionSection,
                                                 MissionTolerance)
from qgis.gui import QgsRubberBand
from qgis.core import QgsPointXY, QgsWkbTypes, QgsDistanceArea, QgsCoordinateReferenceSystem, QgsProject


class RectangleTemplateWidget(QWidget, Ui_RectangleTemplateWidget):

    def __init__(self, canvas, msglog, current_missiontrack, parent=None):
        super(RectangleTemplateWidget, self).__init__(parent)
        self.setupUi(self)
        self.canvas = canvas
        self.msglog = msglog
        self.current_missiontrack = current_missiontrack
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.rubber_band = None
        self.rubber_band_points = None
        self.initial_point = None

        self.template_type = 'rectangle_template'
        self.wp = list()
        self.mission = None
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')

        self.wp_list = []

        self.rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.setWidth(2)
        self.rubber_band.setColor(QColor("green"))

        self.rubber_band_points = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setColor(QColor("green"))
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.rubber_band_points.setIconSize(10)

        self.initial_point = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.initial_point.setColor(QColor("red"))
        self.initial_point.setIcon(QgsRubberBand.ICON_CIRCLE)
        self.initial_point.setIconSize(10)

        self.onTarget = False
        self.area_points = None
        self.missionAreaDefined = False

        # Get the tools
        self.rectBy3Points_tool = RectBy3PointsTool(self.canvas)
        self.rectByFixedExtentTool = RectByFixedExtentTool(self.canvas, 0.0, 0.0)
        self.rect_from_center_tool = RectFromCenterTool(self.canvas)
        self.rect_from_center_fixed_tool = RectFromCenterFixedTool(self.canvas, 0.0, 0.0)

        self.drawRectangleButton.clicked.connect(self.draw_mission_area)
        self.centerOnTargetButton.clicked.connect(self.draw_mission_area)
        self.rectBy3Points_tool.msgbar.connect(self.pass_message_bar)

        self.depthButton.setAutoExclusive(False)
        self.altitudeButton.setAutoExclusive(False)

        self.depthButton.setChecked(True)
        self.altitudeButton.setChecked(False)

        self.alongTrackLabel.setEnabled(False)
        self.acrossTrackLabel.setEnabled(False)
        self.alongTLength.setEnabled(False)
        self.acrossTLength.setEnabled(False)

        self.fixedExtent.toggled.connect(self.fixed_extend_toggled)
        self.depthButton.toggled.connect(self.depth_toggled)
        self.altitudeButton.toggled.connect(self.altitude_toggled)

        self.initial_point_comboBox.currentIndexChanged.connect(self.change_initial_point)

    def get_template_mission(self):
        return self.mission

    def fixed_extend_toggled(self):
        is_checked = self.fixedExtent.isChecked()
        self.alongTrackLabel.setEnabled(is_checked)
        self.acrossTrackLabel.setEnabled(is_checked)
        self.alongTLength.setEnabled(is_checked)
        self.acrossTLength.setEnabled(is_checked)

    def depth_toggled(self):
        if self.depthButton.isChecked():
            self.altitudeButton.setChecked(False)

    def altitude_toggled(self):
        if self.altitudeButton.isChecked():
            self.depthButton.setChecked(False)

    def pass_message_bar(self, msg):
        self.msglog.logMessage("")
        self.msglog.logMessage(msg, "Lawn Mower", 0)

    def draw_mission_area(self):
        self.onTarget = False
        sender = self.sender().objectName()
        if not self.missionAreaDefined:
            if self.automaticExtent.isChecked():
                if sender == self.drawRectangleButton.objectName():
                    self.msglog.logMessage("Click starting point", "Lawn Mower", 0)
                    # Draw mission area
                    self.rectBy3Points_tool = RectBy3PointsTool(self.canvas)
                    self.canvas.setMapTool(self.rectBy3Points_tool)
                    self.rectBy3Points_tool.msgbar.connect(self.pass_message_bar)
                    self.rectBy3Points_tool.rb_reset_signal.connect(self.clear_initial_point)
                    self.rectBy3Points_tool.rbFinished.connect(self.create_mission_area)
                elif sender == self.centerOnTargetButton.objectName():
                    self.onTarget = True
                    self.msglog.logMessage("Click center point", "Lawn Mower", 0)
                    # Draw mission area
                    self.rect_from_center_tool = RectFromCenterTool(self.canvas)
                    self.canvas.setMapTool(self.rect_from_center_tool)
                    self.rect_from_center_tool.msgbar.connect(self.pass_message_bar)
                    self.rect_from_center_tool.rb_reset_signal.connect(self.clear_initial_point)
                    self.rect_from_center_tool.rbFinished.connect(self.create_mission_area)
                self.missionAreaDefined = True
                return

            elif self.fixedExtent.isChecked():
                if self.alongTLength.value() != 0.0 and self.acrossTLength.value() != 0.0:
                    if sender == self.drawRectangleButton.objectName():
                        self.msglog.logMessage("Click starting point", "Lawn Mower", 0)

                        self.rectByFixedExtentTool = RectByFixedExtentTool(self.canvas,
                                                                           self.alongTLength.value(),
                                                                           self.acrossTLength.value())
                        self.canvas.setMapTool(self.rectByFixedExtentTool)
                        self.rectByFixedExtentTool.msgbar.connect(self.pass_message_bar)
                        self.rectByFixedExtentTool.rb_reset_signal.connect(self.clear_initial_point)
                        self.rectByFixedExtentTool.rbFinished.connect(self.create_mission_area)
                        self.missionAreaDefined = True
                    elif sender == self.centerOnTargetButton.objectName():
                        self.onTarget = True
                        self.msglog.logMessage("Click center point", "Lawn Mower", 0)

                        self.rect_from_center_fixed_tool = RectFromCenterFixedTool(self.canvas,
                                                                                   self.alongTLength.value(),
                                                                                   self.acrossTLength.value())
                        self.canvas.setMapTool(self.rect_from_center_fixed_tool)
                        self.rect_from_center_fixed_tool.msgbar.connect(self.pass_message_bar)
                        self.rect_from_center_fixed_tool.rb_reset_signal.connect(self.clear_initial_point)
                        self.rect_from_center_fixed_tool.rbFinished.connect(self.create_mission_area)
                    return

                else:
                    QMessageBox.warning(None,
                                        "Mission Template",
                                        "<center>Track lengths must be different from zero. </center>",
                                        QMessageBox.Close)

                    return
        else:

            self.deactivate_tool()

            self.rubber_band.reset(QgsWkbTypes.LineGeometry)
            self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
            self.initial_point.reset(QgsWkbTypes.PointGeometry)
            self.missionAreaDefined = False
            self.draw_mission_area()

    def clear_initial_point(self):
        """
        Reset the initial point rubber band from canvas
        """
        if self.initial_point is not None:
            self.initial_point.reset(QgsWkbTypes.PointGeometry)

    def change_initial_point(self):
        """
        Change the initial point
        """
        self.clear_initial_point()
        if self.area_points is not None:
            area = self.area_points
            index = self.initial_point_comboBox.currentIndex()

            self.initial_point.addPoint(area[index])

    def create_mission_area(self, geom):
        self.pass_message_bar("")
        self.clear_initial_point()
        if geom is not None:
            # Store points to variables
            self.area_points = [QgsPointXY(geom.vertexAt(0)),
                                QgsPointXY(geom.vertexAt(1)),
                                QgsPointXY(geom.vertexAt(2)),
                                QgsPointXY(geom.vertexAt(3))]

            self.change_initial_point()

            self.missionAreaDefined = True

    def preview_tracks(self):
        """ preview tracks on the canvas"""
        if self.missionAreaDefined:
            if self.altitudeButton.isChecked() and self.depthAltitudeBox.value() == 0:
                QMessageBox.warning(None,
                                    "Mission Template",
                                    "<center>Altitude must be different from zero. </center>",
                                    QMessageBox.Close)
            else:
                self.wp_list = self.compute_tracks(self.get_area_points())
                self.track_to_mission(self.wp_list, self.get_z(), self.get_altitude_mode(),
                                                self.get_speed(),
                                                self.get_x_tolerance(), self.get_y_tolerance(), self.get_z_tolerance())

                # show rubber band with temporal tracks
                self.rubber_band.reset(QgsWkbTypes.LineGeometry)
                self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
                self.initial_point.reset(QgsWkbTypes.PointGeometry)
                for wp in self.wp_list:
                    self.rubber_band.addPoint(QgsPointXY(wp.x(), wp.y()))
                    self.rubber_band_points.addPoint(QgsPointXY(wp.x(), wp.y()))
                self.rubber_band_points.show()
                self.rubber_band.show()

                self.unset_map_tool()
        else:
            QMessageBox.warning(None,
                                "Mission Template",
                                "<center>Define first an area for the mission. </center>",
                                QMessageBox.Close)

    def get_area_points(self):
        return self.area_points

    def get_num_across_tracks(self):
        return int(self.numAcrossTracks.value())

    def get_altitude_mode(self):
        return self.altitudeButton.isChecked()

    def get_z(self):
        return self.depthAltitudeBox.value()

    def get_speed(self):
        return self.speed_doubleSpinBox.value()

    def get_x_tolerance(self):
        return self.x_tolerance_doubleSpinBox.value()

    def get_y_tolerance(self):
        return self.y_tolerance_doubleSpinBox.value()

    def get_z_tolerance(self):
        return self.z_tolerance_doubleSpinBox.value()

    def get_mission_type(self):
        return self.template_type

    def compute_tracks(self, area_points):

        """
             Compute rectangle tracks
            :param area_points: points defining the extent of the tracks, they should be in WGS 84 lat/lon.
                                first two points define the along track direction.
            :return: list of ordered waypoints of rectangle trajectory
            """

        index = self.initial_point_comboBox.currentIndex()
        if index == 0:
            new_area = [area_points[0],
                        area_points[1],
                        area_points[2],
                        area_points[3]]
        elif index == 1:
            new_area = [area_points[1],
                        area_points[2],
                        area_points[3],
                        area_points[0]]
        elif index == 2:
            new_area = [area_points[2],
                        area_points[3],
                        area_points[0],
                        area_points[1]]
        elif index == 3:
            new_area = [area_points[3],
                        area_points[0],
                        area_points[1],
                        area_points[2]]

        new_area.append(area_points[index])

        return new_area

    def track_to_mission(self, wp_list, z, altitude_mode, speed, tolerance_x, tolerance_y, tolerance_z):

        self.mission = Mission()
        for wp in range(len(wp_list)):
            if wp == 0:
                # first step type waypoint
                step = MissionStep()
                mwp = MissionWaypoint(MissionPosition(wp_list[wp].y(), wp_list[wp].x(), z, altitude_mode),
                                      speed,
                                      MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                step.add_maneuver(mwp)
                self.mission.add_step(step)
            else:
                # rest of steps type section
                step = MissionStep()
                mwp = MissionSection(MissionPosition(wp_list[wp - 1].y(), wp_list[wp - 1].x(), z, altitude_mode),
                                     MissionPosition(wp_list[wp].y(), wp_list[wp].x(), z, altitude_mode),
                                     speed,
                                     MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                step.add_maneuver(mwp)
                self.mission.add_step(step)

    def delete_widget(self):
        self.delete_all(self.layout())
        self.deleteLater()
        self.close()

    def delete_all(self, layout):
        """
        delete all widget from layout
        :param layout: layout is a qt layout
        """
        if layout is not None:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_all(item.layout())

    def unset_map_tool(self):
        """
        Unset map tool from canvas.
        """
        if self.automaticExtent.isChecked():
            if self.onTarget:
                self.canvas.unsetMapTool(self.rect_from_center_tool)
            else:
                self.canvas.unsetMapTool(self.rectBy3Points_tool)
        if self.fixedExtent.isChecked():
            if self.onTarget:
                self.canvas.unsetMapTool(self.rect_from_center_fixed_tool)
            else:
                self.canvas.unsetMapTool(self.rectByFixedExtentTool)

    def deactivate_tool(self):
        """
        Deactivate tool.
        """
        if self.rectBy3Points_tool:
            self.rectBy3Points_tool.deactivate()
        elif self.rectByFixedExtentTool:
            self.rectByFixedExtentTool.deactivate()
        if self.rect_from_center_tool:
            self.rect_from_center_tool.deactivate()
        elif self.rect_from_center_fixed_tool:
            self.rect_from_center_fixed_tool.deactivate()

    def close(self):

        self.unset_map_tool()
        self.deactivate_tool()

        if self.rubber_band is not None:
            self.canvas.scene().removeItem(self.rubber_band)
            del self.rubber_band
            self.rubber_band = None
        if self.rubber_band_points is not None:
            self.canvas.scene().removeItem(self.rubber_band_points)
            del self.rubber_band_points
            self.rubber_band_points = None
        if self.initial_point is not None:
            self.canvas.scene().removeItem(self.initial_point)
            del self.initial_point
            self.initial_point = None
