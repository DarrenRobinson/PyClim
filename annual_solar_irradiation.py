from __future__ import division

import math
import matplotlib.pyplot as plt
import numpy as np

from climateanalysis import illuminance_irradiance as ilr
from climateanalysis import solar as sol


def annual_solar_irradiation(glbl_h_rad_data, diffuse_h_rad_data, latitude, longitude, timezone, timeshift=-0.5,
                             use_isotropic=False, use_diffuse_only=False):
    """
    Calculates hourly solar irradiation data for a year.

    Args:
        glbl_h_rad_data: Hourly global horizontal radiation data for a year for a location.
        diffuse_h_rad_data: Hourly diffuse horizontal radiation data for a year for a location.
        latitude: Latitude (degrees)
        longitude: Longitude (degrees)
        timezone: The time zone of the location
        timeshift:
        use_isotropic:
        use_diffuse_only:

    Returns:
        Calculated hourly solar irradiation data for a year.
    """

    solar_alts = []
    solar_azimuths = []
    solar_time_diffs = []
    cos_angle_incds = []
    igbeta_list = []

    annualirrad_list = []

    first_pass = True
    for tilt_angle in range(0, 95, 10):  # tilt degrees?
        for wall_azimuth_angle in range(0, 360, 10):  # azimuth degrees?
            cumulative_hour_index = 0
            globalirradbeta = 0
            for day_of_year in range(1, 366):  # days of year
                if first_pass:
                    solar_time_diffs.append(sol.time_diff(day_of_year, False, longitude, timezone, timeshift))
                    # This populates a list of daily SR, SS times, for the solar availability plots
                for hour_of_day in range(1, 25):  # hours of day
                    if first_pass:
                        solar_alts.append(
                            sol.altitude_angle(day_of_year,
                                               hour_of_day + solar_time_diffs[day_of_year - 1],
                                               latitude))
                        solar_azimuths.append(
                            sol.azimuth_angle(day_of_year,
                                              hour_of_day + solar_time_diffs[day_of_year - 1],
                                              latitude))

                    cos_angle_incds.append(
                        sol.cosine_angle_incidence(wall_azimuth_angle,
                                                   tilt_angle,
                                                   solar_alts[cumulative_hour_index],
                                                   solar_azimuths[cumulative_hour_index]))
                    igbeta_list.append(
                        ilr.igbeta(day_of_year,
                                   cos_angle_incds[cumulative_hour_index],
                                   glbl_h_rad_data[cumulative_hour_index],
                                   diffuse_h_rad_data[cumulative_hour_index],
                                   np.radians(solar_alts[cumulative_hour_index]),
                                   tilt_angle * math.pi / 180,
                                   use_isotropic,
                                   use_diffuse_only))

                    globalirradbeta += igbeta_list[cumulative_hour_index]
                    cumulative_hour_index += 1

            first_pass = False
            annualirrad_list.append(globalirradbeta)
            del cos_angle_incds[:]
            del igbeta_list[:]

    return annualirrad_list


def irradiation_surface_plot(glbl_h_rad_data, diffuse_h_rad_data, latitude, longitude, timezone, timeshift=-0.5,
                             use_isotropic=False, use_diffuse_only=False):
    """

    Prepares a solar irradiation surface plot.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        glbl_h_rad_data: Hourly global horizontal radiation data for a year for a location.
        diffuse_h_rad_data: Hourly diffuse horizontal radiation data for a year for a location.
        latitude: Latitude (degrees)
        longitude: Longitude (degrees)
        timezone: The time zone of the location
        timeshift:
        use_isotropic:
        use_diffuse_only:
    """
    irradiation_data = annual_solar_irradiation(glbl_h_rad_data, diffuse_h_rad_data, latitude, longitude,
                                                timezone, timeshift, use_isotropic, use_diffuse_only)
    if use_isotropic:
        # This creates a 2D irradiation surface plot
        xlist = np.linspace(0, 350, 36)
        ylist = np.linspace(0, 90,
                            10)  # Note: theer need to be 19 subdivisions (here and for Z) for 5o bins of altitude
        X, Y = np.meshgrid(xlist, ylist)
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        # this part converts the list into an array and reshapes it, to match the x,y dimensions
        Z = np.array(irradiation_data) * 10 ** -6
        Z = Z.reshape(10, 36)
        cp = ax.contourf(X, Y, Z, 16, cmap='plasma',
                         alpha=1.0)  # NB: 16 sets number of division; alpha sets opacity; 'magma', 'jet' and
        # 'viridis' are also good cmaps
        fig.colorbar(cp, label=r'Solar irradiation, $MWh/$m^2$')  # Adds a colorbar
        ax.set_title('Annual Solar Irradiation Surface Plot: Isotropic Sky')
        ax.set_xlabel('Collector azimuth, deg')
        ax.set_ylabel('Collector tilt, deg')
    else:
        # This creates a 2D irradiation surface plot
        xlist = np.linspace(0, 350, 36)
        ylist = np.linspace(0, 90,
                            10)  # Note: theer need to be 19 subdivisions (here and for Z) for 5o bins of altitude
        X, Y = np.meshgrid(xlist, ylist)
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        # this part converts the list into an array and reshapes it, to match the x,y dimensions
        Zprime = np.array(irradiation_data) * 10 ** -6
        Zprime = Zprime.reshape(10, 36)
        cp = ax.contourf(X, Y, Zprime, 16, cmap='plasma',
                         alpha=1.0)  # NB: 16 sets number of division; alpha sets opacity; 'magma', 'jet' and
        # 'viridis' are also good cmaps
        fig.colorbar(cp, label=r'Solar irradiation, $MWh/m^2$')  # Adds a colorbar
        ax.set_title('Annual Solar Irradiation Surface Plot: Anisotropic Sky')
        ax.set_xlabel('Collector azimuth, deg')
        ax.set_ylabel('Collector tilt, deg')

