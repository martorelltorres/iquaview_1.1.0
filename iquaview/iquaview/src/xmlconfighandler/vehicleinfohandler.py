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
 Helper classes to read the xml structure associated to vehicle info in the AUV config file
"""

from iquaview.src.xmlconfighandler.auvconfigcheckxml import ConfigCheckXML
from iquaview.src.xmlconfighandler.xmlconfigparser import XMLConfigParser


class VehicleInfoHandler(object):
    def __init__(self, config):
        config_check_xml = ConfigCheckXML(config)
        if not config_check_xml.exists():
            config_check_xml.exec_()

        # last auv config xml
        self.configParser = XMLConfigParser(config.csettings['configs_path']
                                            + '/'
                                            + config.csettings['last_auv_config_xml'])

    def read_configuration(self):
        # get Vehicle Info
        xml_vehicle_info = self.configParser.first_match(self.configParser.root, "vehicle_info")

        return xml_vehicle_info

    def write(self):
        self.configParser.write()
