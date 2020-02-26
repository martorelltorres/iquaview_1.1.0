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
 Widget to display information about the current mission
"""

import datetime

from PyQt5.QtWidgets import QWidget
from qgis.core import QgsDistanceArea, QgsProject, QgsPointXY

from iquaview.src.ui.ui_mission_info import Ui_missionInfo
from iquaview.src.cola2api.mission_types import PARK_MANEUVER


class MissionInfo(QWidget, Ui_missionInfo):

    def __init__(self, canvas, current_missiontrack=None, parent=None):
        super(MissionInfo, self).__init__(parent)
        self.setupUi(self)

        crs = canvas.mapSettings().destinationCrs()
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
        self.distance_calc.setEllipsoid(crs.ellipsoidAcronym())

        self.current_missiontrack = current_missiontrack
        self.current_missiontrack.mission_changed.connect(self.update_values)
        self.current_mission = current_missiontrack.get_mission()

        self.update_values()

    def set_current_mission(self, current_mission):
        """

        :param current_mission: current mission
        :type current_mission: Mission
        """
        self.current_mission = current_mission

    def update_values(self):
        """ Updates values"""
        self.n_waypoints.setText(str(self.current_mission.get_length()))

        first_step = self.current_mission.get_step(0)
        last_step = self.current_mission.get_step(self.current_mission.get_length() - 1)
        if first_step is None:
            self.first_waypoint_onsurface.setText("-")
            self.last_waypoint_onsurface.setText("-")
            self.estimated_time.setText("-")
            self.total_distance.setText("-")

        else:
            if float(first_step.get_maneuver().get_position().z) == 0.0 \
                    and not first_step.get_maneuver().get_position().altitude_mode:
                self.first_waypoint_onsurface.setText("True")
            else:
                self.first_waypoint_onsurface.setText("False")

            if float(last_step.get_maneuver().get_position().z) == 0.0 \
                    and not last_step.get_maneuver().get_position().altitude_mode:
                self.last_waypoint_onsurface.setText("True")
            else:
                self.last_waypoint_onsurface.setText("False")

            self.calculate_estimated_time_and_distance()

    def calculate_estimated_time_and_distance(self):
        # mission empty
        if self.current_mission.get_length() == 0:
            self.estimated_time.setText(str(datetime.timedelta(seconds=0)))

        else:
            total_time = 0
            total_distance = 0

            if self.current_mission.get_step(0).get_maneuver().get_maneuver_type() == PARK_MANEUVER:  # park
                total_time = float(self.current_mission.get_step(0).get_maneuver().time)
                self.estimated_time.setText(str(datetime.timedelta(seconds=int(total_time))))

            for i in range(0, self.current_mission.get_length() - 1):
                previous_step = self.current_mission.get_step(i)
                next_step = self.current_mission.get_step(i + 1)

                previous_pos = QgsPointXY(float(previous_step.get_maneuver().get_position().get_longitude()),
                                          float(previous_step.get_maneuver().get_position().get_latitude()))
                next_pos = QgsPointXY(float(next_step.get_maneuver().get_position().get_longitude()),
                                      float(next_step.get_maneuver().get_position().get_latitude()))

                distance = self.distance_calc.measureLine([previous_pos, next_pos])
                total_distance += distance

                if next_step.get_maneuver().get_maneuver_type() == PARK_MANEUVER:  # park
                    time = float(next_step.get_maneuver().time)
                    total_time += time

                if float(next_step.get_maneuver().get_speed()) == 0:
                    time = 0
                else:
                    # estimated speed is 80% of speed
                    time = distance / (float(next_step.get_maneuver().get_speed()) * 0.8)
                total_time += time

            self.total_distance.setText(str(int(total_distance))+"m")
            self.estimated_time.setText(str(datetime.timedelta(seconds=int(total_time))))
