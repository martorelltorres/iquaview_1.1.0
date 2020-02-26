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
 Widget to show the heading of the vehicle.
"""

import sys
from PyQt5.QtCore import pyqtSignal, Qt, pyqtProperty, pyqtSlot, QPoint, QSize
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPalette, QFont, QFontMetricsF, QPolygon
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QVBoxLayout


class CompassWidget(QWidget):
    angleChanged = pyqtSignal(float)

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                           225: "SW", 270: "W", 315: "NW"}
        self.north_color = QColor(231, 116, 113)
        self.setMinimumWidth(150)
        self.setMinimumHeight(150)
        self.data = None

    def paintEvent(self, event):
        """ paint the compass widget"""
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.draw_markings(painter)
        self.draw_needle(painter)

        painter.end()

    def draw_markings(self, painter):
        """ draw markings"""
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)

        painter.setFont(font)
        painter.setPen(QPen(QBrush(Qt.black), 1, Qt.SolidLine))

        i = 0
        while i < 360:

            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i]) / 2.0, -52,
                                 self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)

            painter.rotate(15)
            i += 15

        painter.restore()

    def draw_needle(self, painter):
        """ draw needle"""
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(self.palette().brush(QPalette.Shadow))

        painter.drawPolygon(
            QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),
                      QPoint(0, 45), QPoint(-10, 0)])
        )

        painter.setBrush(self.north_color)

        painter.drawPolygon(
            QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),
                      QPoint(0, -30), QPoint(-5, -25)])
        )

        painter.restore()

    def sizeHint(self):
        """ return the sizehint"""
        return QSize(150, 150)

    def angle(self):
        """set angle"""
        return self._angle

    def set_data(self, data):
        """ set new 'data'"""
        self.data = data
        angle = float(self.data['orientation']['yaw'] * (180 / 3.14159))
        self.set_angle(angle)

    @pyqtSlot(float)
    def set_angle(self, angle):

        if angle != self._angle:
            self._angle = angle
            self.angleChanged.emit(angle)
            self.update()

    angle = pyqtProperty(float, angle, set_angle)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    compass = CompassWidget()
    spinBox = QSpinBox()
    spinBox.setRange(0, 359)
    spinBox.valueChanged.connect(compass.set_angle)

    layout = QVBoxLayout()
    layout.addWidget(compass)
    layout.addWidget(spinBox)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())
