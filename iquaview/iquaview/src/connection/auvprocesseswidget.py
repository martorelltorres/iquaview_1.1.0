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
 Widget to control the processes that are launched/terminated inside the vehicle.
"""

import logging

from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QPixmap
from iquaview.src.ui.ui_auvprocesses import Ui_AUVProcessesWidget
from iquaview.src.connection.connectionclient import ConnectionClient
from iquaview.src.connection.cola2status import Cola2Status

logger = logging.getLogger(__name__)


class AUVProcessesWidget(QWidget, Ui_AUVProcessesWidget):
    processchanged = pyqtSignal(str)

    def __init__(self, config, vehicle_info, parent=None):
        super(AUVProcessesWidget, self).__init__(parent)
        self.setupUi(self)
        self.config = config
        self.vehicle_info = vehicle_info
        self.send_button.clicked.connect(self.send)
        self.terminate_button.clicked.connect(self.terminate)
        self.cc = ConnectionClient(self.vehicle_info.get_vehicle_ip(), self.vehicle_info.get_vehicle_port())
        self.cc.connection_failure.connect(self.connection_failed)
        self.cc.connection_ok.connect(self.connection_ok)
        self.cc.start_cc_thread()
        self.connected = False

        self.connection_label.setText("Vehicle")
        self.cola2_label.setText("COLA2")

        self.update_connection_indicator()
        self.cola2status = Cola2Status(self.config, self.vehicle_info, self.cola2_label, self.cola2_indicator)

    def set_start_process_items(self):
        data = self.cc.send("list")
        logger.info(data)
        processes = data[:-1].split(',')
        processes.insert(0, "restart vehicle pc")
        model = QStandardItemModel(len(processes), 1)

        first_item = QStandardItem("-- Start Processes --")
        first_item.setBackground(QBrush(QColor(200, 200, 200)))
        model.setItem(0, 0, first_item)

        for i, processes in enumerate(processes):
            item = QStandardItem(processes)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            model.setItem(i + 1, 0, item)

        self.startprocess_combo.setModel(model)

    def set_terminate_process_items(self):
        data = self.cc.send("on")
        logger.info(data)
        processes = data[:-1].split(',')

        model = QStandardItemModel(len(processes), 1)
        first_item = QStandardItem("-- Terminate Processes --")
        first_item.setBackground(QBrush(QColor(200, 200, 200)))
        model.setItem(0, 0, first_item)

        for i, processes in enumerate(processes):
            item = QStandardItem(processes)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            model.setItem(i + 1, 0, item)

        self.terminateprocess_combo.setModel(model)

    def connect(self):
        # Update connection with current values
        self.cc.ip = self.vehicle_info.get_vehicle_ip()
        self.cc.port = self.vehicle_info.get_vehicle_port()

    def disconnect_auvprocesses(self):
        self.cc.disconnect()
        self.connected = False
        self.update_connection_indicator()
        self.startprocess_combo.setEnabled(False)
        self.terminateprocess_combo.setEnabled(False)
        self.send_button.setEnabled(False)
        self.terminate_button.setEnabled(False)

        self.cola2status.disconnect_cola2status()

    def send(self):
        logger.info(self.startprocess_combo.currentText())
        if self.startprocess_combo.currentIndex() != 0:
            if self.terminateprocess_combo.findText(self.startprocess_combo.currentText()) != -1:
                reply = QMessageBox.question(self,
                                             "Process already running",
                                             "The process {} is already running in the vehicle. Do you want to restart it? ".format(
                                                 self.startprocess_combo.currentText()),
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    self.cc.send("terminate " + self.startprocess_combo.currentText())
                    self.cc.send(self.startprocess_combo.currentText())
                    self.processchanged.emit(
                        "Process {} has been restarted".format(self.startprocess_combo.currentText()))
            else:
                if self.startprocess_combo.currentIndex() == 1:
                    reply = QMessageBox.question(self,
                                                 "Reboot request",
                                                 "You are about to reboot the vehicle PC. Do you want to continue?",
                                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                    if reply == QMessageBox.Yes:
                        self.cc.send("restart")
                        self.processchanged.emit("Vehicle PC is rebooting")
                else:
                    self.cc.send(self.startprocess_combo.currentText())
                    self.terminateprocess_combo.removeItem(
                        self.terminateprocess_combo.findText("No running processes", Qt.MatchFixedString))
                    self.terminateprocess_combo.addItem(self.startprocess_combo.currentText())
                    self.processchanged.emit(
                        "Process {} has been started".format(self.startprocess_combo.currentText()))
                    self.set_terminate_process_items()

    def terminate(self):
        logger.info(self.terminateprocess_combo.currentText())
        self.cc.send("terminate " + self.terminateprocess_combo.currentText())
        self.processchanged.emit(
            "Process {} has been terminated".format(self.terminateprocess_combo.currentText()))
        self.terminateprocess_combo.removeItem(self.terminateprocess_combo.currentIndex())
        self.set_terminate_process_items()

    def connection_failed(self):
        self.connected = False
        self.update_connection_indicator()
        self.startprocess_combo.setEnabled(False)
        self.terminateprocess_combo.setEnabled(False)
        self.send_button.setEnabled(False)
        self.terminate_button.setEnabled(False)
        self.connect()

    def connection_ok(self):
        self.connected = True
        self.update_connection_indicator()
        self.set_start_process_items()
        self.set_terminate_process_items()
        self.startprocess_combo.setEnabled(True)
        self.terminateprocess_combo.setEnabled(True)
        self.send_button.setEnabled(True)
        self.terminate_button.setEnabled(True)

    def update_connection_indicator(self):

        if not self.connected:
            self.connection_indicator.setPixmap(QPixmap(":/resources/red_led.svg"))
            self.connection_label.setStyleSheet('font:italic; color:red')
        else:
            self.connection_indicator.setPixmap(QPixmap(":/resources/green_led.svg"))
            self.connection_label.setStyleSheet('font:italic; color:green')
