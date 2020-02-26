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
 Class to handle the loading/saving of the different IquaView configuration parameters
"""

import yaml as yaml
import os.path
import logging
from shutil import copytree

logger = logging.getLogger(__name__)

DEFAULTCONFIG = {'canvas_marker_mode': 'auto',
                 'canvas_marker_scale': 400,
                 'configs_path': '/auv_configs',
                 'coordinate_format': 'degree',
                 'default_project_name': 'guiproject.qgs',
                 'gps_ip': '127.0.0.1',
                 'vrp_offset_x': 0.0,
                 'vrp_offset_y': 0.0,
                 'gps_offset_x': 4.0,
                 'gps_offset_y': 3.0,
                 'gps_offset_z': 0.0,
                 'gps_offset_heading': 0.0,
                 'gps_hdt_port': 4000,
                 'gps_gga_port': 4000,
                 'gps_serial': 'false',
                 'gps_serial_baudrate': 4800,
                 'gps_serial_port': 'internalGPS',
                 'joystick_device': '/dev/input/js0',
                 'last_auv_config_xml': 'sparus2_configuration.xml',
                 'last_open_project': '',
                 'usbl_ip': '127.0.0.1',
                 'usbl_offset_x': -3.0,
                 'usbl_offset_y': -2.0,
                 'usbl_offset_z': 0.0,
                 'usbl_offset_heading': 0.0,
                 'usbl_own_id': 1,
                 'usbl_port': 9200,
                 'usbl_target_id': 2,
                 'vessel_length': 15.0,
                 'vessel_width': 7.0,
                 'visibility_north_arrow': 0.0,
                 'visibility_scale_bar': 0.0
                 }


class Config:
    def __init__(self):
        self.settings = None
        self.csettings = None
        self.loaded_path = ''

    def load(self):

        home = os.path.expanduser('~')
        iquaview_dir = os.path.join(home, '.iquaview')
        if not os.path.isdir(iquaview_dir):
            # create folder
            os.makedirs(iquaview_dir)

        # todo:ask user for custom configs_path
        auv_configs_path = os.path.dirname(os.path.abspath(__file__))
        auv_configs_path = auv_configs_path + '/../auv_configs'
        if not os.path.isdir(home + '/auv_configs'):
            copytree(auv_configs_path, home + '/auv_configs')

        # if app.config not exist or is empty
        if not os.path.isfile(iquaview_dir + "/app.config") or os.stat(iquaview_dir + "/app.config").st_size == 0:
            # create app.config
            f = open(iquaview_dir + "/app.config", "w+")

            # set configs_path on app.config
            DEFAULTCONFIG['configs_path'] = home + '/auv_configs'
            for key, value in DEFAULTCONFIG.items():
                f.write(key + ': ' + str(value) + '\n')
            f.close()

        path = os.path.join(iquaview_dir, "app.config")

        with open(path, 'r') as f:
            self.settings = yaml.load(f)
            if self.settings is None:
                self.settings = {}
                self.csettings = {}
            else:
                for key, value in DEFAULTCONFIG.items():
                    if key in self.settings:
                        pass
                    else:
                        self.settings[key] = value

            self.loaded_path = path

    def save(self, path=None):
        """
        Save the settings to disk. The last path is used if no path is given.
        :param path:
        :return:
        """
        if not path:
            path = self.loaded_path

        with open(path, 'w') as f:
            yaml.dump(data=self.settings, stream=f, default_flow_style=False)

        logger.debug(self.settings)

    @property
    def settings(self):
        return self.__settings

    @settings.setter
    def settings(self, settings):
        self.__settings = settings

    @property
    def csettings(self):
        return self.__csettings

    @csettings.setter
    def csettings(self, csettings):
        self.__csettings = csettings
