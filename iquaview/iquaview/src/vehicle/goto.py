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
 Dialog to send a goto command to the vehicle.
 It allows to define graphically the destination point by clicking the map.
"""
import logging

from PyQt5.QtCore import pyqtSignal, QEvent, QTimer
from PyQt5.QtWidgets import QDialog, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QColor, QValidator
from PyQt5 import QtCore

from qgis.gui import QgsMapToolEmitPoint, QgsMapToolPan, QgsRubberBand
from qgis.core import QgsWkbTypes, QgsPointXY, QgsDistanceArea, QgsProject

from iquaview.src.cola2api.cola2_interface import (SubscribeToTopic,
                                                   send_goto_service,
                                                   send_trigger_service,
                                                   get_ros_param)
from iquaview.src.ui.ui_go_to_dlg import Ui_GoToDialog
from iquaview.src.utils.busywidget import BusyWidget
from iquaview.src.utils.textvalidator import validate_custom_double, get_color, get_custom_double_validator
from iquaview.src.xmlconfighandler.vehicledatahandler import VehicleDataHandler

logger = logging.getLogger(__name__)


class GoToDialog(QDialog, Ui_GoToDialog):
    going_signal = pyqtSignal()
    map_tool_change_signal = pyqtSignal()
    dialog_finished_signal = pyqtSignal()

    def __init__(self, config, canvas, ip, port, vehicle_namespace, vehicledata, parent=None):
        super(GoToDialog, self).__init__(parent)
        self.config = config
        self.canvas = canvas
        self.ip = ip
        self.port = port
        self.vehicle_namespace = vehicle_namespace
        self.vehicle_data = vehicledata
        self.setupUi(self)
        self.getCoordinatesButton.setIcon(QIcon(":/resources/pickPointInMap.svg"))
        self.installEventFilter(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_goto_status)
        self.subscribed = False

        self.goto_status = None
        self.mission_active = None
        self.active_controller = None

        crs = self.canvas.mapSettings().destinationCrs()
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())

        self.Ok_pushButton.clicked.connect(self.on_accept)
        self.cancel_pushButton.clicked.connect(self.on_reject)

        double_validator = get_custom_double_validator()
        self.zLineEdit.setValidator(double_validator)
        self.zLineEdit.textChanged.connect(self.validate_double)
        self.latitudeLineEdit.textChanged.connect(self.validate_double)
        self.longitudeLineEdit.textChanged.connect(self.validate_double)
        self.surgeLineEdit.setValidator(double_validator)
        self.surgeLineEdit.textChanged.connect(self.validate_double)

        self.pointTool = QgsMapToolEmitPoint(self.canvas)
        self.pointTool.canvasClicked.connect(self.map_clicked)
        self.getCoordinatesButton.clicked.connect(self.get_coordinates)

        self.rubber_band_points = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        self.rubber_band_points.setColor(QColor("red"))
        self.rubber_band_points.setIcon(QgsRubberBand.ICON_CROSS)
        self.rubber_band_points.setIconSize(15)

    def set_ip(self, ip):
        """ Set IP"""
        self.ip = ip

    def set_port(self, port):
        """ Set Port """
        self.port = port

    def is_going(self):
        """
        Get goto state
        :return: Return True if auv is going, otherwise False
        """

        going = False

        data = self.vehicle_data.get_captain_state()
        # if receive data from auv
        if data is not None:
            # 1 GO TO
            if data == 1:
                going = True
        else:
            # back compatibility
            data = self.vehicle_data.get_goto_status()
            active_controller = self.vehicle_data.get_active_controller()
            mission_active = self.vehicle_data.get_mission_active()
            # if receive data from auv
            if (data is not None
                    and active_controller is not None
                    and mission_active is not None
                    and data['valid_data'] == 'new_data'):
                status_list = data['status_list']
                if len(status_list) > 0:
                    # last goal status
                    status = status_list[len(status_list) - 1]['status']
                    # 1 going
                    if (status == 1 and active_controller == 1 and not mission_active):
                        going = True
        return going

    def on_accept(self):
        """ On click accept, send service with the values on the fields and subscribes to goto service"""
        try:
            if self.is_acceptable():
                altitude_mode = self.altitudeModeCheckBox.isChecked()
                x = float(self.latitudeLineEdit.text())
                y = float(self.longitudeLineEdit.text())
                z = float(self.zLineEdit.text())
                surge = float(self.surgeLineEdit.text())
                tolerance_x = float(self.x_tolerance_doubleSpinBox.value())
                tolerance_y = float(self.y_tolerance_doubleSpinBox.value())
                tolerance_z = float(self.z_tolerance_doubleSpinBox.value())

                if self.is_allowed_distance(x, y):

                    enable_goto = self.vehicle_data.get_goto_service()
                    # send goto service with params
                    result = send_goto_service(self.ip, self.port, self.vehicle_namespace + enable_goto, z,
                                               altitude_mode, x, y, z, surge,
                                               tolerance_x, tolerance_y, tolerance_z)
                    if result['result']:

                        if result['values']['success']:
                            self.goto_status = None
                            self.dialog_finished_signal.emit()
                            self.accept()
                        else:
                            try:
                                message = result['values']['message']
                            # back compatibility
                            except Exception as e:
                                message = "There is another execution in progress."
                            logger.warning("'Go to' failed")
                            QMessageBox.critical(self,
                                                 "Go to failed",
                                                 message,
                                                 QMessageBox.Close)
                            self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
                            self.on_reject()
                    else:
                        message = "Error sending 'Go to' Service"
                        logger.error(message)
                        QMessageBox.critical(self,
                                             "Go to failed",
                                             message,
                                             QMessageBox.Close)
                        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
                        self.on_reject()

                else:
                    message = "Enter a point within the allowed distance: "\
                              + str(self.get_max_dist_allowed()) \
                              + "m"
                    logger.error(message)
                    QMessageBox.critical(self,
                                         "Go to failed",
                                         message,
                                         QMessageBox.Close)
                    self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)

        except OSError as oe:
            logger.error("Connection Refused")
            QMessageBox.critical(self,
                                 "Go to failed",
                                 "Connection Refused: " + oe.strerror,
                                 QMessageBox.Close)
            self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)

        except ConnectionRefusedError:
            logger.error("Connection Refused")
            QMessageBox.critical(self,
                                 "Go to failed",
                                 "Connection Refused",
                                 QMessageBox.Close)
            self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)

    def update_goto_status(self):
        self.subscribed = True
        self.timer.start(1000)

    def refresh_goto_status(self):
        """ check the goto status"""
        if self.subscribed:
            data = self.vehicle_data.get_captain_state()
            # if receive data from auv
            if data is not None:
                if (data != self.goto_status):
                    # 1 GO TO
                    if data == 1:
                        logger.info("Going")
                        self.going_signal.emit()
                    elif self.goto_status == 1 and data != 1:
                        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
                        self.going_signal.emit()

                    self.goto_status = data
            else:
                #back compatibility
                data = self.vehicle_data.get_goto_status()
                active_controller = self.vehicle_data.get_active_controller()
                mission_active = self.vehicle_data.get_mission_active()
                # if receive data from auv
                if (data is not None
                        and active_controller is not None
                        and mission_active is not None
                        and data['valid_data'] == 'new_data'):
                    status_list = data['status_list']
                    if len(status_list) > 0:
                        # last goal status
                        status = status_list[len(status_list) - 1]['status']
                        if (status != self.goto_status
                                or active_controller != self.active_controller
                                or self.mission_active != mission_active):
                            # 1 going
                            if status == 1 and active_controller == 1 and not mission_active:
                                logger.info("Going")
                                self.going_signal.emit()
                            # 3 on goal
                            elif status == 3:
                                logger.info("On goal")
                                self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
                                self.going_signal.emit()
                            elif self.goto_status == 1 and status != 1:
                                self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
                                self.going_signal.emit()

                            self.goto_status = status
                            self.active_controller = active_controller
                            self.mission_active = mission_active

    def validate_double(self):
        """ validate the text of the sender"""
        sender = self.sender()
        state = validate_custom_double(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def is_acceptable(self):
        """
        check if the text of the fields of goto are acceptables
        :return: return True if the values are acceptable, otherwise False
        """
        return (validate_custom_double(self.zLineEdit.text()) == QValidator.Acceptable and
                validate_custom_double(self.latitudeLineEdit.text()) == QValidator.Acceptable and
                validate_custom_double(self.longitudeLineEdit.text()) == QValidator.Acceptable and
                validate_custom_double(self.surgeLineEdit.text()) == QValidator.Acceptable)

    def get_coordinates(self):
        """Set the maptool to pointTool"""
        self.map_tool_change_signal.emit()  # Emit signal to warn mainwindow that we are changing a maptool
        self.canvas.setMapTool(self.pointTool)

    def map_clicked(self, point):
        """Set the coordinates from 'point' to longitude and latitude lineEdits"""
        # reset icon_cross rubber_band_points
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)

        self.longitudeLineEdit.setText(str(point[0]))
        self.latitudeLineEdit.setText(str(point[1]))
        self.pointTool.deactivate()
        # add new icon_cross rubber_band_point
        self.rubber_band_points.addPoint(point)
        self.canvas.setMapTool(QgsMapToolPan(self.canvas))

    def is_allowed_distance(self, x_goal, y_goal):
        """

        :param x_goal: longitude
        :param y_goal: latitude
        :return: return true if the distance is allowed, otherwise false
        """
        allowed = False
        data = self.vehicle_data.get_nav_sts()
        if data is not None and data['valid_data'] != 'disconnected':
            lat = float(data['global_position']['latitude'])
            lon = float(data['global_position']['longitude'])
            pos = QgsPointXY(lon, lat)
            pos_goal = QgsPointXY(y_goal, x_goal)

            distance = self.distance_calc.measureLine([pos, pos_goal])
            max_dist = self.get_max_dist_allowed()

            if distance <= max_dist:
                allowed = True

        return allowed

    def get_max_dist_allowed(self):
        """ Get the maximum distance allowed to waypoint"""
        return float(get_ros_param(self.ip, 9091,
                                   self.vehicle_namespace + '/captain/max_distance_to_waypoint')['value'])

    def disable_goto(self):
        """ Send a service that disables goto"""
        disable_goto = self.vehicle_data.get_disable_goto_service()
        if disable_goto is not None:
            response = send_trigger_service(self.ip, self.port, self.vehicle_namespace + disable_goto)
            try:
                if not response['values']['success']:
                    QMessageBox.critical(self,
                                         "Disable 'Go to' failed",
                                         response['values']['message'],
                                         QMessageBox.Close)
            # back compatibility
            except Exception as e:
                logger.warning("The disable goto response can not be read")

    def on_reject(self):
        """ reject goto"""
        self.going_signal.emit()
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
        self.dialog_finished_signal.emit()
        self.reject()

    def closeEvent(self, event):
        """ close event and call function on_reject"""
        self.on_reject()

    def eventFilter(self, widget, event):
        """ Event filter"""
        if (event.type() == QEvent.KeyPress
                and isinstance(widget, GoToDialog)):
            key = event.key()
            if key == QtCore.Qt.Key_Escape:
                # capture Key Escape for emit going_signal
                self.going_signal.emit()

        return QWidget.eventFilter(self, widget, event)

    def disconnect(self):
        """ Disconnect timer and topic """
        self.rubber_band_points.reset(QgsWkbTypes.PointGeometry)
        self.subscribed = False
        self.goto_status = None
        if self.timer:
            self.timer.stop()
