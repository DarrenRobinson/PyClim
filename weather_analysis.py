from __future__ import division

import math
import matplotlib.pyplot as plt
import numpy as np
from climateanalysis import solar as sol
from climateanalysis import illuminance_irradiance as ilr


def _daily_sunrise_sunset_times(longitude, latitude, timezone, timeshift=-0.5, use_eq_time_only=False):
    """
    Produces Sunset and Sunrise time lists, each containing the sunset/rise time for each day of the year.

    Args:
        longitude(float): Longitude (degrees)
        latitude(float): Latitude (degrees)
        timezone: The time zone of the location
        timeshift:
        use_eq_time_only:

    Returns:
        The sunrise and sunset times for each day of the year.
    """
    daily_sunrise_times = []
    daily_sunset_times = []
    for day in range(1, 366):
        sunset_time, sunrise_time = sol.rise_set_times(day, latitude)
        solar_clock_time_diff = sol.time_diff(day, use_eq_time_only, longitude, timezone, timeshift)
        daily_sunrise_times.append(max(1, sunrise_time + solar_clock_time_diff))
        daily_sunset_times.append(min(24, sunset_time + solar_clock_time_diff))

    return daily_sunset_times, daily_sunrise_times


def _hourly_illuminance_values(global_h_radiation, diffuse_h_radiation, longitude, latitude, timezone, globaleff=False,
                               timeshift=-0.5):
    """
    Calculates the hourly illuminance values for a year.

    Args:
        global_h_radiation: A years worth of hourly global horizontal radiation data for a location.
        diffuse_h_radiation: A years worth of hourly diffuse horizontal radiation data for a location.
        longitude: Longitude (degrees)
        latitude: Latitude (degrees)
        timezone: The timezone of the location
        globaleff:
        timeshift:

    Returns:
        The hourly illuminance values for a year.
    """
    hourly_illuminance = []
    cumulative_day = 0
    for day in range(1, 366):
        cumulative_day += 1
        for hour in range(1, 25):
            dT = sol.time_diff(cumulative_day, False, longitude, timezone, timeshift)
            illuminance = 0
            solalt = sol.altitude_angle(cumulative_day, hour + dT, latitude, in_radians=True)
            if solalt > 0 and global_h_radiation[24 * (cumulative_day - 1) + hour - 1] > 0:
                ibn = (global_h_radiation[24 * (cumulative_day - 1) + hour - 1] - diffuse_h_radiation[
                    24 * (cumulative_day - 1) + hour - 1]) / math.sin(
                    solalt)
                if globaleff and diffuse_h_radiation[24 * (cumulative_day - 1) + hour - 1] > 0:
                    illuminance = global_h_radiation[24 * (cumulative_day - 1) + hour - 1] \
                                  * ilr.luminous_efficacy(globaleff,
                                                          cumulative_day,
                                                          solalt,
                                                          diffuse_h_radiation[24 * (cumulative_day - 1) + hour - 1],
                                                          ibn)
                elif globaleff is False and diffuse_h_radiation[24 * (cumulative_day - 1) + hour - 1] > 0:
                    illuminance = diffuse_h_radiation[24 * (cumulative_day - 1) + hour - 1] \
                                  * ilr.luminous_efficacy(globaleff,
                                                          cumulative_day,
                                                          solalt,
                                                          diffuse_h_radiation[24 * (cumulative_day - 1) + hour - 1],
                                                          ibn)
            hourly_illuminance.append(illuminance * 10 ** -3)
    return hourly_illuminance


