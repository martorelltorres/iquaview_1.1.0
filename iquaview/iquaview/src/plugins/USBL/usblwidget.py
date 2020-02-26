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
 Widget to connect the USBL device and display information from it.
 It displays the USBL track, GPS track and the track according to the AUV navigation
 that is transmitted back acoustically in the map canvas.
 Also shows some status information retrieved from the received acoustic communication.
"""

import math
import time
import logging
from importlib import util

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QColor

from qgis.core import QgsPointXY, QgsWkbTypes

from iquaview.src.ui.ui_usbl import Ui_USBLWidget
from iquaview.src.canvastracks.canvasmarker import CanvasMarker

if util.find_spec('usblcontroller') is not None:
    import usblcontroller

logger = logging.getLogger(__name__)


class USBLWidget(QWidget, Ui_USBLWidget):
    usbl_connected = pyqtSignal(bool)
    gpsconnectionfailed = pyqtSignal()
    mission_started = pyqtSignal()
    mission_stopped = pyqtSignal()

    def __init__(self, canvas, config, vehicle_info, mission_sts, parent=None):
        super(USBLWidget, self).__init__(parent)
        self.setupUi(self)

        self.canvas = canvas
        self.config = config
        self.vehicle_info = vehicle_info
        self.mission_sts = mission_sts

        self.default_color_gps = Qt.darkGreen
        width = self.config.csettings["vessel_width"]
        length = self.config.csettings["vessel_length"]
        self.marker_gps = CanvasMarker(self.canvas, self.default_color_gps, ":/resources/vessel.svg", width, length,
                                       marker_mode=True, config=config)

        self.trackwidget_gps.init("GPS track",
                                  self.canvas,
                                  self.default_color_gps,
                                  QgsWkbTypes.LineGeometry,
                                  self.marker_gps)

        self.default_color_usbl = Qt.red
        self.marker_usbl = CanvasMarker(self.canvas, self.default_color_usbl,
                                        None, orientation=False)
        self.trackwidget_usbl.init("USBL track",
                                   self.canvas,
                                   self.default_color_usbl,
                                   QgsWkbTypes.PointGeometry,
                                   self.marker_usbl)

        self.default_color_auv = QColor(Qt.darkYellow)
        self.default_color_auv.setAlpha(80)
        #":/resources/" + vehicle_info.get_vehicle_type() + "/vehicle.svg"
        self.marker_auv = CanvasMarker(self.canvas, self.default_color_auv,
                                       None,
                                       float(vehicle_info.get_vehicle_width()),
                                       float(vehicle_info.get_vehicle_length()))

        self.trackwidget_auv.init("AUV track",
                                  self.canvas,
                                  self.default_color_auv,
                                  QgsWkbTypes.LineGeometry,
                                  self.marker_auv)


        # set signals
        self.connectButton.clicked.connect(self.connect)

        self.connected = False
        self.gps_connection_failed = False
        self.set_label_disconnected()
        self.timer = QTimer()
        self.timer.timeout.connect(self.usbl_update_canvas)
        self.gpsconnectionfailed.connect(self.stop_canvas_updates)

        self.last_ping = 0
        self.last_usbl_time = 0.0
        self.last_auv_time = 0.0


        # self.waiting_mission_start = True
        # self.waiting_mission_stop = True
        # self.t_check_mission_start = threading.Thread(target=self.check_mission_start)
        # self.t_check_mission_start.daemon = True
        # self.t_check_mission_stop = threading.Thread(target=self.check_mission_stop)
        # self.t_check_mission_stop.daemon = True

        self.controller = usblcontroller.USBLController(config, vehicle_info.get_vehicle_code())

    def connect(self):
        if not self.controller.is_connected():
            try:
                self.controller.connect()

                self.connectButton.setText("Disconnect")
                self.timer.start(1000)
                self.usbl_status_label.setText("Connected")
                self.usbl_status_label.setStyleSheet('font:italic; color:green')
                self.usbl_connected.emit(True)

                self.gps_connection_failed = False
                if not self.controller.e_usbl.get_gps_initialized():
                    self.stop_canvas_updates()

            except Exception as e:
                logger.error("No connection to USBL: {}".format(e))
                QMessageBox.critical(self, "USBL Connection Failed",
                                     "Connection with USBL could not be established: \n"+str(e),
                                     QMessageBox.Close)
                self.set_label_disconnected()
                # self.connected = False
                self.disable_center_buttons()
                self.disconnect()
        else:
            self.disconnect()

    def usbl_update_canvas(self):
        if self.controller.is_connected():
            pos_auv = None
            pos_usbl = None
            auv_heading = None

            data = self.controller.usbl_update_sensed_on_surface_data()
            data_auv = self.controller.usbl_update_auv_data()
            data_gps = self.controller.usbl_update_gps_data()


            usbl_time = float(data['time'])
            if usbl_time != 0.0 and usbl_time != self.last_usbl_time:  # if valid and new data
                usbl_lat = float(data['latitude'])
                usbl_lon = float(data['longitude'])
                usbl_height = -float(data['depth'])  # negative
                usbl_time = float(data['time'])
                pos_usbl = QgsPointXY(usbl_lon, usbl_lat)
                usbl_position = "{:.5F}, {:.5F}".format(usbl_lat, usbl_lon)
                self.usbl_position_label.setText(usbl_position)
                self.usbl_depth_label.setText("{:.3F}".format(usbl_height))
                self.last_ping = 0
                self.last_usbl_time = usbl_time
            else:
                self.last_ping = self.last_ping + 1
            self.usbl_lastping_label.setText(str(self.last_ping))

            auv_time = float(data_auv['time'])
            if auv_time != 0.0 and auv_time != self.last_auv_time:  # if valid data
                logger.info("Received data back from AUV")
                auv_lat = float(data_auv['latitude'])
                auv_lon = float(data_auv['longitude'])
                auv_depth = float(data_auv['depth'])
                auv_heading = float(data_auv['heading'])
                auv_error = int(data_auv['error'])
                self.last_auv_time = auv_time

                pos_auv = QgsPointXY(auv_lon, auv_lat)
                auv_position = "{:.5F}, {:.5F}".format(auv_lat, auv_lon)
                self.auv_position_label.setText(auv_position)
                self.auv_depth_label.setText("{:.3F}".format(auv_depth))

                code = self.vehicle_info.get_vehicle_code()
                if code == 'status_code':
                    self.mission_sts.assign_status(auv_error)
                else:
                    self.mission_sts.assign_status_error_code(auv_error)
                [status, status_color] = self.mission_sts.get_status()
                if status == "":
                    status = "connected"
                    status_color = 'green'
                self.usbl_status_label.setText(status)
                self.usbl_status_label.setStyleSheet('font:italic; color:{}'.format(status_color))


            if data_gps is not None and data_gps['status'] == 'new_data':

                if (data_gps['quality'] >= 1) and (data_gps['quality'] <= 5):
                    gps_lat = data_gps['latitude']
                    gps_lon = data_gps['longitude']
                    gps_heading = data_gps['heading']
                    pos_gps = QgsPointXY(gps_lon, gps_lat)
                    # update canvas
                    self.trackwidget_gps.track_update_canvas(pos_gps,
                                                             math.radians(
                                                                 gps_heading - self.config.csettings['gps_offset_heading']))
                # update canvas
                if pos_usbl is not None:
                    self.trackwidget_usbl.track_update_canvas(pos_usbl, 0)
                if pos_auv is not None and auv_heading is not None:
                    self.trackwidget_auv.track_update_canvas(pos_auv, auv_heading)

            elif data_gps['status'] == 'old_data':
                now = time.time()
                if (now - data_gps['time']) > 5.0:
                     self.gpsconnectionfailed.emit()

    def send_abort_and_surface(self):
        self.controller.send_abort_and_surface()
        self.usbl_status_label.setText("Sending Abort and Surface...")

    def send_emergency_surface(self):
        self.controller.send_emergency_surface()
        self.usbl_status_label.setText("Sending Emergency Surface...")

    def send_informative(self):
        logger.info("Setting USBL command to Informative")
        self.controller.send_informative()
        self.usbl_status_label.setText("Sending Informative Cmd...")

    def send_start_mission(self):
        logger.info("Start mission from  USBL...")
        self.usbl_status_label.setText("Sending Start Mission...")
        self.controller.send_start_mission()

    def send_stop_mission(self):
        logger.info("Stop mission from  USBL...")
        self.controller.send_stop_mission()
        self.usbl_status_label.setText("Sending Stop Mission...")

    def set_enable_update(self, enable):
        logger.info("Set ", enable, "updates from USBL...")
        self.controller.set_enable_update(enable)

    def stop_canvas_updates(self):
        self.trackwidget_usbl.close()
        self.trackwidget_gps.close()
        self.trackwidget_auv.close()
        self.disable_center_buttons()

        if not self.gps_connection_failed:
            QMessageBox.critical(self,
                                 "Gps connection failed",
                                 "Gps connection was lost. "
                                 "You have connection with the USBL but you can not show the position on the map",
                                 QMessageBox.Close)
            self.gps_connection_failed = True

    def disconnect(self):
        self.last_ping = 0
        self.last_usbl_time = 0.0
        self.last_auv_time = 0.0

        self.controller.disconnect()

        self.trackwidget_usbl.close()
        self.trackwidget_gps.close()
        self.trackwidget_auv.close()
        self.disable_center_buttons()
        if self.timer:
            self.timer.stop()

        self.connectButton.setText("Connect")
        self.set_label_disconnected()
        self.usbl_connected.emit(False)


    def set_label_disconnected(self):
        self.usbl_status_label.setText("Disconnected")
        self.usbl_status_label.setStyleSheet('font:italic; color:red')

    def disable_center_buttons(self):
        self.trackwidget_usbl.centerButton.setEnabled(False)
        self.trackwidget_auv.centerButton.setEnabled(False)
        self.trackwidget_gps.centerButton.setEnabled(False)

    def check_mission_start(self):
        while self.waiting_mission_start:
            logger.info("Waiting for mission to start...")
            mission_executing = self.mission_sts.is_mission_in_execution()
            if mission_executing:
                self.controller.send_informative()
                self.waiting_mission_start = False
                self.usbl_status_label.setText("Mission Started")
                self.mission_started.emit()
            time.sleep(1.0)

    def check_mission_stop(self):
        while self.waiting_mission_stop:
            mission_executing = self.mission_sts.is_mission_in_execution()
            if not mission_executing:
                self.controller.send_informative()
                self.waiting_mission_stop = False
                self.usbl_status_label.setText("Mission Stopped")
                self.mission_stopped.emit()
            time.sleep(1.0)

    def is_connected(self):
        return self.controller.is_connected()

    def update_width_and_length(self):
        width = self.config.csettings["vessel_width"]
        length = self.config.csettings["vessel_length"]
        self.marker_gps.set_width(width)
        self.marker_gps.set_length(length)
        self.usbl_update_canvas()
