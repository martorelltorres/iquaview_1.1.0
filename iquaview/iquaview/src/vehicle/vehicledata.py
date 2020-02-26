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
 Class to subscribe to topics
"""
import logging
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtWidgets import QMessageBox
from iquaview.src.cola2api.cola2_interface import SubscribeToTopic
from iquaview.src.xmlconfighandler.vehicledatahandler import VehicleDataHandler

logger = logging.getLogger(__name__)


class VehicleData(QObject):
    state_signal = pyqtSignal()

    def __init__(self, config, vehicle_info):
        super(VehicleData, self).__init__()

        self.config = config
        self.vehicle_info = vehicle_info

        self.subscribed = False
        self.state = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)

        self.topics = dict()
        self.current_data = dict()

        self.topic_names = self.read_xml_topics()
        #read services from xml
        self.services = self.read_xml_services()
        #read lauch list
        self.launchlist = self.read_xml_launch_list()

    def read_xml_topics(self):
        """

        Read a vehicle data topics from a XML

        :return: return vehicle data topics in a dictionary
        """
        vd_handler = VehicleDataHandler(self.config)
        # get vehicle data topics
        xml_vehicle_data_topics = vd_handler.read_topics()

        topic_names = dict()

        for topic in xml_vehicle_data_topics:
            topic_names[topic.get('id')] = topic.text

        topic_names['rosout'] = '/rosout_agg'

        return topic_names

    def read_xml_services(self):
        """

        Read a vehicle data services from a XML

        :return: return vehicle data services in a dictionary
        """
        vd_handler = VehicleDataHandler(self.config)
        # get vehicle data topics
        xml_vehicle_data_services = vd_handler.read_services()

        services_names = dict()

        for service in xml_vehicle_data_services:
            services_names[service.get('id')] = service.text

        logger.debug("Services loaded: ", services_names)

        return services_names

    def read_xml_launch_list(self):
        """

        Read a launch list from a XML

        :return: return launchs in a dictionary
        """
        vd_handler = VehicleDataHandler(self.config)
        # get launch list
        xml_launch_list = vd_handler.read_launch_list()

        launch_list = dict()

        for launch in xml_launch_list:
            launch_list[launch.get('id')] = launch.text

        logger.debug("Launch commands loaded: ", launch_list)

        return launch_list

    def subscribe_topics(self):

        """
        Subscribe topics
        """

        ip = self.vehicle_info.get_vehicle_ip()
        port = 9091
        vehicle_namespace = self.vehicle_info.get_vehicle_namespace()
        try:
            for key, value in self.topic_names.items():
                if key == 'rosout':
                    self.topics[key] = SubscribeToTopic(ip, port, value, 30, True)
                elif key == 'thruster setpoints':
                    self.topics[key] = None
                elif 'usage' in key:
                    self.topics[key] = SubscribeToTopic(ip, port, vehicle_namespace+value, 10)
                else:
                    self.topics[key] = SubscribeToTopic(ip, port, vehicle_namespace+value)

            self.subscribed = True

            self.timer.start(1000)

        except:
            logger.error("Connection with COLA2 could not be established")
            QMessageBox.critical(self.parent(),
                                 "Connection with AUV Failed",
                                 "Connection with COLA2 could not be established",
                                 QMessageBox.Close)
            self.state_signal.emit()
            self.subscribed = False

    def unsubscribe_topic(self, key):
        """
        Unsubscribe topic with key key
        :param key: the key of the topic in the xml
        """
        if self.topics[key] is not None:
            self.topics[key].close()

    def subscribe_topic(self, key):
        """
        Subscribe topic with key key
        :param key: the key of the topic in the xml
        """
        ip = self.vehicle_info.get_vehicle_ip()
        port = 9091
        vehicle_namespace = self.vehicle_info.get_vehicle_namespace()
        value = self.topic_names[key]
        if self.topics[key] is not None:
            self.topics[key].close()
        self.topics[key] = SubscribeToTopic(ip, port, vehicle_namespace+value)

    def is_subscribed_to_topic(self, key):
        """
        Get True if is subscribed to topic with key 'key', otherwise False
        :param key: key of the topic
        :return: Return True if is subscribed to topic with key 'key', otherwise False
        """
        if self.topics[key] is not None and self.topics[key].get_keepgoing():
            return True
        else:
            return False

    def refresh_data(self):
        """
        start timer and refresh data

        """
        if self.subscribed:
            for key, value in self.topics.items():
                if key == 'rosout':
                    buffer = value.get_buffer()
                    self.set_buffer(key, buffer)
                    value.clear_buffer()

                else:
                    if value is not None:
                        data = value.get_data()
                        self.set_data(key, data)

    def get_vehicle_status(self):
        """ get vehicle status."""
        return self.current_data['vehicle status']

    def get_safety_supervisor_status(self):
        """ Get safety supervisor status."""
        return self.current_data['safety supervisor status']

    def get_nav_sts(self):
        """ Get navigation status."""
        return self.current_data['navigation status']

    def get_desired_pose(self):
        """ Get merged world waypoint req. (Desires pose)"""
        return self.current_data['merged world waypoint req']

    def get_desired_twist(self):
        """ Get merged body velocity req. (Desired twist)"""
        return self.current_data['merged body velocity req']

    def get_total_time(self):
        """ Get total time."""
        if self.current_data.get('total time') is None:
            return None

        return self.current_data['total time']

    def get_watchdog(self):
        """ Get watchdog."""
        if self.current_data.get('watchdog') is None:
            return None

        return self.current_data['watchdog']

    def get_goto_status(self):
        """ Get goto status"""
        if self.current_data is None:
            return None
        if self.current_data.get('goto status') is None:
            return None

        return self.current_data['goto status']

    def get_thrusters_status(self):
        """ Get thrusters status"""
        if self.current_data is None:
            return None
        if self.current_data.get('vehicle status') is None:
            return None
        if self.current_data.get('vehicle status').get('thrusters_enabled') is None:
            return None
        return self.current_data['vehicle status']['thrusters_enabled']

    def get_active_controller(self):
        """ Get active controller"""
        if self.current_data is None:
            return None
        if self.current_data.get('vehicle status') is None:
            return None
        if self.current_data.get('vehicle status').get('active_controller') is None:
            return None
        return self.current_data['vehicle status']['active_controller']

    def get_battery_charge(self):
        """ Get battery charge"""
        if self.current_data is None:
            return None
        if self.current_data.get('vehicle status') is None:
            return None
        if self.current_data.get('vehicle status').get('battery_charge') is None:
            return None
        return self.current_data['vehicle status']['battery_charge']

    def get_captain_state(self):
        """ Get captain state """
        if self.current_data is None:
            return None
        if self.current_data.get('vehicle status') is None:
            return None
        if self.current_data.get('vehicle status').get('captain_state') is None:
            return None
        return self.current_data['vehicle status']['captain_state']

    def get_cpu_usage(self):
        """get cpu usage"""
        if self.current_data is None:
            return None
        if self.current_data.get('cpu usage') is None:
            return None
        if self.current_data.get('cpu usage').get('data') is None:
            return None
        return self.current_data['cpu usage']['data']

    def get_ram_usage(self):
        """get ram usage"""
        if self.current_data is None:
            return None
        if self.current_data.get('ram usage') is None:
            return None
        if self.current_data.get('ram usage').get('data') is None:
            return None
        return self.current_data['ram usage']['data']

    def get_thruster_setpoints(self):
        """ get thruster setpoints topic"""
        if self.current_data is None:
            return None
        if self.current_data.get('thruster setpoints') is None:
            return None
        return self.current_data['thruster setpoints']

    def get_mission_active(self):
        """ Get mission active"""
        if self.current_data is None:
            return None
        if self.current_data.get('vehicle status') is None:
            return None
        if self.current_data.get('vehicle status').get('mission_active') is None:
            return None
        return self.current_data['vehicle status']['mission_active']

    def get_total_steps(self):
        """ Get total steps"""
        if self.current_data is None:
            return None
        if self.current_data.get('vehicle status') is None:
            return None
        if self.current_data.get('vehicle status').get('total_steps') is None:
            return None
        return self.current_data['vehicle status']['total_steps']

    def get_status_code(self):
        """ Get the status code"""
        if self.current_data is None:
            return None
        if self.current_data.get('safety supervisor status') is None:
            return None
        if self.current_data.get('safety supervisor status').get('status_code') is None:
            return None

        return self.current_data['safety supervisor status']['status_code']

    # back compatibility
    def get_error_code(self):
        """ Get the error code"""
        if self.current_data is None:
            return None
        if self.current_data.get('safety supervisor status') is None:
            return None
        if self.current_data.get('safety supervisor status').get('error_code') is None:
            return None

        return self.current_data['safety supervisor status']['error_code']

    def get_recovery_action(self):
        """ Get recovery action"""
        if self.current_data is None:
            return None

        if self.current_data.get('safety supervisor status') is None:
            return None

        recovery_action = self.current_data['safety supervisor status']['recovery_action']
        error_level = recovery_action['error_level']
        error_string = recovery_action['error_string']
        return error_level, error_string

    def get_rosout(self):
        """ Get rosout"""
        if self.current_data.get('rosout') is None:
            return None

        if not self.current_data['rosout']:
            return None

        return self.current_data['rosout']

    def get_calibrate_magnetometer_service(self):
        """ Get calibrate magnetometer service"""
        if self.services is None:
            return None
        if self.services.get('calibrate magnetometer') is None:
            return None
        return self.services['calibrate magnetometer']

    def get_stop_magnetometer_calibration_service(self):
        """ Get stop magnetometer calibration"""
        if self.services is None:
            return None
        if self.services.get('stop magnetometer calibration') is None:
            return None
        return self.services['stop magnetometer calibration']

    def get_keep_position_service(self):
        """ Get keep position service"""
        if self.services is None:
            return None
        if self.services.get('keep position') is None:
            return None

        return self.services['keep position']

    def get_disable_keep_position_service(self):
        """ Get disable keep position service"""
        if self.services is None:
            return None
        if self.services.get('disable keep position') is None:
            return None

        return self.services['disable keep position']

    def get_disable_all_keep_positions_service(self):
        """ Get disable safety keep position service"""
        if self.services is None:
            return None
        if self.services.get('disable all keep positions') is None:
            return None

        return self.services['disable all keep positions']

    def get_reset_timeout_service(self):
        """ Get reset timeout service"""
        if self.services is None:
            return None
        if self.services.get('reset timeout') is None:
            return None

        return self.services['reset timeout']

    def get_goto_service(self):
        """ Get goto service"""
        if self.services is None:
            return None
        if self.services.get('enable goto') is None:
            return None

        return self.services['enable goto']

    def get_disable_goto_service(self):
        """ Get disable goto service"""
        if self.services is None:
            return None
        if self.services.get('disable goto') is None:
            return None

        return self.services['disable goto']

    def get_enable_thrusters_service(self):
        """ Get enable thrusters service"""
        if self.services is None:
            return None
        if self.services.get('enable thrusters') is None:
            return None

        return self.services['enable thrusters']

    def get_disable_thrusters_service(self):
        """ Get disable thrusters service"""
        if self.services is None:
            return None
        if self.services.get('disable thrusters') is None:
            return None

        return self.services['disable thrusters']

    def get_enable_mission_service(self):
        """ Get enable mission service"""
        if self.services is None:
            return None
        if self.services.get('enable mission') is None:
            return None

        return self.services['enable mission']

    def get_disable_mission_service(self):
        """get disable mission service"""
        if self.services is None:
            return None
        if self.services.get('disable mission') is None:
            return None

        return self.services['disable mission']

    def get_teleoperation_launch(self):
        """ get teleoperation launch"""
        if self.launchlist is None:
            return None
        if self.launchlist.get('teleoperation') is None:
            return None

        return self.launchlist['teleoperation']

    def set_data(self, identifier, data):
        """
        set data 'data' in  self.current_data list with key 'identifier'

        :param identifier: key to identify the data
        :param data: new data to update
        """

        if data:
            self.current_data[identifier] = data
        else:
            self.state_signal.emit()

    def set_buffer(self, identifier, buffer):
        """
        set data 'buffer' in  self.current_data list with key 'identifier'

        :param identifier: key to identify the data
        :param buffer: new data to update
        """

        self.current_data[identifier] = buffer

    def is_subscribed(self):
        """ get subscribed state"""
        return self.subscribed

    def disconnect(self):
        """ Disconnect subscribers and stop timer"""
        self.subscribed = False

        for key, subscriber in self.topics.items():
            if subscriber is not None:
                subscriber.close()

        self.timer.stop()