def temp_frequency_histogram(dry_bulb_temperatures):
    """
    Prepares a frequency histogram of Dry Bulb Temperatures for the input data.
    NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        dry_bulb_temperatures: A years worth of hourly global horizontal radiation data for a location.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), tight_layout=True)
    ax2 = ax.twinx()
    ax.set_title("Temperature Frequency Histogram")
    ax.set_xlabel('Temperature Bins, oC')
    ax.set_ylabel('Counts [grey]')
    ax2.set_ylabel('Cumulative Counts [red / blue]')
    # plots a standard frequency distribution
    xrange = int(max(dry_bulb_temperatures) - int(min(dry_bulb_temperatures)))
    ax.hist(dry_bulb_temperatures, xrange, alpha=0.3, histtype='step', color='darkgray', lw=3)
    # creates a y2 axis for the cumulative distribution
    ax2.hist(dry_bulb_temperatures, bins=xrange, cumulative=True, alpha=1, histtype='step', color='red', lw=3)
    ax2.hist(dry_bulb_temperatures, bins=xrange, cumulative=-1, alpha=1, histtype='step', color='blue', lw=3)


def wind_speed_frequency_histogram(wind_speeds):
    """
    Prepares a frequency histogram of Wind Speeds for the input data.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        wind_speeds: A years worth of hourly wind speed data.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), tight_layout=True)
    ax2 = ax.twinx()
    ax.set_title("Wind Speed Frequency Histogram")
    ax.set_xlabel('Wind Speed Bins, m/s')
    ax.set_ylabel('Counts [grey]')
    ax2.set_ylabel('Cumulative Counts [red]')
    # plots a standard frequency distribution
    xrange = int(max(wind_speeds) - int(min(wind_speeds)))
    ax.hist(wind_speeds, xrange, alpha=0.3, histtype='step', color='darkgray', lw=3)
    # creates a y2 axis for the cumulative distribution
    ax2.hist(wind_speeds, bins=xrange, cumulative=True, alpha=1, histtype='step', color='red', lw=3)


def cumulative_illuminance_frequency_histogram(global_h_radiation, diffuse_h_radiation, longitude, latitude,
                                               timezone, globaleff=False, timeshift=-0.5):
    """
    Prepares a cumulative illuminance histogram.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
              e.g. run plt.show() to show the graph or plt.savefig() to save the graph .
    Args:
         global_h_radiation: A years worth of hourly global horizontal radiation data for a location.
        diffuse_h_radiation: A years worth of hourly diffuse horizontal radiation data for a location.
        longitude: Longitude (degrees)
        latitude: Latitude (degrees)
        timezone: The timezone of the location
        globaleff:
        timeshift:
    """
    hourly_illuminances = _hourly_illuminance_values(global_h_radiation, diffuse_h_radiation, longitude, latitude,
                                                     timezone, globaleff, timeshift)
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), tight_layout=True)
    xrange = int((max(hourly_illuminances) - int(min(hourly_illuminances))))
    ax.hist(hourly_illuminances, xrange, alpha=1, histtype='stepfilled', color='red', cumulative=-1,
            range=[1, max(hourly_illuminances)])

    ax.set_title("Inverse Cumulative Illuminance Frequency Histogram")
    ax.set_xlabel('Illuminance Bins, klux')
    ax.set_ylabel('Cumulative Counts')


# ========== AVAILABILITY SURFACE PLOTS ===========
def daylight_availability_surface_plot(global_h_radiation, diffuse_h_radiation, longitude, latitude,
                                       timezone, globaleff=False, timeshift=-0.5, use_eq_time_only=False):
    """
    This creates a 2D daylight availability surface plot
    NOTE: the chart is asymmetric because of the hour-centred convention.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        global_h_radiation: A years worth of hourly global horizontal radiation data for a location.
        diffuse_h_radiation: A years worth of hourly diffuse horizontal radiation data for a location.
        longitude: Longitude (degrees)
        latitude: Latitude (degrees)
        timezone: The timezone of the location
        globaleff:
        timeshift:
    """
    hourly_illuminances = _hourly_illuminance_values(global_h_radiation, diffuse_h_radiation, longitude, latitude,
                                                     timezone, globaleff, timeshift)
    sunset_times, sunrise_times = _daily_sunrise_sunset_times(longitude, latitude, timezone, timeshift,
                                                              use_eq_time_only)
    # Creating the Plot
    day_list = range(1, 366)
    xlist = np.linspace(0, 23, 24)
    ylist = np.linspace(1, 365, 365)
    X, Y = np.meshgrid(xlist, ylist)
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    # this part converts the list into an array and reshapes it, to match the x,y dimensions
    Z = np.array(hourly_illuminances)
    Z = Z.reshape(365, 24)
    cp = ax.contourf(Y, X, Z, 16, cmap='jet')  # 'plasma', 'jet' and 'viridis' are also good cmaps
    if not globaleff:
        fig.colorbar(cp, label='diffuse horizontal illuminance, kLux')  # Adds a colorbar
    else:
        fig.colorbar(cp, label='global horizontal illuminance, kLux')  # Adds a colorbar
    ax.set_title('Daylight Availability Surface Plot')
    ax.set_xlabel('Time, days')
    ax.set_ylabel('Time, hours')
    # TODO should the day_list just be a list of 1-365. I think it should given the way the code is written. Wouldn't handle missing days but that is likely out of scope.
    plt.plot(day_list, sunrise_times, c='red')
    plt.plot(day_list, sunset_times, c='red')


