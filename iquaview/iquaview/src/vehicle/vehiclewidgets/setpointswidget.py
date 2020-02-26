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
 Widget to monitor the thrusters setpoints of the vehicle.
"""

import sys
from PyQt5.QtCore import pyqtSignal, QRect, Qt, pyqtProperty, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QDoubleSpinBox, QVBoxLayout


class SetpointsWidget(QWidget):
    chargeChanged = pyqtSignal(list)

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self._setpoints = []
        self.n_setpoints = 0

        self.white = QColor(255, 255, 255)
        self.black = QColor(0, 0, 0)
        self.green = QColor(51, 255, 51)
        self.yellow = QColor(255, 255, 51)
        self.red = QColor(255, 0, 0)

        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.setMaximumWidth(200)
        self.setMaximumHeight(200)
        self.data = None

        # Defining sizes
        self.ex_min_y = 0
        self.in_min_y = self.ex_min_y + 5
        self.ex_min_x = 0
        self.in_min_x = self.ex_min_x + 5
        self.exterior_width = self.width()
        self.interior_width = self.exterior_width - 10
        self.exterior_height = self.height()
        self.interior_height = self.exterior_height - 10

    def paintEvent(self, ev):
        """ paint the thrusters setpoints widget"""
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # draw black margin
        painter.setBrush(self.black)
        rect = QRect(self.ex_min_x, self.ex_min_y, self.exterior_width, self.exterior_height)
        painter.drawRoundedRect(rect, 10.0, 10.0)
        # draw transparent background
        painter.setBrush(self.white)
        rectTransp = QRect(self.in_min_x, self.in_min_y, self.interior_width, self.interior_height)
        painter.drawRoundedRect(rectTransp.intersected(rect), 5.0, 5.0)

        if self.n_setpoints != 0:
            setpoint_width = self.interior_width / self.n_setpoints
            # draw setpoints
            setpoints = self._setpoints
            i = 0
            for item in setpoints:

                if item >= 0:
                    max_y = self.in_min_y + (self.interior_height)/2
                    min_y = max_y - ((self.interior_height / 2) * item)
                    painter.setBrush(self.green)

                    text_y_position = min_y - 5
                    if item > 0.8:
                        text_y_position += 25
                else:
                    min_y = self.in_min_y + self.interior_height/2
                    max_y = min_y + ((self.interior_height / 2) * item)
                    painter.setBrush(self.red)

                    text_y_position = min_y + abs(max_y - min_y) - 5
                    if item > -0.75:
                        text_y_position += 25

                rectCharge = QRect(self.in_min_x + (setpoint_width * i),
                                   min_y,
                                   setpoint_width,
                                   abs(max_y-min_y))

                painter.drawRoundedRect(rectCharge, 5.0, 5.0)
                painter.setPen(QPen(QBrush(Qt.black), 1, Qt.SolidLine))
                painter.drawText(self.in_min_x + (setpoint_width * i) + setpoint_width/2 - 10,
                                 text_y_position,
                                 str(int(item*100)) + '%')
                i +=1

        # draw origin line
        painter.setBrush(self.black)
        rect_origin_line = QRect(self.in_min_x, (self.in_min_y + self.interior_height) / 2, self.interior_width, 2)
        painter.drawRect(rect_origin_line)

        painter.end()

    def setpoints(self):
        """ return charge value"""
        return self._setpoints

    def set_data(self, data):
        """ set 'data'"""
        self.data = data
        if data:
            self.setSetpoints(data['setpoints'])

    def clear_setpoints(self):
        """ clear setpoints"""
        for i in range(self.n_setpoints):
            self._setpoints[i] = 0

    @pyqtSlot(float)
    def setSetpoints(self, setpoints):
        """
        Set setpoints
        :param setpoints: list of setpoints
        :type setpoints: list
        """
        self.n_setpoints = len(setpoints)
        self._setpoints = setpoints
        self.chargeChanged.emit(setpoints)
        self.update()

    setpoints = pyqtProperty(float, setpoints, setSetpoints)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = QWidget()
    setpointswidget = SetpointsWidget()
    t_setpoints = [0, 0, 0]

    def setone(value):
        t_setpoints[0] = value
        setpointswidget.setSetpoints(t_setpoints)

    def settwo(value):
        t_setpoints[1] = value
        setpointswidget.setSetpoints(t_setpoints)

    def setthree(value):
        t_setpoints[2] = value
        setpointswidget.setSetpoints(t_setpoints)


    spinBoxone = QDoubleSpinBox()
    spinBoxtwo = QDoubleSpinBox()
    spinBoxthree = QDoubleSpinBox()
    spinBoxone.setSingleStep(0.01)
    spinBoxtwo.setSingleStep(0.01)
    spinBoxthree.setSingleStep(0.01)
    spinBoxone.setRange(-1, 1)
    spinBoxtwo.setRange(-1, 1)
    spinBoxthree.setRange(-1, 1)
    spinBoxone.valueChanged.connect(setone)
    spinBoxtwo.valueChanged.connect(settwo)
    spinBoxthree.valueChanged.connect(setthree)

    layout = QVBoxLayout()
    layout.addWidget(setpointswidget)
    layout.addWidget(spinBoxone)
    layout.addWidget(spinBoxtwo)
    layout.addWidget(spinBoxthree)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())



