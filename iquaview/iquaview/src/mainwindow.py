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
 Main window class.
 Sets up the main interface elements and triggers the corresponding actions according to user inputs.
"""

# =============================================================================
# Stdlib imports
# =============================================================================
import os
import logging
import subprocess
import threading
from importlib import util

# ==============================================================================
# Qt imports
# ==============================================================================
from PyQt5.QtCore import Qt, QFileInfo, qVersion, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow,
                             QAction,
                             QDockWidget,
                             QFileDialog,
                             QMessageBox,
                             QSizePolicy,
                             QFrame,
                             QLabel,
                             QToolBar,
                             QDialog,
                             QToolButton
                             )

# ==============================================================================
# Qgis imports
# ==============================================================================
from qgis.core import (QgsApplication,
                       QgsCoordinateReferenceSystem,
                       QgsProject,
                       QgsLayerTreeModel,
                       QgsVectorLayer,
                       QgsMapLayer,
                       QgsVectorFileWriter,
                       Qgis,
                       QgsFeature,
                       QgsGeometry,
                       QgsWkbTypes)

from qgis.gui import (QgsLayerTreeMapCanvasBridge,
                      QgsLayerTreeView,
                      QgsMapToolPan,
                      QgsMapToolZoom,
                      QgsMessageBar,
                      QgsMessageBarItem,
                      QgsScaleWidget,
                      QgsDoubleSpinBox)

# ==============================================================================
# Local imports
# ==============================================================================
from iquaview.src import __version__
from iquaview.src import (options,
                          resources_qgis
                          )
from iquaview.src.utils import busywidget
from iquaview.src.vehicle import keeppositionstatus, vehicledata, logwidget, calibratemagnetometer, thrustersstatus, \
    timeoutwidget, goto, vehicleinfo, auvconfigparams
from iquaview.src.plugins.pluginmanager import PluginManager
from iquaview.src.mission import missionstatus, missionactive, missioncontroller
from iquaview.src.tools import vesselpossystem, measuretool
from iquaview.src.connection.settings import connectionsettings
from iquaview.src.connection import auvprocesseswidget
from iquaview.src.canvastracks import auvposewidget, gpswidget

from iquaview.src.vehicle.checklist import check_list, check_list_selector
from iquaview.src.cola2api import cola2_interface
from iquaview.src.config import Config
from iquaview.src.utils.coordinateconverter import *
from iquaview.src.tools.coordinateconverterwidget import CoordinateConverterDialog
from iquaview.src.mapsetup.decoration import scalebar, northarrow

from iquaview.src.mapsetup import (addlayers,
                                   badlayerhandler,
                                   menuprovider,
                                   nedorigindrawer,
                                   pointfeaturedlg,
                                   movelandmarktool)
from iquaview.src.ui import ui_mainwindow
from iquaview.src.vehicle.vehiclewidgets import vehiclewidgets

logger = logging.getLogger(__name__)


class MainWindow(ui_mainwindow.Ui_MainWindow, QMainWindow):
    """
    Main application window
    """

    def __init__(self):
        """
        initialization

        """
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Read configs
        self.config = Config()
        self.config.load()
        self.config.csettings = self.config.settings

        # vehicle info
        self.vehicle_info = vehicleinfo.VehicleInfo(self.config)
        logger.info(self.config.settings)

        # Initialization of objects
        self.auv_pose = None
        self.gps_pose = None
        # process launch teleoperation
        self.process_teleop = None
        # process rqt_robot_monitor
        self.process_robot_monitor = None
        self.timer_robot_monitor = None
        self.auv_on_wifi = False

        # vehicle data
        self.vehicle_data = vehicledata.VehicleData(self.config, self.vehicle_info)

        # Menu bar
        self.project_menu = self.menubar.addMenu("Project")
        self.view_menu = self.menubar.addMenu("View")
        self.vehicle_menu = self.menubar.addMenu("Vehicle")
        self.mission_menu = self.menubar.addMenu("Mission")
        self.tools_menu = self.menubar.addMenu("Tools")

        # Actions for project
        self.new_project_action = QAction(QIcon(":/resources/mActionFileNew.svg"), "New Project", self)
        self.new_project_action.setShortcut("Ctrl+n")
        self.open_project_action = QAction(QIcon(":/resources/mActionFileOpen.svg"), "Open Project", self)
        self.open_project_action.setShortcut("Ctrl+o")
        self.save_project_action = QAction(QIcon(":/resources/mActionSave.svg"), "Save Project", self)
        self.save_project_action.setShortcut("Ctrl+s")
        self.saveprojectas_action = QAction(QIcon(":/resources/mActionSaveAs.svg"), "Save Project As", self)
        self.saveprojectas_action.setShortcut("Ctrl+Shift+s")
        self.add_layer_action = QAction(QIcon(":/resources/mActionAddLayer.png"), "Add Layer", self)
        self.add_landmark_point_action = QAction(QIcon(":/resources/mActionAddLandmarkPoint.svg"),
                                                 "Add Landmark Point",
                                                 self)
        self.add_landmark_point_action.setCheckable(True)
        self.move_landmark_point_action = QAction(QIcon(":/resources/mActionMoveLandmarkPoint.svg"),
                                                  "Move Landmark Point", self)
        self.move_landmark_point_action.setCheckable(True)
        self.connection_settings_action = QAction(QIcon(":/resources/mActionConnectionSettings.svg"),
                                                  "Connection Settings", self)
        self.options_action = QAction(QIcon(":/resources/mActionOptions.svg"), "Options...", self)
        self.quit_action = QAction(QIcon(":/resources/mActionFileExit.png"), "Quit", self)
        self.quit_action.setShortcut("Ctrl+q")

        self.project_menu.addActions([self.new_project_action,
                                      self.open_project_action,
                                      self.save_project_action,
                                      self.saveprojectas_action,
                                      self.project_menu.addSeparator(),
                                      self.add_layer_action,
                                      self.connection_settings_action])

        landmarks_menu = self.project_menu.addMenu("Landmark tools")
        landmarks_menu.addActions([self.add_landmark_point_action, self.move_landmark_point_action])
        self.project_menu.addMenu(landmarks_menu)

        self.project_menu.addActions([self.project_menu.addSeparator(),
                                      self.options_action,
                                      self.project_menu.addSeparator(),
                                      self.quit_action])

        # Actions for view
        self.zoom_in_action = QAction(QIcon(":/resources/mActionZoomIn.png"), "Zoom In", self)
        self.zoom_in_action.setShortcut("Ctrl++")
        self.zoom_out_action = QAction(QIcon(":/resources/mActionZoomOut.png"), "Zoom Out", self)
        self.zoom_out_action.setShortcut("Ctrl+-")
        self.pan_action = QAction(QIcon(":/resources/mActionPan.svg"), "Pan", self)
        self.pan_action.setShortcut("Ctrl+p")
        self.boat_pose_action = QAction(QIcon(":/resources/mActionBoatPose.svg"), "Show Vessel Pose", self)
        self.boat_pose_action.setCheckable(True)
        self.boat_pose_action.setShortcut("Ctrl+v")
        self.vehicle_widgets_action = QAction("Vehicle Widgets", self)
        self.vehicle_widgets_action.setCheckable(True)
        self.scale_bar_action = QAction("Scale Bar", self)
        self.scale_bar_action.setCheckable(True)
        self.north_arrow_action = QAction("North Arrow", self)
        self.north_arrow_action.setCheckable(True)

        self.view_menu.addActions([self.zoom_in_action,
                                   self.zoom_out_action,
                                   self.pan_action,
                                   self.boat_pose_action])
        self.view_menu.addSeparator()

        view_menu_panels  = self.view_menu.addMenu("Panels")
        view_menu_decorations = self.view_menu.addMenu("Decorations")
        view_menu_toolbar = self.view_menu.addMenu("Toolbars")
        view_menu_widgets = self.view_menu.addMenu("Vehicle Widgets")

        # Actions for Vehicle (wifi)
        self.auv_config_parameters_action = QAction(QIcon(":/resources/mActionAUVConfigParameters.svg"),
                                                    "AUV Configuration Parameters", self)
        self.checklist_action = QAction(QIcon(":/resources/mActionCheckList.svg"), "Check List", self)
        self.joystick_teleop_action = QAction(QIcon(":/resources/joystick.png"), "Enable Joystick Teleoperation", self)
        self.joystick_teleop_action.setCheckable(True)
        self.joystick_teleop_action.setShortcut("Ctrl+j")

        if self.vehicle_data.get_calibrate_magnetometer_service() is not None:
            self.calibrate_magnetometer_action = QAction(QIcon(":/resources/compass.svg"),
                                                         "Calibrate Magnetometer",
                                                         self)
            self.calibrate_magnetometer_action.setCheckable(True)

        self.robot_monitor_action = QAction(QIcon(":/resources/robot_monitor.svg"), "Open Robot Monitor", self)
        self.robot_monitor_action.setCheckable(True)
        self.robot_monitor_action.setShortcut("Ctrl+r")
        self.reset_timeout_action = QAction(QIcon(":/resources/actionResetTimeout.svg"), "Reset Timeout", self)

        self.auv_pose_action = QAction(QIcon(":/resources/"
                                             + self.vehicle_info.get_vehicle_type()
                                             + "/mActionAUVPose.svg"),
                                       "Monitor AUV Pose",
                                       self)

        self.auv_pose_action.setCheckable(True)
        self.auv_pose_action.setShortcut("Ctrl+a")
        self.enable_keep_position_action = QAction(QIcon(":resources/mActionEnableKeepPosition.svg"),
                                                   "Enable Keep Position", self)
        self.enable_keep_position_action.setCheckable(True)
        self.disable_thrusters_action = QAction(QIcon(":resources/mActionDisableThrusters.svg"), "Disable Thrusters",
                                                self)
        self.disable_thrusters_action.setCheckable(True)
        self.goto_action = QAction(QIcon(":resources/goto.svg"), "Go to", self)
        self.goto_action.setCheckable(True)
        self.goto_action.setShortcut("Ctrl+g")
        self.execute_mission_action = QAction(QIcon(":/resources/mActionExecuteMission.svg"), "Execute Mission", self)
        self.execute_mission_action.setCheckable(True)

        self.vehicle_menu.addActions([self.auv_config_parameters_action,
                                      self.checklist_action,
                                      self.joystick_teleop_action])
        if self.vehicle_data.get_calibrate_magnetometer_service() is not None:
            self.vehicle_menu.addAction(self.calibrate_magnetometer_action)
        self.vehicle_menu.addActions([self.robot_monitor_action,
                                      self.reset_timeout_action,
                                      self.auv_pose_action,
                                      self.enable_keep_position_action,
                                      self.disable_thrusters_action,
                                      self.goto_action,
                                      self.execute_mission_action])

        # Actions for Mission
        self.new_mission_action = QAction(QIcon(":/resources/mActionNewMission.svg"), "New Mission", self)
        self.load_mission_action = QAction(QIcon(":/resources/mActionLoadMissionFile.svg"), "Load Mission", self)
        self.save_mission_action = QAction(QIcon(":/resources/mActionSaveMission.svg"), "Save Mission", self)
        self.saveas_mission_action = QAction(QIcon(":/resources/mActionSaveAsMission.svg"), "Save Mission As...", self)
        self.send_mission_action = QAction(QIcon(":/resources/mActionSendMission.svg"),
                                           "Upload Mission to Vehicle",
                                           self)
        self.edit_wp_mission_action = QAction(QIcon(":/resources/mActionEditWaypoints.svg"), "Edit Mission Waypoints",
                                              self)
        self.edit_wp_mission_action.setShortcut("Ctrl+e")
        self.select_features_mission_action = QAction(QIcon(":/resources/mActionEditMultipleWaypoints.svg"),
                                                      "Select Mission Waypoints for Multiple Edition",
                                                      self)
        self.template_mission_action = QAction(QIcon(":/resources/mActionAddMissionTemplate.svg"),
                                               "Add Mission Template",
                                               self)
        self.move_mission_action = QAction(QIcon(":/resources/mActionMoveMission.svg"), "Move Mission", self)
        self.edit_wp_mission_action.setCheckable(True)
        self.select_features_mission_action.setCheckable(True)
        self.template_mission_action.setCheckable(True)
        self.move_mission_action.setCheckable(True)
        self.execute_mission_action.setCheckable(True)

        self.mission_menu.addActions([self.new_mission_action,
                                      self.load_mission_action,
                                      self.save_mission_action,
                                      self.saveas_mission_action,
                                      self.send_mission_action,
                                      self.edit_wp_mission_action,
                                      self.select_features_mission_action,
                                      self.template_mission_action,
                                      self.move_mission_action])

        # Actions for Tools
        self.measure_distance_action = QAction(QIcon(":/resources/mActionMeasure.png"), "Measure Distance Tool", self)
        self.measure_distance_action.setCheckable(True)
        self.measure_distance_action.setShortcut("Ctrl+m")
        self.measure_angle_action = QAction(QIcon(":/resources/mActionMeasureAngle.svg"), "Measure Angle Tool", self)
        self.measure_angle_action.setCheckable(True)
        self.measure_area_action = QAction(QIcon(":/resources/mActionMeasureArea.svg"), "Measure Area Tool", self)
        self.measure_area_action.setCheckable(True)

        self.coordinate_converter_action = QAction(QIcon(":/resources/converter.svg"), "Coordinate Converter", self)
        self.vessel_pos_system_action = QAction("Vessel Position System", self)

        measure_tools_menu = self.tools_menu.addMenu("Measure Tools")
        measure_tools_menu.addActions([self.measure_distance_action,
                                    self.measure_angle_action,
                                    self.measure_area_action])

        self.tools_menu.addActions([self.coordinate_converter_action,
                                   self.vessel_pos_system_action])
        self.tools_menu.addMenu(measure_tools_menu)

        # Add actions to project toolbar
        self.project_toolbar = QToolBar("Project tools")
        self.project_toolbar.setObjectName("Project tools")
        self.project_toolbar.addAction(self.new_project_action)
        self.project_toolbar.addAction(self.open_project_action)
        self.project_toolbar.addAction(self.save_project_action)
        self.project_toolbar.addAction(self.saveprojectas_action)
        self.project_toolbar.addAction(self.add_layer_action)
        self.project_toolbar.addAction(self.connection_settings_action)

        bt = QToolButton()
        bt.setPopupMode(QToolButton.MenuButtonPopup)
        bt.addActions([self.add_landmark_point_action, self.move_landmark_point_action])
        bt.setDefaultAction(self.add_landmark_point_action)
        bt.triggered.connect(self.change_menu_tool)
        self.project_toolbar.addWidget(bt)

        self.addToolBar(self.project_toolbar)

        # Toolbar for View
        self.view_toolbar = QToolBar("View Tools")
        self.view_toolbar.setObjectName("View Tools")
        self.view_toolbar.addAction(self.zoom_in_action)
        self.view_toolbar.addAction(self.zoom_out_action)
        self.view_toolbar.addAction(self.pan_action)
        self.view_toolbar.addAction(self.boat_pose_action)
        self.addToolBar(self.view_toolbar)

        # Toolbar for Tools
        self.tools_toolbar = QToolBar("Tools")
        self.tools_toolbar.setObjectName("Tools")

        bt = QToolButton()
        bt.setPopupMode(QToolButton.MenuButtonPopup)
        bt.addActions([self.measure_distance_action,
                       self.measure_angle_action,
                       self.measure_area_action])
        bt.setDefaultAction(self.measure_distance_action)
        bt.triggered.connect(self.change_menu_tool)
        self.tools_toolbar.addWidget(bt)
        self.tools_toolbar.addAction(self.coordinate_converter_action)
        self.addToolBar(self.tools_toolbar)

        # Toolbar for Mission
        self.mission_toolbar = QToolBar("Mission Tools")
        self.mission_toolbar.setObjectName("Mission Tools")
        self.mission_toolbar.addAction(self.new_mission_action)
        self.mission_toolbar.addAction(self.load_mission_action)
        self.mission_toolbar.addAction(self.save_mission_action)
        self.mission_toolbar.addAction(self.saveas_mission_action)
        self.mission_toolbar.addAction(self.send_mission_action)
        self.mission_toolbar.addAction(self.edit_wp_mission_action)
        self.mission_toolbar.addAction(self.select_features_mission_action)
        self.mission_toolbar.addAction(self.template_mission_action)
        self.mission_toolbar.addAction(self.move_mission_action)
        self.addToolBar(self.mission_toolbar)

        # Toolbar for AUV Processes
        self.addToolBarBreak()
        self.connection_toolbar = QToolBar("AUV Processes")
        self.connection_toolbar.setObjectName("AUV Processes")
        self.auv_processes_widget = auvprocesseswidget.AUVProcessesWidget(self.config, self.vehicle_info)
        self.connection_toolbar.addWidget(self.auv_processes_widget)
        self.addToolBar(self.connection_toolbar)

        # Toolbar for Vehicle (wifi)
        self.auvwifi_toolbar = QToolBar("Vehicle tools (WiFi)")
        self.auvwifi_toolbar.setObjectName("Vehicle tools (WiFi)")

        self.auvwifi_toolbar.addAction(self.auv_config_parameters_action)
        self.auvwifi_toolbar.addAction(self.checklist_action)
        self.auvwifi_toolbar.addAction(self.joystick_teleop_action)
        if self.vehicle_data.get_calibrate_magnetometer_service() is not None:
            self.auvwifi_toolbar.addAction(self.calibrate_magnetometer_action)
        self.auvwifi_toolbar.addAction(self.robot_monitor_action)
        self.auvwifi_toolbar.addAction(self.reset_timeout_action)
        self.timeout_widget = timeoutwidget.TimeoutWidget(self.vehicle_info, self.vehicle_data)
        self.auvwifi_toolbar.addWidget(self.timeout_widget)

        self.auvwifi_toolbar.addAction(self.auv_pose_action)
        self.auvwifi_toolbar.addAction(self.enable_keep_position_action)
        self.auvwifi_toolbar.addAction(self.disable_thrusters_action)
        self.auvwifi_toolbar.addAction(self.goto_action)
        self.auvwifi_toolbar.addAction(self.execute_mission_action)

        self.addToolBar(self.auvwifi_toolbar)

        # set priority to expand dock widgets
        # left/right dockwidgets have more priority than top/bottom dockwidgets on corners
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        # Dock for Layer Legend
        self.legend_dock = QDockWidget("Layers", self)
        self.legend_dock.setObjectName("layers")
        self.legend_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.legend_dock.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.legend_dock)
        self.legend_dock.visibilityChanged.connect(self.layers_dock_visibility_changed)


        # Dock for Mission Info
        self.minfo_dock = QDockWidget("Mission Info", self)
        self.minfo_dock.setObjectName("Mission Info")
        self.minfo_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.minfo_dock.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.RightDockWidgetArea, self.minfo_dock)
        self.minfo_dock.setStyleSheet("QDockWidget { font: bold; }")
        self.minfo_dock.setWindowTitle("Mission Info")
        self.minfo_dock.hide()

        # Dock for Waypoint Edit
        self.wp_dock = QDockWidget("Waypoint Editing", self)
        self.wp_dock.setObjectName("Waypoint Editing")
        self.wp_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.wp_dock.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.RightDockWidgetArea, self.wp_dock)
        self.wp_dock.setStyleSheet("QDockWidget { font: bold; }")
        self.wp_dock.setWindowTitle("Mission Waypoint Editor")
        self.wp_dock.hide()

        # Dock for Mission Templates
        self.templates_dock = QDockWidget("Mission Templates", self)
        self.templates_dock.setObjectName("Mission Templates")
        self.templates_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.templates_dock.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.RightDockWidgetArea, self.templates_dock)
        self.templates_dock.setStyleSheet("QDockWidget { font: bold; }")
        self.templates_dock.setWindowTitle("Mission Templates")
        self.templates_dock.hide()

        # dock for Graphical vehicle Widgets
        self.vehicle_w_dock = QDockWidget("Vehicle Widgets")
        self.vehicle_w_dock.setObjectName("Vehicle Widgets Dock")
        self.vehicle_w_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        self.vehicle_w_dock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.vehicle_w_dock)
        self.vehicle_w_dock.setStyleSheet("QDockWidget { font: bold; }")
        self.vehicle_widgets = vehiclewidgets.VehicleWidgets(self.vehicle_info, self.vehicle_data)
        self.vehicle_w_dock.setWidget(self.vehicle_widgets)
        self.vehicle_w_dock.visibilityChanged.connect(self.vehicle_widgets_dock_visibility_changed)

        # dock for Log Info
        self.log_dock = QDockWidget("Log info")
        self.log_dock.setObjectName("Log info Dock")
        # self.log_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        self.log_dock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_dock)
        self.log_dock.setStyleSheet("QDockWidget { font: bold; }")
        self.log_widget = logwidget.LogWidget(self.vehicle_data)
        self.log_dock.setWidget(self.log_widget)
        self.log_dock.visibilityChanged.connect(self.log_dock_visibility_changed)
        self.log_dock.hide()

        # Message Bar
        self.msg_bar = QgsMessageBar(self.canvas)
        self.msg_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addWidget(self.msg_bar, 0, 0, Qt.AlignTop)

        self.vehicle_msg_bar = QgsMessageBar(self.canvas)
        self.vehicle_msg_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addWidget(self.vehicle_msg_bar, 1, 0, Qt.AlignTop)

        # Set canvas
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.setDestinationCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))

        # widget to show coordinates
        self.label_xy = QLabel()
        self.label_xy.setFrameStyle(QFrame.StyledPanel)
        self.label_xy.setMinimumWidth(400)
        self.label_xy.setAlignment(Qt.AlignCenter)
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.addPermanentWidget(self.label_xy, 0)

        # Setup scale widget
        self.scale_widget = QgsScaleWidget()
        self.rotate_widget = QgsDoubleSpinBox()
        self.rotate_widget.setSuffix(u"\u00b0")
        self.rotate_widget.setRange(-360, 360)
        self.rotate_widget.setSingleStep(5)
        self.status_bar.addPermanentWidget(self.scale_widget, 0)
        self.status_bar.addPermanentWidget(self.rotate_widget, 0)

        # Project handler
        self.proj = QgsProject.instance()
        self.proj.setFileName("")
        self.bad_layer_handler = badlayerhandler.BadLayerHandler(callback=self.failed_layers)
        self.proj.setBadLayerHandler(self.bad_layer_handler)

        self.scale_bar = scalebar.ScaleBar(self.proj, self.canvas)
        self.north_arrow = northarrow.NorthArrow(self.proj, self.canvas)

        # Message log handler
        self.msg_log = QgsApplication.messageLog()
        self.msg_log.messageReceived.connect(self.msgbar_catcher)

        # Set map tools
        self.tool_pan = QgsMapToolPan(self.canvas)
        self.tool_pan.setAction(self.pan_action)
        self.tool_zoom_in = QgsMapToolZoom(self.canvas, False)
        self.tool_zoom_in.setAction(self.zoom_in_action)
        self.tool_zoom_out = QgsMapToolZoom(self.canvas, True)
        self.tool_zoom_out.setAction(self.zoom_out_action)
        self.tool_measure_distance = measuretool.MeasureDistanceTool(self.canvas, self.msg_log)
        self.tool_measure_angle = measuretool.MeasureAngleTool(self.canvas, self.msg_log)
        self.tool_measure_area = measuretool.MeasureAreaTool(self.canvas, self.msg_log)
        self.tool_move_landmark = movelandmarktool.MoveLandmarkTool(self.canvas)

        self.point_feature = pointfeaturedlg.PointFeatureDlg(self.canvas, self.proj, self)
        self.point_feature.landmark_added.connect(self.add_map_layer)
        self.point_feature.landmark_removed.connect(self.remove_map_layer)
        self.point_feature.map_tool_change_signal.connect(self.map_tool_change)
        self.point_feature.finish_add_landmark_signal.connect(self.finish_add_landmark)

        # Set signals for Project actions
        self.new_project_action.triggered.connect(self.clear_project)
        self.open_project_action.triggered.connect(self.open_project)
        self.save_project_action.triggered.connect(self.save_project)
        self.saveprojectas_action.triggered.connect(self.save_project_as)
        self.add_layer_action.triggered.connect(self.add_layer)
        self.add_landmark_point_action.triggered.connect(self.add_landmark_point)
        self.move_landmark_point_action.triggered.connect(self.move_landmark_point)
        self.connection_settings_action.triggered.connect(self.connection_settings)
        self.options_action.triggered.connect(self.edit_options)
        self.quit_action.triggered.connect(self.close)

        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.pan_action.triggered.connect(self.pan)
        self.measure_distance_action.triggered.connect(self.measure_distance)
        self.measure_angle_action.triggered.connect(self.measure_angle)
        self.measure_area_action.triggered.connect(self.measure_area)
        self.boat_pose_action.triggered.connect(self.show_boat_pose)
        self.vehicle_widgets_action.triggered.connect(self.vehicle_widgets_visibility)
        self.scale_bar_action.triggered.connect(self.scale_bar_visibility)
        self.north_arrow_action.triggered.connect(self.north_arrow_visibility)

        self.auv_config_parameters_action.triggered.connect(self.auv_config_params)
        self.checklist_action.triggered.connect(self.checklist)
        self.joystick_teleop_action.toggled.connect(self.launch_teleoperation)
        self.reset_timeout_action.triggered.connect(self.reset_timeout)
        if self.vehicle_data.get_calibrate_magnetometer_service() is not None:
            self.calibrate_magnetometer_action.triggered.connect(self.on_click_calibrate_magnetometer)
        self.robot_monitor_action.triggered.connect(self.robot_monitor)
        # self.auv_processes_widget.cc.connection_failure.connect(self.connection_failed)
        self.auv_processes_widget.processchanged.connect(self.process_changed)

        self.auv_pose_action.triggered.connect(self.show_auv_pose)
        self.enable_keep_position_action.triggered.connect(self.enable_keep_position)
        self.disable_thrusters_action.triggered.connect(self.disable_thrusters)
        self.goto_action.triggered.connect(self.goto)

        self.new_mission_action.triggered.connect(self.new_mission)
        self.load_mission_action.triggered.connect(self.load_mission)
        self.save_mission_action.triggered.connect(self.save_mission)
        self.saveas_mission_action.triggered.connect(self.saveas_mission)
        self.send_mission_action.triggered.connect(self.send_mission_to_auv)

        self.coordinate_converter_action.triggered.connect(self.coordinate_converter)
        self.vessel_pos_system_action.triggered.connect(self.vessel_pos_system)

        self.edit_wp_mission_action.toggled.connect(self.edit_wp_mission)
        self.select_features_mission_action.toggled.connect(self.select_features_mission)
        self.template_mission_action.toggled.connect(self.add_template_mission)
        self.move_mission_action.toggled.connect(self.move_mission)
        self.execute_mission_action.triggered.connect(self.execute_mission)

        self.canvas.xyCoordinates.connect(self.show_xy)
        self.canvas.scaleChanged.connect(self.show_scale)
        self.scale_widget.scaleChanged.connect(self.on_scale_changed)
        self.rotate_widget.valueChanged.connect(self.on_rotation_changed)

        # Layer tree view
        self.init_layer_treeview()

        # Start connection with vehicle
        self.auv_processes_widget.connect()

        # Handle for NED origin drawer
        self.ned_origin_drawer = nedorigindrawer.NEDOriginDrawer(self.proj, self.vehicle_info)

        # Handle for mission controller
        self.mission_ctrl = missioncontroller.MissionController(self.config,
                                                                self.vehicle_info,
                                                                self.proj,
                                                                self.canvas,
                                                                self.view,
                                                                self.wp_dock,
                                                                self.templates_dock,
                                                                self.minfo_dock,
                                                                self.msg_log)
        self.mission_ctrl.mission_added.connect(self.add_map_layer)
        self.mission_ctrl.template_closed.connect(self.template_closed)
        self.mission_ctrl.stop_mission_editing.connect(self.disable_mission_editing)

        logger.info("Loading last project: {}".format(self.config.settings['last_open_project']))
        self.load_project(self.config.settings['last_open_project'])

        # thrusters status
        self.thrusters_status = thrustersstatus.ThrustersStatus(self.vehicle_data)
        self.thrusters_status.thrusters_signal.connect(self.change_icon_thrusters)

        # mission active status
        self.mission_active = missionactive.MissionActive(self.vehicle_data)
        self.mission_active.mission_signal.connect(self.change_icon_mission)

        # keep position
        self.keep_position_status = keeppositionstatus.KeepPositionStatus(self.vehicle_data, self.msg_log)
        self.keep_position_status.keep_position_signal.connect(self.change_icon_keep_position)
        # goto
        self.goto_dialog = goto.GoToDialog(self.config, self.canvas, self.vehicle_info.get_vehicle_ip(), 9091,
                                           self.vehicle_info.get_vehicle_namespace(), self.vehicle_data, self)
        self.goto_dialog.going_signal.connect(self.change_icon_goto)
        self.goto_dialog.map_tool_change_signal.connect(self.map_tool_change)
        self.goto_dialog.dialog_finished_signal.connect(self.pan)

        if self.vehicle_data.get_calibrate_magnetometer_service() is not None:
            self.calibrate_magnetometer = calibratemagnetometer.CalibrateMagnetometer(self.vehicle_info,
                                                                                      self.vehicle_data)
            self.calibrate_magnetometer.calibrate_magnetometer_signal.connect(self.calibrate_magnetometer_result)

        self.mission_sts = missionstatus.MissionStatus(self.vehicle_data, self.msg_log)

        self.auv_wifi_connected(False)
        self.activate_mission_tools(False)

        # create qactions to add at view_menu
        self.log_action = QAction("Log Info", self)
        self.log_action.setShortcut("Ctrl+l")
        self.log_action.setCheckable(True)
        self.log_action.setChecked(False)
        self.log_action.triggered.connect(self.open_log)

        self.legend_action = QAction("Layers", self)
        self.legend_action.setCheckable(True)
        self.legend_action.setChecked(True)
        self.legend_action.triggered.connect(self.open_legend)

        view_menu_panels.addActions([self.legend_action,
                                     self.log_action])

        self.project_toolbar_action = QAction("Project", self)
        self.project_toolbar_action.setCheckable(True)
        self.project_toolbar_action.setChecked(True)
        self.project_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.project_toolbar))

        self.view_toolbar_action = QAction("View", self)
        self.view_toolbar_action.setCheckable(True)
        self.view_toolbar_action.setChecked(True)
        self.view_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.view_toolbar))

        self.tools_toolbar_action = QAction("Tools", self)
        self.tools_toolbar_action.setCheckable(True)
        self.tools_toolbar_action.setChecked(True)
        self.tools_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.tools_toolbar))

        self.mission_toolbar_action = QAction("Mission", self)
        self.mission_toolbar_action.setCheckable(True)
        self.mission_toolbar_action.setChecked(True)
        self.mission_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.mission_toolbar))

        self.connection_toolbar_action = QAction("AUV Processes", self)
        self.connection_toolbar_action.setCheckable(True)
        self.connection_toolbar_action.setChecked(True)
        self.connection_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.connection_toolbar))

        self.auvwifi_toolbar_action = QAction("Vehicle tools (WiFi)", self)
        self.auvwifi_toolbar_action.setCheckable(True)
        self.auvwifi_toolbar_action.setChecked(True)
        self.auvwifi_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.auvwifi_toolbar))

        # add actions on view_menu_toolbar, to change toolbar visibility
        view_menu_toolbar.addActions([self.project_toolbar_action,
                                      self.view_toolbar_action,
                                      self.tools_toolbar_action,
                                      self.mission_toolbar_action,
                                      self.connection_toolbar_action,
                                      self.auvwifi_toolbar_action])
        # create QAction's to change Vehicle widgets state
        self.resources_action = QAction("Resources", self)
        self.resources_action.setCheckable(True)
        self.resources_action.setChecked(True)
        self.resources_action.setEnabled(False)
        self.resources_action.triggered.connect(self.vehicle_widgets.resources_state_changed)

        self.compass_action = QAction("Compass", self)
        self.compass_action.setCheckable(True)
        self.compass_action.setChecked(True)
        self.compass_action.setEnabled(False)
        self.compass_action.triggered.connect(self.vehicle_widgets.compass_state_changed)

        self.depth_altitude_action = QAction("Depth/Altitude", self)
        self.depth_altitude_action.setCheckable(True)
        self.depth_altitude_action.setChecked(True)
        self.depth_altitude_action.setEnabled(False)
        self.depth_altitude_action.triggered.connect(self.vehicle_widgets.depthaltitude_state_changed)

        self.roll_pitch_action = QAction("Roll/Pitch", self)
        self.roll_pitch_action.setCheckable(True)
        self.roll_pitch_action.setChecked(True)
        self.roll_pitch_action.setEnabled(False)
        self.roll_pitch_action.triggered.connect(self.vehicle_widgets.rollpitch_state_changed)

        self.velocimeter_action = QAction("Velocimeter", self)
        self.velocimeter_action.setCheckable(True)
        self.velocimeter_action.setChecked(True)
        self.velocimeter_action.setEnabled(False)
        self.velocimeter_action.triggered.connect(self.vehicle_widgets.velocimeter_state_changed)

        self.table_action = QAction("Table", self)
        self.table_action.setCheckable(True)
        self.table_action.setChecked(True)
        self.table_action.setEnabled(False)
        self.table_action.triggered.connect(self.vehicle_widgets.table_state_changed)

        self.setpoints_action = QAction("Setpoints", self)
        self.setpoints_action.setCheckable(True)
        self.setpoints_action.setChecked(True)
        self.setpoints_action.setEnabled(False)
        self.setpoints_action.triggered.connect(self.vehicle_widgets.setpoints_state_changed)

        view_menu_widgets.addAction(self.vehicle_widgets_action)
        view_menu_widgets.addSeparator()
        view_menu_widgets.addActions([self.resources_action,
                                      self.compass_action,
                                      self.depth_altitude_action,
                                      self.roll_pitch_action,
                                      self.velocimeter_action,
                                      self.table_action,
                                      self.setpoints_action])

        view_menu_decorations.addAction(self.scale_bar_action)
        view_menu_decorations.addAction(self.north_arrow_action)

        self.plugin_manager = PluginManager(self.proj, self.canvas, self.config, self.vehicle_info, self.mission_sts,
                                            self.boat_pose_action, self.menubar, view_menu_toolbar)
        if util.find_spec('usblcontroller') is not None:
            self.addToolBar(self.plugin_manager.get_usbl().get_usbl_toolbar())
            self.plugin_manager.get_usbl().signal_create_dock.connect(self.addDockWidget)
            self.plugin_manager.get_usbl().signal_enable_boat_pose_action.connect(self.enable_boat_pose_action)

        #add the help menu at the end
        self.help_menu = self.menubar.addMenu("Help")

        self.about_action = QAction(QIcon(":/resources/iquaview_vector.svg"), "About", self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addActions([self.about_action])

        self.set_decorations_visibility()

        self.setContextMenuPolicy(Qt.NoContextMenu)

        # Activate pan tool by default
        self.pan()

    def create_auv_position_dockwidget(self):
        """
        Create auv position dockwidget.

        """

        # Dock for AUV Position
        self.auvp_dw = QDockWidget()
        self.auvp_dw.setObjectName("AUVDockWidget")
        self.auvp_dw.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.auvp_dw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.auvp_dw)
        self.auvp_dw.setStyleSheet("QDockWidget { font: bold; }")
        self.auvp_dw.setWindowTitle("AUV monitoring (WiFi)")
        # set WA_DeleteOnClose attribute to catch Close button on QDockWidget with a destroyed signal
        self.auvp_dw.setAttribute(Qt.WA_DeleteOnClose)
        # connect destroyed signal to disconnect auvpw and auvpose widget
        self.auvp_dw.destroyed.connect(self.disconnect_auvp_dw)

    def create_gps_dockwidget(self):
        """ Create GPS dockwidget."""
        # Dock for GPS
        self.gps_dw = QDockWidget()
        self.gps_dw.setObjectName("GPSDockWidget")
        self.gps_dw.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.gps_dw)
        self.gps_dw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(9, 9, 9, 9)
        self.gps_dw.setStyleSheet("QDockWidget { font: bold; }")
        self.gps_dw.setWindowTitle("Vessel Position")
        # set atrribute delete on close
        self.gps_dw.setAttribute(Qt.WA_DeleteOnClose)
        self.gps_dw.destroyed.connect(self.disconnect_gps_dw)

    def disconnect_auvp_dw(self):
        """ Disconnect auv pose dockwidget."""

        if self.auv_pose is not None:
            # disconnect AUVPoseWidget
            if self.auv_pose.is_connected():
                self.auv_pose.disconnect()

            self.auv_pose.deleteLater()
            self.auv_pose = None
        self.auv_pose_action.setChecked(False)

    def disconnect_gps_dw(self):
        """ Disconnect GPS docwidget."""

        if self.gps_pose is not None:
            if self.gps_pose.is_connected():
                self.gps_pose.disconnect()

            self.gps_pose.deleteLater()
            self.gps_pose = None

        if self.boat_pose_action is not None:
            self.boat_pose_action.setChecked(False)

    def clear_project(self):
        """
        clear the project - removes all settings and resets it back to an empty.

        """
        self.proj.clear()
        self.canvas.refresh()

    def open_project(self):
        """
        Open QFileDialog to find a project with extension .qgs

        """
        filename = QFileDialog.getOpenFileName(self, 'Open Project', "", '*.qgs')
        if filename[0] != '':
            self.proj.clear()
            self.load_project(filename[0])

    def load_project(self, filename):
        """
        Load a project with the filename name.

        :param filename: name of the project

        """
        if filename != '':
            self.proj.setFileName(filename)
            self.proj.read()
            logger.info("Loaded a total of {} layers".format(len(self.proj.mapLayers())))
            for l in self.proj.mapLayers().values():
                if l.customProperty("mission_xml") is not None:
                    self.mission_ctrl.load_mission(l.customProperty("mission_xml"))
                    self.proj.removeMapLayer(l)
                elif l.customProperty("ned_origin") is not None:
                    self.proj.removeMapLayer(l)
            self.status_bar.showMessage("Project opened", 1500)
            self.config.settings['last_open_project'] = filename
            self.config.save()
            self.rotate_widget.setValue(self.canvas.rotation())

    def save_project(self, from_save_as=False):
        """
        Save current project.

        """

        if self.proj.fileName() == "":
            self.save_project_as()
        else:
            save = True
            if not from_save_as:
                if self.are_missions_modified():
                    reply = QMessageBox.question(self, 'Save project',
                                                 "You are about to save the project with some unsaved missions. "
                                                 "If you proceed the unsaved missions changes will be lost. Do you want to continue?",
                                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.No:
                        save = False

            if save:
                temporal_layers = list()
                for l in self.proj.mapLayers().values():
                    logger.info("Layer {} : type {}".format(l.name(), l.source()))
                    # if does not start with / means source is not a path and therefore is a  memory layer, should be saved
                    if l.source()[0] != "/":
                        if l.customProperty("mission_xml") is not None:
                            self.mission_ctrl.set_current_mission(l)
                            current_mission = self.mission_ctrl.get_current_mission()
                            if current_mission.is_saved():
                                self.save_vector_layer(l)
                            else:
                                # copy to temporary layer
                                temp_layer = l.clone()
                                temp_layer.setRenderer(l.renderer().clone())
                                waypoints = current_mission.find_waypoints_in_mission()
                                feature = QgsFeature()
                                if l.geometryType() == QgsWkbTypes.LineGeometry:
                                    feature.setGeometry(QgsGeometry.fromPolyline(waypoints))
                                elif l.geometryType() == QgsWkbTypes.PointGeometry:
                                    feature.setGeometry(QgsGeometry.fromPoint(waypoints[0]))
                                temp_layer.dataProvider().addFeatures([feature])
                                current_mission.set_mission_layer(temp_layer)
                                temporal_layers.append(temp_layer)

                                self.proj.removeMapLayer(l)

                        else:
                            self.save_vector_layer(l)

                    else:
                        # split source
                        source_last = l.source().split('/')
                        # split source_name
                        source_name = source_last[-1].rsplit('.', 1)
                        # if layer name and layer source are different, rename source
                        if l.name() != source_name[0]:
                            self.delete_vector_layer(l.source())
                            self.save_vector_layer(l)

                self.proj.write()
                # add temporal layers to proj
                for layer in temporal_layers:
                    self.proj.addMapLayer(layer)
                self.status_bar.showMessage("Project saved", 1500)
                self.config.settings['last_open_project'] = self.proj.fileName()
                self.config.save()

    def save_project_as(self):
        """
        Open a QfileDialog to save current project.

        """
        save = True
        if self.are_missions_modified():
            reply = QMessageBox.question(self, 'Save project',
                                          "You are about to save the project with some unsaved missions. "
                                          "If you proceed the unsaved missions changes will be lost. Do you want to continue?",
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                save = False

        if save:
            filename = QFileDialog.getSaveFileName(self, 'Save Project', "", '*.qgs')
            if filename[0] != '':

                if not filename[0].endswith('.qgs'):
                    self.proj.setFileName(filename[0] + '.qgs')
                else:
                    self.proj.setFileName(filename[0])
                self.save_project(True)

    def save_vector_layer(self, layer):
        """
        Save a vector layer in the current project.

        :param layer: layer to save

        """
        # if it is a vector layer and has a valid geometry and layer is not a mission
        if (layer.type() == 0) and (layer.geometryType() not in [3, 4]) and \
                (layer.customProperty("mission_xml") is None) and \
                (layer.customProperty("ned_origin") is None):
            if not os.path.exists(os.path.dirname(self.proj.fileName()) + '/layers/'):
                os.mkdir(os.path.dirname(self.proj.fileName()) + '/layers/')
            layer_name = os.path.dirname(self.proj.fileName()) + '/layers/' + layer.name() + '.shp'
            ret = QgsVectorFileWriter.writeAsVectorFormat(layer,
                                                          layer_name,
                                                          "utf-8",
                                                          QgsCoordinateReferenceSystem(4326,
                                                                                       QgsCoordinateReferenceSystem.EpsgCrsId),
                                                          "ESRI Shapefile")
            if ret == QgsVectorFileWriter.NoError:
                logger.info(layer.name() + " saved to " + layer_name)
            # After saving always delete layer and reload from saved file
            renderer = layer.renderer()
            file_info = QFileInfo(layer_name)
            base_name = file_info.baseName()

            vlayer = QgsVectorLayer(layer_name, base_name, "ogr")
            if not vlayer.isValid():
                logger.info("Failed to load layer!")
            vlayer.setRenderer(renderer.clone())
            self.proj.removeMapLayer(layer)
            self.proj.addMapLayer(vlayer)

    def delete_vector_layer(self, file_name):
        """
        Delete a vector layer of the current project.

        :param file_name: name of the layer

        """

        # delete shapefile. *.dbf, *.prj, *.qpj, *.shp, *.shx extensions
        QgsVectorFileWriter.deleteShapeFile(file_name)
        if file_name.endswith('.shp'):
            # split fileName and extension
            file_name = file_name[:-4]
            # join fileName and .cpg
            cpg_file = file_name + ".cpg"
            # remove file
            if os.path.isfile(cpg_file):
                os.remove(cpg_file)

    def zoom_in(self):
        """
        Set 'zoom in' as a current tool.

        """

        self.map_tool_change()
        self.canvas.setMapTool(self.tool_zoom_in)

    def zoom_out(self):
        """
        Set 'zoom out' as a current tool.

        """
        self.map_tool_change()
        self.canvas.setMapTool(self.tool_zoom_out)

    def pan(self):
        """
        Set 'pan' as a current tool.

        """
        self.map_tool_change()
        self.canvas.setMapTool(self.tool_pan)

    def show_xy(self, p):
        """
        Set point as text to display in self.label_xy.

        :param p: point
        :type: p: QgsPointXY

        """
        coordinate_format = self.config.csettings['coordinate_format']
        if coordinate_format == "degree_minute":
            x, y = degree_to_degree_minute(p.x(), p.y())

        elif coordinate_format == "degree_minute_second":
            x, y = degree_to_degree_minute_second(p.x(), p.y())
        else:
            x = p.x()
            y = p.y()

        # Show coordinates
        self.label_xy.setText(str(y) + " , " + str(x))

    def show_scale(self, scale):
        """
        Show scale.

        :param scale: current scale
        :type: float

        """

        self.scale_widget.setScale(scale)

    def on_scale_changed(self):
        """ Set scale on canvas. """
        self.canvas.zoomScale(self.scale_widget.scale())

    def on_rotation_changed(self, rot):
        """
        Set new rotation 'rot'.

        :param rot: rotation of the canvas
        :type: float

        """
        if rot == 360.0 or rot == -360.0:
            self.rotate_widget.setValue(0)

        self.canvas.setRotation(rot)
        self.canvas.refresh()

    def map_tool_change(self):
        """Uncheck a conflicting tool that may be set as maptool"""
        if type(self.canvas.mapTool()) == self.mission_ctrl.get_edit_wp_mission_tool():
            self.canvas.mapTool().hide_point_cursor_band()
        if self.canvas.mapTool() == self.point_feature.tool_add_landmark:
            self.add_landmark_point_action.setChecked(False)
        if self.canvas.mapTool() == self.tool_measure_distance:
            self.measure_distance_action.setChecked(False)
            self.tool_measure_distance.reset()
        if self.canvas.mapTool() == self.tool_measure_angle:
            self.measure_angle_action.setChecked(False)
            self.tool_measure_angle.reset()
        if self.canvas.mapTool() == self.tool_move_landmark:
            self.move_landmark_point_action.setChecked(False)
        if self.canvas.mapTool() == self.tool_measure_area:
            self.measure_area_action.setChecked(False)
            self.tool_measure_area.reset()

    def measure_distance(self):
        """
        Set 'measure' as a current tool.

        """
        self.map_tool_change()
        if self.measure_distance_action.isChecked():
            self.canvas.setMapTool(self.tool_measure_distance)
        else:
            self.pan()

    def measure_angle(self):
        """
        Set 'measure angle' as a current tool.

        """
        self.map_tool_change()
        if self.measure_angle_action.isChecked():
            self.canvas.setMapTool(self.tool_measure_angle)
        else:
            self.pan()

    def measure_area(self):
        """
        Set 'measure area' as a current tool.

        """
        self.map_tool_change()
        if self.measure_area_action.isChecked():
            self.canvas.setMapTool(self.tool_measure_area)
        else:
            self.pan()

    def change_menu_tool(self, action):
        """ change the measure tool from qtoolbutton"""
        sender = self.sender()
        sender.setDefaultAction(action)


    def init_layer_treeview(self):
        """
        Initialize layer tree view.

        """

        self.root = self.proj.layerTreeRoot()
        self.root.visibilityChanged.connect(self.change_mission_markers_visibility)
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)
        self.view = QgsLayerTreeView(self)
        self.view.setModel(self.model)
        self.legend_dock.setWidget(self.view)
        self.menu_provider = menuprovider.MenuProvider(self.view, self.canvas, self.proj)
        self.view.setMenuProvider(self.menu_provider)
        self.view.currentNode().nameChanged.connect(self.set_mission_modified)
        self.canvas.zoomToFullExtent()
        self.canvas.show()

        # self.view.currentLayerChanged.connect(self.layer_changed)
        self.proj.layerWillBeRemoved[QgsMapLayer].connect(self.layer_will_be_removed)
        self.model.dataChanged.connect(self.layer_changed)

    def add_layer(self):
        """ Open AddLayers Dialog"""
        addlayer = addlayers.AddLayersDlg(self.proj, self.canvas, self.msg_log)
        result = addlayer.exec_()

    def add_landmark_point(self):
        """ Set 'Add Landmark' as a current tool."""
        self.map_tool_change()

        if self.add_landmark_point_action.isChecked():
            self.point_feature.reset()
            self.point_feature.show()
        else:
            self.pan()

    def move_landmark_point(self):
        """ Set 'Move Landmark' as a current tool."""
        self.map_tool_change()
        if self.move_landmark_point_action.isChecked():
            self.tool_move_landmark.set_landmark_layer(self.view.currentLayer())
            self.canvas.setMapTool(self.tool_move_landmark)
        else:
            self.pan()

    def finish_add_landmark(self):
        """ Uncheck add_landmark action and set pan as maptool"""
        self.add_landmark_point_action.setChecked(False)
        self.pan()

    def layer_changed(self):
        """ If layer changed, set as a current layer."""
        layer = self.view.currentLayer()
        if layer.type() == QgsMapLayer.VectorLayer:
            if self.is_mission_layer(layer):
                self.activate_mission_tools(True)
                self.move_landmark_point_action.setEnabled(False)
                # if is a mission layer set corresponding mt to current mission track in mission controller
                self.mission_ctrl.set_current_mission(layer)
                self.mission_ctrl.set_current_mission_name(layer.name())
                self.mission_ctrl.set_current_mission_filename(layer.name())

            elif self.is_single_point_layer(layer) and (layer.dataProvider().storageType() == "ESRI Shapefile"
                                                        or layer.dataProvider().storageType() == "Memory storage"):
                # only layers that are not missions, in .shp format or in memory and with only one point will be moved
                self.activate_mission_tools(False)
                self.move_landmark_point_action.setEnabled(True)

            else:
                self.activate_mission_tools(False)
                self.move_landmark_point_action.setEnabled(False)
        else:
            self.activate_mission_tools(False)
            self.move_landmark_point_action.setEnabled(False)

    def is_mission_layer(self, layer):
        """
        check if layer is a mission.

        :param layer:
        :return: return boolean
        """
        if layer is None:
            return False
        elif layer.customProperty("mission_xml") is None:
            return False
        else:
            return True

    def is_single_point_layer(self, layer):
        """
        check if layer has only one point
        :param layer:
        :return: return boolean
        """
        if layer is None:
            return False
        elif layer.featureCount() == 1:
            feature_it = layer.dataProvider().getFeatures()
            feature = next(feature_it, None)
            if feature is not None:
                if feature.geometry().wkbType() == QgsWkbTypes.Point:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def layer_will_be_removed(self, layer):
        """
        Remove layer.

        :param layer: layer

        """

        logger.info("Removing layer {}".format(layer.name()))
        if self.is_mission_layer(layer):
            self.mission_ctrl.remove_mission(layer)

    def failed_layers(self, layers):
        """
        Called when layers have failed to load from the current project
        """
        logger.info("Error while loading layers")
        for layer in layers:
            self.msg_log.logMessage("Failed to load layer " + layer, "LoadingProjectLayers", 1)

    def msgbar_catcher(self, msg, tag, level):
        """
        Called when info/warning/error messages are logged to show them in the message bar
        """
        # Disconnect temporaly the messageReceived signal to avoid loops from messages generated
        # when pushing a message to the msgbar.

        self.msg_log.messageReceived.disconnect(self.msgbar_catcher)
        if level <=2:
            self.change_msg(self.msg_bar, msg, tag, level)
        else:
            self.change_msg(self.vehicle_msg_bar, msg, tag, level)
        self.msg_log.messageReceived.connect(self.msgbar_catcher)


    def change_msg(self,msg_bar, msg, tag, level):
        if msg == "":
            msg_bar.clearWidgets()
        else:
            if level == 0:
                msg_bar.pushItem(QgsMessageBarItem("Info: ", msg, Qgis.Info, 0, self.centralwidget))
            elif level == 1:
                msg_bar.pushItem(QgsMessageBarItem("Warning: ", msg, Qgis.Warning, 0, self.centralwidget))
            elif level == 2:
                msg_bar.pushItem(QgsMessageBarItem("Error: ", msg, Qgis.Critical, 0, self.centralwidget))
            elif level == 3:
                if (msg_bar.currentItem() is None
                        or (msg != msg_bar.currentItem().text()
                            and msg_bar.currentItem().level() != Qgis.Critical)):
                    msg_bar.pushItem(QgsMessageBarItem("Warning: ", msg, Qgis.Warning, 0, self.centralwidget))
            elif level == 4:
                if msg_bar.currentItem() is None or msg != msg_bar.currentItem().text():
                    msg_bar.pushItem(QgsMessageBarItem("Status Code: ", msg, Qgis.Critical, 0, self.centralwidget))
            elif level == 5:
                if msg_bar.currentItem() is None or msg != msg_bar.currentItem().text():
                    msg_bar.pushItem(QgsMessageBarItem("Error Code: ", msg, Qgis.Critical, 0, self.centralwidget))
            elif level == 6:
                if msg_bar.currentItem() is None or msg != msg_bar.currentItem().text():
                    msg_bar.pushItem(QgsMessageBarItem("Recovery Action: ", msg, Qgis.Critical, 0, self.centralwidget))


    def edit_options(self):
        """ Open Options Dialog."""
        od = options.OptionsDlg(self.config, self.vehicle_info)
        od.exec_()

    def connection_settings(self):
        """ Open Connection Settings Dialog."""
        csd = connectionsettings.ConnectionSettingsDlg(self.config, self.vehicle_info)
        csd.exec_()

    def checklist(self):
        """ Open a Checklist selector Dialog."""
        try:
            cl_selectord = check_list_selector.ChecklistSelectorDlg(self.config)
            result = cl_selectord.exec_()
            if result == QDialog.Accepted:
                cld = check_list.read_configuration(self.vehicle_info,
                                                    self.config,
                                                    cl_selectord.get_current_check_list())
        except:
            logger.error("Connection with COLA2 could not be established")
            QMessageBox.critical(self,
                                 "Connection with AUV Failed",
                                 "Connection with COLA2 could not be established",
                                 QMessageBox.Close)

    def launch_teleoperation(self):
        """ Launch a teleoperation."""
        if self.joystick_teleop_action.isChecked():

            launch_command = self.vehicle_data.get_teleoperation_launch()
            # get vehicle ip
            ip = self.vehicle_info.get_vehicle_ip()
            # launch a subprocess to teleoperate robot with joystick
            launch = "ROS_MASTER_URI=http://" + ip + ":11311/ " + launch_command + " joystickDevice:=" + \
                     self.config.csettings['joystick_device']
            # launch teleoperation on background
            self.process_teleop = subprocess.Popen(launch, shell=True, executable="/bin/bash")
            self.joystick_teleop_action.setToolTip("Disable Joystick Teleoperation")
        else:
            self.terminate_teleoperation()

    def terminate_teleoperation(self):
        if self.process_teleop is not None:
            self.process_teleop.terminate()
            # wait to finish
            self.process_teleop.wait()
        self.joystick_teleop_action.setToolTip("Enable Joystick Teleoperation")
        self.joystick_teleop_action.setChecked(False)

    def reset_timeout(self):
        """ Reset Timeout."""
        self.timeout_widget.reset_timeout()

    def on_click_calibrate_magnetometer(self):
        """ Start calibrate magnetometer."""

        if self.calibrate_magnetometer_action.isChecked():
            confirmation_msg = "Are you sure you want to initiate the procedure to calibrate the magnetometer?\n\n" \
                               "The vehicle must be submerged and once you start, it will perform clockwise turns " \
                               "during 150 seconds followed by counterclockwise turns for another 150 seconds."
            reply = QMessageBox.question(self, 'Calibrate Confirmation',
                                         confirmation_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:

                calibrate = self.vehicle_data.get_calibrate_magnetometer_service()
                if calibrate is not None:
                    self.calibrate_magnetometer.start_calibrate_magnetometer()
                else:
                    QMessageBox.critical(self,
                                         "Calibrate Magnetometer error",
                                         "The service 'Calibrate Magnetometer' could not be sent.",
                                         QMessageBox.Close)

            else:
                self.calibrate_magnetometer_action.setChecked(False)
        else:
            stop_magnetometer_calibration = self.vehicle_data.get_stop_magnetometer_calibration_service()
            if stop_magnetometer_calibration is not None:
                self.calibrate_magnetometer.stop_magnetometer_calibration()

    def calibrate_magnetometer_result(self, result):
        """
        Calibrate Magnetometer result.

        :param result: calibrate magnetometer result

        """

        # receive calibrate magnetometer server status
        if not result:
            QMessageBox.critical(self,
                                 "Connection with AUV Failed",
                                 "Connection with COLA2 could not be established",
                                 QMessageBox.Close)
        self.calibrate_magnetometer_action.setChecked(False)

    def robot_monitor(self):
        """ Open rqt robot monitor."""

        if self.robot_monitor_action.isChecked():
            ip = self.vehicle_info.get_vehicle_ip()
            my_env = os.environ.copy()
            my_env["ROS_MASTER_URI"] = "http://" + ip + ":11311/"
            logger.info("ROS_MASTER_URI: {}".format(my_env["ROS_MASTER_URI"]))
            # command = "ROS_MASTER_URI=http://"+ ip + ":11311/" #rosrun rqt_robot_monitor rqt_robot_monitor"
            self.process_robot_monitor = subprocess.Popen(['rosrun',
                                                           'rqt_robot_monitor',
                                                           'rqt_robot_monitor',
                                                           'diagnostics_agg:='+self.vehicle_info.get_vehicle_namespace()+'/diagnostics_agg'],
                                                          env=my_env)  # shell=True,executable = "/bin/bash")
            self.robot_monitor_action.setToolTip("Close Robot Monitor")
            self.check_robot_monitor()
        else:
            if self.process_robot_monitor is not None:
                self.process_robot_monitor.terminate()
                # wait to finish
                self.process_robot_monitor.wait()
            self.robot_monitor_action.setToolTip("Open Robot Monitor")
            self.boat_pose_action.setChecked(False)

    def check_robot_monitor(self):
        """ Check if robot monitor is running."""

        # if exist robot monitor process
        if self.process_robot_monitor is not None:
            # timer to check state
            self.timer_robot_monitor = threading.Timer(3.0, self.check_robot_monitor).start()
            # if robot monitor process state is diferent to none and 0 or less
            if self.process_robot_monitor.poll() is not None and self.process_robot_monitor.poll() <= 0:
                # if exist timer
                if self.timer_robot_monitor:
                    self.timer_robot_monitor.cancel()
                # terminate robot monitor process
                self.process_robot_monitor.terminate()
                # wait to finish
                self.process_robot_monitor.wait()
                self.process_robot_monitor = None
                # change tip and uncheck action
                self.robot_monitor_action.setToolTip("Open Robot Monitor")
                self.robot_monitor_action.setChecked(False)

    def vehicle_widgets_visibility(self):
        """ Change vehicle widgets visibility."""

        if self.vehicle_widgets_action.isChecked():
            self.vehicle_w_dock.show()
        else:
            self.vehicle_w_dock.hide()

    def scale_bar_visibility(self):
        """
        Change Scale Bar visibility.
        """
        if self.scale_bar_action.isChecked():
            self.scale_bar.show()
        else:
            self.scale_bar.hide()
        self.canvas.refresh()
        self.config.settings['visibility_scale_bar'] = int(self.scale_bar_action.isChecked())
        self.config.save()

    def north_arrow_visibility(self):
        """
        Change North Arrow visibility.
        """
        if self.north_arrow_action.isChecked():
            self.north_arrow.show()
        else:
            self.north_arrow.hide()
        self.canvas.refresh()
        self.config.settings['visibility_north_arrow'] = int(self.north_arrow_action.isChecked())
        self.config.save()

    def set_decorations_visibility(self):
        """

        Set Decorations visibility
        """
        visibility_north_arrow = self.config.settings['visibility_north_arrow']
        visibility_scale_bar = self.config.settings['visibility_scale_bar']

        self.north_arrow_action.setChecked(visibility_north_arrow)
        self.scale_bar_action.setChecked(visibility_scale_bar)
        self.north_arrow_visibility()
        self.scale_bar_visibility()

    def connection_failed(self):
        """ Show connection failed message on status bar."""
        self.status_bar.showMessage("Connection failed", 1500)

    def process_changed(self, msg):
        """
        Show message msg on status bar.

        :param msg: message
        :type msg: string
        """
        self.status_bar.showMessage(msg, 1500)

    def auv_config_params(self):
        """ Open AUV Config Params dialog."""
        acpd = auvconfigparams.AUVConfigParamsDlg(self.config, self.vehicle_info)
        acpd.applied_changes.connect(self.timeout_widget.set_timeout)
        try:
            acpd.init()
            acpd.exec_()
            self.ned_origin_drawer.update_ned_point()
        except:
            logger.error("Connection with COLA2 could not be established")
            QMessageBox.critical(self,
                                 "Connection with AUV Failed",
                                 "Connection with COLA2 could not be established",
                                 QMessageBox.Close)

    def show_boat_pose(self):
        """ Show boat pose."""
        if self.boat_pose_action.isChecked():
            self.create_gps_dockwidget()
            self.gps_pose = gpswidget.GPSWidget(self.canvas, self.config)
            self.gps_pose.setAttribute(Qt.WA_DeleteOnClose)
            self.gps_dw.setWidget(self.gps_pose)
            self.gps_dw.show()
            self.gps_pose.connect()
            self.boat_pose_action.setToolTip("Hide Vessel Pose")
        else:
            self.disconnect_gps_dw()
            self.gps_dw.close()
            self.gps_dw = None
            self.boat_pose_action.setToolTip("Show Vessel Pose")

    def show_auv_pose(self):
        """ Show AUV pose."""
        if self.auv_pose_action.isChecked():
            # Dock for AUV Position
            self.create_auv_position_dockwidget()
            self.auv_pose = auvposewidget.AUVPoseWidget(self.canvas, self.vehicle_info, self.vehicle_data,
                                                        self.mission_sts)
            # set WA_DeleteOnClose attribute no destroy widget on close
            self.auv_pose.setAttribute(Qt.WA_DeleteOnClose)
            self.auvp_dw.setWidget(self.auv_pose)
            self.auvp_dw.show()
            self.auv_pose.auv_wifi_connected.connect(self.auv_wifi_connected)
            self.auv_pose.emit_connection()
            self.auv_pose_action.setToolTip("Hide AUV Monitoring")
        else:
            # function close() call function destroy() on self.auvpw (qdockwidget)
            # because the widget has attribute Qt.WA_DeleteOnClose
            # and destroyed signal is connected with disconnectAUVpw()
            self.disconnect_auvp_dw()
            self.auvp_dw.close()
            self.auvp_dw = None
            self.auv_pose_action.setToolTip("Show AUV Monitoring")

    def vehicle_widgets_dock_visibility_changed(self):
        """ Change vehicle widgets dock visibility."""
        if self.vehicle_w_dock.isHidden():
            self.vehicle_widgets_action.setChecked(False)
            self.resources_action.setEnabled(False)
            self.compass_action.setEnabled(False)
            self.depth_altitude_action.setEnabled(False)
            self.roll_pitch_action.setEnabled(False)
            self.velocimeter_action.setEnabled(False)
            self.table_action.setEnabled(False)
            self.setpoints_action.setEnabled(False)
        else:
            self.vehicle_widgets_action.setChecked(True)
            self.resources_action.setEnabled(True)
            self.compass_action.setEnabled(True)
            self.depth_altitude_action.setEnabled(True)
            self.roll_pitch_action.setEnabled(True)
            self.velocimeter_action.setEnabled(True)
            self.table_action.setEnabled(True)
            self.setpoints_action.setEnabled(True)

    def log_dock_visibility_changed(self):
        """ Change log action check."""
        if self.log_dock.isHidden():
            self.log_action.setChecked(False)
        else:
            self.log_action.setChecked(True)

    def open_log(self):
        """ Change log dock visibility """
        if self.log_dock.isHidden():
            self.log_dock.setFloating(True)
            self.log_dock.show()
        else:
            self.log_dock.hide()

    def layers_dock_visibility_changed(self):
        """Change layers action check"""
        if self.legend_dock.isHidden():
            self.legend_action.setChecked(False)
        else:
            self.legend_action.setChecked(True)

    def open_legend(self):
        """ Change layers legend dock visibility """
        if self.legend_dock.isHidden():
            self.legend_dock.show()
        else:
            self.legend_dock.hide()

    def enable_keep_position(self):
        """ Change keep position status."""

        ip = self.vehicle_info.get_vehicle_ip()
        port = 9091
        vehicle_namespace = self.vehicle_info.get_vehicle_namespace()
        if self.keep_position_status.get_keep_position_enabled():
            #back compatibility
            if self.keep_position_status.is_old_version():
                disable_keep_position = self.vehicle_data.get_disable_keep_position_service()
            else:
                disable_keep_position = self.vehicle_data.get_disable_all_keep_positions_service()

            if disable_keep_position is not None:
               response = cola2_interface.send_trigger_service(ip, port,
                                                               vehicle_namespace+disable_keep_position)
               try:
                   if not response['values']['success']:
                       QMessageBox.critical(self,
                                            "Disable keep position failed",
                                            response['values']['message'],
                                            QMessageBox.Close)
                       self.change_icon_keep_position()
               # back compatibility
               except Exception as e:
                   logger.warning("Disable keep position response can not be read")
            else:
                QMessageBox.critical(self,
                                     "Keep Position error",
                                     "The service 'Disable Keep Position' could not be sent.",
                                     QMessageBox.Close)
                self.change_icon_keep_position()
        else:
            keep_position = self.vehicle_data.get_keep_position_service()
            if keep_position is not None:
                response = cola2_interface.send_trigger_service(ip, port,
                                                                vehicle_namespace+keep_position)
                try:
                    if not response['values']['success']:
                        QMessageBox.critical(self,
                                             "Enable keep position failed",
                                             response['values']['message'],
                                             QMessageBox.Close)
                        self.change_icon_keep_position()
                # back compatibility
                except Exception as e:
                    logger.warning("Enable keep position response can not be read")
            else:
                QMessageBox.critical(self,
                                     "Keep Position error",
                                     "The service 'Keep Position' could not be sent.",
                                     QMessageBox.Close)
                self.change_icon_keep_position()

    def change_icon_keep_position(self):
        """ change keep position icon."""
        if self.keep_position_status.get_keep_position_enabled():
            icon = QIcon(":resources/mActionDisableKeepPosition.svg")
            self.enable_keep_position_action.setToolTip("Disable Keep Position")
            self.enable_keep_position_action.setChecked(True)
        else:
            icon = QIcon(":resources/mActionEnableKeepPosition.svg")
            self.enable_keep_position_action.setToolTip("Enable Keep Position")
            self.enable_keep_position_action.setChecked(False)
            self.msg_log.logMessage("", "Keep position", 3)


        self.enable_keep_position_action.setIcon(icon)

    def disable_thrusters(self):
        """ Change thrusters status."""
        ip = self.vehicle_info.get_vehicle_ip()
        port = 9091
        vehicle_namespace = self.vehicle_info.get_vehicle_namespace()
        # if self.actionDisableThrusters.isChecked():
        if self.thrusters_status.get_thrusters_enabled():
            disable_thrusters = self.vehicle_data.get_disable_thrusters_service()
            if disable_thrusters is not None:
                cola2_interface.send_empty_service(ip, port,
                                                   vehicle_namespace + disable_thrusters)
            else:
                QMessageBox.critical(self,
                                     "Disable thrusters error",
                                     "The service 'Disable Thrusters' could not be sent.",
                                     QMessageBox.Close)

        else:
            enable_thrusters = self.vehicle_data.get_enable_thrusters_service()
            if enable_thrusters is not None:
                cola2_interface.send_empty_service(ip, port,
                                                   vehicle_namespace + enable_thrusters)
                #/girona500/controller/enable_thrusters
            else:
                QMessageBox.critical(self,
                                     "Enable thrusters error",
                                     "The service 'Enable Thrusters' could not be sent.",
                                     QMessageBox.Close)

    def change_icon_thrusters(self):
        """ Change thrusters icon."""
        # if self.actionDisableThrusters.isChecked():
        if self.thrusters_status.get_thrusters_enabled():
            icon = QIcon(":resources/mActionDisableThrusters.svg")
            self.disable_thrusters_action.setToolTip("Disable Thrusters")
            self.disable_thrusters_action.setChecked(False)

        else:
            icon = QIcon(":resources/mActionEnableThrusters.svg")
            self.disable_thrusters_action.setToolTip("Enable Thrusters")
            self.disable_thrusters_action.setChecked(True)

        self.disable_thrusters_action.setIcon(icon)

    def auv_wifi_connected(self, connected):
        """
        Start connection with AUV

        :param connected: conection with AUV
        :type connected:  bool
        """
        if connected:
            self.subscribe_topics()

            if self.vehicle_data.is_subscribed():
                self.auv_on_wifi = True
                self.enable_keep_position_action.setEnabled(True)
                self.disable_thrusters_action.setEnabled(True)
                self.goto_action.setEnabled(True)
                self.execute_mission_action.setEnabled(True)
                self.reset_timeout_action.setEnabled(True)
                self.vehicle_widgets_action.setEnabled(True)
                self.ned_origin_drawer.update_ned_point()
                # self.ned_origin_drawer.update_ned_point()
                # self.mission_sts.mission_started.connect(self.mission_started_wifi)
                # self.mission_sts.mission_stopped.connect(self.mission_stopped_wifi)
                self.vehicle_w_dock.show()

        else:
            self.auv_on_wifi = False
            self.enable_keep_position_action.setEnabled(False)
            self.disable_thrusters_action.setEnabled(False)
            self.goto_action.setEnabled(False)
            self.execute_mission_action.setEnabled(False)
            self.reset_timeout_action.setEnabled(False)
            self.vehicle_widgets_action.setEnabled(False)
            # self.mission_sts.mission_started.disconnect()
            # self.mission_sts.mission_stopped.disconnect()
            self.disconnect_objects()

            self.vehicle_w_dock.hide()

    def activate_mission_tools(self, activate):
        """
        Change mission tools enable.

        :param activate: is mission tools activaded
        :type activate: bool
        """

        if activate:
            self.save_mission_action.setEnabled(True)
            self.saveas_mission_action.setEnabled(True)
            self.edit_wp_mission_action.setEnabled(True)
            self.select_features_mission_action.setEnabled(True)
            self.send_mission_action.setEnabled(True)
            self.move_mission_action.setEnabled(True)
            self.template_mission_action.setEnabled(True)
            if self.auv_on_wifi:
                self.execute_mission_action.setEnabled(True)
        else:
            self.save_mission_action.setEnabled(False)
            self.saveas_mission_action.setEnabled(False)
            self.edit_wp_mission_action.setEnabled(False)
            self.select_features_mission_action.setEnabled(False)
            self.send_mission_action.setEnabled(False)
            self.move_mission_action.setEnabled(False)
            self.template_mission_action.setEnabled(False)

    def new_mission(self):
        """ Create new mission."""
        if self.proj.fileName() is "":
            reply = QMessageBox.warning(None, "No opened project",
                                        "You do not have any project open to create the mission. \n Open a project or save the current one.")
        else:
            self.disable_mission_editing()
            self.mission_ctrl.new_mission()

    def save_mission(self):
        """ Save current mission."""
        self.disable_mission_editing()

        # check if missions folder is exisiting:
        if not os.path.exists(os.path.dirname(self.proj.fileName()) + '/missions/'):
            os.mkdir(os.path.dirname(self.proj.fileName()) + '/missions/')

        try:
            saved = self.mission_ctrl.save_mission()
            if saved:
                QMessageBox.information(self,
                                        "Mission saved",
                                        "Mission file saved in {}".format(
                                            self.mission_ctrl.get_current_mission_filename()),
                                        QMessageBox.Close)
        except Exception as e:
            logger.error("Mission file could not be saved.")
            QMessageBox.critical(self,
                                 e.args[0],
                                 "Mission file could not be saved.",
                                 QMessageBox.Close)

    def saveas_mission(self):
        """ Save current mission."""
        self.disable_mission_editing()

        # check if missions folder is exisiting:
        if not os.path.exists(os.path.dirname(self.proj.fileName()) + '/missions/'):
            os.mkdir(os.path.dirname(self.proj.fileName()) + '/missions/')

        try:
            saved, mission_filename = self.mission_ctrl.saveas_mission()
            if saved:
                QMessageBox.information(self,
                                        "Mission saved",
                                        "Mission file saved in {}".format(
                                            mission_filename),
                                        QMessageBox.Close)
        except Exception as e:
            logger.error("Mission file could not be saved.")
            QMessageBox.critical(self,
                                 e.args[0],
                                 "Mission file could not be saved.",
                                 QMessageBox.Close)

    def load_mission(self):
        """ Load a mission."""
        if self.proj.fileName() is "":
            reply = QMessageBox.warning(None, "No opened project",
                                        "You do not have any project open to load the mission. \n Open a project or save the current one.")

        else:
            self.disable_mission_editing()
            filename = QFileDialog.getOpenFileName(self, 'Load Mission', "", '*.xml')
            if filename[0]:
                try:
                    self.mission_ctrl.load_mission(filename[0])
                except Exception as e:
                    logger.error("Mission file could not be saved.")
                    QMessageBox.critical(self,
                                         e.args[0],
                                         "Mission file could not be loaded, make sure is a valid mission file.",
                                         QMessageBox.Close)

    def edit_wp_mission(self):
        """ Allows edition of waypoint mission. """
        self.map_tool_change()

        if self.edit_wp_mission_action.isChecked():
            # uncheck others tools
            self.check_mission_edit_tools('editwp')
            # hide current mission layer
            self.view.currentNode().setItemVisibilityChecked(False)
            self.mission_ctrl.edit_wp_mission()
        else:
            self.mission_ctrl.finish_edit_wp_mission()
            self.view.currentNode().setItemVisibilityChecked(True)

            self.pan()

    def select_features_mission(self):
        """ Allows select features mission. """
        self.map_tool_change()

        if self.select_features_mission_action.isChecked():
            # uncheck others tools
            self.check_mission_edit_tools('selectfeatures')
            self.mission_ctrl.select_features_mission()

        else:
            self.mission_ctrl.finish_select_features_mission()
            self.pan()

    def add_template_mission(self):
        """ Allows add template in  mission."""

        self.map_tool_change()

        if self.template_mission_action.isChecked():
            self.check_mission_edit_tools('template')
            self.mission_ctrl.add_template_mission()
        else:
            if self.mission_ctrl.is_template_modified():
                reply = QMessageBox.question(self,
                                             "Template track not saved to mission",
                                             "Template Tracks were not saved to mission. Do you want to save them before closing template edition?",
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.mission_ctrl.save_template_tracks_to_mission()

            self.mission_ctrl.close_template_editing()

    def are_missions_modified(self):
        """
        Get missions modified state
        :return: return True if a mission has been modified, otherwise False
        """
        missions_are_modified = False
        for mission in self.mission_ctrl.get_mission_list():
            if mission.is_modified():
                missions_are_modified = True

        return missions_are_modified

    def set_mission_modified(self):
        """ Set modified state of the current mission layer to True"""
        if self.view.currentLayer().customProperty("mission_xml") is not None:
            self.mission_ctrl.get_current_mission().set_modified(True)

    def add_map_layer(self, layer):
        """
        Add layer to  the current project, view and canvas

        :param layer: layer
        """
        self.proj.addMapLayer(layer, True)
        self.view.setCurrentLayer(layer)
        self.canvas.refresh()

    def remove_map_layer(self, layer):
        """
         Remove layer of current project, view and canvas

         :param layer: layer
         """
        self.proj.removeMapLayer(layer)
        self.canvas.refresh()

    def move_mission(self):
        """ Allows to move the mission."""

        self.map_tool_change()

        if self.move_mission_action.isChecked():
            self.check_mission_edit_tools('move')
            self.view.currentNode().setItemVisibilityChecked(True)
            self.mission_ctrl.move_mission()
        else:
            self.pan()

    def disable_mission_editing(self):
        """
        closes any mission editing mode open
        """
        # check if we were editing something, first close template edition if existing as this resorts to wp editing
        if self.template_mission_action.isChecked():
            self.template_mission_action.setChecked(False)
        if self.edit_wp_mission_action.isChecked():
            self.edit_wp_mission_action.setChecked(False)
        if self.move_mission_action.isChecked():
            self.move_mission_action.setChecked(False)
        if self.select_features_mission_action.isChecked():
            self.select_features_mission_action.setChecked(False)

    def change_icon_mission(self):
        """ Change icon of the self.execute_mission_action"""
        if self.mission_active.get_mission_active():
            icon = QIcon(":resources/mActionStopMission.svg")
            self.execute_mission_action.setToolTip("Stop Mission")
            self.execute_mission_action.setChecked(True)
        else:
            self.execute_mission_action.setToolTip("Execute Mission")
            icon = QIcon(":resources/mActionExecuteMission.svg")
            self.execute_mission_action.setChecked(False)
        self.execute_mission_action.setIcon(icon)

    def execute_mission(self):
        """ Execute the last mission sent to the AUV. """
        ip = self.vehicle_info.get_vehicle_ip()
        port = 9091
        vehicle_namespace = self.vehicle_info.get_vehicle_namespace()

        if self.execute_mission_action.isChecked():
            if (not self.disable_thrusters_action.isChecked()) \
                    and (not self.enable_keep_position_action.isChecked()):
                if self.joystick_teleop_action.isChecked():
                    logger.info("Stopping joystick connection")
                    self.terminate_teleoperation()

                enable_mission = self.vehicle_data.get_enable_mission_service()

                if enable_mission is not None and self.check_disk_capacity():

                        response = cola2_interface.send_trigger_service(ip, port,
                                                            vehicle_namespace + enable_mission)
                        try:
                            if not response['values']['success']:
                                QMessageBox.critical(self,
                                                     "Execute mission failed",
                                                     response['values']['message'],
                                                     QMessageBox.Close)
                                self.change_icon_mission()

                        # back compatibility
                        except Exception as e:
                            logger.warning("The execute mission service response can not be read")
                else:
                    self.execute_mission_action.setChecked(False)
                    QMessageBox.critical(self,
                                         "Enable mission error",
                                         "The service 'Enable mission' could not be sent.",
                                         QMessageBox.Close)

                # self.mission_sts.start_check_mission_start()
            else:
                self.execute_mission_action.setChecked(False)
                # thrusters disabled
                if self.disable_thrusters_action.isChecked():
                    QMessageBox.warning(self,
                                        "Mission start",
                                        "Mission cannot start. Thrusters are disabled.",
                                        QMessageBox.Close)
                # keep position enabled
                else:
                    QMessageBox.warning(self,
                                        "Mission start",
                                        "Mission cannot start. Keep position are enabled.",
                                        QMessageBox.Close)

        else:
            disable_mission = self.vehicle_data.get_disable_mission_service()
            if disable_mission is not None:
                response = cola2_interface.send_trigger_service(ip, port,
                                                                vehicle_namespace + disable_mission)
                try:
                    if not response['values']['success']:
                        QMessageBox.critical(self,
                                             "Disable mission failed",
                                             response['values']['message'],
                                             QMessageBox.Close)
                        self.change_icon_mission()

                # back compatibility
                except Exception as e:
                    logger.warning("The disable mission response can not be read")
                #/girona500/captain/disable_mission
            else:
                QMessageBox.critical(self,
                                     "Disable mission error",
                                     "The service 'Disable mission' could not be sent.",
                                     QMessageBox.Close)
            # self.mission_sts.start_check_mission_stop()

    def mission_started_wifi(self):
        """ Set StopMission icon to self.execute_mission_action"""
        logger.info("Mission started")
        icon = QIcon(":resources/mActionStopMission.svg")
        self.execute_mission_action.setIcon(icon)
        # self.actionExecuteMission.setChecked(True)

    def mission_stopped_wifi(self):
        """ Set ExecuteMission icon to self.execute_mission_action"""
        logger.info("Mission stopped")
        icon = QIcon(":resources/mActionExecuteMission.svg")
        self.execute_mission_action.setIcon(icon)
        self.execute_mission_action.setChecked(False)

    def check_mission_edit_tools(self, current):
        """
        The mission edit tools different from the current will be False.


        :param current: current edit tool
        :type current: string
