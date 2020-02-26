# -*- coding: utf-8 -*-
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
 Utils to perform computations with points and angles
"""

from qgis.core import QgsPointXY, QgsDistanceArea, QgsGeometry
import math


def wrap_angle(angle):
    return angle + (2.0 * math.pi * math.floor((math.pi - angle) / (2.0 * math.pi)))


def get_angle_of_line_between_two_points(p1, p2, angle_unit="degrees"):
    x_diff = p2.x() - p1.x()
    y_diff = p2.y() - p1.y()

    if angle_unit == "radians":
        return math.atan2(y_diff, x_diff)
    else:
        return math.degrees(math.atan2(y_diff, x_diff))


def calc_pente(p1, p2):
    """
    Return the slope of the line represents by two points : p1 and p2

    :param p1: The first point
    :param p2: The second point
    :type p1: QgsPointXY
    :type p2: QgsPointXY
    :return: Return the slope (degre)
    :rtype: float
    """

    num = p1.x() - p2.x()
    denum = p1.y() - p2.y()

    # Avoid division by zero
    if num == 0:
        # Return a negative value if denum > 0
        if denum > 0:
            return -90
        else:
            # else return a positive value
            return 90
    # Same as above with denum
    elif denum == 0:
        if num > 0:
            return -90
        else:
            return 90
    else:
        return denum / num


def calc_angle_existant(p1, p2):
    """
    Return the angle of the line represents by two points : p1 and p2

    :param p1: The first point
    :param p2: The second point
    :type p1: QgsPointXY
    :type p2: QgsPointXY
    :return: Return the angle (degre)
    :rtype: float
    """

    a = calc_pente(p1, p2)  # The slope of the segment p1-p2
    length_p1p2 = QgsDistanceArea().measureLine(p1, p2)  # Hypothenuse
    length_adjacent = math.fabs(p2.y() - p1.y())  # Adjacent
    if length_p1p2 == 0:  # Normally you can't have a length of 0 but avoid division by zero
        angle_CAB = 0
    else:
        angle_CAB = math.acos(length_adjacent / length_p1p2)  #

    # Correction of angle_CAB
    if a < 0:
        angle_CAB = angle_CAB - math.pi / 2
    elif a > 0:
        angle_CAB = math.pi / 2 - angle_CAB

    return angle_CAB


def calc_is_collinear(p0, p1, p2):
    # Test if point p2 is on left/on/right of the line [p0p1]
    # 1 left
    # 0 collinear
    # -1 right

    sens = ((p1.x() - p0.x()) * (p2.y() - p0.y()) - (p1.y() - p0.y()) * (p2.x() - p0.x()))

    if sens > 0:
        return -1
    elif sens < 0:
        return 1
    else:
        return 0


def calc_milieu_line(p1, p2):
    return QgsPointXY((p1.x() + p2.x()) / 2.0, (p1.y() + p2.y()) / 2.0)


def calc_parallel_segment(p1, p2, dist):
    # from cadtools (c) Stefan ZIegler

    if dist == 0:
        points = [p1, p2]
        g = QgsGeometry.fromPolyline(points)
        return g

    dn = QgsDistanceArea().measureLine(p1, p2)
    x3 = p1.x() + dist * (p1.y() - p2.y()) / dn
    y3 = p1.y() - dist * (p1.x() - p2.x()) / dn
    p3 = QgsPointXY(x3, y3)

    x4 = p2.x() + dist * (p1.y() - p2.y()) / dn
    y4 = p2.y() - dist * (p1.x() - p2.x()) / dn
    p4 = QgsPointXY(x4, y4)

    points = [p3, p4]
    g = QgsGeometry.fromPolyline(points)

    return g


def distance(start, end):
    # Assumes points are WGS 84 lat/long
    # Returns great circle distance in meters
    radius = 6378137  # meters
    flattening = 1 / 298.257223563

    # Convert to radians with reduced latitudes to compensate
    # for flattening of the earth as in Lambert's formula
    start_lon = start.x() * math.pi / 180
    start_lat = math.atan2((1 - flattening) * math.sin(start.y() * math.pi / 180), math.cos(start.y() * math.pi / 180))
    end_lon = end.x() * math.pi / 180
    end_lat = math.atan2((1 - flattening) * math.sin(end.y() * math.pi / 180), math.cos(end.y() * math.pi / 180))

    # Haversine formula
    arc_distance = (math.sin((end_lat - start_lat) / 2) ** 2) + \
                   (math.cos(start_lat) * math.cos(end_lat) * (math.sin((end_lon - start_lon) / 2) ** 2))

    return 2 * radius * math.atan2(math.sqrt(arc_distance), math.sqrt(1 - arc_distance))


def bearing(start, end):
    # Assumes points are WGS 84 lat/long
    # http://www.movable-type.co.uk/scripts/latlong.html

    start_lon = start.x() * math.pi / 180
    start_lat = start.y() * math.pi / 180
    end_lon = end.x() * math.pi / 180
    end_lat = end.y() * math.pi / 180

    return math.atan2(math.sin(end_lon - start_lon) * math.cos(end_lat),
                      (math.cos(start_lat) * math.sin(end_lat))
                      - (math.sin(start_lat) * math.cos(end_lat) * math.cos(end_lon - start_lon))) * 180 / math.pi


def endpoint(start, dist, degrees_bearing):
    # Sphere aproximation
    # Assumes points are WGS 84 lat/long, distance in meters,
    # bearing in degrees with north = 0, east = 90, west = -90
    # http://www.movable-type.co.uk/scripts/latlong.html
    radius = 6378137.0  # meters

    start_lon = start.x() * math.pi / 180
    start_lat = start.y() * math.pi / 180
    bearing = degrees_bearing * math.pi / 180

    end_lat = math.asin((math.sin(start_lat) * math.cos(dist / radius)) +
                        (math.cos(start_lat) * math.sin(dist / radius) * math.cos(bearing)))
    end_lon = start_lon + math.atan2(math.sin(bearing) * math.sin(dist / radius) * math.cos(start_lat),
                                     math.cos(dist / radius) - (math.sin(start_lat) * math.sin(end_lat)))

    return QgsPointXY(end_lon * 180 / math.pi, end_lat * 180 / math.pi)

def endpoint_ellipsoid(start, dist, degrees_bearing):
    # Ellipsoid aproximation
    # Assumes points are WGS 84 lat/long, distance in meters,
    # bearing in degrees with north = 0, east = 90, west = -90
    # https://www.movable-type.co.uk/scripts/latlong-vincenty.html
    start_lon = start.x() * math.pi / 180
    start_lat = start.y() * math.pi / 180
    bearing = degrees_bearing * math.pi / 180
    d = dist

    a = 6378137
    f = 0.003352813
    b = 6356752.3142

    sin_angle1 = math.sin(bearing)
    cos_angle1 = math.cos(bearing)

    tan_U1 = (1-f) * math.tan(start_lat)
    cos_U1 = 1 / math.sqrt((1+ tan_U1*tan_U1))
    sin_U1 = tan_U1 * cos_U1
    o1 = math.atan2(tan_U1, cos_angle1)
    sin_angle = cos_U1 * sin_angle1
    cosSq_angle = 1 - sin_angle*sin_angle
    uSq = cosSq_angle * (a*a - b*b) / (b*b)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))

    r1 = d / (b*A)
    r2 = 0.0
    iteration = 0
    while abs(r1 - r2 > 1e-12) and iteration < 100:
        cos2roM = math.cos(2*o1 + r1)
        sin_ro = math.sin(r1)
        cos_ro = math.cos(r1)
        dif_ro = B * sin_ro * (cos2roM + B/4 * (cos_ro * (-1 + 2*cos2roM*cos2roM) -
                                                B/6 * cos2roM * (-3 +4*sin_ro*sin_ro) *
                                                (-3 + 4*cos2roM*cos2roM)))
        r2 = r1
        r1 = d / (b*A) + dif_ro
        iteration += 1

    x = sin_U1*sin_ro - cos_U1*cos_ro*cos_angle1
    lon = math.atan2(sin_ro*sin_angle1, cos_U1*cos_ro - sin_U1*sin_ro*cos_angle1)
    C = f/16 * cosSq_angle*(4+f * (4 - 3*cosSq_angle))
    L = lon - (1-C) * f * sin_angle * (r1 + C*sin_ro * (cos2roM+C*cos_ro * (-1 + 2*cos2roM*cos2roM)))

    end_lon = (start_lon + L + 3*math.pi) % (2*math.pi) - math.pi
    end_lat = math.atan2(sin_U1 * cos_ro + cos_U1 * sin_ro * cos_angle1, (1 - f) * math.sqrt(sin_angle * sin_angle + x * x))

    return QgsPointXY(end_lon * 180 / math.pi, end_lat * 180 / math.pi)

def magnitude(p1, p2):
    """

    :param p1: The first point
    :param p2: The second point
    :type p1: QgsPointXY
    :type p2: QgsPointXY
    :return: Return distance between p1 and p2
    """
    vect_x = p2.x() - p1.x()
    vect_y = p2.y() - p1.y()
    return math.sqrt(vect_x ** 2 + vect_y ** 2)


def intersect_point_to_line(point, line_start, line_end):
    """

    :param point: The point that will be projected on the line
    :param line_start: The first point of line
    :param line_end: The second point of line
    :type point: QgsPointXY
    :type line_start: QgsPointXY
    :type line_end: QgsPointXY
    :return: return the projection of the point on the line
    """

    # distances between vertex
    start_to_p = magnitude(line_start, point)
    end_to_p = magnitude(line_end, point)
    start_to_end = magnitude(line_start, line_end)
    # cosines theorem, angle in radians
    r = ((end_to_p ** 2) - (start_to_p ** 2) - (start_to_end ** 2)) / (-2 * start_to_p * start_to_end)
    if r > 1:
        r = 1
    elif r < -1:
        r = -1
    angle_s = math.acos(r)

    # get small angle of vertex-point
    angle_p_small = math.pi/2 - angle_s
    # get distance between start and projection
    c = start_to_p * math.sin(angle_p_small)

    # get projection position from line
    xp = line_start.x() + (c / start_to_end) * (line_end.x() - line_start.x())
    yp = line_start.y() + (c / start_to_end) * (line_end.y() - line_start.y())

    return QgsPointXY(xp, yp)


def is_between( ax, ay, bx, by, cx, cy):
        """
        Calculate if point C (cx, cy) is between points: A (ax, ay) and B (bx, by)
        :param ax: point A, x-coordinate
        :param ay: point A, y-coordinate
        :param bx: point B, x-coordinate
        :param by: point B, y-coordinate
        :param cx: point C, x-coordinate
        :param cy: point C, x-coordinate
        :return: return True if C is between A and B, otherwise False
        """
        cross_product = (cy - ay) * (bx - ax) - (cx - ax) * (by - ay)
        if abs(cross_product) == 0:
            dist_a_to_c = math.sqrt((cx - ax) ** 2 + (cy - ay) ** 2)
            dist_c_to_b = math.sqrt((cx - bx) ** 2 + (cy - by) ** 2)
            dist_a_to_b = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
            if dist_a_to_c + dist_c_to_b != dist_a_to_b:  # if point c is not in between points a and b
                return False

        dot_product = (cx - ax) * (bx - ax) + (cy - ay) * (by - ay)
        if dot_product < 0:
            return False

        squared_length_ba = (bx - ax) ** 2 + (by - ay) ** 2
        if dot_product > squared_length_ba:
            return False

        return True