def solar_availability_surface_plot(global_h_radiation, longitude, latitude, timezone, timeshift=-0.5,
                                    use_eq_time_only=False):
    """
    This creates a 2D solar availability surface plot
    NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        global_h_radiation: A years worth of hourly global horizontal radiation data for a location.
        longitude: Longitude (degrees)
        latitude: Latitude (degrees)
        timezone: The timezone of the location
        timeshift:
        use_eq_time_only:
    """
    sunset_times, sunrise_times = _daily_sunrise_sunset_times(longitude, latitude, timezone, timeshift,
                                                              use_eq_time_only)
    day_list = range(1, 366)
    xlist = np.linspace(0, 23, 24)
    ylist = np.linspace(1, 365, 365)
    X, Y = np.meshgrid(xlist, ylist)
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    # this part converts the list into an array and reshapes it, to match the x,y dimensions
    Z = np.array(global_h_radiation)
    Z = Z.reshape(365, 24)
    cp = ax.contourf(Y, X, Z, 16, cmap='jet')  # 'plasma', 'jet' and 'viridis' are also good cmaps
    fig.colorbar(cp, label='Global horizontal solar irradiance, W/m^2')  # Adds a colorbar
    ax.set_title('Solar Availability Surface Plot')
    ax.set_xlabel('Time, days')
    ax.set_ylabel('Time, hours')

    plt.plot(day_list, sunrise_times, c='red')
    plt.plot(day_list, sunset_times, c='red')


# ====== END =======


# ========= VIOLIN PLOTS ============
# These are all similar so could be made into a single function. For clarity I think they will be left like this
# however.
def _generate_monthly_hourly_data_matrix(hourly_data_for_year):
    """
    Intended for internal use only.
    Generates a matrix of hourly data values for a years worth of hourly data readings. Each row of the matrix corresponds
    to the hourly data from 1 month of the year, this data is not separated into individual days.

    Args:
        hourly_data_for_year: A list of values corresponding to hourly readings for an entire year.
    Returns:
        A matrix with rows for each month of the year.
    """
    cumulative_day_count = 0
    matrix = []
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # TODO - Look at extracting to a constant
    for month_num in range(0, 12):
        matrix.append([])
        for day_num in range(1, days_in_months[month_num] + 1):
            cumulative_day_count += 1
            for hour in range(0, 24):
                matrix[month_num].append(hourly_data_for_year[24 * (cumulative_day_count - 1) + hour])
    return matrix


def dry_bulb_temp_violin_plot(dry_bulb_temperatures):
    """
    Prepares a dry bulb temperature violin plot.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        dry_bulb_temperatures: A years worth of hourly global horizontal radiation data for a location.

    Returns:

    """
    dry_bulb_temp_matrix = _generate_monthly_hourly_data_matrix(dry_bulb_temperatures)
    _, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_title('Dry Bulb Temperature Violin Plot')
    ax.set_xlabel('Time, months')
    ax.set_ylabel('Temperature, oC')
    plt.violinplot(dry_bulb_temp_matrix)


def wind_speeds_violin_plot(wind_speeds):
    """
    Prepares a wind speed violin plot.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        wind_speeds: A years worth of hourly wind speed data.

    Returns:

    """
    wind_speeds_matrix = _generate_monthly_hourly_data_matrix(wind_speeds)
    _, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_title('Wind Speed Violin Plot')
    ax.set_xlabel('Time, months')
    ax.set_ylabel('Wind Speed, m/s')
    plt.violinplot(wind_speeds_matrix)


