from __future__ import division

import matplotlib.pyplot as plt
import numpy as np

wind_speeds_list = []
wind_directions = []
wind_temperatures = []


def _windrose_sector_temps_speeds(dry_bulb_temps, wind_directions, wind_speeds, num_sectors, return_temps=False):
    """
    Calculates the Wind Speed or Wind Temperature data that will be plotted in each of the sectors of the Wind Rose.
    Will return Wind Speeds by default.
    Intended for internal use only.

     Args:
         dry_bulb_temps(List[float]): List of Dry Bulb Temperatures (degrees C) for a given location over a given time period
         wind_directions(List[float]): List of Wind Directions (degrees) for the same location and time period
         wind_speeds(List[float]): List of Wind Speeds (m/s) for the same location and time period
         num_sectors(int): The number of sectors that will appear on the plotted Wind Rose.
         return_temps(bool): Whether or not to return Wind Temperatures instead of Wind Speeds. False by default.

     Returns(List[]):
        Wind Speed or Wind Temperature values for plotting on Wind Rose using the plot_wind_rose function.
    """
    max_wind_speed = int(max(wind_speeds))
    max_wind_temp = int(max(dry_bulb_temps))
    min_wind_temp = int(min(dry_bulb_temps))
    # Preallocate arrays for values
    rose_sector_wind_speeds = np.zeros((max_wind_speed + 1, num_sectors + 1))
    # TODO - A FUNDAMENTAL CHANGE HAD BEEN MADE HERE
    # rose_sector_wind_temps = np.zeros((max_wind_temp - min_wind_temp + 1, num_sectors + 1))
    # WILL ONLY WORK IF THE MINIMUM TEMP VALUE IS NEGATIVE
    # EDIT: Still unsure whether is is correct, negative temperatures will add a frequency point to high temperatures
    # due to the way indexing works with negative values, should all the values be offset if a negative value is used?
    # e.g, for a python list, list = [1,2,3], list[-1] >> 3.
    # In which case indexing by temperature will result in negative temperatures adding to higher temperature frequencies.
    # My understanding may be incorrect
    # Contact: rmhbowland1@sheffield.ac.uk if further discussion desired.
    if min_wind_temp < 0:
        rose_sector_wind_temps = np.zeros((max_wind_temp - min_wind_temp + 1, num_sectors + 1))
    else:
        rose_sector_wind_temps = np.zeros((max_wind_temp + 1, num_sectors + 1))
    # ====================================================
    for j in range(0, 8760):
        sectornum = int(wind_directions[j] / (360 / num_sectors))
        speednum = int(wind_speeds[j])
        tempnum = int(dry_bulb_temps[j])
        zval = rose_sector_wind_speeds[speednum][sectornum]
        zpval = rose_sector_wind_temps[tempnum][sectornum]
        rose_sector_wind_speeds[speednum][sectornum] = zval + 1
        rose_sector_wind_temps[tempnum][sectornum] = zpval + 1

    rose_sector_wind_speeds[0][0] = 0
    if return_temps:
        return rose_sector_wind_temps
    return rose_sector_wind_speeds


# TODO - see if this can be reworked so that it'll take less parameters e.g rather than 3 lists use a diff data
#  structure. This will likely be very dependent on how we store in the database an how we can pull things out.
def plot_windrose(dry_bulb_temps, wind_directions, wind_speeds, lower_percentile_limit, upper_percentile_limit,
                  num_sectors=16, plot_temps=False, invert_radial_axis=False):
    """
    Prepares a Wind Rose plot using the input data and configuration options.
    NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        dry_bulb_temps(List[float]): List of Dry Bulb Temperatures (degrees C) for a given location over a given time period.
        wind_directions(List[float]): List of Wind Directions (degrees) for the same location and time period.
        wind_speeds(List[float]): List of Wind Speeds (m/s) for the same location and time period.
        num_sectors(int): The number of sectors that will appear on the plotted Wind Rose.
        lower_percentile_limit(int): Sets the lower bounds of the colormap.
        upper_percentile_limit(int): Sets the upper bounds of the colormap.
        plot_temps(bool): Whether or not to plot Wind Temperatures instead of Wind Speeds. False by default.
        invert_radial_axis: Whether or not to invert the radial axis. CURRENTLY NOT IMPLEMENTED DUE TO PYTHON2 INCOMPATABILITY
    """
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    azimuth_list = np.radians(np.linspace(0, 360, (num_sectors + 1)))
    print plot_temps
    if plot_temps:
        ax.set_title('Annual Wind Rose: with Temperature in Radial Sectors')
        ax.set_ylim(
            [int(np.percentile(dry_bulb_temps, lower_percentile_limit)),
             int(np.percentile(dry_bulb_temps, upper_percentile_limit))])
        max_wind_temp = int(max(dry_bulb_temps))
        min_wind_temp = int(min(dry_bulb_temps))
        # TODO - UNSURE THIS IS CORRECT
        if min_wind_temp < 0:
            tempzen_list = np.linspace(min_wind_temp, max_wind_temp + 1, (max_wind_temp - min_wind_temp + 1))
        else:
            tempzen_list = np.linspace(min_wind_temp, max_wind_temp + 1, (max_wind_temp + 1))
        # =========================
        tempval_list = _windrose_sector_temps_speeds(dry_bulb_temps, wind_directions,
                                                     wind_speeds, num_sectors, return_temps=True)
        cp = ax.pcolormesh(azimuth_list, tempzen_list, tempval_list, cmap='jet')
        fig.colorbar(cp, label='Annual Hours: Wind approaching from ith Direction at jth Temperature')
    else:
        ax.set_title('Annual Wind Rose: with Wind Speed in Radial Sectors')
        ax.set_ylim([int(np.percentile(wind_speeds, lower_percentile_limit)),
                     int(np.percentile(wind_speeds, upper_percentile_limit))])
        max_wind_speed = int(max(wind_speeds))
        zenith_list = np.linspace(0, max_wind_speed + 1, (max_wind_speed + 1))
        value_list = _windrose_sector_temps_speeds(dry_bulb_temps, wind_directions, wind_speeds, num_sectors)
        cp = ax.pcolormesh(azimuth_list, zenith_list, value_list, cmap='jet')
        fig.colorbar(cp, label='Annual Hours: Wind approaching from ith Direction at jth Speed')
    plt.tight_layout()
