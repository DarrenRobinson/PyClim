from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
import math
from climateanalysis import solar as sol


def _plot_sunpaths(latitude, month_list, colour_list):
    """
    Intended for internal use only.

    Args:
        latitude: Latitude (degrees)
        month_list:
        colour_list:
    """
    azimuth_angles_rads = []
    altitude_angles_degrees = []
    sunpath_x = []
    sunpath_y = []
    sunpath_julian_days = [355, 325, 294, 264, 233, 202, 172, 141, 111, 80, 52, 21]
    for month in range(1, 8):
        position = 0
        day = sunpath_julian_days[month - 1]
        sunset_hour, sunrise_hour = sol.rise_set_times(day, latitude)

        if sunset_hour < 24:
            # in this case we need to plot from the non-integer sunrise time, through to sunset
            altitude_angles_degrees.append(sol.altitude_angle(day, sunrise_hour, latitude))
            azimuth_angles_rads.append(sol.azimuth_angle(day, sunrise_hour, latitude, in_radians=True))
            sunpath_x.append((90 - altitude_angles_degrees[0]) * math.sin(azimuth_angles_rads[0]))
            sunpath_y.append((90 - altitude_angles_degrees[0]) * math.cos(azimuth_angles_rads[0]))

            for hour in range(int(math.ceil(sunrise_hour)), int(sunrise_hour) + 2 * (12 - int(sunrise_hour))):
                position = position + 1
                altitude_angles_degrees.append(sol.altitude_angle(day, hour, latitude))
                azimuth_angles_rads.append(sol.azimuth_angle(day, hour, latitude, in_radians=True))
                sunpath_x.append((90 - altitude_angles_degrees[position]) * math.sin(azimuth_angles_rads[position]))
                sunpath_y.append((90 - altitude_angles_degrees[position]) * math.cos(azimuth_angles_rads[position]))

            altitude_angles_degrees.append(sol.altitude_angle(day, sunset_hour, latitude))
            azimuth_angles_rads.append(sol.azimuth_angle(day, sunset_hour, latitude, in_radians=True))
            sunpath_x.append(90 * math.sin(azimuth_angles_rads[position + 1]))
            sunpath_y.append(90 * math.cos(azimuth_angles_rads[position + 1]))
        else:
            # in this case we simply need to plot for the entire 24h period
            for hour in range(0, 25):
                altitude_angles_degrees.append(sol.altitude_angle(day, hour, latitude))
                azimuth_angles_rads.append(sol.azimuth_angle(day, hour, latitude, in_radians=True))
                sunpath_x.append((90 - altitude_angles_degrees[position]) * math.sin(azimuth_angles_rads[position]))
                sunpath_y.append((90 - altitude_angles_degrees[position]) * math.cos(azimuth_angles_rads[position]))
                position = position + 1

        plt.plot(sunpath_x, sunpath_y, c=colour_list[7 - month], label=(month_list[month - 1]), marker='o')

        del altitude_angles_degrees[:]
        del azimuth_angles_rads[:]
        del sunpath_x[:]
        del sunpath_y[:]


def _plot_time_curves(latitude, use_eq_time_only, use_clock_time):
    """
    Intended for internal use only.

    Args:
        latitude:
        use_eq_time_only:
        use_clock_time:
    """
    time_curve_x = []
    time_curve_y = []
    lat_radians = np.radians(latitude)
    # if the sun is below the horizon during the summer solstice for this hour then skip
    if lat_radians > 0:
        summerday = 172
    else:
        summerday = 355
    for hour in range(0, 25):
        for day in range(1, 366):
            if sol.altitude_angle(summerday, hour, latitude, in_radians=True) > 0:
                # this controls whether solar time curves of the analemma are plotted
                if use_clock_time:
                    EqT = sol.time_diff(day, use_eq_time_only, 0, 0, 0)  #!!!!! SHOULD THESE BE CONFIGURABLE?
                else:
                    EqT = 0
                altitude_angle_degrees = sol.altitude_angle(day, hour + EqT, latitude)
                if np.radians(altitude_angle_degrees) > 0:
                    azimuth_angle_radians = sol.azimuth_angle(day, hour + EqT, latitude, in_radians=True)
                    time_curve_x.append((90 - (altitude_angle_degrees)) * math.sin(azimuth_angle_radians))
                    time_curve_y.append((90 - (altitude_angle_degrees)) * math.cos(azimuth_angle_radians))
        plt.plot(time_curve_x, time_curve_y, c='darkblue')
        del time_curve_x[:]
        del time_curve_y[:]


