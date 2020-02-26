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
 Classes to load check action dialog
"""

from iquaview.src.cola2api.cola2_interface import send_action_service
from iquaview.src.ui import ui_action_check
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog


class LoadCheckActionDialog(QDialog, ui_action_check.Ui_Dialog):
    def __init__(self, ip, port, vehicle_namespace, description, name_action, action_id, parameters, position,
                 parent=None):
        super(LoadCheckActionDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Check Action")
        self.back_clk = False
        self.back_pushButton.clicked.connect(self.on_click_back)
        self.x_next_pushButton.clicked.connect(self.accept_fail)
        self.x_next_pushButton.setIcon(QtGui.QIcon(":/resources/Red_X.svg"))
        self.tick_next_pushButton.clicked.connect(self.accept_pass)
        self.tick_next_pushButton.setIcon(QtGui.QIcon(":/resources/Green_tick.svg"))
        self.correct_values = False
        self.description.setText(description)
        self.name.setText(name_action)
        self.action_id = action_id
        self.params = parameters
        self.ip = ip
        self.port = port
        self.vehicle_namespace = vehicle_namespace
        self.pushButton.clicked.connect(self.on_click_action_service)
        # first dialog
        if position == 0:
            self.back_pushButton.setEnabled(False)
        else:
            self.back_pushButton.setEnabled(True)

    def accept_pass(self):
        self.correct_values = True
        self.accept()

    def accept_fail(self):
        self.correct_values = False
        self.accept()

    def isChecked(self):
        return self.correct_values

    def on_click_action_service(self):
        send_action_service(self.ip, self.port, self.vehicle_namespace + self.action_id, self.params)

    def on_click_back(self):
        self.back_clk = True
        self.accept()

    def back_clicked(self):
        return self.back_clk
