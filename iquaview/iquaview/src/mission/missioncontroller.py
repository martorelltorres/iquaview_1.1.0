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
 Manages the creation, loading, saving and uploading of missions.
"""

import datetime
import os
import subprocess
import logging

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QMessageBox
from qgis.core import QgsVectorLayer

from iquaview.src.mission.inserttemplatewidget import InsertTemplateWidget
from iquaview.src.mission.missioninfo import MissionInfo
from iquaview.src.mission.maptools import selectfeaturestool
from iquaview.src.mission.maptools.edittool import EditTool
from iquaview.src.mission.maptools.movefeaturetool import MoveFeatureTool
from iquaview.src.mission.missioneditionwidget.waypointeditwidget import WaypointEditWidget
from iquaview.src.mission.missiontrack import MissionTrack
from iquaview.src.mission.newmissiondlg import NewMissionDlg

logger = logging.getLogger(__name__)


class MissionController(QObject):
    manual_entry = pyqtSignal()
    template_closed = pyqtSignal()
    stop_mission_editing = pyqtSignal()
    mission_added = pyqtSignal(QgsVectorLayer)

    def __init__(self, config, vehicle_info, proj, canvas, view, wp_dock, template_dock, minfo_dock, msglog):
        super(MissionController, self).__init__()
        self.config = config
        self.vehicle_info = vehicle_info
        self.proj = proj
        self.canvas = canvas
        self.view = view
        self.wp_dock = wp_dock
        self.current_mission = None
        self.template_dock = template_dock
        self.minfo_dock = minfo_dock
        self.msglog = msglog

        self.tool_edit_wp_mission = None
        self.selectfeattool = None
        self.template_insertion_widget = None

        self.editing = False

        self.mission_list = list()

    def get_edit_wp_mission_tool(self):
        return self.tool_edit_wp_mission

    def get_mission_list(self):
        """ Returns mission_list"""
        return self.mission_list

    def new_mission(self):
        """
        Add new mission to current project
        :return: return True if mission is created correctly, otherwise False
        """
        # display dialog for creating mission
        new_mission_dlg = NewMissionDlg()
        result = new_mission_dlg.exec_()

        if result == QDialog.Accepted:
            name = new_mission_dlg.get_mission_name()

            date = datetime.datetime.now()
            datestr = date.strftime('%y%m%d%H%M%S')
            # create  mission structure
            mt = MissionTrack(datestr + '_' + name,
                              os.path.dirname(self.proj.fileName()) + '/missions/' + datestr + '_' + name + '.xml',
                              canvas=self.canvas)

            # render layer
            mt.render_mission()
            mt.set_modified(True)
            self.mission_list.append(mt)
            self.mission_added.emit(mt.get_mission_layer())

            return True
        else:
            # cancel has been clicked
            return False

    def load_mission(self, filename):
        """
        Load a mission with name 'filename'
        :param filename: name of the mission
        """
        logger.info("Loading mission {}".format(filename))
        # set layer name from the filename
        name = os.path.splitext(os.path.basename(filename))[0]
        # Create new missiontrack and load from file
        mt = MissionTrack(name, canvas=self.canvas)
        try:
            mt.load_mission(filename)
            mt.render_mission()
            self.mission_list.append(mt)
            # add new layer in the project
            self.mission_added.emit(mt.get_mission_layer())

        except:
            logger.error("Invalid Mission File")
            raise Exception("Invalid Mission File")

    def remove_mission(self, layer):
        """ Remove a mission with associated layer 'layer'
        :param layer: associtated layer to the mission
        """
        for mt in self.mission_list:
            if mt.get_mission_layer() == layer:
                logger.info("Removing mission {}".format(mt.get_mission_name()))
                mt.remove_start_end_markers()
                self.mission_list.remove(mt)
                if self.current_mission.get_mission_layer() == layer:
                    self.finish_edit_wp_mission()
                    self.finish_select_features_mission()
                    self.close_template_editing()
                    self.stop_mission_editing.emit()

    def set_current_mission(self, layer):
        """
        Set layer 'layer' to current_mission
        :param layer:
        """

        # find mt corresponding to the layer
        for mt in self.mission_list:
            if mt.get_mission_layer() == layer:
                self.current_mission = mt

            else:
                "Current layer is not a mission layer"

    def get_current_mission(self):
        """ Returns current mission"""
        return self.current_mission

    def get_current_mission_layer(self):
        """ Returns current mission layer"""
        return self.current_mission.get_mission_layer()

    def get_current_mission_filename(self):
        """ Returns current mission filename"""
        return self.current_mission.get_mission_filename()

    def get_current_mission_name(self):
        """ Returns current mission name"""
        return self.current_mission.get_mission_name()

    def set_current_mission_name(self, name):
        """
        Set new name to current mission
        :param name: name of the mission
        """
        self.current_mission.set_mission_name(name)

    def set_current_mission_filename(self, name):
        """
        Set filename to current mission
        :param name: filename of the mission
        """
        filename = os.path.dirname(self.proj.fileName()) + '/missions/' + name + '.xml'
        self.current_mission.set_mission_filename(filename)

    def save_mission(self):
        """Save mission"""
        saved = self.current_mission.save_mission()
        return saved

    def saveas_mission(self):
        """Save mission as new name"""
        saved, mission_filename = self.current_mission.saveas_mission()
        return saved, mission_filename

    def edit_wp_mission(self):
        """ open a waypoint edit widget"""
        self.wpeditw = WaypointEditWidget(self.config,
                                          self.current_mission,
                                          self.vehicle_info.get_vehicle_namespace())
        self.wp_dock.setWidget(self.wpeditw)

        self.missioninfo = MissionInfo(self.canvas, self.current_mission)
        self.minfo_dock.setWidget(self.missioninfo)

        self.tool_edit_wp_mission = EditTool(self.current_mission, self.canvas, self.msglog)
        self.canvas.setMapTool(self.tool_edit_wp_mission)

        self.tool_edit_wp_mission.wp_clicked.connect(self.wp_clicked)
        self.wpeditw.control_state_signal.connect(self.tool_edit_wp_mission.set_control_state)
        self.wp_dock.show()
        self.minfo_dock.show()
        self.canvas.setFocus()

    def select_features_mission(self):
        """ open a waypoint edit widget with multiple_edition."""
        self.wpeditw = WaypointEditWidget(self.config,
                                          self.current_mission,
                                          self.vehicle_info.get_vehicle_namespace(),
                                          multiple_edition=True)
        self.wp_dock.setWidget(self.wpeditw)

        self.missioninfo = MissionInfo(self.canvas, self.current_mission)
        self.minfo_dock.setWidget(self.missioninfo)

        self.selectfeattool = selectfeaturestool.SelectFeaturesTool(self.current_mission, self.canvas)
        self.canvas.setMapTool(self.selectfeattool)

        self.selectfeattool.selection_clicked.connect(self.selection_clicked)
        self.wp_dock.show()
        self.minfo_dock.show()
        self.canvas.setFocus()

    def add_template_mission(self):
        """ Open a insert template widget"""
        self.template_insertion_widget = InsertTemplateWidget(self.canvas, self.msglog, self.view, self.current_mission)
        self.template_dock.setWidget(self.template_insertion_widget)
        self.template_insertion_widget.save_tracks.connect(self.close_template_editing)

        self.missioninfo = MissionInfo(self.canvas, self.current_mission)
        self.missioninfo.set_current_mission(self.template_insertion_widget.preview_mission)
        self.template_insertion_widget.preview_mission_signal.connect(self.missioninfo.update_values)
        self.minfo_dock.setWidget(self.missioninfo)

        self.template_dock.show()
        self.minfo_dock.show()

    def save_template_tracks_to_mission(self):
        """ Merge the template tracks to mission"""
        self.template_insertion_widget.merge_template_mission()

    def close_template_editing(self):
        """ Close template editing"""
        if self.template_insertion_widget is not None:
            self.template_insertion_widget.close()
        self.template_dock.hide()
        self.minfo_dock.hide()
        self.template_closed.emit()
        self.template_insertion_widget = None

    def is_template_modified(self):
        """
        :return: return true if template is modified, otherwise False
        """
        return self.template_insertion_widget.is_template_modified()

    def move_mission(self):
        """ Set MapTool MoveFeatureTool"""
        logger.debug("Setting move tool")
        tool_move_feature = MoveFeatureTool(self.current_mission, self.canvas)
        self.canvas.setMapTool(tool_move_feature)
        self.canvas.setFocus()

    def finish_edit_wp_mission(self):
        """ Finish edit waypoint mission"""
        if self.tool_edit_wp_mission is not None:
            self.tool_edit_wp_mission.close_band()
        self.wp_dock.hide()
        self.minfo_dock.hide()
        self.canvas.unsetMapTool(self.tool_edit_wp_mission)
        del self.tool_edit_wp_mission
        self.tool_edit_wp_mission = None

    def finish_select_features_mission(self):
        """ finish  multiple edition """
        if self.selectfeattool is not None:
            self.selectfeattool.deactivate()
        self.wp_dock.hide()
        self.minfo_dock.hide()
        self.canvas.unsetMapTool(self.selectfeattool)
        del self.selectfeattool
        self.selectfeattool = None

    def wp_clicked(self, wp):
        """
        Slot to handle when a mission step has been clicked from the map tool
        """
        logger.debug("I clicked a waypoint {}".format(wp))
        self.wpeditw.show_mission_step(wp)

    def selection_clicked(self, wp_list):
        """
        Slot to handle when a select features mission has been clicked from the map tool
        """

        self.wpeditw.show_multiple_features(wp_list)

    def send_mission_to_auv(self):
        """ Send the mission to vehicle"""
        if not self.current_mission.is_modified():
            mission_file = self.get_current_mission_filename()
            name = os.path.basename(mission_file)
            if name.rfind('\"') != -1:
                name = name.replace("\"", "\\\"")
            if name.rfind('`') != -1:
                name = name.replace("`", "\\`")
            user = self.vehicle_info.get_vehicle_user()
            server = self.vehicle_info.get_vehicle_ip()
            remotepath = self.vehicle_info.get_remote_mission_path()

            # make link to last copied mission
            name_target = "\"{}/{}\"".format(remotepath, name)
            name_link = remotepath + '/last_mission.xml'
            cmd = "ln -sf {} {}".format(name_target, name_link)
            try:
                subprocess.run(["scp", mission_file, "{}@{}:{}".format(user, server, remotepath)],
                               check=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
                logger.info("Copied mission file.")

                subprocess.run(["ssh", "{}@{}".format(user, server), cmd],
                               check=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
                logger.info("Linked mission file.")

                QMessageBox.information(None,
                                        "Mission upload",
                                        "Mission upload successfully",
                                        QMessageBox.Close)

            except subprocess.CalledProcessError as e:
                logger.error("Mission upload error: {}".format(e.stderr))
                QMessageBox.critical(None,
                                     "Mission upload",
                                     "Mission upload error: {}".format(e.stderr),
                                     QMessageBox.Close)

        else:
            logger.error("Mission file you are trying to upload to vehicle is not saved locally. Save it first")
            QMessageBox.critical(None,
                                 "Mission not saved",
                                 "Mission file you are trying to upload to vehicle is not saved locally. Save it first",
                                 QMessageBox.Close)
