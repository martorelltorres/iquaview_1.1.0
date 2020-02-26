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
 Widget to monitor the battery level of the vehicle.
"""

import sys
from PyQt5.QtCore import pyqtSignal, QRect, Qt, pyqtProperty, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QVBoxLayout


class BatteryWidget(QWidget):
    chargeChanged = pyqtSignal(float)

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self._charge = 0

        self.white = QColor(255, 255, 255)
        self.black = QColor(0, 0, 0)
        self.green = QColor(51, 255, 51)
        self.yellow = QColor(255, 255, 51)
        self.red = QColor(255, 0, 0)

        self.setMinimumWidth(110)
        self.setMinimumHeight(75)
        self.setMaximumWidth(110)
        self.setMaximumHeight(75)
        self.data = None

        # Defining sizes of battery
        self.ex_top_left_y = 25                                     #top left corner, Y position, exterior border (black)
        self.in_top_left_y = self.ex_top_left_y + 5                 #top left corner, Y position, interior border (white, filler)
        self.ex_top_left_x = 6                                      #top left corner, X position, exterior border (black)
        self.in_top_left_x = self.ex_top_left_x + 5                 #top left corner, X position, interior border (white, filler)
        self.exterior_width = self.width() - 15                     #Width of the drawing, exterior border (black)
        self.interior_width = self.exterior_width - 10              #Width of the drawing, interior border (white)
        self.exterior_height = self.height() - 40                   #Height of the drawing, exterior border (black)
        self.interior_height = self.exterior_height - 10            #Height of the drawing, interior border (white)
        self.total_width = self.width() - 20 - self.ex_top_left_x   #Width of the battery bar drawing (green)

    def paintEvent(self, ev):
        """ paint the battery widget"""
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # draw positive terminal
        painter.setBrush(self.black)
        rect_p_terminal = QRect(self.width() - 7, self.height() / 2, self.width() / 30, self.height() / 8)
        painter.drawRect(rect_p_terminal)
        # draw battery
        painter.setBrush(self.black)
        rect = QRect(self.ex_top_left_x, self.ex_top_left_y, self.exterior_width, self.exterior_height)
        painter.drawRoundedRect(rect, 10.0, 10.0)
        # draw transparent background
        painter.setBrush(self.white)
        rect_transp = QRect(self.in_top_left_x, self.in_top_left_y, self.interior_width, self.interior_height)
        painter.drawRoundedRect(rect_transp.intersected(rect), 5.0, 5.0)
        # draw charge
        charge = self._charge
        # charge on pixels 0 to 100
        if charge > 100:
            charge = 100
        if charge < 0:
            charge = 0
        rect_charge = QRect(self.in_top_left_x, self.in_top_left_y, self.total_width * charge / 100, self.interior_height)

        if charge > 45:
            color = self.green
        elif charge < 20:
            color = self.red
        else:
            color = self.yellow
        painter.setBrush(color)
        painter.drawRoundedRect(rect_charge, 5.0, 5.0)
        painter.setPen(QPen(QBrush(Qt.black), 1, Qt.SolidLine))
        painter.drawText(self.width() / 2 - (self.width() / 8), self.height() / 2 + 10, str(int(charge)) + '%')
        painter.end()

    def charge(self):
        """ return charge value"""
        return self._charge

    def set_data(self, data):
        """ set 'data'"""
        self.data = data
        if data:
            self.setCharge(data)

    @pyqtSlot(float)
    def setCharge(self, charge):

        if charge != self._charge:
            self._charge = charge
            self.chargeChanged.emit(charge)
            self.update()

    charge = pyqtProperty(float, charge, setCharge)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    velocimeter = BatteryWidget()
    spinBox = QSpinBox()
    spinBox.setRange(0, 359)
    spinBox.valueChanged.connect(velocimeter.setCharge)

    layout = QVBoxLayout()
    layout.addWidget(velocimeter)
    layout.addWidget(spinBox)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())

