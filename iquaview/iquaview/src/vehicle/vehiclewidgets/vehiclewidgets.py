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
Sets the widget containing all the graphical vehicle widgets
including battery, compass, roll/pitch, depth/altitude, velocimeter,
and table of current and desired pose requests.
"""

import matplotlib

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, pyqtSignal

from iquaview.src.vehicle.vehiclewidgets import (compasswidget,
                                                 rollpitchwidget,
                                                 tablewidget,
                                                 resourceswidget,
                                                 setpointswidget)
from iquaview.src.vehicle.vehiclewidgets import depthaltitudewidget, velocimeterwidget

from iquaview.src.ui.ui_vehicle_widgets import Ui_VehicleWidgets

matplotlib.use("Qt5Agg")


class VehicleWidgets(QWidget, Ui_VehicleWidgets):
    """

    This class contains all subgraphicwidgets

    """

    refresh_signal = pyqtSignal()

    def __init__(self, vehicle_info, vehicledata, parent=None):
        super(VehicleWidgets, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_timer)

        self.table = None

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.vehicle_info = vehicle_info
        self.vehicle_data = vehicledata
        self.layout = self.scrollAreaWidgetContents.layout()
        self.refresh_signal.connect(self.refresh)
        self.setMinimumHeight(250)

    def file_quit(self):
        self.close()
        self.disconnect()

    def compass_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.compass.show()
        else:
            self.compass.hide()

    def depthaltitude_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.depthaltitudecanvas.show()
        else:
            self.depthaltitudecanvas.hide()

    def rollpitch_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.rollpitch.show()
        else:
            self.rollpitch.hide()

    def velocimeter_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.velocimeter.show()
        else:
            self.velocimeter.hide()

    def table_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.table.show()
        else:
            self.table.hide()

    def resources_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.resourcesusage.show()
        else:
            self.resourcesusage.hide()

    def setpoints_state_changed(self):
        sender = self.sender()
        if sender.isChecked():
            self.setpoints.show()
        else:
            self.setpoints.hide()

    def connect(self):
        self.resourcesusage = resourceswidget.ResourcesWidget()
        self.depthaltitudecanvas = depthaltitudewidget.DepthAltitudeCanvas(self, f_width=3, f_height=2, dpi=100)
        self.compass = compasswidget.CompassWidget()
        self.rollpitch = rollpitchwidget.RollPitchWidget()
        self.velocimeter = velocimeterwidget.VelocimeterWidget()
        self.table = tablewidget.TablePoseWidget(self.vehicle_info, self.vehicle_data)
        self.setpoints = setpointswidget.SetpointsWidget()

        self.layout.addWidget(self.resourcesusage)
        self.layout.addWidget(self.compass)
        self.layout.addWidget(self.rollpitch)
        self.layout.addWidget(self.velocimeter)
        self.layout.addWidget(self.depthaltitudecanvas)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.setpoints)
        self.scrollAreaWidgetContents.setFocus()

        self.connected = True
        self.start_updating_data()

    def start_updating_data(self):
        self.table.connect()
        self.timer.start(1000)

    def start_timer(self):
        if self.connected:
            self.refresh_signal.emit()

    def refresh(self):

        data = self.vehicle_data.get_nav_sts()
        if data is not None and data['valid_data'] == 'new_data':
            self.depthaltitudecanvas.set_data(data)
            self.compass.set_data(data)
            self.rollpitch.set_data(data)
            self.velocimeter.set_data(data)

        battery_charge = self.vehicle_data.get_battery_charge()
        cpu_usage = self.vehicle_data.get_cpu_usage()
        ram_usage = self.vehicle_data.get_ram_usage()
        self.resourcesusage.set_data(battery_charge, cpu_usage, ram_usage)

        thrusters_enabled = self.vehicle_data.get_thrusters_status()
        thruster_setpoints = self.vehicle_data.get_thruster_setpoints()

        if (not thrusters_enabled) and self.vehicle_data.is_subscribed_to_topic('thruster setpoints'):
            self.vehicle_data.unsubscribe_topic('thruster setpoints')
            self.setpoints.clear_setpoints()

        if thrusters_enabled and (not self.vehicle_data.is_subscribed_to_topic('thruster setpoints')):
            self.vehicle_data.subscribe_topic('thruster setpoints')

        if thruster_setpoints is not None and thruster_setpoints['valid_data'] == 'new_data':
            self.setpoints.set_data(thruster_setpoints)

    def disconnect(self):
        # clear previous widgets
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        # disconnect
        self.connected = False
        # close thread and timer
        self.timer.stop()
        if self.table:
            self.table.disconnect()
