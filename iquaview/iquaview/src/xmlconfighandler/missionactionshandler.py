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
 Helper classes to read the xml structure associated to actions in the AUV config file
"""
import logging
from iquaview.src.xmlconfighandler.xmlconfigparser import XMLConfigParser

logger = logging.getLogger(__name__)


class MissionActionsHandler(object):
    def __init__(self, config):

        self.filename = config.csettings['configs_path'] + '/' + config.csettings['last_auv_config_xml']
        logger.debug("Reading Mission Actions XML...")
        self.configParser = XMLConfigParser(self.filename)

    def get_actions(self):
        """
        Get a list of action from xml structure configuration
        :return: return a list of actions from a xml structure configuration
        """
        # get misison actions
        mission_actions = self.configParser.first_match(self.configParser.root, "mission_actions")
        # all actions
        actions = self.configParser.all_matches(mission_actions, "action")
        return actions

    def get_name_from_param(self, param):
        """ Get name from 'param'"""
        return self.configParser.first_match(param, "param_name").text

    def get_type_from_param(self, param):
        """ Get type from 'param'"""
        return self.configParser.first_match(param, "param_type").text
