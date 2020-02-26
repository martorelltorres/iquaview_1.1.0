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
import logging
from iquaview.src.utils.busywidget import BusyWidget
from iquaview.src.cola2api.cola2_interface import SubscribeToTopic

logger = logging.getLogger(__name__)


class CheckListField(object):
    def __init__(self, name=None, description=None, value=None):
        self.field_name = name
        self.field_description = description
        self.field_value = value

    def set_value(self, value):
        self.field_value = value


class Topic(object):
    def __init__(self):
        self.fields = list()
        self.topic_name = None

    def set_topic(self, topic=None):
        for value in topic:
            if value.tag == "topic_name":
                logger.debug("             Topic Name: {}".format(value.text))
                self.topic_name = value
            if value.tag == "field":
                field = CheckListField(value[0], value[1])
                self.fields.append(field)

    def get_topic_data(self, ip, port, vehicle_namespace):
        # topic subscribe
        subs = SubscribeToTopic(ip, port, vehicle_namespace+self.topic_name.text)
        self.bw = BusyWidget(title="Getting data...")
        self.bw.on_start()
        self.bw.exec_()
        try:
            for field in self.fields:
                logger.debug("             Field:")
                logger.debug("                 Field Name: {}".format(field.field_name.text))
                logger.debug("                 Field Description: {}".format(field.field_description.text))
                data = subs.get_data()
                if data['valid_data'] == 'new_data':
                    # split name
                    name_list = field.field_name.text.split("/")
                    for item in name_list:
                        data = data[item]
                    field.set_value(data)
                logger.debug("                 Topic value -> {} ".format(field.field_value))
        except Exception as e:
            logger.debug("Impossible to catch fields: ".format(e))
            field.set_value("ERROR: impossible to read")

        subs.close()
        return self.fields
