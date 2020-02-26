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
 Widget to show current and desired pose requests for all vehicle axes
"""

from PyQt5.QtWidgets import QWidget, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from iquaview.src.ui.ui_table_widget import Ui_Table
import numpy as np


class TablePoseWidget(QWidget, Ui_Table):
    update_table_signal = pyqtSignal()

    def __init__(self, vehicle_info, vehicledata, parent=None):
        super(TablePoseWidget, self).__init__(parent)
        self.setupUi(self)
        # for every column, resize to contents
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.vehicle_data = vehicledata

        self.ip = vehicle_info.get_vehicle_ip()
        self.port = 9091
        self.connected = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)

        self.data = None
        self.desired_pose_data = None
        self.desired_twist_data = None
        self.update_table_signal.connect(self.update_table)

    def connect(self):
        """ set connected state to true and start timer"""
        self.connected = True
        self.timer.start(1000)

    def refresh(self):
        """ send signal to update table"""
        if self.connected:
            self.update_table_signal.emit()

    def update_table(self):
        """ Update the table widget"""
        data = self.vehicle_data.get_nav_sts()
        d_pose_data = self.vehicle_data.get_desired_pose()
        d_twist_data = self.vehicle_data.get_desired_twist()
        if data is not None and data['valid_data'] == 'new_data':
            self.data = data
        if d_pose_data is not None and d_pose_data['valid_data'] == 'new_data':
            self.desired_pose_data = d_pose_data
        if d_twist_data is not None and d_twist_data['valid_data'] == 'new_data':
            self.desired_twist_data = d_twist_data

        if self.data is not None and self.desired_pose_data is not None and self.desired_twist_data is not None:
            # current pose
            item = self.tableWidget.item(0, 0)
            item.setText("%.2f" % (self.data['position']['north']))
            item = self.tableWidget.item(0, 1)
            item.setText("%.2f" % (self.data["position"]["east"]))
            item = self.tableWidget.item(0, 2)
            item.setText("%.2f" % (self.data["position"]["depth"]))

            roll = self.rad2deg(self.data["orientation"]["roll"])
            item = self.tableWidget.item(0, 3)
            item.setText("%.2f" % roll)

            pitch = self.rad2deg(self.data["orientation"]["pitch"])
            item = self.tableWidget.item(0, 4)
            item.setText("%.2f" % pitch)

            yaw = self.rad2deg(self.data["orientation"]["yaw"])
            if yaw < 0.0:
                yaw = yaw + 360.0
            item = self.tableWidget.item(0, 5)
            item.setText("%.2f" % yaw)

            # desired pose
            item = self.tableWidget.item(1, 0)
            self.change_item_enabled(item, self.desired_pose_data['disable_axis']['x'])
            item.setText("%.2f" % (self.desired_pose_data['position']['north']))
            item = self.tableWidget.item(1, 1)
            self.change_item_enabled(item, self.desired_pose_data['disable_axis']['y'])
            item.setText("%.2f" % (self.desired_pose_data['position']['east']))
            item = self.tableWidget.item(1, 2)
            self.change_item_enabled(item, self.desired_pose_data['disable_axis']['z'])
            item.setText("%.2f" % (self.desired_pose_data['position']['depth']))

            roll = self.rad2deg(self.desired_pose_data['orientation']['roll'])
            item = self.tableWidget.item(1, 3)
            self.change_item_enabled(item, self.desired_pose_data['disable_axis']['roll'])
            item.setText("%.2f" % roll)

            pitch = self.rad2deg(self.desired_pose_data['orientation']['pitch'])
            item = self.tableWidget.item(1, 4)
            self.change_item_enabled(item, self.desired_pose_data['disable_axis']['pitch'])
            item.setText("%.2f" % pitch)

            yaw = self.rad2deg(self.desired_pose_data['orientation']['yaw'])
            if yaw < 0.0:
                yaw = yaw + 360
            item = self.tableWidget.item(1, 5)
            self.change_item_enabled(item, self.desired_pose_data['disable_axis']['yaw'])
            item.setText("%.2f" % yaw)

            # current twist
            item = self.tableWidget.item(2, 0)
            item.setText("%.2f" % (self.data['body_velocity']['x']))
            item = self.tableWidget.item(2, 1)
            item.setText("%.2f" % (self.data['body_velocity']['y']))
            item = self.tableWidget.item(2, 2)
            item.setText("%.2f" % (self.data['body_velocity']['z']))

            roll = self.rad2deg(self.data['orientation_rate']['roll'])
            item = self.tableWidget.item(2, 3)
            item.setText("%.2f" % roll)

            pitch = self.rad2deg(self.data['orientation_rate']['pitch'])
            item = self.tableWidget.item(2, 4)
            item.setText("%.2f" % pitch)

            yaw = self.rad2deg(self.data['orientation_rate']['yaw'])
            item = self.tableWidget.item(2, 5)
            item.setText("%.2f" % yaw)

            # desired twist
            item = self.tableWidget.item(3, 0)
            self.change_item_enabled(item, self.desired_twist_data['disable_axis']['x'])
            item.setText("%.2f" % (self.desired_twist_data['twist']['linear']['x']))
            item = self.tableWidget.item(3, 1)
            self.change_item_enabled(item, self.desired_twist_data['disable_axis']['y'])
            item.setText("%.2f" % (self.desired_twist_data['twist']['linear']['y']))
            item = self.tableWidget.item(3, 2)
            self.change_item_enabled(item, self.desired_twist_data['disable_axis']['z'])
            item.setText("%.2f" % (self.desired_twist_data['twist']['linear']['z']))
            item = self.tableWidget.item(3, 3)
            self.change_item_enabled(item, self.desired_twist_data['disable_axis']['roll'])
            item.setText("%.2f" % (self.rad2deg(self.desired_twist_data['twist']['angular']['x'])))
            item = self.tableWidget.item(3, 4)
            self.change_item_enabled(item, self.desired_twist_data['disable_axis']['pitch'])
            item.setText("%.2f" % (self.rad2deg(self.desired_twist_data['twist']['angular']['y'])))
            item = self.tableWidget.item(3, 5)
            self.change_item_enabled(item, self.desired_twist_data['disable_axis']['yaw'])
            item.setText("%.2f" % (self.rad2deg(self.desired_twist_data['twist']['angular']['z'])))

        self.tableWidget.viewport().update()

    def rad2deg(self, rad):
        """
        convert radians 'rad' in degrees
        :return: return 'rad' in degrees"""
        return rad * 180.0 / np.pi

    def change_item_enabled(self, item, disabled):
        """
        Change item enable status

        :param item: item is a QTableitemwidget
        :param disabled: disabled is a bool. True if item is disabled, False if is enabled
        """

        if disabled:
            item.setFlags(Qt.ItemIsSelectable
                          | Qt.ItemIsDragEnabled
                          | Qt.ItemIsUserCheckable)
        else:
            item.setFlags(Qt.ItemIsSelectable
                          | Qt.ItemIsDragEnabled
                          | Qt.ItemIsUserCheckable
                          | Qt.ItemIsEnabled)

    def resizeEvent(self, event):
        super(TablePoseWidget, self).resizeEvent(event)
        table_size = self.tableWidget.height()
        side_header_height = self.tableWidget.horizontalHeader().height()
        table_size -= side_header_height
        number_of_rows = self.tableWidget.rowCount()
        remaining_height = table_size % number_of_rows
        for rowNum in range(self.tableWidget.rowCount()):
            if remaining_height > 0:
                self.tableWidget.setRowHeight(rowNum, int(table_size / number_of_rows) + 1)
                remaining_height -= 1
            else:
                self.tableWidget.setRowHeight(rowNum, int(table_size / number_of_rows))

    def disconnect(self):
        self.connected = False

        self.timer.stop()
