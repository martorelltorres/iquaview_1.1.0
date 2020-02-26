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
 Widget to graphically show the depth and altitude of the vehicle
"""

import matplotlib
matplotlib.use("Qt5Agg")

import numpy as np
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# build a rectangle in axes coords
left, width = .05, 1
bottom, height = .05, 1
right = width - left
top = height - bottom


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, f_width=5, f_height=4, dpi=100):
        fig = Figure(figsize=(f_width, f_height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.set_facecolor('none')
        # We want the axes cleared every time plot() is called

        self.compute_initial_figure()

        self.axes.get_xaxis().set_visible(False)
        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Fixed,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class DepthAltitudeCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.x = np.array([0.0])
        self.depth_array = np.array([0.0])
        self.total_array = np.array([0.0])
        self.data = None

    def set_data(self, data):
        self.data = data
        self.update_figure()

    def compute_initial_figure(self):
        self.axes.plot([0], [0], 'r')

    def update_figure(self):
        # get depth and altitude from data
        depth = float(self.data['position']['depth'])
        altitude = float(self.data['altitude'])

        if altitude < 0:
            altitude = 0
        # delete the most old value
        if len(self.depth_array) >= 30:
            self.depth_array = np.delete(self.depth_array, 0)
            self.total_array = np.delete(self.total_array, 0)

        # append new value
        if len(self.depth_array) < 30:
            self.depth_array = np.append(self.depth_array, depth)
            self.total_array = np.append(self.total_array, altitude + depth)

        # append value on x
        if len(self.x) < len(self.depth_array):
            self.x = np.append(self.x, len(self.x))
        # self.x +=1

        # plot on widget
        self.axes.cla()
        self.axes.plot(self.x, self.depth_array, 'g', self.x, self.total_array, 'r')
        if (not self.axes.yaxis_inverted()):
            self.axes.invert_yaxis()
        minimum = int(np.amin(self.depth_array))-(np.amax(self.total_array)/20)
        if minimum < 0:
            minimum = -(np.amax(self.total_array)/20)
        self.axes.set_ylim(ymax=minimum)

        # to change altitude color
        if altitude <= 5.0:
            color = 'orange'
        else:
            color = 'blue'

        # add text
        self.axes.text(right, top, "Depth: %.1f m\n" % depth +
                                   "Alt: %.1f m" % altitude,
                       horizontalalignment='right',
                       verticalalignment='top',
                       transform=self.axes.transAxes,
                       color=color)

        self.draw()