l
        """
        if current == 'move':
            self.edit_wp_mission_action.setChecked(False)
            self.select_features_mission_action.setChecked(False)
            if self.template_mission_action.isChecked():
                self.template_mission_action.setChecked(False)
            self.move_mission_action.setChecked(True)
        elif current == 'editwp':
            self.move_mission_action.setChecked(False)
            self.template_mission_action.setChecked(False)
            self.select_features_mission_action.setChecked(False)
            self.edit_wp_mission_action.setChecked(True)
        elif current == 'template':
            self.move_mission_action.setChecked(False)
            self.edit_wp_mission_action.setChecked(False)
            self.select_features_mission_action.setChecked(False)
            self.template_mission_action.setChecked(True)
        elif current == 'selectfeatures':
            self.move_mission_action.setChecked(False)
            self.edit_wp_mission_action.setChecked(False)
            if self.template_mission_action.isChecked():
                self.template_mission_action.setChecked(False)
            self.select_features_mission_action.setChecked(True)

    def template_closed(self):
        """ Uncheck Template Mission Action and Check Edit Wp Mission Action"""
        self.template_mission_action.setChecked(False)
        self.edit_wp_mission_action.setChecked(True)

    def send_mission_to_auv(self):
        """ Send mission to AUV"""
        self.mission_ctrl.send_mission_to_auv()

    def goto(self):
        """ Show goto dialog."""
        ip = self.vehicle_info.get_vehicle_ip()
        port = 9091
        if self.goto_action.isChecked():
            self.goto_action.setChecked(False)
            # set ip and port
            self.goto_dialog.set_ip(ip)
            self.goto_dialog.set_port(port)
            # show go to dialog
            self.goto_dialog.show()
        else:
            # on actionGoTo uncheck
            # disable goto
            self.goto_dialog.disable_goto()

            # restart default icon
            icon = QIcon(":resources/goto.svg")
            self.goto_action.setIcon(icon)

    def change_icon_goto(self):
        """
        Set icon depending goto status
        :param going: goto status
        :return: bool
        """
        going = self.goto_dialog.is_going()
        if self.goto_dialog.is_going():
            icon = QIcon(":resources/stopGoto.svg")
        else:
            icon = QIcon(":resources/goto.svg")

        self.goto_action.setChecked(going)
        self.goto_action.setIcon(icon)

    def change_toolbar_visibility(self, toolbar):
        """
        Change toolbar visibility

        :param toolbar: toolbar
        """
        sender = self.sender()
        if sender.isChecked():
            toolbar.setVisible(True)
        else:
            toolbar.setVisible(False)

    def change_mission_markers_visibility(self, treelayer):
        """
        change start end vertex markers
        :param treelayer:
        """
        if self.is_mission_layer(treelayer.layer()):
            mission_list = self.mission_ctrl.get_mission_list()
            for mt in mission_list:
                if mt.get_mission_layer() == treelayer.layer():
                    if not treelayer.isVisible():
                        mt.hide_start_end_markers()
                    else:
                        mt.update_start_end_markers()

    def subscribe_topics(self):
        """
        subscribe topics and call function to refresh data
        """
        self.vehicle_data.subscribe_topics()

        if self.vehicle_data.is_subscribed():

            self.bw = busywidget.BusyWidget(title="Subscribing to the topics...")
            self.bw.on_start()
            self.bw.exec_()

            self.auv_pose.connect()
            self.timeout_widget.connect()
            self.thrusters_status.update_thrusters_status()
            self.mission_active.update_mission_status()
            self.keep_position_status.update_keep_position_status()
            self.goto_dialog.update_goto_status()
            self.vehicle_widgets.connect()
            self.log_widget.connect()

        else:
            self.auv_pose.disconnect()
            self.disconnect_objects()

    def coordinate_converter(self):
        """ Open Coordinate Converter dialog"""
        coord_converter = CoordinateConverterDialog()
        coord_converter.exec_()

    def vessel_pos_system(self):
        """ Open vessel pos system """
        vessel_pos_system = vesselpossystem.VesselPositionSystem(config=self.config)
        result = vessel_pos_system.exec_()
        if result == QDialog.Accepted:
            if self.gps_pose is not None:
                self.gps_pose.update_width_and_length()
            if util.find_spec('usblcontroller') is not None:
                usbl_widget = self.plugin_manager.get_usbl().get_usbl_widget()
                if usbl_widget is not None:
                    usbl_widget.update_width_and_length()

    def enable_boat_pose_action(self):
        """ Enable boat pose action."""
        if self.boat_pose_action is not None:
            logger.info("enabling boat pose action")
            self.boat_pose_action.setEnabled(True)

    def check_disk_capacity(self):
        """
        check the auv disk capacity
        :return: return True if (used disk)<75 or the user wants to continue, otherwise False
        """
        try:
            user = self.vehicle_info.get_vehicle_user()
            server = self.vehicle_info.get_vehicle_ip()

            disk_usage_command = "ssh " + "{}@{}".format(user,
                                                         server) + " df --total  | grep total | grep -"
            ps = subprocess.Popen(disk_usage_command, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
            output = ps.communicate()[0].decode()
            for line in output.split('\n'):
                if "total" in line:
                    values = line.split()
                    free_space = values[3]
                    disk_usage, __ = values[4].split('%')

                    free_space_gb = int(free_space) / (1024*1024)

                    if int(disk_usage) > 75:
                        reply = QMessageBox.warning(self,
                                                    "Enable mission warning",
                                                    "{:.2f} GB of disk space left. \n".format(free_space_gb) +
                                                    "{:s} % of the disk has been used. \n".format(disk_usage) +
                                                    "Be aware that you can run out of disk space within the mission. "
                                                    "Do you want to continue?",
                                                    QMessageBox.Yes, QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            return True
                        else:
                            return False
                    else:
                        return True
            raise Exception("could not parse disk check command")
        except Exception as e:
            logger.error("Disk capacity could not be checked")
            reply = QMessageBox.warning(self,
                                        "Enable mission warning",
                                        "Disk capacity could not be checked: {} \n".format(e.args[0]) +
                                        "Be aware that you can run out of disk space within the mission. Do you want to continue?",
                                        QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                return True
            else:
                return False


    def about(self):
        about_msg = QMessageBox()

        pixmap = QPixmap(":/resources/iquaview.png")
        pixmap = pixmap.scaled(QSize(550, 393), Qt.KeepAspectRatio)
        about_msg.setIconPixmap(pixmap)
        about_msg.setText("<p><b>Iqua Robotics </b><p>"+
                          "<p>IQUAview version: "+__version__+"</p>"+
                          "<a href='mailto:support@iquarobotics.com'>support@iquarobotics.com</a>" +
                          "<p>Tested with: </p>" +
                          "<ul>" +
                          "<li> Qt 5.9.5</li>" +
                          "<li>Qqis 3.4.5-Madeira</li>" +
                          "</ul>" +
                          "<p>Currently running: </p>" +
                          "<ul>"+
                          "<li> Qt "+qVersion()+"</li>" +
                          "<li>Qqis "+Qgis.QGIS_VERSION+"</li>" +
                          "</ul>")
        about_msg.setWindowTitle("About")

        about_msg.exec_()

    def disconnect_objects(self):
        """
        Disconnect multiple objects
        """
        self.vehicle_data.disconnect()
        self.timeout_widget.disconnect()
        self.thrusters_status.disconnect()
        self.keep_position_status.disconnect()
        self.mission_active.disconnect()
        self.vehicle_widgets.disconnect()
        self.log_widget.disconnect()
        self.goto_dialog.disconnect()

    def closeEvent(self, event):
        """ Overrides closeEvent"""
        super(QMainWindow, self).closeEvent(event)

        self.boat_pose_action = None

        # self.view.currentLayerChanged.disconnect(self.layer_changed)
        self.proj.layerWillBeRemoved[QgsMapLayer].disconnect(self.layer_will_be_removed)
        self.model.dataChanged.disconnect(self.layer_changed)
        logger.info("Disconnecting from vehicle")
        self.auv_processes_widget.disconnect_auvprocesses()
        self.disconnect_objects()
        self.timeout_widget.cancel_timer()
        self.disconnect_auvp_dw()
        self.disconnect_gps_dw()
        self.plugin_manager.disconnect_plugins()

        if self.process_teleop is not None:
            self.process_teleop.terminate()
            # wait to finish
            self.process_teleop.wait()
        if self.timer_robot_monitor:
            self.timer_robot_monitor.cancel()
        if self.process_robot_monitor is not None:
            self.process_robot_monitor.terminate()
            # wait to finish
            self.process_robot_monitor.wait()

