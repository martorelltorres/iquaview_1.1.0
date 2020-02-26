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
 Dialog to display the log info
"""

from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QWidget
from iquaview.src.ui.ui_log import Ui_Log


class LogWidget(QWidget, Ui_Log):
    new_data_signal = pyqtSignal(dict)

    def __init__(self, vehicle_data):
        super(LogWidget, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Log Info")
        self.vehicle_data = vehicle_data
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.connected = False
        self.new_data_signal.connect(self.update_log)

        self.plainTextEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.plainTextEdit.customContextMenuRequested.connect(self.show_context_menu)

    def connect(self):
        """ set connected start to True and start timer"""
        self.connected = True
        self.timer.start(1000)

    def refresh_data(self):
        """Refresh log data."""
        if self.connected:
            info = self.vehicle_data.get_rosout()
            if info is not None and info[0]['valid_data'] == 'new_data':
                for data in info:
                    self.new_data_signal.emit(data)

    def update_log(self, data):
        """
        Append data in log.

        :param data: data from auv
        :type data: dict
        """

        tf = self.plainTextEdit.currentCharFormat()

        if data['level'] == 0:

            tf.setForeground(QBrush(Qt.gray))
            msg_type = "[DEBUG]"

        elif data['level'] == 2:

            tf.setForeground(QBrush(Qt.black))
            msg_type = "[INFO]"

        elif data['level'] == 4:

            tf.setForeground(QBrush(Qt.darkYellow))
            msg_type = "[WARN]"

        elif data['level'] == 8:

            tf.setForeground(QBrush(Qt.red))
            msg_type = "[ERROR]"

        elif data['level'] == 16:
            tf.setForeground(QBrush(Qt.darkRed))
            msg_type = "[FATAL]"

        time = "[" + str(data['header']['stamp']['secs']) + "." + str(data['header']['stamp']['nsecs']) + "]"
        string = msg_type + " " + time + " " + data['msg']

        self.plainTextEdit.setCurrentCharFormat(tf)
        self.plainTextEdit.appendPlainText(string)

    def show_context_menu(self, pos):
        """
        Show the context menu.
        :param pos: mouse click position
        :type pos: QPoint
        """
        menu = self.plainTextEdit.createStandardContextMenu(pos)
        clear = menu.addAction("Clear Log")
        action = menu.exec_(self.plainTextEdit.mapToGlobal(pos))
        if action == clear:
            self.plainTextEdit.clear()

    def disconnect(self):
        """ Disconnect and cancel timer."""
        self.connected = False
        self.timer.stop()
