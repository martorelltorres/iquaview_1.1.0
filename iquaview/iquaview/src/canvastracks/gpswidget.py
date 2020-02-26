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
 Widget to connect to the GPS and show its track on the map.
"""

import math
import logging

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from qgis.core import QgsPointXY, QgsWkbTypes
from iquaview.src.ui.ui_gps import Ui_GPSwidget
from iquaview.src.canvastracks.canvasmarker import CanvasMarker
from iquaview.src.cola2api.gps_driver import GpsDriver

logger = logging.getLogger(__name__)


class GPSWidget(QWidget, Ui_GPSwidget):

    def __init__(self, canvas, config, parent=None):
        super(GPSWidget, self).__init__(parent)
        self.setupUi(self)

        self.canvas = canvas
        self.config = config
        self.default_color = Qt.darkGreen

        width = self.config.csettings["vessel_width"]
        length = self.config.csettings["vessel_length"]

        self.marker = CanvasMarker(self.canvas, self.default_color,
                                   ":/resources/vessel.svg", width, length,
                                   marker_mode=True, config=config)
        self.trackwidget.init("GPS track", self.canvas, self.default_color, QgsWkbTypes.LineGeometry, self.marker)
        self.gps = None
        self.connected = False
        self.set_label_disconnected()

        # set signals
        self.connectButton.clicked.connect(self.connect)

        self.timer = QTimer()
        self.timer.timeout.connect(self.gps_update_canvas)

    def connect(self):
        if not self.connected:
            try:
                if self.config.csettings['gps_serial']:
                    self.gps = GpsDriver(serial_port=self.config.csettings['gps_serial_port'],
                                         baud_rate=self.config.csettings['gps_serial_baudrate'])
                else:
                    self.gps = GpsDriver(ip_addr=self.config.csettings['gps_ip'],
                                         hdt_port=self.config.csettings['gps_hdt_port'],
                                         gga_port=self.config.csettings['gps_gga_port'])

                self.gps.connect()

                self.gps.gpsconnectionfailed.connect(self.connection_failed)
                self.gps.gpsparsingfailed.connect(self.parsing_failed)
                self.connectButton.setText("Disconnect")
                self.connected = True
                self.timer.start(1000)
                self.gps_status_label.setText("Connected")
                self.gps_status_label.setStyleSheet('font:italic; color:green')
            except:
                logger.error("Connection with GPS could not be established")
                QMessageBox.critical(self,
                                     "Connection Failed",
                                     "Connection with GPS could not be established",
                                     QMessageBox.Close)
                self.connected = False
                self.set_label_disconnected()
                self.trackwidget.centerButton.setEnabled(False)
                self.disconnect()
        else:
            self.disconnect()

    def disconnect(self):
        if self.gps is not None:
            self.gps.close()
        self.timer.stop()
        self.connected = False
        self.trackwidget.close()
        self.connectButton.setText("Connect")
        self.trackwidget.centerButton.setEnabled(False)

        self.set_label_disconnected()

    def gps_update_canvas(self):
        if self.connected:
            data = self.gps.get_data()
            if data['status'] == 'new_data' and (data['quality'] >= 1) and (data['quality'] <= 5):
                gps_lat = data['latitude']
                gps_lon = data['longitude']
                gps_heading = data['heading']
                pos = QgsPointXY(gps_lon, gps_lat)
                self.trackwidget.track_update_canvas(pos,
                                                     math.radians(gps_heading-self.config.csettings['gps_offset_heading']))
                self.gps_status_label.setText("Connected, receiving signal")
                self.gps_status_label.setStyleSheet('font:italic; color:green')

            elif data['status'] == 'old_data':
                self.parsing_failed()


    def set_label_disconnected(self):
        self.gps_status_label.setText("Disconnected")
        self.gps_status_label.setStyleSheet('font:italic; color:red')

    def parsing_failed(self):
        self.gps_status_label.setText("Connected, NO signal")
        self.gps_status_label.setStyleSheet('font:italic; color:red')

    def connection_failed(self):
        QMessageBox.critical(self,
                             "Connection Failed",
                             "Connection with GPS could not be established",
                             QMessageBox.Close)
        self.disconnect()

    def is_connected(self):
        return self.connected

    def update_width_and_length(self):
        width = self.config.csettings["vessel_width"]
        length = self.config.csettings["vessel_length"]
        self.marker.set_width(width)
        self.marker.set_length(length)
        self.gps_update_canvas()
