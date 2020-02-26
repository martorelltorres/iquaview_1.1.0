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

"""Set of functions and classes to communicate with COLA2 through rosbridge."""

import json
import socket
import threading
import time
import logging

logger = logging.getLogger(__name__)


def send_action_service(ip, port, action_id, params):
    """Call a ROS service of type action."""
    message_dict = {"service": action_id, "op": "call_service",
                    "args": {"param": params}}
    message = json.dumps(message_dict)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.encode())
    response = s.recv(1024)
    data = json.loads(response.decode())
    s.close()
    return data['result']


def send_empty_service(ip, port, action_id):
    """Call a ROS service of type Empty."""
    message_dict = {"service": action_id, "op": "call_service",
                    "args": {}}
    message = json.dumps(message_dict)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.encode())
    response = s.recv(1024)
    data = json.loads(response.decode())
    s.close()
    return data['result']


def send_trigger_service(ip, port, action_id):
    """Call a ROS service of type Trigger."""
    message_dict = {"service": action_id, "op": "call_service",
                    "args": {}}
    message = json.dumps(message_dict)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.encode())
    response = s.recv(1024)
    data = json.loads(response.decode())
    s.close()
    return data


def send_goto_service(ip, port, service, altitude, altitude_mode, x, y, z, surge, tolerance_x, tolerance_y,
                      tolerance_z):
    """Call a ROS service of type GOTO."""
    message_dict = {"service": service,
                    "op": "call_service",
                    "args":
                        {"yaw": 0.0,
                         "altitude": altitude,
                         "altitude_mode": altitude_mode,
                         "blocking": False,
                         "priority": 10,
                         "reference": 1,
                         "position": {
                             "x": x,
                             "y": y,
                             "z": z
                         },
                         "disable_axis": {
                             "x": False,
                             "y": True,
                             "z": False,
                             "roll": True,
                             "pitch": True,
                             "yaw": False
                         },
                         "position_tolerance": {
                             "x": tolerance_x,
                             "y": tolerance_y,
                             "z": tolerance_z
                         },
                         "linear_velocity": {
                             "x": surge,
                             "y": 0.0,
                             "z": 0.5
                         }
                         }
                    }
    message = json.dumps(message_dict)
    logger.info('send: {} '.format(message))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.encode())
    response = s.recv(1024)
    data = json.loads(response.decode())
    s.close()
    return data


def get_ros_param(ip, port, name):
    """Obtain param from ROS param server."""
    message_dict = {"service": "/rosapi/get_param", "op": "call_service",
                    "args": {"name": name}}
    message = json.dumps(message_dict)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.encode())
    response = s.recv(1024)
    data = json.loads(response.decode())
    s.close()
    return data['values']


def set_ros_param(ip, port, name, value):
    """OSet param to ROS param server."""
    """value if number = "1", "1234,12" ... if boolean "True" or "False"
       if string "\"string\""."""

    message_dict = {"service": "/rosapi/set_param", "op": "call_service",
                    "args": {"name": name, "value": value}}
    message = json.dumps(message_dict)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.encode())
    response = s.recv(1024)
    data = json.loads(response.decode())
    s.close()
    return data['result']


class SubscribeToTopic:
    """Class helper to subscribe to ROS topic using rosbridge."""

    def __init__(self, ip, port, topic, timeout=5, buffer_enabled=False):
        try:
            """Class constructor."""
            message_dict = {"op": "subscribe", "topic": topic, "throttle_rate": 1}
            self.message = json.dumps(message_dict)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.settimeout(timeout)
            self.s.connect((ip, port))
            self.buffer = list()
            self.buffer_enabled = buffer_enabled
            self.data = dict()
            self.keepgoing = True
            self.t = threading.Thread(target=self.read_topic)
            self.t.daemon = True
            self.t.start()
        except:
            raise

    def read_topic(self):
        """Infinite loop that updates last topic data."""
        self.s.send(self.message.encode())
        retries = 0
        while self.keepgoing:
            try:
                response = self.s.recv(4096)
                received = True

            except Exception as e:
                received = False
                send_decoded = json.loads(self.message)
                logger.warning("{} {} ".format(send_decoded['topic'], e))
                time.sleep(0.05)
                self.data['valid_data'] = 'old_data'
                retries += 1
                if retries > 5:
                    self.data['valid_data'] = 'disconnected'

            try:
                if received:
                    d = json.loads(response.decode())
                    self.data = d['msg']
                    self.data['valid_data'] = 'new_data'
                    retries = 0
            except Exception as e:
                send_decoded = json.loads(self.message)
                logger.warning("{} {} ".format(send_decoded['topic'], e))
                time.sleep(0.05)
                self.data['valid_data'] = 'corrupt_data'
                retries += 1
                if retries > 25:
                    self.data['valid_data'] = 'disconnected'

            if self.buffer_enabled:
                data = self.data
                response = None
                self.buffer.append(data)

    def get_data(self):
        """Return the last topic data received."""
        return self.data

    def get_buffer(self):
        buffer = self.buffer[:]
        return buffer

    def clear_buffer(self):
        if self.buffer:
            del self.buffer[:]

    def get_keepgoing(self):
        return self.keepgoing

    def close(self):
        self.keepgoing = False
        self.buffer_enabled = False
        self.s.close()


if __name__ == "__main__":
    IP = "127.0.0.1"
    port = 9090
    total_time = SubscribeToTopic(IP, port, "/cola2_safety/total_time")
    time.sleep(3)
    logger.info(total_time.get_data()['total_time'])
