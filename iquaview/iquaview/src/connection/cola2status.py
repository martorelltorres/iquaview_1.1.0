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
 Class to periodically check cola2 state.
"""

import time
import logging
from iquaview.src.cola2api.cola2_interface import SubscribeToTopic
from iquaview.src.utils.workerthread import Worker
from iquaview.src.xmlconfighandler.vehicledatahandler import VehicleDataHandler

from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QThreadPool
from PyQt5.QtGui import QPixmap

logger = logging.getLogger(__name__)


class Cola2Status(QObject):
    reconnect_signal = pyqtSignal()
    cola2_connected = pyqtSignal(bool)
    update_data_signal = pyqtSignal()

    def __init__(self, config, vehicleinfo, label, indicator):
        super(Cola2Status, self).__init__()
        self.config = config
        self.vehicleinfo = vehicleinfo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.subscribed = False
        self.total_time_topic = None
        self.t_time = 0
        self.cola2_label = label
        self.cola2_indicator = indicator
        self.cola2_label.setStyleSheet('font:italic; color:red')
        self.cola2_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))

        self.reconnect_signal.connect(self.start_cola2_thread)
        self.update_data_signal.connect(self.start_timer)

        self.iswatchdog = False

        self.t_time_text = None
        vd_handler = VehicleDataHandler(self.config)
        # get vehicle data topics
        xml_vehicle_data_topics = vd_handler.read_topics()
        # back compatibility
        for topic in xml_vehicle_data_topics:
            if topic.get('id') == "total time":
                self.t_time_text = topic.text
                self.iswatchdog = False

            elif (topic.get('id') == "watchdog"):
                self.t_time_text = topic.text
                self.iswatchdog = True

        self.threadpool = QThreadPool()
        self.start_cola2_thread()

    def start_cola2_thread(self):
        # self.t = threading.Thread(target=self.update_cola2_status)
        # self.t.daemon = True
        # self.t.start()
        worker = Worker(self.update_cola2_status)  # Any other args, kwargs are passed to the run function
        self.threadpool.start(worker)

    def update_cola2_status(self):
        try:
            self.subscribed = True
            self.total_time_topic = SubscribeToTopic(self.vehicleinfo.get_vehicle_ip(),
                                                     9091,
                                                     self.vehicleinfo.get_vehicle_namespace()+self.t_time_text)
            self.cola2_connected.emit(True)
            self.update_data_signal.emit()
        except OSError as oe:
            logger.error("Disconnecting cola2 status {}".format(oe))
            self.disconnect_cola2status()
        except:
            logger.error("Disconnecting cola2 status")
            self.disconnect_cola2status()

        if not self.subscribed:
            time.sleep(5)
            # self.update_cola2_status()
            self.reconnect_signal.emit()

    def start_timer(self):
        self.timer.start(1000)

    def update_data(self):
        try:
            if self.subscribed:
                if self.total_time_topic:
                    data = self.total_time_topic.get_data()
                    if data and data['valid_data'] == 'new_data':
                        if self.iswatchdog:
                            if self.t_time != data['data']:
                                self.t_time = data['data']
                                self.cola2_label.setStyleSheet('font:italic; color:green')
                                self.cola2_indicator.setPixmap(QPixmap(":/resources/green_led.svg"))
                            else:
                                self.cola2_label.setStyleSheet('font:italic; color:red')
                                self.cola2_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))

                        elif self.t_time != data['total_time']:
                            self.t_time = data['total_time']
                            self.cola2_label.setStyleSheet('font:italic; color:green')
                            self.cola2_indicator.setPixmap(QPixmap(":/resources/green_led.svg"))
                        else:
                            self.cola2_label.setStyleSheet('font:italic; color:red')
                            self.cola2_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))

                    else:

                        if data and data['valid_data'] == 'disconnected':
                            self.disconnect_cola2status()
                            self.reconnect_signal.emit()
                        else:
                            self.cola2_label.setStyleSheet('font:italic; color:red')
                            self.cola2_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))

                else:
                    self.cola2_label.setStyleSheet('font:italic; color:red')
                    self.cola2_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))
        except:
            self.disconnect_cola2status()
            self.reconnect_signal.emit()

    def is_subscribed(self):
        return self.subscribed

    def disconnect_cola2status(self):
        self.cola2_connected.emit(False)
        self.subscribed = False
        self.cola2_label.setStyleSheet('font:italic; color:red')
        self.cola2_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))

        if self.total_time_topic:
            # close subscription
            self.total_time_topic.close()

        self.timer.stop()

        self.total_time_topic = None

        self.threadpool.clear()

