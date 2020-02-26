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
 Widget to handle the editing of a clicked waypoint,
 allowing to change coordinates, depth/altitude, controller type
 and actions that should be performed at each waypoint.
"""

import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QValidator, QHelpEvent
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QDialog, QMessageBox

from iquaview.src.cola2api.mission_types import (WAYPOINT_MANEUVER,
                                                 SECTION_MANEUVER,
                                                 PARK_MANEUVER,
                                                 MissionStep,
                                                 MissionPark,
                                                 MissionPosition,
                                                 MissionTolerance,
                                                 MissionWaypoint,
                                                 MissionAction,
                                                 MissionSection)
from iquaview.src.mission.missioneditionwidget.loadaddactiondialog import Loadaddactiondialog
from iquaview.src.ui.ui_waypoint_edit import Ui_WaypointEditWidget
from iquaview.src.utils.textvalidator import validate_custom_double, get_color, get_custom_double_validator

logger = logging.getLogger(__name__)


class WaypointEditWidget(QWidget, Ui_WaypointEditWidget):
    control_state_signal = pyqtSignal(bool)

    def __init__(self, config, mission_track, vehicle_namespace, multiple_edition=False, parent=None):
        super(WaypointEditWidget, self).__init__(parent)
        self.setupUi(self)
        self.displaying = False
        self.mission_track = mission_track
        self.config = config
        self.vehicle_namespace = vehicle_namespace
        self.multiple_edition = multiple_edition

        self.same_altitude = True

        # Setting validators
        double_validator = get_custom_double_validator()
        self.z_lineEdit.setValidator(double_validator)
        self.speedlineEdit.setValidator(double_validator)
        self.parkTime_lineEdit.setValidator(double_validator)
        self.tolerance_x_lineEdit.setValidator(double_validator)
        self.tolerance_y_lineEdit.setValidator(double_validator)
        self.tolerance_z_lineEdit.setValidator(double_validator)

        if multiple_edition:
            self.previousWpButton.setEnabled(False)
            self.previousWpButton.hide()
            self.nextWpButton.setEnabled(False)
            self.nextWpButton.hide()
            self.addAction_pushButton.setEnabled(False)
            self.removeAction_pushButton.setEnabled(False)

        self.delete_pushButton.clicked.connect(self.on_click_remove)
        self.comboBox.currentIndexChanged.connect(self.on_box_changed)
        self.latitude_lineEdit.textChanged.connect(self.on_text_changed)
        self.longitude_lineEdit.textChanged.connect(self.on_text_changed)
        self.z_lineEdit.textChanged.connect(self.on_text_changed)
        self.parkTime_lineEdit.textChanged.connect(self.on_text_changed)
        self.speedlineEdit.textChanged.connect(self.on_text_changed)
        self.tolerance_x_lineEdit.textChanged.connect(self.on_text_changed)
        self.tolerance_y_lineEdit.textChanged.connect(self.on_text_changed)
        self.tolerance_z_lineEdit.textChanged.connect(self.on_text_changed)
        self.removeAction_pushButton.clicked.connect(self.rm_action)
        self.addAction_pushButton.clicked.connect(self.add_action)
        # self.altitude_checkBox.toggled.connect(self.altitude_mode_changed)
        self.altitude_checkBox.clicked.connect(self.altitude_mode_clicked)
        self.previousWpButton.clicked.connect(self.load_previous_wp)
        self.nextWpButton.clicked.connect(self.load_next_wp)

        self.parkTime_lineEdit.hide()
        self.parkTime_label.hide()

        self.show_step = -1
        self.step_list = list()
        self.mCtrl = False

        if not multiple_edition:
            self.load_next_wp()
            self.mission_track.mission_changed.connect(self.show_mission_step)

    def on_text_changed(self, string):
        sender = self.sender()

        state = validate_custom_double(sender.text())
        color = get_color(state)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

        if state == QValidator.Acceptable:

            if sender == self.z_lineEdit:
                if (float(self.z_lineEdit.text()) == 0.0
                        and not self.altitude_checkBox.isChecked()
                        and not self.same_altitude):
                    reply = QMessageBox.warning(None, "Mission Error",
                                                "Z can not be 0 in Altitude Mode")
                    sender.undo()

            if self.is_valid_altitude():
                self.apply_changes()
            else:
                sender.undo()

    def altitude_mode_clicked(self):
        sender = self.sender()
        self.same_altitude = True
        self.altitude_checkBox.setStyleSheet("")
        if self.is_valid_altitude():
            self.apply_changes()
        else:
            self.altitude_checkBox.setChecked(False)

    def altitude_mode_changed(self):
        if self.is_valid_altitude():
            self.apply_changes()
        # else:
        #     self.altitude_checkBox.setChecked(not self.altitude_checkBox.isChecked())

    def is_latitude_acceptable(self):
        return validate_custom_double(self.latitude_lineEdit.text()) == QValidator.Acceptable

    def is_longitude_acceptable(self):
        return validate_custom_double(self.longitude_lineEdit.text()) == QValidator.Acceptable

    def is_z_acceptable(self):
        return validate_custom_double(self.z_lineEdit.text()) == QValidator.Acceptable

    def is_park_time_acceptable(self):
        return validate_custom_double(self.parkTime_lineEdit.text()) == QValidator.Acceptable

    def is_speed_acceptable(self):
        return validate_custom_double(self.speedlineEdit.text()) == QValidator.Acceptable

    def is_tolerance_x_acceptable(self):
        return validate_custom_double(self.tolerance_x_lineEdit.text()) == QValidator.Acceptable

    def is_tolerance_y_acceptable(self):
        return validate_custom_double(self.tolerance_y_lineEdit.text()) == QValidator.Acceptable

    def is_tolerance_z_acceptable(self):
        return validate_custom_double(self.tolerance_z_lineEdit.text()) == QValidator.Acceptable

    def is_tolerance_acceptable(self):
        return ((self.is_tolerance_x_acceptable() and float(self.tolerance_x_lineEdit.text()) != 0.0)
                and (self.is_tolerance_y_acceptable() and float(self.tolerance_y_lineEdit.text()) != 0.0)
                and (self.is_tolerance_z_acceptable() and float(self.tolerance_z_lineEdit.text()) != 0.0))

    def on_click_remove(self):
        if self.multiple_edition:
            for step in reversed(self.step_list):
                self.mission_track.remove_step(step)
            self.show_empty_mission_step()

        else:
            if self.show_step >= 0:
                self.mission_track.remove_step(self.show_step)

    def is_valid_altitude(self):
        is_valid = True
        if self.multiple_edition:
            for step in self.step_list:
                if (self.altitude_checkBox.isChecked()
                   and (float(self.mission_track.get_step(step).get_maneuver().get_position().get_z()) == 0.0
                        or (self.z_lineEdit.text() and float(self.z_lineEdit.text()) == 0.0))):
                    reply = QMessageBox.warning(None, "Mission Error",
                                                "Z can not be 0 in Altitude Mode")
                    is_valid = False
                    break
                    # self.altitude_checkBox.setChecked(False)

        else:
            if not self.z_lineEdit.text():
                is_valid = False
            elif self.altitude_checkBox.isChecked() and float(self.z_lineEdit.text()) == 0.0:
                reply = QMessageBox.warning(None, "Mission Error",
                                            "Z can not be 0 in Altitude Mode")
                # self.altitude_checkBox.setChecked(False)
                is_valid = False
            else:
                is_valid = True
        return is_valid

    # on click save current wp
    def apply_changes(self):
        mission_step_list = []
        id_list = []

        if not self.multiple_edition:
            self.step_list = list()
            if self.show_step >= 0:
                self.step_list.append(self.show_step)

        for step in reversed(self.step_list):

            logger.debug(
                "Save: Mission has {} steps. Im going to update step {}".format(self.mission_track.get_mission_length(),
                                                                                step))

            if self.is_latitude_acceptable():
                latitude = self.latitude_lineEdit.text()
            else:
                latitude = self.mission_track.get_step(step).get_maneuver().get_position().get_latitude()

            if self.is_longitude_acceptable():
                longitude = self.longitude_lineEdit.text()
            else:
                longitude = self.mission_track.get_step(step).get_maneuver().get_position().get_longitude()

            if self.is_z_acceptable():
                z = self.z_lineEdit.text()
            else:
                z = self.mission_track.get_step(step).get_maneuver().get_position().get_z()
            if self.same_altitude:
                altitude_mode = self.altitude_checkBox.isChecked()
            else:
                altitude_mode = self.mission_track.get_step(step).get_maneuver().get_position().get_altitude_mode()

            tolerance = self.mission_track.get_step(step).get_maneuver().get_tolerance()

            if self.is_tolerance_x_acceptable() and self.is_tolerance_acceptable():
                tolerance_x = self.tolerance_x_lineEdit.text()
            else:
                tolerance_x = tolerance.x

            if self.is_tolerance_y_acceptable() and self.is_tolerance_acceptable():
                tolerance_y = self.tolerance_y_lineEdit.text()
            else:
                tolerance_y = tolerance.y

            if self.is_tolerance_z_acceptable() and self.is_tolerance_acceptable():
                tolerance_z = self.tolerance_z_lineEdit.text()
            else:
                tolerance_z = tolerance.z

            if self.comboBox.isEnabled() and self.comboBox.count() < 4:
                controller = self.comboBox.currentText()
            else:
                man_type = self.mission_track.get_step(step).get_maneuver().get_maneuver_type()
                if man_type == WAYPOINT_MANEUVER:
                    controller = "waypoint"
                elif man_type == SECTION_MANEUVER:
                    controller = "section"
                elif man_type == PARK_MANEUVER:
                    controller = "park"
                else:
                    controller = "-"

            if controller == "park":
                if self.is_park_time_acceptable():
                    park_time = self.parkTime_lineEdit.text()
                elif self.mission_track.get_step(step).get_maneuver().get_maneuver_type() == PARK_MANEUVER:
                    park_time = self.mission_track.get_step(step).get_maneuver().get_time()
                else:
                    park_time = 0

            if controller == "waypoint" or controller == "section":
                if self.is_speed_acceptable():
                    speed = self.speedlineEdit.text()
                else:
                    speed = self.mission_track.get_step(step).get_maneuver().get_speed()

            # first waypoint cannot be a section
            if step == 0 and controller == "section":
                reply = QMessageBox.warning(None, "Mission Error",
                                            "First waypoint cannot be of type Section")
                if self.multiple_edition:
                    self.comboBox.addItem("-")
                    self.comboBox.setCurrentIndex(3)
                else:
                    man_type = self.mission_track.get_step(0).get_maneuver().get_maneuver_type()
                    if man_type == WAYPOINT_MANEUVER:
                        self.comboBox.setCurrentIndex(0)
                    elif man_type == PARK_MANEUVER:
                        self.comboBox.setCurrentIndex(2)
            else:
                mission_step = MissionStep()
                if controller == "park":
                    logger.debug("park")
                    park = MissionPark(MissionPosition(latitude, longitude, z, altitude_mode),
                                       0.5,
                                       park_time,
                                       MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                    mission_step.add_maneuver(park)
                elif controller == "section":
                    logger.debug("section")
                    previous_position = self.mission_track.get_step(step - 1).get_maneuver().get_position()
                    sec = MissionSection(
                        MissionPosition(previous_position.latitude, previous_position.longitude, previous_position.z,
                                        altitude_mode),
                        MissionPosition(latitude, longitude, z, altitude_mode),
                        speed,
                        MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                    mission_step.add_maneuver(sec)
                elif controller == "waypoint":
                    logger.debug("waypoint")
                    wp = MissionWaypoint(MissionPosition(latitude, longitude, z, altitude_mode),
                                         speed,
                                         MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                    mission_step.add_maneuver(wp)

                # copy actions to updated step
                mission_step.actions = self.mission_track.get_step(step).get_actions()
                mission_step_list.append(mission_step)
                id_list.append(step)

        self.mission_track.update_steps(id_list, mission_step_list)

    # controller box changed
    def on_box_changed(self, i):
        # waypoint, section or park
        if i < 3:
            # remove '-' item
            if self.comboBox.count() == 4:
                self.comboBox.removeItem(3)

            if i == 2:  # park
                self.parkTime_lineEdit.show()
                self.parkTime_label.show()
                self.parkTime_lineEdit.setEnabled(True)

                self.speedlineEdit.hide()
                self.speedLabel.hide()
                self.speedlineEdit.setEnabled(False)

            else:
                self.parkTime_lineEdit.hide()
                self.parkTime_label.hide()
                self.parkTime_lineEdit.setEnabled(False)

                self.speedlineEdit.show()
                self.speedLabel.show()
                self.speedlineEdit.setEnabled(True)

            if self.is_valid_altitude():
                self.apply_changes()
        else:
            self.parkTime_lineEdit.hide()
            self.parkTime_label.hide()
            self.speedlineEdit.hide()
            self.speedLabel.hide()



    # add new action
    def add_action(self):
        load_dialog = Loadaddactiondialog(self.config)
        result = load_dialog.exec_()
        if result == QDialog.Accepted:
            mission_action = MissionAction(self.vehicle_namespace+load_dialog.get_action_id(),
                                           load_dialog.get_params())

            logger.debug(mission_action)

            self.mission_track.get_step(self.show_step).add_action(mission_action)
            self.show_mission_step(self.show_step)

    # remove action
    def rm_action(self):
        logger.debug(self.show_step)
        self.mission_track.get_step(self.show_step).remove_action(self.listWidget_3.currentRow())
        self.show_mission_step(self.show_step)

    def show_mission_step(self, wp):
        if not self.displaying:
            self.displaying = True
            logger.debug("Showing mission with len: {},  step: {} ".format(self.mission_track.get_mission_length(), wp))
            if wp != -1:
                self.altitude_checkBox.setEnabled(True)
                self.z_lineEdit.setEnabled(True)
                self.comboBox.setEnabled(True)
                self.speedlineEdit.setEnabled(True)
                self.parkTime_lineEdit.setEnabled(True)

                self.show_step = wp

                self.TitleWaypointLabel.setText("Waypoint {}".format(self.show_step + 1))
                mission_step = self.mission_track.get_step(self.show_step)
                maneuver = mission_step.get_maneuver()

                if maneuver.get_maneuver_type() == WAYPOINT_MANEUVER:  # for Waypoint
                    position = maneuver.get_position()
                    self.comboBox.setCurrentIndex(0)
                    self.speedlineEdit.setText(str(maneuver.get_speed()))
                elif maneuver.get_maneuver_type() == SECTION_MANEUVER:  # for a Section
                    self.comboBox.setCurrentIndex(1)
                    self.speedlineEdit.setText(str(maneuver.get_speed()))
                    position = maneuver.get_final_position()
                elif maneuver.get_maneuver_type() == PARK_MANEUVER:  # for Park
                    position = maneuver.get_position()
                    self.comboBox.setCurrentIndex(2)
                    self.parkTime_lineEdit.setText(str(maneuver.get_time()))

                # latitude
                if not self.latitude_lineEdit.text() or self.latitude_lineEdit.text() != position.get_latitude():
                    if float(position.get_latitude()).is_integer() and float(position.get_latitude()) != 0.0:
                        self.latitude_lineEdit.setText(str(int(position.get_latitude())))
                    else:
                        self.latitude_lineEdit.setText(str(position.get_latitude()))
                # longitude
                if not self.longitude_lineEdit.text() or self.longitude_lineEdit.text() != position.get_longitude():
                    if float(position.get_longitude()).is_integer() and float(position.get_longitude()) != 0.0:
                        self.longitude_lineEdit.setText(str(int(position.get_longitude())))
                    else:
                        self.longitude_lineEdit.setText(str(position.get_longitude()))

                # altitude mode
                self.altitude_checkBox.setChecked(position.get_altitude_mode())
                self.apply_changes()

                # z
                if not self.z_lineEdit.text() or self.z_lineEdit.text() != position.get_z():
                    if float(position.get_z()).is_integer() and float(position.get_z()) != 0.0:
                        self.z_lineEdit.setText(str(int(float(position.get_z()))))
                    else:
                        self.z_lineEdit.setText(str(position.get_z()))

                # tolerance
                tolerance = maneuver.get_tolerance()

                if not self.tolerance_x_lineEdit.text() or float(self.tolerance_x_lineEdit.text()) != float(tolerance.x):
                    if float(tolerance.x).is_integer() and float(tolerance.x) != 0.0:
                        self.tolerance_x_lineEdit.setText(str(int(float(tolerance.x))))
                    else:
                        self.tolerance_x_lineEdit.setText(str(tolerance.x))

                if not self.tolerance_y_lineEdit.text() or float(self.tolerance_y_lineEdit.text()) != float(tolerance.y):
                    if float(tolerance.y).is_integer() and float(tolerance.y) != 0.0:
                        self.tolerance_y_lineEdit.setText(str(int(float(tolerance.y))))
                    else:
                        self.tolerance_y_lineEdit.setText(str(tolerance.y))

                if not self.tolerance_z_lineEdit.text() or float(self.tolerance_z_lineEdit.text()) != float(tolerance.z):
                    if float(tolerance.z).is_integer() and float(tolerance.z) != 0.0:
                        self.tolerance_z_lineEdit.setText(str(int(float(tolerance.z))))
                    else:
                        self.tolerance_z_lineEdit.setText(str(tolerance.z))

                self.listWidget_3.clear()
                actions = mission_step.get_actions()
                for a in actions:
                    action = QListWidgetItem()
                    text = a.get_action_id()
                    for param in a.get_parameters():
                        text += ", " + param.value
                    action.setText(text)
                    action.setData(Qt.UserRole, a)
                    self.listWidget_3.addItem(action)

            else:
                self.show_empty_mission_step()

            self.displaying = False


    def show_empty_mission_step(self):
        self.show_step = -1
        self.step_list = list()
        self.TitleWaypointLabel.setText("Mission is empty")

        self.comboBox.setCurrentIndex(0)
        self.speedlineEdit.setText("")
        self.parkTime_lineEdit.setText("")

        self.latitude_lineEdit.setText("")
        self.longitude_lineEdit.setText("")
        self.z_lineEdit.setText("")

        self.tolerance_x_lineEdit.setText("")
        self.tolerance_y_lineEdit.setText("")
        self.tolerance_z_lineEdit.setText("")

        self.altitude_checkBox.setChecked(False)
        self.altitude_checkBox.setStyleSheet("")

        self.listWidget_3.clear()

    def show_multiple_features(self, step_list):
        self.show_empty_mission_step()
        logger.debug("step list: " + str(step_list))
        if step_list:
            step_list.sort()
            self.step_list = step_list
            # if only have one step
            if len(step_list) == 1:
                self.show_mission_step(step_list[0])
            # more than one step
            else:
                # set title
                title = self.create_title(step_list)
                self.TitleWaypointLabel.setText(title)

                same_maneuver = True
                same_speed = True
                same_park = True
                same_lat = True
                same_lon = True
                same_z = True
                same_tolerance_x = True
                same_tolerance_y = True
                same_tolerance_z = True
                self.same_altitude = True

                # every list step
                for i in range(0, len(step_list)):
                    self.show_step = step_list[i]
                    mission_step = self.mission_track.get_step(self.show_step)
                    maneuver = mission_step.get_maneuver()

                    j = i + 1
                    while 0 <= j < len(step_list):
                        wp = step_list[j]
                        mission_step_two = self.mission_track.get_step(wp)
                        maneuver_two = mission_step_two.get_maneuver()

                        if maneuver.get_maneuver_type() == maneuver_two.get_maneuver_type():
                            # maneuver is waypoint or section
                            if maneuver.get_maneuver_type() == WAYPOINT_MANEUVER \
                                    or maneuver.get_maneuver_type() == SECTION_MANEUVER:
                                if float(maneuver.get_speed()) != float(maneuver_two.get_speed()):
                                    same_speed = False
                            # maneuver is a park
                            else:
                                if float(maneuver.get_time()) != float(maneuver_two.get_time()):
                                    same_park = False
                        else:
                            same_maneuver = False
                            self.parkTime_lineEdit.hide()
                            self.parkTime_label.hide()
                            self.speedlineEdit.hide()
                            self.speedLabel.hide()

                        position = maneuver.get_position()
                        position_two = maneuver_two.get_position()

                        if float(position.get_latitude()) != float(position_two.get_latitude()):
                            same_lat = False

                        if float(position.get_longitude()) != float(position_two.get_longitude()):
                            same_lon = False

                        if float(position.get_z()) != float(position_two.get_z()):
                            same_z = False

                        if position.get_altitude_mode() != position_two.get_altitude_mode():
                            color = '#fff79a'  # yellow
                            self.altitude_checkBox.setStyleSheet(
                                ("QCheckBox:indicator:unchecked { background-color: %s }" % color))
                            self.same_altitude = False
                            self.altitude_checkBox.setChecked(False)

                        tolerance = maneuver.get_tolerance()
                        tolerance_two = maneuver_two.get_tolerance()
                        if float(tolerance.x) != float(tolerance_two.x):
                            same_tolerance_x = False
                        if float(tolerance.y) != float(tolerance_two.y):
                            same_tolerance_y = False
                        if float(tolerance.z) != float(tolerance_two.z):
                            same_tolerance_z = False

                        j += 1

                self.show_step = step_list[0]
                mission_step = self.mission_track.get_step(self.show_step)
                maneuver = mission_step.get_maneuver()

                if same_maneuver:
                    self.comboBox.setEnabled(True)
                    self.speedlineEdit.setEnabled(True)
                    self.parkTime_lineEdit.setEnabled(True)
                    if maneuver.get_maneuver_type() == WAYPOINT_MANEUVER:  # for Waypoint
                        self.comboBox.setCurrentIndex(0)
                        position = maneuver.get_position()
                        if same_speed:
                            self.speedlineEdit.setText(str(maneuver.get_speed()))
                        else:
                            self.speedlineEdit.setText("")

                    elif maneuver.get_maneuver_type() == SECTION_MANEUVER:  # for a Section
                        self.comboBox.setCurrentIndex(1)
                        position = maneuver.get_position()

                        if same_speed:
                            self.speedlineEdit.setText(str(maneuver.get_speed()))
                        else:
                            self.speedlineEdit.setText("")
                    elif maneuver.get_maneuver_type() == PARK_MANEUVER:  # for Park
                        self.comboBox.setCurrentIndex(2)
                        position = maneuver.get_position()

                        if same_park:
                            self.parkTime_lineEdit.setText(str(maneuver.get_time()))
                        else:
                            self.parkTime_lineEdit.setText("")
                elif self.comboBox.count() < 4:
                    self.comboBox.addItem("-")
                    self.comboBox.setCurrentIndex(3)

                if same_lat:
                    self.latitude_lineEdit.setText(str(position.get_latitude()))
                else:
                    self.latitude_lineEdit.setText("")

                if same_lon:
                    self.longitude_lineEdit.setText(str(position.get_longitude()))
                else:
                    self.longitude_lineEdit.setText("")

                if self.same_altitude:
                    self.altitude_checkBox.setStyleSheet("")
                    self.altitude_checkBox.setChecked(position.get_altitude_mode())
                    self.altitude_checkBox.setEnabled(True)

                if same_z:
                    self.z_lineEdit.setText(str(position.get_z()))
                else:
                    self.z_lineEdit.setText("")

                if same_tolerance_x:
                    self.tolerance_x_lineEdit.setText(str(tolerance.x))
                else:
                    self.tolerance_x_lineEdit.setText("")

                if same_tolerance_y:
                    self.tolerance_y_lineEdit.setText(str(tolerance.y))
                else:
                    self.tolerance_y_lineEdit.setText("")

                if same_tolerance_z:
                    self.tolerance_z_lineEdit.setText(str(tolerance.z))
                else:
                    self.tolerance_z_lineEdit.setText("")
        else:
            self.show_empty_mission_step()

    # load previous waypoint
    def load_previous_wp(self):
        length = self.mission_track.get_mission_length()
        if length > 0:
            if self.show_step > 0:
                # switch to previous wp
                self.show_mission_step(self.show_step - 1)
            else:
                # if current wp is 0 switch to last wp
                last = length - 1
                self.show_mission_step(last)
        else:
            self.show_empty_mission_step()

    # load next waypoint
    def load_next_wp(self):
        length = self.mission_track.get_mission_length()
        if length > 0:
            if self.show_step < (length - 1):
                # switch to next wp
                self.show_mission_step(self.show_step + 1)
            else:
                # if current wp is the last switch to first wp
                self.show_mission_step(0)
        else:
            self.show_empty_mission_step()

    def create_title(self, step_list):
        """
        Creates a title with a step list and returns it. In case of the title not fitting in the available space,
        it gets shortened and a tooltip is created to show all steps in step list
        """
        # Check available space
        max_width = self.scrollArea.width() - 50
        ppchar = 6.75  # pixels per character aprox
        limit_achieved = False
        title = "Waypoints: "

        # write wp selected
        for wp in step_list:
            s = str(wp + 1)
            if wp != step_list[-1]:
                s += ","
            # limit maximum length of the title
            if (len(title) * ppchar + len(s) * ppchar) > max_width:
                limit_achieved = True
                break
            title += s

        tool_tip_text = ""
        if limit_achieved:  # Rewrite title accounting for less space due to the " ...+xx" at the end
            max_width = max_width - 75
            title = "Waypoints: "
            count = 0
            for wp in step_list:
                s = str(wp + 1) + ","
                if (len(title) * ppchar + len(s) * ppchar) > max_width:
                    title += " ...+" + str(len(step_list) - count) + " points"
                    break
                title += s
                count += 1

            #  Create ToolTip text
            cont = 0
            for wp in step_list:
                tool_tip_text += str(wp + 1)
                if wp != step_list[-1]:
                    tool_tip_text += ", "
                cont += 1
                if cont % 10 == 0 and wp < len(step_list)-1:
                    tool_tip_text += "\n"

        self.TitleWaypointLabel.setToolTip(tool_tip_text)

        return title

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True
            self.control_state_signal.emit(True)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False
            self.control_state_signal.emit(False)

    def resizeEvent(self, event):
        title = self.create_title(self.step_list)
        self.TitleWaypointLabel.setText(title)
