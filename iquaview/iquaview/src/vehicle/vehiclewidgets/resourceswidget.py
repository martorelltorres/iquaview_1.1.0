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
 Widget to monitor cpu and ram usage, it also contains batterywidget
"""


from PyQt5.QtWidgets import QWidget
from iquaview.src.ui.ui_resourceswidget import Ui_ResourcesWidget
from iquaview.src.vehicle.vehiclewidgets import batterywidget


class ResourcesWidget(QWidget, Ui_ResourcesWidget):

    def __init__(self, parent=None):
        super(ResourcesWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Resources Usage Widget")

        self._cpu = 0
        self._ram = 0
        self._charge = 0

        self.battery = batterywidget.BatteryWidget()
        self.battery_layout.addWidget(self.battery)

    def set_data(self, battery_charge, cpu, ram):
        """
        Set battery charge, cpu usage and ram usage on widget
        :param battery_charge: charge of battery
        :param cpu: cpu usage
        :param ram:  ram usage
        """
        if battery_charge is not None:
            self.battery.set_data(battery_charge)
        if cpu is not None:
            self.cpu_usage_label.setText(str(int(cpu))+'%')
        if ram is not None:
            self.ram_usage_label.setText(str(int(ram))+'%')


