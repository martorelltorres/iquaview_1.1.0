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
 Classes to parse a check list xml file and dynamically load the
 items into dialogs to show the data to the user so that he/she
 can evaluate the correctness of the data.
"""

import logging
from iquaview.src.xmlconfighandler.checklisthandler import CheckListHandler
from iquaview.src.vehicle.checklist.loadcheckactiondlg import LoadCheckActionDialog
from iquaview.src.vehicle.checklist.loadcheckparamdlg import LoadCheckParamDialog
from iquaview.src.vehicle.checklist.loadsummarydlg import LoadSummaryDialog
from iquaview.src.vehicle.checklist.topic import Topic
from PyQt5.QtWidgets import QDialog

logger = logging.getLogger(__name__)


class CheckTopic(object):
    """Checklist Topic"""

    def __init__(self, name=None, topic=None):
        self.name = name
        self.topic = Topic()
        logger.debug("           Name: {}".format(self.name.text))
        self.topic.set_topic(topic)

    def get_ct_topic(self, ip, port, vehicle_namespace):
        return self.topic.get_topic_data(ip, port, vehicle_namespace)


class CheckAction(object):
    """Checklist Action"""

    def __init__(self, name=None, action_id=None, parameters=None):
        self.name = name
        self.action_id = action_id
        self.parameters = list()
        logger.debug("           Name: {}".format(self.name.text))
        logger.debug("           Action ID: {}".format(self.action_id.text))

        for param in parameters:
            self.parameters.append(param.text)
            logger.debug("             Param: ".format(param.text))

    def get_name(self):
        return self.name.text

    def get_action_id(self):
        return self.action_id.text

    def get_parameters(self):
        return self.parameters


class CheckItem(object):
    """ Checklist Item"""

    def __init__(self, description=None):
        self.description = description
        self.check_topics = list()
        self.check_actions = list()
        self.correct_values = False


def read_configuration(vehicle_info, config, chk_name):
    """
    Read the checklist 'chk_name' from configuration 'config' and
    load Actions and Params from checklist.
    Finally load Summary Dialog.

    :param vehicle_info:
    :type vehicle_info: VehicleInfo
    :param config:
    :tyep config: Config
    :param chk_name:
    :type  chk_name: String

    """
    ip = vehicle_info.get_vehicle_ip()
    port = 9091
    vehicle_namespace = vehicle_info.get_vehicle_namespace()

    cl_handler = CheckListHandler(config)
    # all check_list items
    check_items = cl_handler.get_items_from_checklist(chk_name)

    n = 0
    check_list = list()
    logger.debug("-------ITEMS--------")
    # for each list item
    while 0 <= n < len(check_items):
        result = False
        load_dialog = None
        item = check_items[n]
        check_item = CheckItem()
        logger.debug(item.tag)
        # get all matches
        description = cl_handler.get_description_from_item(item)
        check_topics = cl_handler.get_check_topics_from_item(item)
        check_actions = cl_handler.get_check_actions_from_item(item)

        logger.debug("     {}".format(description.tag))
        # description
        logger.debug("          {}".format(description.text))
        check_item.description = description.text
        # check topic
        if check_topics:
            for c_topic in check_topics:
                check_topic = CheckTopic(c_topic[0], c_topic[1])
                check_item.check_topics.append(check_topic)

            load_dialog = LoadCheckParamDialog(check_item.description, check_item.check_topics, n,
                                               ip, port, vehicle_namespace)
            result = load_dialog.exec_()

        # check action
        elif check_actions:
            for c_action in check_actions:
                check_action = CheckAction(c_action[0], c_action[1], c_action[2])
                check_item.check_actions.append(check_action)
            # TODO accept more than one check_action in dialog
            load_dialog = LoadCheckActionDialog(ip,
                                                port,
                                                vehicle_namespace,
                                                check_item.description, check_action.get_name(),
                                                check_action.get_action_id(),
                                                check_action.get_parameters(), n)
            result = load_dialog.exec_()

        if result == QDialog.Accepted:
            if not load_dialog.back_clicked():
                check_item.correct_values = load_dialog.isChecked()
                check_list.append(check_item)
                n += 1
            else:
                n -= 1
                if n >= 0:
                    check_list.pop()
        else:
            # on close dialog, break while and put n=0 to no show summary
            n = 0
            break

    logger.debug("--------------------")
    # if check more than 1 item, show summary
    if n > 0:
        summary = LoadSummaryDialog(chk_name)
        summary.set_summary(check_list)
        summary.exec_()
