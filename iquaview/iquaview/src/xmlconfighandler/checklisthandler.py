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
 Helper classes to read the xml structure associated to check lists in the AUV config file
"""

from iquaview.src.xmlconfighandler.xmlconfigparser import XMLConfigParser


class CheckListHandler(object):
    def __init__(self, config):
        self.filename = config.csettings['configs_path'] + '/' + config.csettings['last_auv_config_xml']
        self.configParser = XMLConfigParser(self.filename)

    def get_check_lists(self):
        """
        Get check_lists
        :return: return all lists from check_lists
        """
        chk_lists = self.configParser.first_match(self.configParser.root, "check_lists")
        # all check_list in check_lists
        lists = self.configParser.all_matches(chk_lists, "check_list")

        return lists

    def get_items_from_checklist(self, checklist_name):
        """
        Get all items from a check_list with name 'checklist_name'
        :param checklist_name: name of the check_list
        :return: return a list of items from a check_list with name 'checklist_name'
        """
        chk_lists = self.configParser.first_match(self.configParser.root, "check_lists")
        # get specific check_list by attribute chk_name
        xml_check_list = self.configParser.first_match(chk_lists, "check_list[@id='" + checklist_name + "']")
        # all check_list items
        check_items = self.configParser.all_matches(xml_check_list, "check_item")

        return check_items

    def get_description_from_item(self, item):
        """ Get description field from 'item'
        :param item: item is a check_item from xml structure configuration
        :return: return description field from 'item'
        """
        description = self.configParser.first_match(item, "description")
        return description

    def get_check_topics_from_item(self, item):
        """
        Get check_topics from 'item'
        :param item: item is a check_item from xml structure configuration
        :return: return a list of check_topics from 'item'
        """
        check_topics = self.configParser.all_matches(item, "check_topic")
        return check_topics

    def get_check_actions_from_item(self, item):
        """
        Get check_actions from 'item'
        :param item: item is a check_item from xml structure configuration
        :return: return a list of check_actions from 'item'
        """
        check_actions = self.configParser.all_matches(item, "check_action")
        return check_actions
