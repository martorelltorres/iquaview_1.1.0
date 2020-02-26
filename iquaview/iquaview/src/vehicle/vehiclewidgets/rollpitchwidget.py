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
 Widget to graphically show the roll and pitch of the vehicle.
 """

import sys
from PyQt5.QtCore import pyqtSignal, Qt, pyqtProperty, pyqtSlot, QPoint, QSize
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPalette, QFont, QFontMetricsF, QPolygon, QPainterPath
from PyQt5.QtWidgets import QWidget, QApplication, QSpinBox, QDoubleSpinBox, QVBoxLayout


class RollPitchWidget(QWidget):
    angleChanged = pyqtSignal(float)

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self._roll = 270.0
        self._pitch = 0.0
        self._margins = 0
        self._pitch_text = ['45º', '40º', '35º', '30º', '25º', '20º', '15º', '10º', '5º', '0º',
                            '-5º', '-10º', '-15º', '-20º', '-25º', '-30º', '-35º', '-40º', '-45º']
        self._pointText = {0: "45º", 30: "-30º", 60: "-15º", 90: "0º", 120: "15º", 150: "30º", 180: "45º",
                           210: "-30º", 240: "-15º", 270: "0.0º", 300: "15º", 330: "30º"}
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

        painter.end()

    def draw_markings(self, painter):
        """ draw markings"""

        size = self.size()
        w = size.width()
        h = size.height()

        font = QFont(self.font())
        font.setPixelSize(15)
        metrics = QFontMetricsF(font)

        painter.save()

        painter.translate(0, (self._pitch * h) / 25)
        painter.setRenderHint(painter.Antialiasing)

        painter.setPen(self.palette().color(QPalette.Shadow))
        painter.setFont(font)

        #-90º to 90º. steps 0.25º
        for i in range(-900, 925, 25):
            pos = (((i / 10.0) + 12.5 ) * h / 25.0)
            if i % 100 == 0 :
                length = w
                painter.drawText(0,
                                 pos,
                                 "{}º".format(int(-i/10)))
                painter.drawText(0,
                                 pos,
                                 "{}º".format(int(-i/10)))

            elif i % 50 == 0:
                length = w
                if i != 0:
                    painter.drawText(0,
                                     pos,
                                     "{}º".format(int(-i / 10)))
                    painter.drawText(0,
                                     pos,
                                     "{}º".format(int(-i / 10)))

            else:
                length = 0.25 * w

            painter.drawLine((w / 2) - (length / 2), pos,
                             (w / 2) + (length / 2), pos)

        painter.setWorldMatrixEnabled(False)

        painter.restore()
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        font.setPixelSize(10)
        painter.setFont(font)
        painter.setPen(QPen(QBrush(Qt.black), 1, Qt.SolidLine))

        i = 0
        while i < 360:

            if i % 30 == 0:
                painter.drawLine(0, -38, 0, -46)
                # painter.setPen(self.palette().color(QPalette.Text))
                painter.drawText(-metrics.width(self._pointText[i]) / 2.0, -48,
                                 self._pointText[i])
                # painter.setPen(self.palette().color(QPalette.Shadow))

            # else:
            # painter.drawLine(0, -46, 0, -48)

            painter.rotate(15)
            i += 15

        painter.restore()

    def draw_needle(self, painter):
        """ draw needle"""

        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._roll)
        scale = min((self.width() - self._margins) / 120.0,
                    (self.height() - self._margins) / 120.0)
        painter.scale(scale, scale)

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QColor(231, 116, 113))

        painter.drawPolygon(
            QPolygon([QPoint(-5, 0), QPoint(0, -48), QPoint(5, 0),
                      QPoint(0, 48), QPoint(-5, 0)])
        )

        # painter.setBrush(self.palette().brush(QPalette.Highlight))

        # painter.drawPolygon(
        #    QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),
        #              QPoint(0, -30), QPoint(-5, -25)])
        # )

        painter.restore()

    def sizeHint(self):

        return QSize(170, 150)

    def roll(self):
        return self._roll

    def pitch(self):
        return self._pitch

    def set_data(self, data):
        self.data = data
        roll = float(self.data['orientation']['roll'] * (180 / 3.14159))
        pitch = float(self.data['orientation']['pitch'] * (180 / 3.14159))
        self.set_angle(roll + 90, pitch)

    @pyqtSlot(float)
    def set_angle(self, roll, pitch):

        if roll != self._roll:
            self._roll = roll
            self.angleChanged.emit(roll)
            self.update()

        if pitch != self._pitch:
            self._pitch = pitch
            self.angleChanged.emit(pitch)
            self.update()

    def set_roll(self, roll):
        if roll != self._roll:
            self._roll = roll
            self.angleChanged.emit(roll)
            self.update()

    def set_pitch(self, pitch):
        if pitch != self._pitch:
            self._pitch = pitch * (180 / 3.14159)
            self.angleChanged.emit(pitch)
            self.update()

    roll = pyqtProperty(float, roll, set_angle)
    pitch = pyqtProperty(float, pitch, set_angle)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    rollpitch = RollPitchWidget()
    spinBox = QSpinBox()
    spinBox.setRange(0, 359)
    spinBox2 = QDoubleSpinBox()
    spinBox2.setSingleStep(0.1)
    spinBox2.setRange(-45, 45)
    spinBox.valueChanged.connect(rollpitch.set_roll)
    spinBox2.valueChanged.connect(rollpitch.set_pitch)

    layout = QVBoxLayout()
    layout.addWidget(rollpitch)
    layout.addWidget(spinBox)
    layout.addWidget(spinBox2)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())
