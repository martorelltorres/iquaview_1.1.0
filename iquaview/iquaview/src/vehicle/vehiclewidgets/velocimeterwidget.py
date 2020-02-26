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
Widget to show graphically the vehicle speed.
"""

import sys
import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt, pyqtProperty, pyqtSlot, QPoint, QSize
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPalette, QFont, QFontMetricsF, QPolygon
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QVBoxLayout


class VelocimeterWidget(QWidget):
    angleChanged = pyqtSignal(float)

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self._angle = 270.0
        self._margins = 10
        self._pointText = {0: "0.6", 30: "0.8", 60: "1.0", 90: "1.2", 120: "1.4", 150: "1.6", 180: "1.8",
                           210: "-0.4", 240: "-0.2", 270: "0.0", 300: "0.2", 330: "0.4"}
        self.brake_color = QColor(231, 116, 113)
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
        self.draw_velocity(painter)

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
        # painter.setPen(self.palette().color(QPalette.Shadow))
        painter.setPen(QPen(QBrush(Qt.black), 1, Qt.SolidLine))

        i = 0
        while i < 360:

            if i % 30 == 0:
                painter.drawLine(0, -40, 0, -50)
                # painter.setPen(self.palette().color(QPalette.Text))
                painter.drawText(-metrics.width(self._pointText[i]) / 2.0, -52,
                                 self._pointText[i])
                # painter.setPen(self.palette().color(QPalette.Shadow))
                if i == 0:
                    painter.setBrush(QBrush(self.brake_color))
                    painter.drawPie(-50, -50, 100, 100, 180 * 16, 16 * 90)
            else:
                painter.drawLine(0, -47, 0, -50)

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
            QPolygon([QPoint(-6, 0), QPoint(0, -45), QPoint(6, 0),
                      QPoint(-10, 0)])
        )

        # painter.setBrush(self.palette().brush(QPalette.Highlight))

        # painter.drawPolygon(
        #    QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),
        #              QPoint(0, -30), QPoint(-5, -25)])
        # )

        painter.restore()

    def draw_velocity(self, painter):
        """ draw velocity"""

        painter.save()

        velocity = 0.0

        if self.data:
            velocity = float(self.data['body_velocity']['x'])

        if velocity > 1.8:
            velocity = 1.8
        if velocity < -0.5:
            velocity = -0.5
        painter.setPen(QPen(QBrush(Qt.blue), 1, Qt.SolidLine))
        painter.drawText(self.width() / 2 - 20, self.height() - (self.height() / 3),
                         str(str("%.2f" % velocity) + "m/s"))
        painter.restore()

    def sizeHint(self):

        return QSize(150, 150)

    def angle(self):
        return self._angle

    def set_data(self, data):
        self.data = data
        velocity = float(self.data['body_velocity']['x'])
        if velocity > 1.8:
            velocity = 1.8
        if velocity < -0.5:
            velocity = -0.5
        ratio = (np.pi / 2) / 0.6
        theta = (velocity * ratio)
        angle = theta * (180 / np.pi) - 90
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
    velocimeter = VelocimeterWidget()
    spinBox = QSpinBox()
    spinBox.setRange(0, 359)
    spinBox.valueChanged.connect(velocimeter.set_angle)

    layout = QVBoxLayout()
    layout.addWidget(velocimeter)
    layout.addWidget(spinBox)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())
