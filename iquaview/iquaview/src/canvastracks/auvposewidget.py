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
 Widget to monitor the position of the AUV provided that there is WiFi (or umbilical) connection.
"""
import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from qgis.core import QgsPointXY, QgsWkbTypes
from iquaview.src.ui.ui_auvpose import Ui_AUVPosewidget
from iquaview.src.canvastracks.canvasmarker import CanvasMarker

logger = logging.getLogger(__name__)


class AUVPoseWidget(QWidget, Ui_AUVPosewidget):
    auv_wifi_connected = pyqtSignal(bool)

    def __init__(self, canvas, vehicle_info, vehicle_data, mission_sts, parent=None):
        super(AUVPoseWidget, self).__init__(parent)
        self.setupUi(self)

        self.canvas = canvas
        self.vehicle_info = vehicle_info
        self.vehicle_data = vehicle_data
        self.mission_sts = mission_sts
        self.default_color = Qt.yellow
        self.marker = CanvasMarker(self.canvas, self.default_color,
                                   ":/resources/" + vehicle_info.get_vehicle_type() + "/vehicle.svg",
                                   float(vehicle_info.get_vehicle_width()), float(vehicle_info.get_vehicle_length()))
        self.trackwidget.init("AUV track", self.canvas, self.default_color, QgsWkbTypes.LineGeometry, self.marker)

        self.connectButton.clicked.connect(self.emit_connection)
        self.connected = False
        # self.mission_sts = MissionStatus(self.config)

        self.timer = QTimer()
        self.timer.timeout.connect(self.auv_pose_update_canvas)

    def emit_connection(self):
        if not self.connected:
            self.auv_wifi_connected.emit(True)
        else:
            self.disconnect("Disconnected")

    def connect(self):
        try:
            self.auv_status_label.setText("Connected")
            self.auv_status_label.setStyleSheet('font:italic; color:green')
            self.connected = True
            self.connectButton.setText("Disconnect")
            self.timer.start(1000)
            self.mission_sts.init_mission_status_wifi()
        except:
            logger.error("No connection with COLA2")
            self.disconnect("No connection with COLA2")
            self.trackwidget.centerButton.setEnabled(False)

    def disconnect(self, msg=''):
        self.auv_wifi_connected.emit(False)
        self.timer.stop()
        self.mission_sts.disconnect()
        self.connected = False
        self.trackwidget.close()
        self.connectButton.setText("Connect")
        self.auv_status_label.setText(msg)
        self.auv_status_label.setStyleSheet('font:italic; color:red')
        self.trackwidget.centerButton.setEnabled(False)

    def auv_pose_update_canvas(self):
        if self.connected:
            data = self.vehicle_data.get_nav_sts()
            if data is not None and data['valid_data'] != 'disconnected':
                lat = float(data['global_position']['latitude'])
                lon = float(data['global_position']['longitude'])
                heading = float(data['orientation']['yaw'])
                depth = float(data['position']['depth'])
                altitude = float(data['altitude'])

                pos = QgsPointXY(lon, lat)
                self.trackwidget.track_update_canvas(pos, heading)
                self.auv_status_label.setText("Receiving data from AUV")
                self.auv_status_label.setStyleSheet('font:italic; color:green')
                [status, status_color] = self.mission_sts.get_status()
                if status != "":
                    self.auv_status_label.setText(status)
                    self.auv_status_label.setStyleSheet('font:italic; color:{}'.format(status_color))

                recovery_action_status = self.mission_sts.get_recovery_action_status()
                self.recovery_action_status_label.setText(recovery_action_status)
                self.recovery_action_status_label.setStyleSheet('font:italic; color: red')

                self.auv_depth_label.setText("{:.2F} m / {:.2F} m".format(depth, altitude))

            else:
                self.disconnect("No navigation data from AUV")

    def is_connected(self):
        return self.connected
