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
Class to draw a scale bar in the map canvas
"""

from PyQt5.QtGui import QPen, QPolygon, QFont, QFontMetrics
from PyQt5.QtCore import Qt
from qgis.gui import QgsMapCanvasItem
from qgis.core import QgsUnitTypes, QgsDistanceArea, QgsProject


class ScaleBar(QgsMapCanvasItem):
    def __init__(self, proj, canvas):
        super(ScaleBar, self).__init__(canvas)
        self.proj = proj
        self.canvas = canvas
        # set font
        self.myfont = QFont("helvetica", 10)
        self.myfontmetrics = QFontMetrics(self.myfont)

        # set crs and ellipsoid
        crs = self.canvas.mapSettings().destinationCrs()
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())

    def paint(self, painter, xxx, xxx2):
        """Paint scalebar on painter."""
        mymajorticksize = 8
        mypreferredsize = 1
        mytextoffsetx = 3
        myscalebarunit = "m"
        mymapunits = QgsUnitTypes.DistanceMeters

        # get height and width
        canvasheight = painter.device().height()
        canvaswidth = painter.device().width()

        # set origins
        myoriginx = canvaswidth - 40
        myoriginy = canvasheight - 20
        # save previous painter
        painter.save()
        # set rotation
        painter.rotate(- self.canvas.rotation())
        # set translation
        painter.translate(myoriginx, myoriginy)

        # calculate size of scale bar for preferred number of map units
        myscalebarwidth = mypreferredsize

        # if scale bar is very small reset to 1/4 of the canvs wide
        if myscalebarwidth < 30:
            # pixels
            myscalebarwidth = canvaswidth / 4.0

        # if scale bar is more than half the cnavs wide keep halving until not
        while myscalebarwidth > canvaswidth / 3.0:
            myscalebarwidth = myscalebarwidth / 3.0

        # get the distance between 2 points
        transform = self.canvas.getCoordinateTransform()
        start_point = transform.toMapCoordinates(0 - myscalebarwidth, 0)
        end_point = transform.toMapCoordinates(0, 0)
        distance = self.distance_calc.measureLine([start_point, end_point])

        # change scale (km,m,cm,mm)
        if mymapunits == QgsUnitTypes.DistanceMeters:
            if distance > 1000.0:
                myscalebarunit = "km"
                distance = distance / 1000
                rounddist = round(distance, 1)
            elif distance < 0.01:
                myscalebarunit = "mm"
                distance = distance * 1000
                rounddist = round(distance, 4)
            elif distance < 0.1:
                myscalebarunit = "cm"
                distance = distance * 100
                rounddist = round(distance, 2)
            else:
                myscalebarunit = "m"
                rounddist = round(distance, 1)

        # set new scalebarwidth
        myroundscalebarwidth = (rounddist * myscalebarwidth / distance)

        # set qpen
        mybackgroundpen = QPen(Qt.black, 4)
        # create bar
        mybararray = QPolygon(2)
        mybararray.putPoints(0,
                             0 - myroundscalebarwidth, 0 + mymajorticksize / 2,
                             0, 0 + mymajorticksize / 2)

        painter.setPen(mybackgroundpen)
        # draw line
        painter.drawPolyline(mybararray)

        # draw 0
        painter.drawText(0 - myroundscalebarwidth - (self.myfontmetrics.width("0") / 2),
                         0 - (self.myfontmetrics.height() / 4),
                         "0")
        # draw max
        painter.drawText(0 - (self.myfontmetrics.width(str(rounddist)) / 2),
                         0 - (self.myfontmetrics.height() / 4),
                         str(rounddist))

        # draw unit label
        painter.drawText((0 + mytextoffsetx),
                         (0 + mymajorticksize),
                         str(myscalebarunit))
        # restore painter
        painter.restore()
