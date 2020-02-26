#!/usr/bin/env python
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
GPS NMEA-183 GGA sequence driver.
"""
import serial
import threading
import time
import socket
import select
import sys
import logging

from PyQt5.QtCore import pyqtSignal, QObject

# from iquaview.src.utils.printcolor import printerror, printdebug

logger = logging.getLogger(__name__)


def degree_minute_to_decimal_degree(degree_minute):
    """ Transform degree minutes values into
        decimal degrees (i.e., 3830.0 --> 38.5)
    """
    degrees = int(degree_minute / 100)
    minutes = degree_minute - (degrees * 100)
    return degrees + minutes / 60.0


class GpsDriver(QObject):
    """Class to handle GPS readings."""

    gpsconnectionfailed = pyqtSignal()
    gpsparsingfailed = pyqtSignal()

    def __init__(self, serial_port=None, baud_rate=9600,
                 ip_addr=None, hdt_port=4000, gga_port=4000, debug=False):
        """Constructor."""
        super(GpsDriver, self).__init__()
        # Init variables
        self.debug = debug
        self.serial_port= serial_port
        self.baud_rate = baud_rate
        self.ip_addr = ip_addr
        self.hdt_port = hdt_port
        self.gga_port = gga_port
        self.time = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.heading = 0.0
        self.quality = -1
        self.altitude = 0.0
        self.mode = "NONE"
        self.is_new_gps_data = True
        self.stream = None
        self.stream_gga = None
        self.stream_hdt = None
        self.t = None
        self.orientation_time = 0.0

    def connect(self):
        # Error check
        if (self.serial_port is not None) and (self.ip_addr is not None):
            line = "gpsdrv: cannot connect to both TCP and serial GPS"
            logger.error(line)
            raise Exception(line)
        elif (self.serial_port is None) and (self.ip_addr is None):
            line = "gpsdrv: no TCP or serial specified"
            logger.error(line)
            raise Exception(line)

        # Connect
        if self.serial_port is not None:
            try:
                s_port = self.serial_port
                if self.serial_port.startswith('tty'):
                    s_port = '/dev/' + self.serial_port

                self.stream = serial.Serial(
                    s_port, self.baud_rate, rtscts=True, dsrdtr=True)
                self.mode = "SERIAL"
            except Exception as e:
                line = "gpsdrv: exception '{}'".format(e)
                logger.error(line)
                line = "gpsdrv: cannot open serial port {}".format(s_port)
                raise Exception(line)
        elif self.ip_addr is not None:
            try:
                if self.hdt_port == self.gga_port:
                    port = self.hdt_port
                    self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.stream.settimeout(2.0)
                    self.stream.connect((self.ip_addr, port))
                    self.stream.setblocking(0)
                    self.mode = "TCP"
                else:
                    self.stream_hdt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.stream_hdt.settimeout(2.0)
                    self.stream_hdt.connect((self.ip_addr, self.hdt_port))
                    self.stream_hdt.setblocking(0)

                    self.stream_gga = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.stream_gga.settimeout(2.0)
                    self.stream_gga.connect((self.ip_addr, self.gga_port))
                    self.stream_gga.setblocking(0)
                    self.mode = "TCP"

            except Exception as e:
                line = "gpsdrv: exception '{}'".format(e)
                logger.error(line)
                line = "gpsdrv: cannot connect to {}:{}".format(self.ip_addr, port)
                logger.error(line)
                raise Exception(line)

        if self.ip_addr and self.hdt_port != self.gga_port:
            # Launch a reading thread
            self.keepgoing = True
            self.t = threading.Thread(target=self.read_gps_from_two_ports)
            self.t.daemon = True
            self.t.start()
        else:
            # Launch a reading thread
            self.keepgoing = True
            self.t = threading.Thread(target=self.read_gps)
            self.t.daemon = True
            self.t.start()

        logger.debug("gpsdrv: mode {}".format(self.mode))
        logger.debug("gpsdrv: started")

    def read_gps_from_two_ports(self):
        """ Parse GPS sequences """
        while self.keepgoing:
            # Check availability
            rlist, _, _ = select.select([self.stream_gga, self.stream_hdt], [], [], 2.0)
            # Something to read
            if rlist:
                for sock in rlist:
                    if sock is self.stream_gga:
                        data = self.stream_gga.recv(1000).decode()
                        lines = data.split('\r\n')
                        for line in lines:
                            self.parse_xxGGA(line)
                    elif sock is self.stream_hdt:
                        # Read from modem
                        data = self.stream_hdt.recv(1000).decode()
                        lines = data.split('\r\n')
                        for line in lines:
                            self.parse_xxHDT(line)
            else:
                now = time.time()
                if (now - self.time) > 5.0:
                    self.is_new_gps_data = False
                    self.keepgoing = False
                    self.gpsconnectionfailed.emit()

    def read_gps(self):
        """ Parse GPS sequences """
        while self.keepgoing:
            if self.mode == "SERIAL":
                try:
                    line = self.stream.readline().decode()
                    logger.debug("<<< gpsdrv: {:s}".format(line))
                    self.parse_xxGGA(line)
                    self.parse_xxHDT(line)
                except UnicodeDecodeError:
                    pass
                except Exception as e:
                    logger.error(e)
                    line = "gpsdrv: error reading serial gps"
                    logger.error(line)
                    self.is_new_gps_data = False
                    self.keepgoing = False
                    self.gpsconnectionfailed.emit()

            elif self.mode == "TCP":
                # Check availability
                rlist, _, _ = select.select([self.stream], [], [], 2.0)
                # Something to read
                if rlist:
                    # Read from modem
                    data = self.stream.recv(1000).decode()
                    lines = data.split('\r\n')
                    for line in lines:
                        logger.debug("<<< gpsdrv: {:s}".format(line))
                        self.parse_xxGGA(line)
                        self.parse_xxHDT(line)
                else:
                    now = time.time()
                    if (now - self.time) > 5.0:
                        self.is_new_gps_data = False
                        self.keepgoing = False
                        self.gpsconnectionfailed.emit()

            # time.sleep(0.05)

    def parse_xxHDT(self, line):
        """ Parse xxHDT sentence that contains heading in degrees
            $xxHDT,XX.X,T
        """
        self.is_new_gps_data = True
        if line.startswith('HDT', 3):
            field = line.split(',')
            if len(field[1]) > 1:
                self.heading = float(field[1])
                self.orientation_time = time.time()

    def parse_xxGGA(self, line):
        """
        Read xxGGA sequence.
        $xxGGA,time,lat,N/S,lon,E/W,fix,sat,hdop,alt,M,hgeo,M,,*chk
        $xxGGA, 082051.800, 3840.3358, N, 00908.4963, W, 1, 9, 0.86, 2.2, M, 50.7, M,, *46
        """
        self.is_new_gps_data = True
        try:
            if line.startswith('GGA', 3):
                field = line.split(',')
                if len(field) > 5:
                    # time, lat, N/S, lon, E/W
                    self.time = time.time()
                    self.latitude = degree_minute_to_decimal_degree(
                        float(field[2]))
                    if field[3] == 'S':
                        self.latitude = self.latitude * -1.0
                    self.longitude = degree_minute_to_decimal_degree(
                        float(field[4]))
                    if field[5] == 'W':
                        self.longitude = self.longitude * -1.0
                if len(field) > 9:
                    self.quality = int(field[6])
                    self.altitude = float(field[9])
        except Exception as e:
            logger.error("gpsdrv: problem parsing $xxGGA: {}".format(e))
            self.gpsparsingfailed.emit()

    def get_data(self):
        """ Returns last gathered latitude, longitude position and time """
        status = "old_data"
        if self.is_new_gps_data:
            status = "new_data"
        #else:
        #    status = "old_data"
        self.is_new_gps_data = False

        return {"time": self.time,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "heading": self.heading,
                "quality": self.quality,
                "altitude": self.altitude,
                "orientation": self.heading,
                "orientation_time": self.orientation_time,
                "status": status}

    def close(self):
        """Close the open connections."""
        self.keepgoing = False
        try:
            if self.t is not None:
                self.t.join()
        except RuntimeError as e:
            logger.error(str(e.args[0]))
        if self.stream is not None:
            self.stream.close()
        if self.stream_hdt is not None:
            self.stream_hdt.close()
        if self.stream_gga is not None:
            self.stream_gga.close()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        logger.info("Usage:\n  {0:s} ip:port\n  {0:s} /dev/tty*".format(sys.argv[0]))
        exit(0)
    if '/' in sys.argv[1]:
        gps = GPSDriver(serial_port=sys.argv[1], baud_rate=int(sys.argv[2]),
                        debug=True)
        gps.connect()
    else:
        ip, port = sys.argv[1].split(':')
        gps = GPSDriver(ip_addr=ip, hdt_port=int(port), gga_port=int(port),
                        debug=True)
        gps.connect()
    # Keep asking gps
    while True:
        time.sleep(0.5)
        logger.info(gps.get_data())
