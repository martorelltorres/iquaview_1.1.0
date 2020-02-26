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
    Class to manage multiple plugins
"""
from importlib import util

from PyQt5.QtCore import QObject

from iquaview.src.plugins.USBL.usblmodule import USBLModule


class PluginManager(QObject):

    def __init__(self, proj, canvas, config, vehicle_info, mission_sts, boat_pose_action, menubar, view_menu_toolbar):
        super(QObject, self).__init__()

        self.plugin_manager = menubar.addMenu("Plugins")

        # USBL
        if util.find_spec('usblcontroller') is not None:
            self.usbl_module = USBLModule(canvas, config, vehicle_info, mission_sts,
                                          boat_pose_action, self.plugin_manager, view_menu_toolbar)

    def get_usbl(self):
        return self.usbl_module

    def disconnect_plugins(self):
        if util.find_spec('usblcontroller') is not None:
            self.usbl_module.disconnect_usbl_dw()
