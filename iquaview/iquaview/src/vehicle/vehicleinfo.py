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
 Class to read and store the xml structure associated to the vehicle_info tag in the AUV config file
"""

from iquaview.src.xmlconfighandler.vehicleinfohandler import VehicleInfoHandler


class VehicleInfo:
    def __init__(self, config):
        self.config = config

        self.vehicle_ip = None
        self.vehicle_port = None
        self.vehicle_type = None
        self.vehicle_name = None
        self.vehicle_width = None
        self.vehicle_length = None
        self.vehicle_code = None
        self.vehicle_namespace = ""
        self.user = None
        self.remote_missions_path = None

        # read XML
        self.read_xml()

    def read_xml(self):
        """

        read the last auv configuration xml loaded, and save the vehicle information

        """
        vi_reader = VehicleInfoHandler(self.config)
        xml_vehicle_info = vi_reader.read_configuration()

        for item in xml_vehicle_info:
            if item.tag == 'vehicle_ip':
                self.vehicle_ip = item.text
            elif item.tag == 'vehicle_port':
                self.vehicle_port = item.text
            elif item.tag == 'vehicle_type':
                self.vehicle_type = item.text
            elif item.tag == 'vehicle_name':
                self.vehicle_name = item.text
            elif item.tag == 'vehicle_width':
                self.vehicle_width = item.text
            elif item.tag == 'vehicle_length':
                self.vehicle_length = item.text
            elif item.tag == 'vehicle_namespace':
                self.vehicle_namespace = item.text
            # back compatibility
            elif item.tag == 'vehicle_code':
                self.vehicle_code = item.text
            elif item.tag == 'user':
                self.user = item.text
            elif item.tag == 'remote_missions_path':
                self.remote_missions_path = item.text

    def get_vehicle_ip(self):
        """
        :return: vehicle ip
        """
        return self.vehicle_ip

    def get_vehicle_port(self):
        """
        :return: vehicle port
        """
        return self.vehicle_port

    def get_vehicle_type(self):
        """
        :return: vehicle type
        """
        return self.vehicle_type

    def get_vehicle_name(self):
        """
        :return: vehicle name
        """
        return self.vehicle_name

    def get_vehicle_width(self):
        """
        :return: vehicle width
        """
        return self.vehicle_width

    def get_vehicle_length(self):
        """
        :return: vehicle length
        """
        return self.vehicle_length

    def get_vehicle_namespace(self):
        """

        :return: vehicle namespace
        """
        return self.vehicle_namespace

    def get_vehicle_code(self):
        """

        :return: vehicle code
        """
        return self.vehicle_code

    def get_vehicle_user(self):
        """
        :return: user
        """
        return self.user

    def get_remote_mission_path(self):
        """
        :return: remote mission path
        """
        return self.remote_missions_path

    def set_vehicle_ip(self, vehicle_ip):
        self.vehicle_ip = vehicle_ip

    def set_vehicle_port(self, vehicle_port):
        self.vehicle_port = vehicle_port

    def set_vehicle_type(self, vehicle_type):
        self.vehicle_type = vehicle_type

    def set_vehicle_name(self, vehicle_name):
        self.vehicle_name = vehicle_name

    def set_vehicle_width(self, vehicle_width):
        self.vehicle_width = vehicle_width

    def set_vehicle_length(self, vehicle_length):
        self.vehicle_length = vehicle_length

    def set_vehicle_namespace(self, vehicle_namespace):
        self.vehicle_namespace = vehicle_namespace

    def set_vehicle_code(self, vehicle_code):
        self.vehicle_code = vehicle_code

    def set_user(self, user):
        self.user = user

    def set_remote_mission_path(self, remote_missions_path):
        self.remote_missions_path = remote_missions_path

    def save(self):
        """

        save the vehicle info inside the last auv configuration xml

        """
        # last auv config xml
        vi_handler = VehicleInfoHandler(self.config)
        xml_vehicle_info = vi_handler.read_configuration()

        for item in xml_vehicle_info:
            if item.tag == 'vehicle_ip':
                item.text = str(self.vehicle_ip)
            elif item.tag == 'vehicle_port':
                item.text = str(self.vehicle_port)
            elif item.tag == 'vehicle_type':
                item.text = str(self.vehicle_type)
            elif item.tag == 'vehicle_name':
                item.text = str(self.vehicle_name)
            elif item.tag == 'vehicle_width':
                item.text = str(self.vehicle_width)
            elif item.tag == 'vehicle_length':
                item.text = str(self.vehicle_length)
            elif item.tag == 'vehicle_namespace':
                item.text = str(self.vehicle_namespace)
            elif item.tag == 'vehicle_code':
                item.text = str(self.vehicle_code)
            elif item.tag == 'user':
                item.text = str(self.user)
            elif item.tag == 'remote_missions_path':
                item.text = str(self.remote_missions_path)

        vi_handler.write()
