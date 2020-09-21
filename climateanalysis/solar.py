""" This Module ..."""
from __future__ import division
import math
import numpy as np


# Exception handling for arcsine and arccosine functions: only necessary
# when using exclusively solar time
# only used for calculating the sun position when inside the arctic or antarctic circle, used in sunpath
# specific instance
def arccos(x):
    if x >= 1:
        arccos = 0
    elif x <= -1:
        arccos = math.pi
    else:
        arccos = math.atan(-x / (-x * x + 1) ** 0.5) + 2 * math.atan(1)
    return arccos


def arcsin(x):
    if x >= 1:
        arcsin = math.pi / 2
    elif x <= -1:
        arcsin = -math.pi / 2
    else:
        arcsin = math.atan(x / (-x * x + 1) ** 0.5)
    return arcsin


def declin_angle(julian_day, in_radians=False):
    """
    Calculate the sun's declination angle for a particular day of the year.

    Args:
        julian_day: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        in_radians: Bool indicating whether or not to return the angle in radians. Default is false.

    Returns:
        The declination angle of the sun in degrees
    """
    tau = 2 * math.pi * (julian_day - 1) / 365
    declin_angle = 0.006918 - 0.399912 * math.cos(tau) + 0.070257 * math.sin(tau) - 0.006758 * math.cos(
        2 * tau) + 0.000907 * math.sin(2 * tau) - 0.002697 * math.cos(3 * tau) + 0.00148 * math.sin(3 * tau)
    if in_radians:
        return declin_angle
    return np.degrees(declin_angle)


def day_length(julian_day, latitude):
    """
    Calculates the number of hours that the sun is above the horizon

    Args:
        julian_day: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        latitude: Latitude in degrees

    Returns:

    """
    lat_radians = np.radians(latitude)
    return 24 * arccos(-math.tan(lat_radians) * math.tan(np.radians(declin_angle(julian_day)))) / math.pi


def rise_set_times(julian_day, latitude):
    """
    Calculates the sunrise and sunset times

    Args:
        julian_day:
        latitude: Latitude in degrees

    Returns:

    """
    DL = day_length(julian_day, latitude)
    sunset_time = 12 + DL / 2
    sunrise_time = 12 - DL / 2
    return sunset_time, sunrise_time


def altitude_angle(julian_day, hour, latitude, in_radians=False):
    """
    Calculates the solar altitude in radians

    Args:
        julian_day: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        hour:
        latitude: Latitude in degrees
        in_radians: Bool indicating whether or not to return the angle in radians. Default is false.

    Returns:
        The altitude angle in degrees.
    """
    lat_radians = np.radians(latitude)
    hour_angle = math.pi * hour / 12
    solar_declin_angle = declin_angle(julian_day, in_radians=True)
    solar_altitude = arcsin(
        math.sin(lat_radians) * math.sin(solar_declin_angle) - math.cos(lat_radians) * math.cos(solar_declin_angle) * math.cos(hour_angle))
    if solar_altitude < 0:
        solar_altitude = 0
    if in_radians:
        return solar_altitude
    return np.degrees(solar_altitude)


def azimuth_angle(julian_day, hour, latitude, in_radians=False):
    """
    Calculates the solar azimuth.

    Args:
        julian_day: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        hour: The hour of the given day
        latitude: Latitude in degrees
        in_radians: Bool indicating whether or not to return the angle in radians. Default is false.

    Returns:
        (Union[float, int, ndarray]): The solar azimuth angle in degrees.
    """
    lat_radians = np.radians(latitude)
    hour_angle = math.pi * hour / 12
    solar_declin_angle = declin_angle(julian_day, in_radians=True)
    solar_alt_angle = altitude_angle(julian_day, hour, latitude, in_radians=True)
    if hour_angle < math.pi:
        solar_azimuth = arccos(
            (-math.sin(lat_radians) * math.sin(solar_alt_angle) + math.sin(solar_declin_angle)) / (math.cos(lat_radians) * math.cos(solar_alt_angle)))
    else:
        solar_azimuth = ((2 * math.pi) - arccos(
            (-math.sin(lat_radians) * math.sin(solar_alt_angle) + math.sin(solar_declin_angle)) / (math.cos(lat_radians) * math.cos(solar_alt_angle))))
    if in_radians:
        return solar_azimuth
    return np.degrees(solar_azimuth)


# Rework to take the params for solar_alt and solar_az + calculate them in the function.
def cosine_angle_incidence(wall_azimuth_angle, surface_tilt_angle, solar_alt, solar_az):
    """
    Calculates the cosine of the angle of incidence on a tilted plane.

    Args:
        wall_azimuth_angle: degrees
        surface_tilt_angle: degrees
        solar_alt: degrees
        solar_az: degrees

    Returns:
        The cosine of the angle of incidence
    """
    wall_azimuth_rads = np.radians(wall_azimuth_angle)
    tilt_angle_rads = np.radians(surface_tilt_angle)
    sol_alt_rads = np.radians(solar_alt)
    sol_az_rads = np.radians(solar_az)
    wallsolaz = math.fabs(sol_az_rads - wall_azimuth_rads)
    CAI = math.cos(sol_alt_rads) * math.cos(wallsolaz) * math.sin(tilt_angle_rads) \
          + math.sin(sol_alt_rads) * math.cos(tilt_angle_rads)
    if CAI < 0:
        CAI = 0
    return CAI


def time_diff(julian_day, EqTonly, longitude, timezone, timeshift=-0.5):
    """
    Calculates the difference between solar time and clock time.

    Args:
        julian_day: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        EqTonly:
        longitude: Longitude in degrees
        timezone: The timezone of the location
        timeshift:

    Returns:
        (float):
    """
    B = 2 * math.pi * (julian_day - 1) / 365
    # The term on the left below, converts from radians, through degrees, to minutes: Earth takes 4minutes to rotate one degree.
    EqT = (4 * 180 / math.pi) * (0.000075 + 0.001868 * math.cos(B) - 0.032077 * math.sin(B) - 0.014615 * math.cos(
        2 * B) - 0.040849 * math.sin(2 * B))
    if not EqTonly:
        # NB: timeshift accounts for the climate file time convention: hour-centred corresponds to +/-30mins
        deltaT = 4 * longitude - 60 * timezone + (60 * timeshift) + EqT
    else:
        deltaT = EqT
    # conversion to hours:
    return deltaT / 60


