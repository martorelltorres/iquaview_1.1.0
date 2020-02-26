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
 Class to handle tasks that take few time and display loading bar meanwhile.
"""

import sys
import time
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QApplication


class TaskThread(QThread):
    """
    class that runs a sleep and then send a signal when it ends

    """
    taskFinished = pyqtSignal()

    def __init__(self, fn=None, *args, **kwargs):
        QThread.__init__(self)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        run sleep and emit signal when it finishes
        """
        if self.fn is None:
            time.sleep(1.2)
        else:
            self.fn(*self.args, **self.kwargs)
        self.taskFinished.emit()


class CmdThread(QThread):
    """
    class that runs a command line and then send a signal when it ends

    """
    taskFinished = pyqtSignal()

    def __init__(self, cmd=None):
        QThread.__init__(self)
        self.cmd = cmd
        self.output = None

    def run(self):
        """
        run command line and emit signal when it finishes

        """
        ps = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.output = ps.communicate()[0]
        self.taskFinished.emit()

    def get_info(self):
        """
        get the information about the process executed
        """
        return self.output.decode()


class BusyWidget(QDialog):
    """
    Busy Dialog
    """

    def __init__(self, title="Loading...", task=TaskThread(), parent=None):
        super(BusyWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setWindowTitle(title)

        # Create a progress bar and a button and add them to the main layout
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 1)
        layout.addWidget(self.progress_bar)

        self.my_task = task
        self.my_task.taskFinished.connect(self.on_finished)

        self.resize(300, 50)

    def on_start(self):
        """
        start progress bar
        """
        self.progress_bar.setRange(0, 0)
        self.my_task.start()

    def on_finished(self):
        """
        finisih progress bar
        """

        # Stop the pulsation
        self.progress_bar.setRange(0, 1)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bw = BusyWidget()
    bw.show()
    bw.on_start()
    sys.exit(app.exec_())
