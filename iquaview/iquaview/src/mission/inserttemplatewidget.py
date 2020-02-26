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
 Widget to insert a new mission template.
 It allows to specify in which waypoint of an existent mission should be inserted.
"""
import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from iquaview.src.ui.ui_insert_template_widget import Ui_InsertTemplateWidget
from iquaview.src.mission.missiontemplates import lawnmowerwidget, rectangletemplatewidget
from iquaview.src.cola2api.mission_types import (Mission)

logger = logging.getLogger(__name__)


class InsertTemplateWidget(QWidget, Ui_InsertTemplateWidget):
    save_tracks = pyqtSignal()
    preview_mission_signal = pyqtSignal()

    def __init__(self, canvas, msglog, view, current_missiontrack, parent=None):
        super(InsertTemplateWidget, self).__init__(parent)
        self.setupUi(self)
        self.canvas = canvas
        self.view = view
        self.msglog = msglog
        self.current_missiontrack = current_missiontrack
        self.insertion_wp = 0
        self.modified = False
        self.template_widget = None
        self.preview_mission = Mission()

        self.templateComboBox.currentIndexChanged.connect(self.template_changed)
        self.insertionPointSpinBox.valueChanged.connect(self.insertion_point_changed)
        self.previewTracksButton.clicked.connect(self.preview_tracks)
        self.saveTracksButton.clicked.connect(self.merge_template_mission)

        self.insertionPointSpinBox.setRange(1, self.current_missiontrack.get_mission_length() + 1)
        self.insertionPointSpinBox.setValue(self.current_missiontrack.get_mission_length() + 1)
        self.template_changed()

    def template_changed(self):
        """ Change between templates"""
        selected_template = self.templateComboBox.currentText()
        logger.debug("template changed now: {}".format(selected_template))
        # Delete previous template widget
        if self.template_widget is not None:
            self.template_widget.delete_widget()
            self.templateWidget.layout().removeWidget(self.template_widget)
            self.template_widget = None

        if selected_template == "Classic Lawn Mower":
            self.template_widget = lawnmowerwidget.LawnMowerWidget(self.canvas, self.msglog,
                                                                   self.current_missiontrack,
                                                                   selected_template)

        elif selected_template == "Spiral Lawn Mower":
            self.template_widget = lawnmowerwidget.LawnMowerWidget(self.canvas, self.msglog,
                                                                   self.current_missiontrack,
                                                                   selected_template)

        elif selected_template == "Rectangle Template":
            self.template_widget = rectangletemplatewidget.RectangleTemplateWidget(self.canvas, self.msglog,
                                                                                   self.current_missiontrack)

        self.templateWidget.layout().addWidget(self.template_widget)
        self.template_widget.show()

    def is_template_modified(self):
        """ Return true if the template has been modified, otherwise False"""
        return self.modified

    def insertion_point_changed(self):
        """ Modifies insert point"""
        self.insertion_wp = self.insertionPointSpinBox.value() - 1

    def preview_tracks(self):
        """ preview tracks on the canvas"""
        self.template_widget.preview_tracks()
        self.modified = True

        template_mission = self.template_widget.get_template_mission()
        insertion_point = self.insertion_wp
        self.preview_mission.copy(self.current_missiontrack.get_mission())

        for step in range(0, template_mission.get_length()):
            self.preview_mission.insert_step(insertion_point, template_mission.get_step(step))
            insertion_point = insertion_point + 1
        self.preview_mission_signal.emit()

    def merge_template_mission(self):
        """ Merge the template with the current mission"""

        # Get mission from template and append it in the current one in the current insertion point
        template_mission = self.template_widget.get_template_mission()
        current_mission = self.current_missiontrack.get_mission()
        insertion_point = self.insertion_wp

        for step in range(0, template_mission.get_length()):
            current_mission.insert_step(insertion_point, template_mission.get_step(step))
            insertion_point = insertion_point + 1
        self.modified = False
        self.current_missiontrack.update_layer_geometry()
        self.view.setCurrentLayer(self.current_missiontrack.get_mission_layer())
        self.current_missiontrack.mission_changed.emit(0)
        self.save_tracks.emit()

    def close(self):
        """ Close template widget"""
        if self.template_widget is not None:
            self.template_widget.close()
