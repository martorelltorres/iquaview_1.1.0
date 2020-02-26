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
    Class to add the USBL functions to the mainwindow
"""

from PyQt5.QtWidgets import QAction, QToolBar, QMessageBox, QDockWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal

from iquaview.src.plugins.USBL import usblwidget


class USBLModule(QObject):

    signal_create_dock = pyqtSignal(int, QDockWidget)
    signal_enable_boat_pose_action = pyqtSignal()

    def __init__(self,canvas, config, vehicle_info, mission_sts, action_boat_pose, menubar, view_menu_toolbar):
        super(QObject, self).__init__()

        self.usblwidget = None
        self.boat_pose_action = action_boat_pose
        self.canvas = canvas
        self.config = config
        self.vehicle_info = vehicle_info
        self.mission_sts = mission_sts

        # Actions for Vehicle (usbl)
        self.usbl_pose_action = QAction(
            QIcon(":/resources/" + vehicle_info.get_vehicle_type() + "/mActionAUVPoseUSBL.svg"),
            "Monitor AUV Pose",
            self)
        self.abort_and_surface_action = QAction(
            QIcon(":/resources/" + vehicle_info.get_vehicle_type() + "/mActionAbortAndSurfaceAcoustic.svg"),
            "Send Abort and Surface",
            self)
        self.emergency_surface_action = QAction(
            QIcon(":/resources/" + vehicle_info.get_vehicle_type() + "/mActionEmergencySurfaceAcoustic.svg"),
            "Send Emergency Surface",
            self)

        self.usbl_start_mission_action = QAction(QIcon(":/resources/mActionExecuteMissionAcoustic.svg"),
                                              "Start Mission", self)

        self.usbl_abort_mission_action = QAction(QIcon(":/resources/mActionStopMissionAcoustic.svg"),
                                              "Stop Mission", self)

        self.usbl_enable_update_action = QAction(QIcon(":/resources/mActionUSBLUpdatesOff.svg"), "Enable Updates", self)

        self.usbl_pose_action.setCheckable(True)
        self.usbl_start_mission_action.setCheckable(True)
        self.usbl_abort_mission_action.setCheckable(True)
        self.abort_and_surface_action.setCheckable(True)
        self.emergency_surface_action.setCheckable(True)
        self.usbl_enable_update_action.setCheckable(True)

        self.usbl_menu = menubar.addMenu("USBL")
        self.usbl_menu.addActions([self.usbl_pose_action,
                                   self.usbl_start_mission_action,
                                   self.usbl_abort_mission_action,
                                   self.usbl_enable_update_action,
                                   self.abort_and_surface_action,
                                   self.emergency_surface_action])

        # Toolbar for Vehicle (usbl)
        self.usbl_toolbar = QToolBar("USBL Tools")
        self.usbl_toolbar.setObjectName("USBL Tools")
        self.usbl_toolbar.addAction(self.usbl_pose_action)
        # self.usbl_toolbar.addAction(self.usbl_start_mission_action)
        # self.usbl_toolbar.addAction(self.usbl_abort_mission_action)
        self.usbl_toolbar.addAction(self.usbl_enable_update_action)
        self.usbl_toolbar.addAction(self.abort_and_surface_action)
        self.usbl_toolbar.addAction(self.emergency_surface_action)

        self.usbl_toolbar_action = QAction("USBL", self)
        self.usbl_toolbar_action.setCheckable(True)
        self.usbl_toolbar_action.setChecked(True)
        self.usbl_toolbar_action.triggered.connect(lambda: self.change_toolbar_visibility(self.usbl_toolbar))

        self.usbl_pose_action.triggered.connect(self.show_usbl_pose)
        self.usbl_start_mission_action.toggled.connect(self.send_start_mission)
        self.usbl_abort_mission_action.toggled.connect(self.send_abort_mission)
        self.usbl_enable_update_action.toggled.connect(self.enable_update)
        self.abort_and_surface_action.toggled.connect(self.send_abort_and_surface)
        self.emergency_surface_action.toggled.connect(self.send_emergency_surface)

        self.usbl_is_connected(False)

        view_menu_toolbar.addAction(self.usbl_toolbar_action)

    def get_usbl_toolbar(self):
        return self.usbl_toolbar

    def get_usbl_widget(self):
        return  self.usblwidget

    def show_usbl_pose(self):
        if self.usbl_pose_action.isChecked():
            # Disconnect gps from boat, will be visible from USBL
            self.boat_pose_action.setChecked(False)
            self.boat_pose_action.setEnabled(False)
            self.create_usbl_dock_widget()
            self.usblwidget = usblwidget.USBLWidget(self.canvas, self.config, self.vehicle_info, self.mission_sts)
            self.usblwidget.setAttribute(Qt.WA_DeleteOnClose)
            self.usblwd.setWidget(self.usblwidget)
            self.usblwd.show()
            self.usblwidget.usbl_connected.connect(self.usbl_is_connected)
            self.usblwidget.connect()
            self.usbl_pose_action.setToolTip("Hide AUV USBL Monitoring")
        else:
            self.usblwd.close()
            self.disconnect_usbl_dw()
            self.usbl_pose_action.setToolTip("Show AUV USBL Monitoring")

    def send_start_mission(self):
        if self.usbl_start_mission_action.isChecked():
            self.usblwidget.send_start_mission()
            # self.usblwidget.mission_stopped.connect(self.mission_stopped_acoustically)

            self.usbl_start_mission_action.setToolTip("Stop Mission")

        else:
            self.usblwidget.send_informative()
            self.usbl_start_mission_action.setToolTip("Start Mission")

            # self.usblwidget.mission_stopped.disconnect()

    def send_abort_mission(self):
        if self.usbl_abort_mission_action.isChecked():
            self.usblwidget.send_stop_mission()
        else:
            self.usblwidget.send_informative()

    def enable_update(self):
        if self.usbl_enable_update_action.isChecked():
            icon = QIcon(":resources/mActionUSBLUpdatesOn.svg")
            self.usbl_enable_update_action.setToolTip("Disable Updates")

            self.usblwidget.set_enable_update(True)
        else:
            icon = QIcon(":resources/mActionUSBLUpdatesOff.svg")
            self.usbl_enable_update_action.setToolTip("Enable Updates")

            self.usblwidget.set_enable_update(False)

        self.usbl_enable_update_action.setIcon(icon)

    def send_abort_and_surface(self):
        if self.abort_and_surface_action.isChecked():
            confirmation_msg = "Are you sure you want to abort the mission?"
            reply = QMessageBox.question(self.parent(),
                                         'Abort Confirmation',
                                         confirmation_msg,
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.usblwidget.send_abort_and_surface()
        else:
            self.usblwidget.send_informative()

    def send_emergency_surface(self):
        if self.emergency_surface_action.isChecked():
            confirmation_msg = "Are you sure you want to abort the mission and send an emergency surface? " \
                               "An emergency surface will require you to restart the architecture afterwards. "
            reply = QMessageBox.question(self.parent(),
                                         'Emergency Surface Confirmation',
                                         confirmation_msg,
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.usblwidget.send_emergency_surface()
        else:
            self.usblwidget.send_informative()

    def mission_started_acoustically(self):
        icon = QIcon(":resources/mActionStopMissionAcoustic.svg")
        self.usbl_start_mission_action.setIcon(icon)
        # self.actionUSBLStartMission.setChecked(True)

    def mission_stopped_acoustically(self):
        icon = QIcon(":resources/mActionExecuteMissionAcoustic.svg")
        self.usbl_start_mission_action.setIcon(icon)
        self.usbl_start_mission_action.setChecked(False)

    def usbl_is_connected(self, connected):
        self.usbl_start_mission_action.setEnabled(connected)
        self.usbl_abort_mission_action.setEnabled(connected)
        self.abort_and_surface_action.setEnabled(connected)
        self.emergency_surface_action.setEnabled(connected)
        self.usbl_enable_update_action.setEnabled(connected)

        if not connected:
            self.usbl_start_mission_action.setChecked(False)
            self.usbl_abort_mission_action.setChecked(False)
            self.abort_and_surface_action.setChecked(False)
            self.emergency_surface_action.setChecked(False)
            self.usbl_enable_update_action.setChecked(False)

    def create_usbl_dock_widget(self):
        # Dock for USBL
        self.usblwd = QDockWidget()
        self.usblwd.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.usblwd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.signal_create_dock.emit(Qt.LeftDockWidgetArea, self.usblwd)
        self.usblwd.setWindowTitle("AUV monitoring (USBL)")
        self.usblwd.setStyleSheet("QDockWidget { font: bold; }")
        self.usblwd.setAttribute(Qt.WA_DeleteOnClose)
        self.usblwd.destroyed.connect(self.disconnect_usbl_dw)

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

    def disconnect_usbl_dw(self):
        if self.usblwidget is not None:
            if self.usblwidget.is_connected():
                self.usblwidget.disconnect()
            self.usblwidget.deleteLater()
            self.usblwidget = None
        self.usbl_pose_action.setChecked(False)
        self.signal_enable_boat_pose_action.emit()