def relative_humidity_violin_plot(relative_humidity_values):
    """
    Prepares a relative humidity violin plot.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        relative_humidity_values: A years worth of hourly relative humidity data for a given location.
    """
    relative_humidity_matrix = _generate_monthly_hourly_data_matrix(relative_humidity_values)
    _, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_title('Relative Humidity Violin Plot')
    ax.set_xlabel('Time, months')
    ax.set_ylabel('Relative Humidity, %')
    plt.violinplot(relative_humidity_matrix)


def diurnal_temp_violin_plot(dry_bulb_temperatures):
    """
    Prepares a diurnal temperature violin plot.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        dry_bulb_temperatures: A years worth of hourly dry bulb temperature data for a given location.
    """
    cumulative_day_count = 0
    diurnal_temp_matrix = []
    day_temp_profile = []
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # TODO - Look at extracting to a constant
    for month_num in range(0, 12):
        diurnal_temp_matrix.append([])
        for day_num in range(1, days_in_months[month_num] + 1):
            cumulative_day_count += 1
            for hour in range(0, 24):
                day_temp_profile.append(dry_bulb_temperatures[24 * (cumulative_day_count - 1) + hour])
            diurnal_temp_matrix[month_num].append(max(day_temp_profile) - min(day_temp_profile))
            del day_temp_profile[:]

    _, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_title('Diurnal Temperature Violin Plot')
    ax.set_xlabel('Time, months')
    ax.set_ylabel('Diurnal temperature, oC')
    plt.violinplot(diurnal_temp_matrix)


# ========= END ============


# ====== DEGREE DAYS =======
def degree_days_histogram(dry_bulb_temperatures, heating_degree_days_base=15.5, cooling_degree_days_base=18):
    """
    Prepares a monthly degree days histogram.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        dry_bulb_temperatures: A years worth of hourly dry bulb temperature data for a given location.
        heating_degree_days_base:
        cooling_degree_days_base:
    """
    # Generating the data
    monthly_heating_degree_days = [0] * 12
    monthly_cooling_degree_days = [0] * 12
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # TODO - Look at extracting to a constant
    cumulative_day_count = 0
    for month_num in range(0, 12):
        for day_num in range(1, days_in_months[month_num] + 1):
            cumulative_day_count += 1
            day_mean_temp = 0
            for hour in range(0, 24):
                day_mean_temp += dry_bulb_temperatures[24 * (cumulative_day_count - 1) + hour] / 24
            if day_mean_temp > cooling_degree_days_base:
                monthly_cooling_degree_days[month_num] = monthly_cooling_degree_days[month_num] \
                                                         + (day_mean_temp - cooling_degree_days_base)
            if day_mean_temp < heating_degree_days_base:
                monthly_heating_degree_days[month_num] = monthly_heating_degree_days[month_num] \
                                                         + (heating_degree_days_base - day_mean_temp)
    # Creating the plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 6), tight_layout=True)
    xlist = np.linspace(1, 12, 12)
    y1 = ax.bar(xlist, monthly_heating_degree_days, alpha=1, color='blue')
    y2 = ax.bar(xlist, monthly_cooling_degree_days, alpha=1, color='red')

    ax.set_title("Monthly Degree-Days")
    ax.set_xlabel('Time, months')
    ax.set_ylabel('Monthly Degree Days')
    plt.legend((y1[0], y2[0]), ('Heating', 'Cooling'), loc='best')
# ========= END ============


# ======== GROUND TEMP PROFILE ========
# def ground_temperature_profile():
#
#
#     for month in range(1, 13):
#         # plt.scatter(tground_matrix[month-1], depth_list, c=Colour_list[month-1], s=20)
#         plt.plot(tground_matrix[month - 1], depth_list, lw=2, c=Colour_list[11 - (month - 1)])
#
#     plt.title("Ground temperature profile")
#     plt.xlabel('temperature, oC')
#     plt.ylabel('depth below surface, m')
#     plt.ylim(plt.ylim()[::-1])
#
#     plt.legend(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
#     plt.show()
# ========= END ============
