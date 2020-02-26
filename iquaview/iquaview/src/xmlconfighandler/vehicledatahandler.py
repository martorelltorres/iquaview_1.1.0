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
 Helper classes to read the xml structure associated to vehicle data in the AUV config file
"""

from iquaview.src.xmlconfighandler.xmlconfigparser import XMLConfigParser


class VehicleDataHandler(object):
    def __init__(self, config):
        self.filename = config.csettings['configs_path'] + '/' + config.csettings['last_auv_config_xml']
        self.configParser = XMLConfigParser(self.filename)

    def read_topics(self):
        # get Vehicle Data topics
        xml_vehicle_data_topics = self.configParser.first_match(self.configParser.root, "vehicle_data_topics")

        return xml_vehicle_data_topics

    def read_services(self):
        # get Vehicle Data services
        xml_vehicle_data_services = self.configParser.first_match(self.configParser.root, "vehicle_data_services")

        return xml_vehicle_data_services

    def read_launch_list(self):
        # get Launch list
        xml_launch_list = self.configParser.first_match(self.configParser.root, "launch_list")

        return xml_launch_list
