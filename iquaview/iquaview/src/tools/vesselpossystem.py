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
 Dialog to set vessel size and set GPS and USBL offsets
"""
from importlib import util

from PyQt5.QtWidgets import (QDialog,
                             QGraphicsScene,
                             QGraphicsPolygonItem,
                             QGraphicsEllipseItem,
                             QGraphicsLineItem,
                             QGraphicsSimpleTextItem)
from PyQt5.QtGui import QPolygonF, QColor, QPainter
from PyQt5.QtCore import QPointF, Qt
from iquaview.src.ui.ui_vesselpossystem import Ui_VesselPosSystem


class VesselPositionSystem(QDialog, Ui_VesselPosSystem):
    def __init__(self, config, parent=None):
        super(VesselPositionSystem, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Vessel Position System")

        self.config = config

        # Set maximum and minimum values
        self.vrp_x_offset_doubleSpinBox.setMaximum(500.0)
        self.vrp_y_offset_doubleSpinBox.setMaximum(500.0)
        self.gps_x_offset_doubleSpinBox.setMaximum(500.0)
        self.gps_y_offset_doubleSpinBox.setMaximum(500.0)

        self.vrp_x_offset_doubleSpinBox.setMinimum(-500.0)
        self.vrp_y_offset_doubleSpinBox.setMinimum(-500.0)
        self.gps_y_offset_doubleSpinBox.setMinimum(-500.0)
        self.gps_x_offset_doubleSpinBox.setMinimum(-500.0)

        self.vessel_length_doubleSpinBox.setMinimum(1.0)
        self.vessel_width_doubleSpinBox.setMinimum(1.0)

        # set config values
        self.set_spinbox_value(self.vessel_length_doubleSpinBox, "vessel_length")
        self.set_spinbox_value(self.vessel_width_doubleSpinBox, "vessel_width")
        self.set_spinbox_value(self.vrp_x_offset_doubleSpinBox, 'vrp_offset_x')
        self.set_spinbox_value(self.vrp_y_offset_doubleSpinBox, 'vrp_offset_y')
        self.set_spinbox_value(self.gps_x_offset_doubleSpinBox, 'gps_offset_x')
        self.set_spinbox_value(self.gps_y_offset_doubleSpinBox, 'gps_offset_y')
        self.set_spinbox_value(self.gps_heading_doubleSpinBox, 'gps_offset_heading')

        # connect spinbox
        self.vessel_length_doubleSpinBox.valueChanged.connect(self.print_vessel)
        self.vessel_width_doubleSpinBox.valueChanged.connect(self.print_vessel)
        self.vrp_x_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
        self.vrp_y_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
        self.gps_x_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
        self.gps_y_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
        self.gps_heading_doubleSpinBox.valueChanged.connect(self.print_vessel)

        if util.find_spec('usblcontroller') is not None:
            self.usbl_x_offset_doubleSpinBox.setMaximum(500.0)
            self.usbl_x_offset_doubleSpinBox.setMinimum(-500.0)
            self.set_spinbox_value(self.usbl_x_offset_doubleSpinBox, 'usbl_offset_x')
            self.usbl_y_offset_doubleSpinBox.setMaximum(500.0)
            self.usbl_y_offset_doubleSpinBox.setMinimum(-500.0)
            self.set_spinbox_value(self.usbl_y_offset_doubleSpinBox, 'usbl_offset_y')
            self.set_spinbox_value(self.usbl_z_offset_doubleSpinBox, 'usbl_offset_z')
            self.set_spinbox_value(self.usbl_heading_doubleSpinBox, 'usbl_offset_heading')
            self.usbl_x_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
            self.usbl_y_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
            self.usbl_z_offset_doubleSpinBox.valueChanged.connect(self.print_vessel)
            self.usbl_heading_doubleSpinBox.valueChanged.connect(self.print_vessel)
        else:
            self.hide_widgets_on_layout(self.usbl_gridLayout)

        # connect accept button
        self.buttonBox.accepted.connect(self.on_accept)

        # set top scene
        self.top_scene = QGraphicsScene(self.top_graphicsView)
        self.top_graphicsView.setScene(self.top_scene)

        self.side_scene = QGraphicsScene(self.side_graphicsView)
        self.side_graphicsView.setScene(self.side_scene)

    def hide_widgets_on_layout(self, layout):
        """
        Hide all widgets from layout
        :param layout: a layout
        """
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            widget = item.widget()
            if widget is not None:
                widget.hide()
            else:
                self.hide_elements(item.layout())

    def set_spinbox_value(self, spinbox, value):
        try:
            spinbox.setValue(self.config.csettings[value])
        except:
            spinbox.setValue(0.0)

    def print_vessel(self):
        """
        printvessel draw vessel, gps, usbl and vessel reference point on a qgraphicsscene

        """
        self.print_top_view()
        self.print_side_view()

    def print_top_view(self):
        """
        draw draw vessel, gps, usbl and vessel reference point on a top_graphicsView
         
        """
        # clear previous scene
        self.top_scene.clear()
        self.top_graphicsView.viewport().update()

        # get vessel spinbox values
        v_width = self.vessel_width_doubleSpinBox.value()
        v_length = self.vessel_length_doubleSpinBox.value()
        vrp_x_on_vessel = self.vrp_x_offset_doubleSpinBox.value()
        vrp_y_on_vessel = self.vrp_y_offset_doubleSpinBox.value()
        gps_x_on_vessel = self.gps_x_offset_doubleSpinBox.value()
        gps_y_on_vessel = self.gps_y_offset_doubleSpinBox.value()

        if util.find_spec('usblcontroller') is not None:
            usbl_x_on_vessel = self.usbl_x_offset_doubleSpinBox.value()
            usbl_y_on_vessel = self.usbl_y_offset_doubleSpinBox.value()
        else:
            usbl_x_on_vessel = 0
            usbl_y_on_vessel = 0
        # get width and height from view
        w_max = self.top_graphicsView.width()
        h_max = self.top_graphicsView.height()

        # set max
        if v_width > v_length:
            max_pix = v_width
        else:
            max_pix = v_length

        # set pixel ratio
        if w_max < h_max:
            pix_ratio = (w_max - 20) / max_pix
        else:
            pix_ratio = (h_max - 20) / max_pix

        # set the size of the vessel
        vessel = QPolygonF([QPointF(pix_ratio * v_width / 2, 0),
                            QPointF(pix_ratio * v_width, pix_ratio * v_length / 4),
                            QPointF(pix_ratio * v_width, pix_ratio * v_length),
                            QPointF(0, pix_ratio * v_length),
                            QPointF(0, pix_ratio * v_length / 4)])
        self.item = QGraphicsPolygonItem(vessel)
        # set brown color
        self.item.setBrush(QColor(210, 180, 140))

        x_origin_scene = (pix_ratio * v_width / 2)
        y_origin_scene = (pix_ratio * v_length / 2)

        # coordinate system
        line_x_coord = QGraphicsLineItem(x_origin_scene,
                                         0,
                                         x_origin_scene,
                                         y_origin_scene)
        line_y_coord = QGraphicsLineItem(x_origin_scene,
                                         y_origin_scene,
                                         pix_ratio * v_width,
                                         y_origin_scene)
        x_label = QGraphicsSimpleTextItem("X", line_x_coord)
        x_label.setPos(x_origin_scene - 10,
                       0 + 10)
        y_label = QGraphicsSimpleTextItem("Y", line_y_coord)
        y_label.setPos(pix_ratio * v_width - 20,
                       y_origin_scene)

        x_origin_scene += vrp_y_on_vessel * pix_ratio
        y_origin_scene += -vrp_x_on_vessel * pix_ratio

        # draw origin point
        origin = QGraphicsEllipseItem(x_origin_scene - 10,
                                      y_origin_scene - 10,
                                      20, 20)
        origin.setBrush(Qt.white)
        line_one_origin = QGraphicsLineItem(x_origin_scene - 10,
                                            y_origin_scene,
                                            x_origin_scene + 10,
                                            y_origin_scene)
        line_two_origin = QGraphicsLineItem(x_origin_scene,
                                            y_origin_scene - 10,
                                            x_origin_scene,
                                            y_origin_scene + 10)

        # gps position
        gps_circle = QGraphicsEllipseItem(x_origin_scene - 10 + gps_y_on_vessel * pix_ratio,
                                          y_origin_scene - 10 - gps_x_on_vessel * pix_ratio,
                                          20, 20)
        gps_circle.setBrush(QColor(143, 188, 143))

        line_one_gps = QGraphicsLineItem(x_origin_scene - 10 + gps_y_on_vessel * pix_ratio,
                                         y_origin_scene - gps_x_on_vessel * pix_ratio,
                                         x_origin_scene + 10 + gps_y_on_vessel * pix_ratio,
                                         y_origin_scene - gps_x_on_vessel * pix_ratio)
        line_two_gps = QGraphicsLineItem(x_origin_scene + gps_y_on_vessel * pix_ratio,
                                         y_origin_scene - 10 - gps_x_on_vessel * pix_ratio,
                                         x_origin_scene + gps_y_on_vessel * pix_ratio,
                                         y_origin_scene + 10 - gps_x_on_vessel * pix_ratio)
        # gps label
        gps_label = QGraphicsSimpleTextItem("GPS", gps_circle)
        gps_label.setPos(x_origin_scene - 10 + gps_y_on_vessel * pix_ratio,
                         y_origin_scene + 10 - gps_x_on_vessel * pix_ratio)

        if util.find_spec('usblcontroller') is not None:
            # usbl position
            usbl_circle = QGraphicsEllipseItem(x_origin_scene - 10 + usbl_y_on_vessel * pix_ratio,
                                               y_origin_scene - 10 - usbl_x_on_vessel * pix_ratio,
                                               20, 20)
            usbl_circle.setBrush(QColor(255, 99, 71))

            line_one_usbl = QGraphicsLineItem(x_origin_scene - 10 + usbl_y_on_vessel * pix_ratio,
                                              y_origin_scene - usbl_x_on_vessel * pix_ratio,
                                              x_origin_scene + 10 + usbl_y_on_vessel * pix_ratio,
                                              y_origin_scene - usbl_x_on_vessel * pix_ratio)
            line_two_usbl = QGraphicsLineItem(x_origin_scene + usbl_y_on_vessel * pix_ratio,
                                              y_origin_scene - 10 - usbl_x_on_vessel * pix_ratio,
                                              x_origin_scene + usbl_y_on_vessel * pix_ratio,
                                              y_origin_scene + 10 - usbl_x_on_vessel * pix_ratio)
            # usbl label
            usbl_label = QGraphicsSimpleTextItem("USBL", usbl_circle)
            if usbl_x_on_vessel == gps_x_on_vessel and usbl_y_on_vessel == gps_y_on_vessel:
                usbl_label.setPos(x_origin_scene - 10 + usbl_y_on_vessel * pix_ratio,
                                  y_origin_scene - 30 - usbl_x_on_vessel * pix_ratio)
            else:
                usbl_label.setPos(x_origin_scene - 10 + usbl_y_on_vessel * pix_ratio,
                                  y_origin_scene + 10 - usbl_x_on_vessel * pix_ratio)

        origin_label = QGraphicsSimpleTextItem("VRP", origin)
        if (usbl_x_on_vessel == 0 and usbl_y_on_vessel == 0) or (gps_x_on_vessel == 0 and gps_y_on_vessel == 0):
            origin_label.setPos(x_origin_scene + 10,
                                y_origin_scene - 10)
        else:
            origin_label.setPos(x_origin_scene - 10,
                                y_origin_scene + 10)

        # fit view/scene
        self.top_graphicsView.setSceneRect(0, 0, pix_ratio * v_width, pix_ratio * v_length)

        # add vessel to the scene
        self.top_graphicsView.scene().addItem(self.item)
        # add origin to the scene
        self.top_graphicsView.scene().addItem(origin)
        self.top_graphicsView.scene().addItem(line_one_origin)
        self.top_graphicsView.scene().addItem(line_two_origin)
        # add gps
        self.top_graphicsView.scene().addItem(gps_circle)
        self.top_graphicsView.scene().addItem(line_one_gps)
        self.top_graphicsView.scene().addItem(line_two_gps)

        if util.find_spec('usblcontroller') is not None:
            # add usbl
            self.top_graphicsView.scene().addItem(usbl_circle)
            self.top_graphicsView.scene().addItem(line_one_usbl)
            self.top_graphicsView.scene().addItem(line_two_usbl)

        # add coord system
        self.top_graphicsView.scene().addItem(line_x_coord)
        self.top_graphicsView.scene().addItem(line_y_coord)
        # set background
        self.top_scene.setBackgroundBrush(QColor(204, 229, 255))

        # set antialiasing renderhint
        self.top_graphicsView.setRenderHint(QPainter.Antialiasing)

    def print_side_view(self):
        """
        draw vessel, usbl and vessel reference point on a side_graphicsView
         
        """

        # clear previous scene
        self.side_scene.clear()
        self.side_graphicsView.viewport().update()

        # get vessel spinbox values
        v_length = self.vessel_length_doubleSpinBox.value()
        v_height = v_length / 3

        vrp_x_on_vessel = self.vrp_x_offset_doubleSpinBox.value()

        if util.find_spec('usblcontroller') is not None:
            usbl_x_on_vessel = self.usbl_x_offset_doubleSpinBox.value()
            usbl_z_on_vessel = self.usbl_z_offset_doubleSpinBox.value()
        else:
            usbl_x_on_vessel = 0
            usbl_z_on_vessel = 0

        # get width and height from view
        w_max = self.side_graphicsView.width()
        h_max = self.side_graphicsView.height()

        # set max
        if v_height > v_length:
            max_pix = v_height
        else:
            max_pix = v_length

        # set pixel ratio
        if w_max < h_max:
            pix_ratio = (w_max - 20) / max_pix
        else:
            pix_ratio = (h_max - 20) / max_pix

        # set the size of the vessel
        vessel = QPolygonF([QPointF(0, 0),
                            QPointF(pix_ratio * v_length, 0),
                            QPointF(pix_ratio * v_length * 3 / 4, pix_ratio * v_height),
                            QPointF(0, pix_ratio * v_height)])
        self.item = QGraphicsPolygonItem(vessel)
        # set brown color
        self.item.setBrush(QColor(210, 180, 140))

        x_origin_scene = (pix_ratio * v_length / 2)
        y_origin_scene = (pix_ratio * v_height / 2)

        # coordinate system
        line_x_coord = QGraphicsLineItem(x_origin_scene,
                                         y_origin_scene,
                                         pix_ratio * v_length - (
                                                 pix_ratio * v_length - pix_ratio * v_length * 3 / 4) / 2,
                                         y_origin_scene)
        line_z_coord = QGraphicsLineItem(x_origin_scene,
                                         y_origin_scene,
                                         x_origin_scene,
                                         pix_ratio * v_height)
        x_label = QGraphicsSimpleTextItem("X", line_x_coord)
        x_label.setPos(pix_ratio * v_length - (pix_ratio * v_length - pix_ratio * v_length * 3 / 4) / 2 - 30,
                       y_origin_scene)
        z_label = QGraphicsSimpleTextItem("Z", line_z_coord)
        z_label.setPos(x_origin_scene - 20,
                       pix_ratio * v_height - 20)

        # set sea background
        sea_polygon = QPolygonF([QPointF(-w_max, y_origin_scene),
                                 QPointF(w_max, y_origin_scene),
                                 QPointF(x_origin_scene + w_max, h_max + usbl_z_on_vessel * pix_ratio),
                                 QPointF(-w_max, h_max + usbl_z_on_vessel * pix_ratio)])
        sea = QGraphicsPolygonItem(sea_polygon)
        sea.setBrush(QColor(204, 229, 255))

        x_origin_scene += vrp_x_on_vessel * pix_ratio

        # draw origin point
        origin = QGraphicsEllipseItem(x_origin_scene - 10,
                                      y_origin_scene - 10,
                                      20, 20)
        origin.setBrush(Qt.white)
        line_one_origin = QGraphicsLineItem(x_origin_scene - 10,
                                            y_origin_scene,
                                            x_origin_scene + 10,
                                            y_origin_scene)
        line_two_origin = QGraphicsLineItem(x_origin_scene,
                                            y_origin_scene - 10,
                                            x_origin_scene,
                                            y_origin_scene + 10)

        if util.find_spec('usblcontroller') is not None:
            # usbl position
            usbl_circle = QGraphicsEllipseItem(x_origin_scene - 10 + usbl_x_on_vessel * pix_ratio,
                                               y_origin_scene - 10 + usbl_z_on_vessel * pix_ratio,
                                               20, 20)
            usbl_circle.setBrush(QColor(255, 99, 71))

            line_one_usbl = QGraphicsLineItem(x_origin_scene - 10 + usbl_x_on_vessel * pix_ratio,
                                              y_origin_scene + usbl_z_on_vessel * pix_ratio,
                                              x_origin_scene + 10 + usbl_x_on_vessel * pix_ratio,
                                              y_origin_scene + usbl_z_on_vessel * pix_ratio)
            line_two_usbl = QGraphicsLineItem(x_origin_scene + usbl_x_on_vessel * pix_ratio,
                                              y_origin_scene - 10 + usbl_z_on_vessel * pix_ratio,
                                              x_origin_scene + usbl_x_on_vessel * pix_ratio,
                                              y_origin_scene + 10 + usbl_z_on_vessel * pix_ratio)

            # define labels

            usbl_label = QGraphicsSimpleTextItem("USBL", usbl_circle)
            usbl_label.setPos(x_origin_scene - 10 + usbl_x_on_vessel * pix_ratio,
                              y_origin_scene + 10 + usbl_z_on_vessel * pix_ratio)

        origin_label = QGraphicsSimpleTextItem("VRP", origin)
        if usbl_x_on_vessel == 0 and usbl_z_on_vessel == 0:
            origin_label.setPos(x_origin_scene + 10,
                                y_origin_scene - 10)
        else:
            origin_label.setPos(x_origin_scene - 10,
                                y_origin_scene + 10)

        # fit view/scene
        self.side_scene.setSceneRect(0, 0, pix_ratio * v_length, pix_ratio * v_height + usbl_z_on_vessel * pix_ratio)

        self.side_graphicsView.scene().addItem(sea)

        # add vessel to the scene
        self.side_graphicsView.scene().addItem(self.item)
        # add origin to the scene
        self.side_graphicsView.scene().addItem(origin)
        self.side_graphicsView.scene().addItem(line_one_origin)
        self.side_graphicsView.scene().addItem(line_two_origin)

        if util.find_spec('usblcontroller') is not None:
            # add usbl
            self.side_graphicsView.scene().addItem(usbl_circle)
            self.side_graphicsView.scene().addItem(line_one_usbl)
            self.side_graphicsView.scene().addItem(line_two_usbl)

        # add coord system
        self.side_graphicsView.scene().addItem(line_x_coord)
        self.side_graphicsView.scene().addItem(line_z_coord)

        # set background
        self.side_scene.setBackgroundBrush(Qt.white)

        # set antialiasing renderhint
        self.side_graphicsView.setRenderHint(QPainter.Antialiasing)

    def on_accept(self):
        """On accept set values on config csettings"""

        self.config.csettings["vessel_width"] = self.vessel_width_doubleSpinBox.value()
        self.config.csettings["vessel_length"] = self.vessel_length_doubleSpinBox.value()

        self.config.csettings["vrp_offset_x"] = self.vrp_x_offset_doubleSpinBox.value()
        self.config.csettings["vrp_offset_y"] = self.vrp_y_offset_doubleSpinBox.value()

        self.config.csettings['gps_offset_x'] = self.gps_x_offset_doubleSpinBox.value()
        self.config.csettings['gps_offset_y'] = self.gps_y_offset_doubleSpinBox.value()
        self.config.csettings['gps_offset_heading'] = self.gps_heading_doubleSpinBox.value()

        if util.find_spec('usblcontroller') is not None:
            self.config.csettings['usbl_offset_x'] = self.usbl_x_offset_doubleSpinBox.value()
            self.config.csettings['usbl_offset_y'] = self.usbl_y_offset_doubleSpinBox.value()
            self.config.csettings['usbl_offset_z'] = self.usbl_z_offset_doubleSpinBox.value()
            self.config.csettings['usbl_offset_heading'] = self.usbl_heading_doubleSpinBox.value()

        self.config.save()

    def resizeEvent(self, qresizeevent):
        super(VesselPositionSystem, self).resizeEvent(qresizeevent)
        self.print_vessel()
