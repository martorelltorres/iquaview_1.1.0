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
 Class to handle the connection to the init server of the vehicle
"""

import socket
import time
import threading
import logging
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QThreadPool

from iquaview.src.utils.workerthread import Worker

logger = logging.getLogger(__name__)


class RepeatedTimer(object):
    def __init__(self, interval, func, *args, **kwargs):
        self._timer     = QTimer()
        self.interval   = interval
        self.function   = func
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False

        self._timer.timeout.connect(self._run)
        self._timer.start(5000)

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.is_running = True

    def stop(self):
        self._timer.stop()
        self.is_running = False


class ConnectionClient(QObject):
    connection_failure = pyqtSignal()
    connection_ok = pyqtSignal()
    reconnect_signal = pyqtSignal()

    def __init__(self, ip, port,):
        super(ConnectionClient, self).__init__()
        self.ip = ip
        self.port = port
        self.sock = None
        self.threadpool = QThreadPool()
        self.timer = QTimer()
        self.timer.timeout.connect(self.watchdog)
        self.reconnect_signal.connect(self.start_cc_thread)
        self.connection_ok.connect(self.start_watchdog_timer)
        # self.rt = RepeatedTimer(5000, self.watchdog)
        self.connected = False

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    def start_cc_thread(self):
        # self.t = threading.Thread(target=self.do_connection)
        # self.t.daemon = True
        # self.t.start()
        worker = Worker(self.do_connection)  # Any other args, kwargs are passed to the run function
        self.threadpool.start(worker)

    def do_connection(self):
        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set timeout
            self.sock.settimeout(3.0)
            server_address = (self.__ip, int(self.__port))
            self.sock.connect(server_address)
            self.connected = True
            self.connection_ok.emit()
            logger.info("Connected")

        except socket.error as e:
            self.disconnect()
            self.connected = False
            self.connection_failure.emit()

        except Exception as e:
            self.disconnect()
            self.connected = False
            self.connection_failure.emit()

        if not self.connected:
            time.sleep(5)
            self.reconnect_signal.emit()

    def start_watchdog_timer(self):
        self.timer.start(5000)

    def watchdog(self):
        try:
            data = self.send("watchdog")
            if data != "watchdogack":
                self.disconnect()
                self.connection_failure.emit()
                self.reconnect_signal.emit()

        except socket.timeout:
            logger.error("timeout error")
            self.disconnect()
            self.connection_failure.emit()
            self.reconnect_signal.emit()
        except socket.error:
            logger.error("socket error occured")
            self.disconnect()
            self.connection_failure.emit()
            self.reconnect_signal.emit()

        except Exception as e:
            logger.error("%s fail to receive ack from the server" % e)
            self.disconnect()
            self.connection_failure.emit()
            self.reconnect_signal.emit()

    def send(self, message):
        self.sock.sendall(message.encode())
        data = self.sock.recv(4096).decode()
        return data


    def disconnect(self):
        # if self.rt:
        #     self.rt.stop()
        self.connected = False
        self.timer.stop()
        if self.sock:
            self.sock.close()

        self.threadpool.clear()