def _plot_horizontal_protractors(wall_azimuth):
    """
    Intended for internal use only.

    Args:
        wall_azimuth: The wall azimuth angle (degrees)
    """
    protractor_x = []
    protractor_y = []
    for theta in range(10, 90, 10):
        for orientation in range(wall_azimuth - 90, wall_azimuth + 100, 10):
            theta_adjusted = math.degrees(math.atan(
                math.tan(theta * math.pi / 180) * math.cos(np.radians(math.fabs(orientation - wall_azimuth)))))
            protractor_x.append((90 - theta_adjusted) * math.sin(np.radians(orientation)))
            protractor_y.append((90 - theta_adjusted) * math.cos(np.radians(orientation)))
        plt.plot(protractor_x, protractor_y, c='darkorange', lw=2, linestyle=':')
        del protractor_x[:]
        del protractor_y[:]


def _plot_vertical_protractors(wall_azimuth):
    """
    Intended for internal use only.

    Args:
        wall_azimuth: The wall azimuth angle (degrees)
    """
    protractor_x = []
    protractor_y = []
    for orientation in range(wall_azimuth - 90, wall_azimuth + 100, 10):
        protractor_x.append(90 * math.sin(np.radians(orientation)))
        protractor_y.append(90 * math.cos(np.radians(orientation)))
        protractor_x.append(0 * math.sin(np.radians(orientation)))
        protractor_y.append(0 * math.cos(np.radians(orientation)))
        plt.plot(protractor_x, protractor_y, c='darkorange', lw=2, linestyle=':')
        del protractor_x[:]
        del protractor_y[:]


def _plot_iso_alt_radial_az(azimuth_increment):
    """
    Intended for internal use only.

    Args:
        azimuth_increment: The azimuth increment (degrees)
    """
    circles_x = []
    circles_y = []
    spokes_x = []
    spokes_y = []
    for circle in range(90, 0, -10):
        for orientation in range(0, 360 + azimuth_increment, azimuth_increment):
            circles_x.append(circle * math.sin(np.radians(orientation)))
            circles_y.append(circle * math.cos(np.radians(orientation)))
            if circle == 80:
                spokes_x.append(90 * math.sin(np.radians(orientation)))
                spokes_y.append(90 * math.cos(np.radians(orientation)))
                spokes_x.append(0 * math.sin(np.radians(orientation)))
                spokes_y.append(0 * math.cos(np.radians(orientation)))
            if circle == 90 and orientation < 360:
                plt.text(95 * math.sin(orientation * math.pi / 180), 95 * math.cos(np.radians(orientation)),
                         str(orientation) + '$^o$', color='darkgray', horizontalalignment='center', fontsize=8)
        # This part doesn't really make sense to me?
        if circle < 90 and circle != 0:
            plt.text((circle + 1) * math.sin(5 * math.pi / 180), (circle + 1) * math.cos(np.radians(orientation)),
                     str(90 - circle) + '$^o$', color='darkgray', horizontalalignment='center', fontsize=8)

        plt.plot(circles_x, circles_y, lw=1, color='darkgray')
        plt.plot(spokes_x, spokes_y, lw=1, color='darkgray')
        del circles_x[:]
        del circles_y[:]
        del spokes_x[:]
        del spokes_y[:]


def plot_sunpath_diagram(latitude, wall_azimuth, azimuth_increment, plot_h_protractors=False, plot_v_protractors=False, use_eq_time_only=True, use_clock_time=False):
    """
    Prepare a Stereoscopic sunpath diagram.

     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        latitude: Latitude (degrees)
        wall_azimuth: The wall azimuth angle (degrees)
        azimuth_increment: The azimuth increment (degrees)
        plot_h_protractors: Whether or not to plot horizontal protractors. False by default.
        plot_v_protractors: Whether or not to plot vertical protractors. False by default.
        use_eq_time_only:
        use_clock_time:
    """
    colour_list = ['firebrick', 'darkorange', 'orange', 'gold', 'green', 'cyan', 'blue']
    month_list = ['Dec', 'Nov/Jan', 'Oct/Feb', 'Sep/Mar', 'Aug/Apr', 'Jul/May', 'Jun']
    plt.figure(figsize=(9, 9))

    # PLOT ISO-ALTITUDE CIRCLES AND RADIAL AZIMUTH LINES
    _plot_iso_alt_radial_az(azimuth_increment)
    # PLOT SUNPATHS
    _plot_sunpaths(latitude, month_list, colour_list)
    # PLOT TIME CURVES
    _plot_time_curves(latitude, use_eq_time_only, use_clock_time)
    # PLOT PROTRACTORS
    if plot_h_protractors:
        _plot_horizontal_protractors(wall_azimuth)
    if plot_v_protractors:
        _plot_vertical_protractors(wall_azimuth)

    lat_radians = np.radians(latitude)
    if lat_radians < 0:
        hemisphere = "S"
    else:
        hemisphere = "N"

    plt.title(
        'Stereographic sunpath diagram, for latitude: ' + str(int(180 * math.fabs(lat_radians) / math.pi)) + '$^o$' + str(
            hemisphere),
        loc='center')
    plt.legend(loc='lower left', frameon=False)
    plt.axis('off')
    plt.tight_layout()

    # plt.savefig("test.svg", format='svg')

