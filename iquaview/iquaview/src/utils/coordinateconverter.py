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
 Helpers for coordinate conversions
"""


def degree_to_degree_minute(lat, lon):
    """
    Transforms coordinates from DDD.DDDDD (float) to a string of DDD, MM.MM """
    lat_degree = __degree_to_degree_minute_aux__(lat)
    lon_degree = __degree_to_degree_minute_aux__(lon)
    # lat_degree = __splitDegreeMinutes__(lat_degree)
    # lon_degree = __splitDegreeMinutes__(lon_degree)

    return lat_degree, lon_degree


def degree_minute_to_degree(lat, lon):
    """
    Transforms latitude and longitude in the format
            DDD MM.MM to the format DDD.DD
    :param lat: lat is a list, first element is degrees, second element is decimal minutes
    :param lon: lon is a list, first element is degrees, second element is decimal minutes
    :return: return lat and lon in degrees (DDD.DD)
    """
    return float(lat[0]) + float(lat[1]) / 60.0, float(lon[0]) + float(lon[1]) / 60.0


def degree_to_degree_minute_second(lat, lon):
    """
    Transforms coordinates from DDD.DDDDD (float) to a string of
    DDDºMM'SS.SSS''
    @param lat: latitude
    @type lat: float
    @param lon: longitude
    @type lon: float
    """
    lat_str = __degree_to_degree_minute_second_aux__(lat)
    lon_str = __degree_to_degree_minute_second_aux__(lon)
    return [lat_str, lon_str]


def degree_minute_second_to_degree(lat, lon):
    """
    Transforms coordinates from DDDºMM'SS.SSS'' string to a  of
    DDD.DDDDD (float)
    @param lat: value in DDDºMM'SS.SSS''
    @type lat: string
    @param lon: value in DDDºMM'SS.SSS''
    @type lon: string
    """
    lat_float = __degree_minute_second_to_degree_aux__(lat)
    lon_float = __degree_minute_second_to_degree_aux__(lon)
    return lat_float, lon_float


def __degree_minute_second_to_degree_aux__(value):
    """
    Transforms coordinates from DDDºMM'SS.SSS'' string to a  of
    DDD.DDDDD (float)
    @param value: value in DDDºMM'SS.SSS''
    @type value: string
    """
    deg, min_sec = str(value).split('º')
    min_sec, rest = min_sec.split('\'\'')
    minute, sec = min_sec.split('\'')

    dd = float(deg) + float(minute) / 60 + float(sec) / (60 * 60)
    return dd


def __degree_to_degree_minute_second_aux__(value):
    """
    Transforms coordinates from DDD.DDDDD (float) to a string of
    DDDºMM'SS.SSS''
    @param value: value in DDD.DDDDD
    @type value: float
    """
    d = int(value)
    t = (value - d) * 60
    m = int(t)
    s = (t - m) * 60
    return "{:d}º {:d}' {:f}''".format(d, m, s)


def __degree_to_degree_minute_aux__(value):
    val = str(value).split('.')
    if val[0] == '':  # for cases like ".25" instead of "0.25"
        val[0] = 0
    if len(val) > 1:
        minute = float('0.' + val[1]) * 60.0
    else:
        minute = 0.0
    if minute < 10.0:
        return "{:d}º 0{:f}'".format(int(val[0]), minute)
    else:
        return "{:d}º {:f}'".format(int(val[0]), minute)


def __split_degree_minutes__(value):
    """ Transform DDDMM.MM to DDD, MM.MM """
    val = str(value).split('.')
    val_min = val[0][-2] + val[0][-1] + '.' + val[1]
    val_deg = ''
    for i in range(len(val[0]) - 2):
        val_deg = val_deg + val[0][i]

    return int(val_deg), float(val_min)
