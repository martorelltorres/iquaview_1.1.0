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
 Helper classes to read the xml structure associated to the ros_params tag in the AUV config file
"""

import logging
from iquaview.src.xmlconfighandler.xmlconfigparser import XMLConfigParser
from iquaview.src.cola2api import cola2_interface

logger = logging.getLogger(__name__)


class Field(object):
    def __init__(self, field_name=None, field_type=None):
        self.field_name = field_name
        self.field_type = field_type

    def get_name(self):
        return self.field_name

    def get_type(self):
        return self.field_type


class FieldArray(object):
    def __init__(self, field_array_name=None, field_array_type=None, field_array_size=None):
        self.field_array_name = field_array_name
        self.field_array_type = field_array_type
        self.field_array_size = field_array_size

    def get_name(self):
        return self.field_array_name

    def get_type(self):
        return self.field_array_type

    def get_size(self):
        return self.field_array_size


class Param(object):
    def __init__(self, description=None, param_value=None):
        self.description = description
        self.field = None
        self.field_array = None
        self.param_value = param_value

    def get_description(self):
        return self.description

    def get_value(self):
        return self.param_value

    def get_name(self):
        if self.field is not None:
            return self.field.get_name()
        else:
            return self.field_array.get_name()

    def get_type(self):
        if self.field is not None:
            return self.field.get_type()
        else:
            return self.field_array.get_type()

    def get_array_size(self):
        if self.field_array is not None:
            return self.field_array.get_size()

    def set_field(self, field_name, field_type):
        self.field = Field(field_name, field_type)

    def set_field_array(self, field_array_name, field_array_type, field_array_size):
        self.field_array = FieldArray(field_array_name, field_array_type, field_array_size)

    def is_array(self):
        return self.field_array is not None

    def set_value(self, value):
        self.param_value = value


class Section(object):
    def __init__(self, description=None, params=None, action_id=None):
        self.description = description
        self.params = list()
        self.action_id = action_id

        if params is not None:
            for param in params:
                self.params.append(param)

    def set_description(self, description):
        self.description = description

    def set_action_id(self, action_id):
        self.action_id = action_id

    def add_param(self, param):
        self.params.append(param)

    def get_description(self):
        return self.description

    def get_params(self):
        return self.params

    def get_action_id(self):
        return self.action_id


class RosParamsReader(object):
    def __init__(self, config, ip, port, vehicle_namespace):

        self.filename = config.csettings['configs_path'] + '/' + config.csettings['last_auv_config_xml']
        self.ip = ip
        self.port = port
        self.vehicle_namespace = vehicle_namespace

    def read_configuration(self):
        logger.debug("Reading  ros_params XML...")
        config_parser = XMLConfigParser(self.filename)
        # get ros_params
        ros_params = config_parser.first_match(config_parser.root, "ros_params")
        # all sections in ros_params
        sections = config_parser.all_matches(ros_params, "section")

        # initialize empty list of sections
        section_list = list()

        # fill section values by reading xml and corresponding param values in the param server
        for section in sections:
            sect = Section()
            logger.debug("section.tag")
            for value in section:
                # description
                if value.tag == 'description':
                    logger.debug("     {} {}".format(value.tag, value.text))
                    sect.set_description(value.text)
                # param
                if value.tag == 'param':
                    logger.debug("     {}".format(value.tag))
                    desc = config_parser.first_match(value, "description").text
                    param = Param(desc)

                    field = config_parser.first_match(value, "field")
                    if field is not None:
                        f_name = config_parser.first_match(field, "field_name").text
                        f_type = config_parser.first_match(field, "field_type").text
                        param.set_field(f_name, f_type)
                    else:
                        field_array = config_parser.first_match(value, "field_array")
                        f_name = config_parser.first_match(field_array, "field_array_name").text
                        f_type = config_parser.first_match(field_array, "field_array_type").text
                        f_size = config_parser.first_match(field_array, "field_array_size").text
                        param.set_field_array(f_name, f_type, f_size)

                    p_value = cola2_interface.get_ros_param(self.ip, self.port,
                                                            self.vehicle_namespace + f_name)['value']
                    param.set_value(p_value)
                    logger.debug("         {}".format(desc))
                    logger.debug("         {}".format(f_name))
                    logger.debug("         {}".format(p_value))
                    logger.debug("         {}".format(f_type))

                    sect.add_param(param)
                # action_id
                if value.tag == 'action_id':
                    logger.debug("     {} {}".format(value.tag, value.text))
                    sect.set_action_id(value.text)

            section_list.append(sect)
        return section_list
