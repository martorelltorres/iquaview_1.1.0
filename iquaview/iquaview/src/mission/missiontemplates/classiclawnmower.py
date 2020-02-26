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
 Classic lawn mower pattern definition
"""

import math
import logging

from iquaview.src.cola2api.mission_types import (Mission,
                                                 MissionStep,
                                                 MissionPosition,
                                                 MissionWaypoint,
                                                 MissionSection,
                                                 MissionTolerance)
from qgis.core import QgsDistanceArea, QgsCoordinateReferenceSystem, QgsProject

logger = logging.getLogger(__name__)


class ClassicLawnMower(object):

    def __init__(self):
        self.template_type = 'classic_lawnmower'
        self.wp = list()
        self.mission = None
        self.distance = QgsDistanceArea()
        self.distance.setSourceCrs(QgsCoordinateReferenceSystem(4326), QgsProject.instance().transformContext())
        self.distance.setEllipsoid('WGS84')

    def get_mission_type(self):
        return self.template_type

    def get_mission(self):
        return self.mission

    def compute_tracks(self, area_points, track_spacing, num_across_tracks):

        """
             Compute lawn-mower tracks
            :param area_points: points defining the extent of the tracks, they should be in WGS 84 lat/lon.
                                first two points define the along track direction.
            :param track_spacing: desired space in meters between consecutive along tracks
            :param num_across_tracks: number of desired across tracks. They will be equally spaced through the area.
            :return: list of ordered waypoints of the lawn-mower trajectory
            """

        dist_along_track = self.distance.measureLine(area_points[0], area_points[1])
        dist_across_track = self.distance.measureLine(area_points[1], area_points[2])
        bearing_along_track = self.distance.bearing(area_points[0], area_points[1])
        bearing_across_track = self.distance.bearing(area_points[1], area_points[2])

        turn_track_dist = length_one_across_track = track_spacing

        num_along_tracks = math.ceil(dist_across_track / length_one_across_track) + 1

        logger.debug("distAlongTrack: {}".format(dist_along_track))
        logger.debug("distAcrossTrack: {}".format(dist_across_track))
        logger.debug("bearingAlongTrack {}:".format(bearing_along_track))
        logger.debug("bearingAcrossTrack {}:".format(bearing_across_track))
        logger.debug("numAlongTrack: {}".format(num_along_tracks))
        logger.debug("numAcrossTrack: {}".format(num_across_tracks))
        logger.debug("lenghtOneAcrossTrack {}".format(length_one_across_track))

        # Initialize with 2 first points
        current_wp = area_points[0]
        next_wp = area_points[1]
        reverse_direction_along = False  # For changing direction of alternate along tracks
        wp_list = [current_wp]

        # Loop to generate all waypoints of along tracks
        for i in range(int(num_along_tracks) * 2 - 1):

            wp_list.append(next_wp)

            current_wp = next_wp
            if i % 2 == 0:  # even, so we just did along track, next draw across track
                next_wp = self.distance.computeSpheroidProject(current_wp, length_one_across_track,
                                                               bearing_across_track)
                reverse_direction_along = not reverse_direction_along
            else:
                # Draw along track
                next_wp = self.distance.computeSpheroidProject(current_wp,
                                                               dist_along_track,
                                                               bearing_along_track + int(
                                                                   reverse_direction_along) * math.radians(180.0))

        # Loop for across tracks
        if num_across_tracks > 0:
            dist_along_track_for_across = dist_along_track / (num_across_tracks + 1)
            # Distance across track after computing all the along tracks
            # (might not match with the across track distance defined on the area mission)
            if reverse_direction_along:
                real_dist_across_track = self.distance.measureLine(wp_list[0], wp_list[-2])
            else:
                real_dist_across_track = self.distance.measureLine(wp_list[0], wp_list[-1])
            next_wp = self.distance.computeSpheroidProject(current_wp, turn_track_dist, bearing_across_track)
            reverse_direction_across = True  # For changing direction of alternate across tracks

            for i in range(num_across_tracks * 2 + 1):
                wp_list.append(next_wp)
                current_wp = next_wp
                if i % 2 == 0:  # Compute waypoint along track
                    next_wp = self.distance.computeSpheroidProject(current_wp,
                                                                   dist_along_track_for_across,
                                                                   bearing_along_track + int(
                                                                       reverse_direction_along) * math.radians(180.0))
                else:  # Compute waypoint across track
                    next_wp = self.distance.computeSpheroidProject(current_wp,
                                                                   real_dist_across_track + 2 * turn_track_dist,
                                                                   bearing_across_track + int(
                                                                       reverse_direction_across) * math.radians(180.0))
                    reverse_direction_across = not reverse_direction_across
        return wp_list

    def track_to_mission(self, wp_list, z, altitude_mode, speed, tolerance_x, tolerance_y, tolerance_z):

        self.mission = Mission()
        for wp in range(len(wp_list)):
            if wp == 0:
                # first step type waypoint
                step = MissionStep()
                mwp = MissionWaypoint(MissionPosition(wp_list[wp].y(), wp_list[wp].x(), z, altitude_mode),
                                      speed,
                                      MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                step.add_maneuver(mwp)
                self.mission.add_step(step)
            else:
                # rest of steps type section
                step = MissionStep()
                mwp = MissionSection(MissionPosition(wp_list[wp - 1].y(), wp_list[wp - 1].x(), z, altitude_mode),
                                     MissionPosition(wp_list[wp].y(), wp_list[wp].x(), z, altitude_mode),
                                     speed,
                                     MissionTolerance(tolerance_x, tolerance_y, tolerance_z))
                step.add_maneuver(mwp)
                self.mission.add_step(step)
