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
 Class for mission track objects.
 Handles the rendering of the associated mission structure (from the mission xml file) to a layer in the interface.
 It also handles all the changes (addition, removal and update of steps) in the mission structure.
 """

import copy
import logging
from qgis.core import (QgsPoint,
                       QgsVectorLayer,
                       QgsVectorFileWriter,
                       QgsCoordinateReferenceSystem,
                       QgsGeometry,
                       QgsFeature,
                       QgsSymbol,
                       QgsSingleSymbolRenderer,
                       QgsSymbolLayerRegistry,
                       QgsDataProvider,
                       QgsWkbTypes)
from iquaview.src.cola2api.mission_types import (SECTION_MANEUVER,
                                                 WAYPOINT_MANEUVER,
                                                 PARK_MANEUVER,
                                                 Mission,
                                                 MissionStep,
                                                 MissionPosition,
                                                 MissionWaypoint,
                                                 MissionSection,
                                                 MissionPark,
                                                 MissionTolerance)

from iquaview.src.mission.startendmarker import StartEndMarker


from PyQt5.QtCore import pyqtSignal, QObject, QFileInfo
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QColor

logger = logging.getLogger(__name__)


class MissionTrack(QObject):
    mission_changed = pyqtSignal(int)
    step_removed = pyqtSignal(int)

    def __init__(self, mission_name="Mission", mission_filename=None, mission_layer=None, mission_renderer=None,
                 canvas=None):
        super(MissionTrack, self).__init__()
        self.mission_filename = mission_filename
        self.mission_name = mission_name
        self.mission_layer = mission_layer
        self.mission_renderer = mission_renderer
        self.mission = Mission()
        self.canvas = canvas
        self.start_end_marker = StartEndMarker(canvas, self.find_waypoints_in_mission(), QColor(200, 0, 0))

        self.saved = False
        self.modified = False

    def is_saved(self):
        """
        :return: return True if mission is saved,  otherwise False
        """
        return self.saved

    def is_modified(self):
        """
        :return: return True if mission is modified,  otherwise False
        """
        return self.modified

    def set_modified(self, modified):
        """ Set modified state"""
        self.modified = modified

    def load_mission(self, filename):
        """ Load mission with name 'filename'"""
        try:
            self.mission.load_mission(filename)
            self.mission_filename = filename
            self.update_start_end_markers()
            self.saved = True
            self.modifed = False
        except:
            logger.error("Invalid mission file")
            raise Exception("Invalid mission file")

    def set_mission(self, mission):
        """ Set Mission."""
        self.mission = mission

    def set_mission_filename(self, filename):
        """ Set Mission Filename"""
        self.mission_filename = filename

    def set_mission_name(self, name):
        """ Set Mission name."""
        self.mission_name = name

    def set_mission_layer(self, layer):
        """ Set mission layer."""
        self.mission_layer.name = self.mission_name
        self.mission_layer = layer

    def set_mission_renderer(self, renderer):
        """ Set mission renderer."""
        self.mission_renderer = renderer
        self.mission_layer.setRenderer(self.mission_renderer)

    def get_mission(self):
        """ Returns the mission"""
        return self.mission

    def get_step(self, step):
        """ Returns the step 'step' of the mission"""
        return self.mission.get_step(step)

    def get_mission_length(self):
        """ Returns mission length"""
        return self.mission.num_steps

    def get_mission_layer(self):
        """ Returns mission layer"""
        return self.mission_layer

    def get_mission_name(self):
        """ Returns mission name"""
        return self.mission_name

    def get_mission_filename(self):
        """ Returns mission filename"""
        return self.mission_filename

    def copy_mission(self):
        """ Returns a copy of the current mission"""
        return copy.deepcopy(self.mission)

    def change_position(self, wp_id, point):
        """
        Changes a position of the waypoint 'wp_id' with a new position 'point'
        :param wp_id: Current step
        :param point: Point position
        """
        position = self.mission.get_step(wp_id).get_maneuver().get_position()
        position.set_lat_lon(point.y(), point.x())
        if wp_id != self.mission.get_length() - 1:  # not last point
            if self.mission.get_step(wp_id + 1).get_maneuver().get_maneuver_type() == SECTION_MANEUVER:
                logger.debug("Next step is a section")
                # if next step is a section change its initial position
                position_next = self.mission.get_step(wp_id + 1).get_maneuver().get_initial_position()
                position_next.set_lat_lon(point.y(), point.x())
        self.mission_changed.emit(wp_id)
        self.update_start_end_markers()
        self.modified = True

    def remove_step(self, wp_id):
        """
        Remove step 'wp_id'
        :param wp_id: the step number to delete
        """
        initial_num_steps = self.mission.num_steps
        # if is first point and next waypoint is a Section, show warning message
        if (wp_id == 0 and
                initial_num_steps > 1 and
                self.mission.get_step(wp_id + 1).get_maneuver().get_maneuver_type() == SECTION_MANEUVER):
            reply = QMessageBox.warning(None, "Mission Error",
                                        "Impossible to remove the point because the next point is a section")

        else:

            if (initial_num_steps - 1 != wp_id and self.mission.get_step(
                    wp_id + 1).get_maneuver().get_maneuver_type() == SECTION_MANEUVER):
                logger.debug("Next step is a section")
                # if it's not the last step
                # if next step is a section change its initial position to the one of the point before
                position_previous = self.mission.get_step(wp_id - 1).get_maneuver().get_position()
                position_next = self.mission.get_step(wp_id + 1).get_maneuver().get_initial_position()
                position_next.set_lat_lon(position_previous.latitude, position_previous.longitude)

            self.mission.remove_step(wp_id)
            self.step_removed.emit(wp_id)

            # When point is deleted, layer may need a geometry type change
            if initial_num_steps <= 2:
                self.update_layer_geometry()

            if wp_id == initial_num_steps - 1:
                # if last waypoint is removed show previous
                self.mission_changed.emit(wp_id - 1)
            else:
                self.mission_changed.emit(wp_id)

            self.update_start_end_markers()

            self.modified = True

    def update_steps(self, id_list, mission_step_list):
        """
        Update the number of the step 'wp_id' with new number 'step'
        :param id_list: list of step ids to update
        :param mission_step_list: list of mission steps to update
        :return:
        """
        if len(id_list) > 0:
            for i in range(0, len(id_list)):
                self.mission.update_step(id_list[i], mission_step_list[i])
            self.mission_changed.emit(id_list[0])
            self.update_start_end_markers()
            self.modified = True

    def add_step(self, wp_id, point):
        """ Add new step"""
        initial_num_steps = self.mission.num_steps
        logger.debug("Add step: Mission has {} steps and wp_id is {}".format(initial_num_steps, wp_id))
        step = MissionStep()
        position = MissionPosition()
        tolerance = MissionTolerance()
        # If more than one point, get maneuver from surrounding waypoint and copy data
        if initial_num_steps > 0:
            if wp_id != 0:

                # if point is at the end or in the middle copy from the previous
                manv_to_copy = self.mission.get_step(wp_id - 1).get_maneuver()

                if manv_to_copy.get_maneuver_type() == SECTION_MANEUVER:
                    # if section, initial pos will be the final pos of the previous
                    manv = MissionSection()
                    position.copy(manv_to_copy.get_position())
                    tolerance.copy(manv_to_copy.get_tolerance())
                    manv.set(manv_to_copy.get_final_position(),
                             position,
                             manv_to_copy.get_speed(),
                             tolerance)
                    manv.get_final_position().set_lat_lon(point.y(), point.x())

                if wp_id != initial_num_steps:
                    # if point in the middle check if next is also section, we need to modify it
                    manv_next = self.mission.get_step(wp_id).get_maneuver()
                    if manv_next.get_maneuver_type() == SECTION_MANEUVER:
                        manv_next.get_initial_position().set_lat_lon(point.y(), point.x())

            else:  # wp_id == 0
                # copy from the next wp, next cannot be a section if was first waypoint until now, so no need to check
                manv_to_copy = self.mission.get_step(wp_id).get_maneuver()

            if manv_to_copy.get_maneuver_type() == WAYPOINT_MANEUVER:
                manv = MissionWaypoint()
                position.copy(manv_to_copy.get_position())
                tolerance.copy(manv_to_copy.get_tolerance())
                manv.set(position, manv_to_copy.get_speed(), tolerance)
                manv.get_position().set_lat_lon(point.y(), point.x())

            elif manv_to_copy.get_maneuver_type() == PARK_MANEUVER:
                manv = MissionPark()
                position.copy(manv_to_copy.get_position())
                tolerance.copy(manv_to_copy.get_tolerance())
                manv.set(position,
                         manv_to_copy.get_speed(),
                         manv_to_copy.get_time(),
                         tolerance)
                manv.get_position().set_lat_lon(point.y(), point.x())

        else:
            # is first point of the mission, fill maneuver by default type waypoint with clicked position
            manv = MissionWaypoint(MissionPosition(point.y(), point.x(), 0.0, False),
                                   0.5,
                                   MissionTolerance(2.0, 2.0, 1.0))  # todo: define default z, mode, speed and tolerance

        step.add_maneuver(manv)

        self.mission.insert_step(wp_id, step)
        logger.debug("Mission has now {} steps".format(self.mission.num_steps))

        # When point is added, layer may need a geometry type change
        if initial_num_steps <= 1:
            self.update_layer_geometry()

        self.mission_changed.emit(wp_id)
        self.update_start_end_markers()
        self.modified = True

    def save_mission(self):
        """ Saves a mission"""
        if self.mission.num_steps == 0:
            reply = QMessageBox.question(None, "Save Mission",
                                         "You are about to save an empty mission. Do you want to proceed?",
                                         QMessageBox.Yes |
                                         QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return False
        elif float(self.mission.get_step(self.mission.get_length() - 1).get_maneuver().get_position().get_z()) != 0.0:
            # vehicle last waypoint is not at zero depth.
            reply = QMessageBox.question(None, "Save Mission",
                                         "You are about to save and the last waypoint is not at zero depth. "
                                         "Do you want to proceed?",
                                         QMessageBox.Yes |
                                         QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return False

        logger.info("Saving mission to {}".format(self.mission_filename))
        self.mission.write_mission(self.mission_filename)
        self.mission_layer.setCustomProperty("mission_xml", self.mission_filename)
        self.saved = True
        self.modified = False
        return True

    def saveas_mission(self):
        """ Save a mission with new name"""
        if self.mission.num_steps == 0:
            reply = QMessageBox.question(None, "Save Mission",
                                         "You are about to save an empty mission. Do you want to proceed?",
                                         QMessageBox.Yes |
                                         QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return False, None
        elif float(self.mission.get_step(self.mission.get_length() - 1).get_maneuver().get_position().get_z()) != 0.0:
            # vehicle last waypoint is not at zero depth.
            reply = QMessageBox.question(None, "Save Mission",
                                         "You are about to save and the last waypoint is not at zero depth. "
                                         "Do you want to proceed?",
                                         QMessageBox.Yes |
                                         QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return False, None

        mission_filename, selected_filter = QFileDialog.getSaveFileName(None, 'Save mission',
                                                   self.mission_filename,
                                                   'XML (*.xml)')

        if mission_filename != '':
            if selected_filter =="XML (*.xml)":
                file_info = QFileInfo(mission_filename)

                self.mission.write_mission(mission_filename)

                logger.debug(file_info.fileName())
                self.set_mission_name(file_info.fileName())
                self.set_mission_filename(mission_filename)
                self.mission_layer.setName(file_info.baseName())
                self.mission_layer.setCustomProperty("mission_xml", self.mission_filename)

                self.saved = True
                self.modified = False

            return True, mission_filename

        else:
            return False, None

    def render_mission(self):
        """
        Render the mission, it will render the mission layer with Point geometry if it has only 1 point
        oterwise it will be with LineString geometry.
        """
        waypoints = self.find_waypoints_in_mission()
        if self.mission_layer is None:
            if len(waypoints) == 1:
                self.mission_layer = QgsVectorLayer(
                    "Point?crs=epsg:4326",
                    self.mission_name,
                    "memory")
                self.mission_layer.setCustomProperty("mission_xml", self.mission_filename)
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry(waypoints[0]))
                self.mission_layer.dataProvider().addFeatures([feature])
            else:
                self.mission_layer = QgsVectorLayer(
                    "LineString?crs=epsg:4326",
                    self.mission_name,
                    "memory")
                self.mission_layer.setCustomProperty("mission_xml", self.mission_filename)
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolyline(waypoints))
                self.mission_layer.dataProvider().addFeatures([feature])

        else:
            # mission layer exists, now check if it has already a feature or not
            feats = self.mission_layer.getFeatures()
            logger.debug("layer feature count {}".format(self.mission_layer.featureCount()))
            if self.mission_layer.featureCount() == 0:
                feature = QgsFeature()
                if len(waypoints) == 1:
                    feature.setGeometry(QgsGeometry(waypoints[0]))
                else:
                    feature.setGeometry(QgsGeometry.fromPolyline(waypoints))
                self.mission_layer.dataProvider().addFeatures([feature])
            else:
                logger.debug("layer has feature mission already, updating...")
                for f in feats:
                    self.mission_layer.dataProvider().deleteFeatures([f.id()])
                    feature = QgsFeature()
                    if len(waypoints) == 1:
                        feature.setGeometry(QgsGeometry(waypoints[0]))
                    else:
                        feature.setGeometry(QgsGeometry.fromPolyline(waypoints))
                    self.mission_layer.dataProvider().addFeatures([feature])

        self.set_mission_renderer(self.get_default_track_renderer())

    def find_waypoints_in_mission(self, indexes=None):
        """
        Gets all waypoints from a mission structure
        """
        waypoints = []
        if indexes is None:
            step_indexes = range(0, self.mission.size())
        else:
            step_indexes = indexes

        for stepindex in step_indexes:
            step = self.mission.get_step(stepindex)
            maneuver = step.get_maneuver()

            if maneuver.get_maneuver_type() == SECTION_MANEUVER:  # for a Section
                position = maneuver.get_final_position()
            else:
                position = maneuver.get_position()  # for Waypoint and Park

            waypoints.append(QgsPoint(float(position.longitude), float(position.latitude)))
        return waypoints

    def get_default_track_renderer(self):
        # Renderer for track lines
        registry = QgsSymbolLayerRegistry()
        line_meta = registry.symbolLayerMetadata("SimpleLine")
        marker_meta = registry.symbolLayerMetadata("MarkerLine")

        symbol = QgsSymbol.defaultSymbol(self.mission_layer.geometryType())

        # Line layer
        line_layer = line_meta.createSymbolLayer(
            {'width': '0.5', 'color': '255,0,0', 'offset': '0.0', 'penstyle': 'solid', 'use_custom_dash': '0',
             'joinstyle': 'bevel', 'capstyle': 'square'})

        # Marker layer
        marker_layer = marker_meta.createSymbolLayer(
            {'width': '1.5', 'color': '255,0,0', 'placement': 'vertex', 'offset': '0.0'})
        sub_symbol = marker_layer.subSymbol()

        # Replace the default layer with our own SimpleMarker
        sub_symbol.deleteSymbolLayer(0)
        cross = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer(
            {'name': 'circle', 'color': '255,0,0', 'color_border': '0,0,0', 'offset': '0,0', 'size': '2.5',
             'angle': '0'})
        sub_symbol.appendSymbolLayer(cross)

        # Replace the default layer with our two custom layers
        symbol.deleteSymbolLayer(0)
        symbol.appendSymbolLayer(line_layer)
        symbol.appendSymbolLayer(marker_layer)

        # Replace the renderer of the current layer
        renderer = QgsSingleSymbolRenderer(symbol)
        return renderer

    def update_start_end_markers(self):
        """ Updates start_end_markers"""
        self.start_end_marker.update_markers(self.find_waypoints_in_mission())

    def hide_start_end_markers(self):
        """ Hide start_end_markers"""
        self.start_end_marker.hide_markers()

    def remove_start_end_markers(self):
        """ Removes start end markers"""
        self.start_end_marker.close_markers()

    def update_layer_geometry(self):
        """
        This function needs to be called every time a point is added or deleted from the layer
        If needed, a new layer is created with the apropiate geometry
        Point if only one point, LineString otherwise
        """
        options = QgsDataProvider.ProviderOptions()
        waypoints = self.find_waypoints_in_mission()
        if (len(waypoints) != 1) and self.mission_layer.geometryType() == QgsWkbTypes.PointGeometry:
            self.mission_layer.setDataSource("LineString?crs=epsg:4326",
                                             self.mission_name,
                                             "memory",
                                             options)
            self.set_mission_renderer(self.get_default_track_renderer())
        elif len(waypoints) == 1 and self.mission_layer.geometryType() == QgsWkbTypes.LineGeometry:
            self.mission_layer.setDataSource("Point?crs=epsg:4326",
                                             self.mission_name,
                                             "memory",
                                             options)
            self.set_mission_renderer(self.get_default_track_renderer())
