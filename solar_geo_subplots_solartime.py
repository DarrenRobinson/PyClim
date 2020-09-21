import matplotlib.pyplot as plt

from climateanalysis import solar as sol


# DAILY DECLINATION ANGLES
def plot_daily_declination_angles():
    """
    Plots daily solar declination angles over a year.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    """
    daily_declination_angles = [sol.declin_angle(day) for day in range(1, 366)]
    fig, ax = plt.subplots()
    ax.plot(range(1, 366), daily_declination_angles, 'b-')
    ax.set_title('Daily Declination Angles')
    ax.set_xlabel('Time, Julian Days')
    ax.set_ylabel('Declination Angle, Degrees')


def plot_clock_solar_time_diff(longitude, time_zone, time_shift=-0.5, use_eq_time_only=False):
    """
    Plots the clock-solar time difference
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        longitude(float): Longitude in degrees
        time_zone: Time zone of the location
        time_shift:
        use_eq_time_only(bool):
    """
    daily_time_diffs = [sol.time_diff(day, use_eq_time_only, longitude, time_zone, time_shift) for day in range(1, 366)]
    fig, ax = plt.subplots()
    ax.plot(range(1, 366), daily_time_diffs, 'y-')
    ax.set_title('Daily Clock-Solar Time Difference')
    ax.set_xlabel('Time, Julian Days')
    ax.set_ylabel('Time Difference, Hours')


# DAILY SOLAR DAY LENGTH
def plot_daily_solar_day_length(latitude):
    """
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        latitude: Latitude (degrees)
    """
    daily_solar_day_lengths = [sol.day_length(day, latitude) for day in range(1, 366)]
    fig, ax = plt.subplots()
    ax.plot(range(1, 366), daily_solar_day_lengths, 'y-')
    ax.set_title('Daily solar day length')
    ax.set_xlabel('Time, Julian Days')
    ax.set_ylabel('Day Length, Hours')


# HOURLY SOLAR ALTITUDE FOR A SELECTED DAY
def plot_hourly_solar_altitude_angles(julian_day, latitude):
    """
    Plots the hourly solar altitude for the selected day.
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.
    Args:
        julian_day: Julian day of year i.e. 1 = first day of year, 365 = last day of year
        latitude: Latitude (degrees)
    """
    hourly_solar_altitudes = [sol.altitude_angle(julian_day, hour, latitude) for hour in range(1, 25)]
    fig, ax = plt.subplots()
    ax.plot(range(1, 25), hourly_solar_altitudes, 'rx-')
    ax.set_title('Hourly Solar Altitude Angles for Day {}'.format(julian_day))
    ax.set_xlabel('Time, Hours')
    ax.set_ylabel('Solar Altitude Angle, Degrees')


# HOURLY SOLAR AZIMUTH ANGLES FOR SELECTED DAY
def plot_hourly_solar_azimuth_angles(julian_day, latitude):
    """
    Plots the hourly solar azimuth for the selected day
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        julian_day: Julian day of year i.e. 1 = first day of year, 365 = last day of year
        latitude: Latitude (degrees)
    """
    hourly_azimuth_angles = [sol.azimuth_angle(julian_day, hour, latitude) for hour in range(1, 25)]
    fig, ax = plt.subplots()
    ax.plot(range(1, 25), hourly_azimuth_angles, 'g-')
    ax.set_title('Hourly Solar Azimuth Angles for Day {}'.format(julian_day))
    ax.set_xlabel('Time, Hours')
    ax.set_ylabel('Solar Azimuth Angle, Degrees')


def plot_hourly_cosine_angle_incidence(julian_day, latitude, wall_azimuth_angle, surface_tilt_angle):
    """
    Plots the hourly cai for the selected day
     NOTE: Additional actions must be taken after running this function to determine what will happen to the graph.
          e.g. run plt.show() to show the graph or plt.savefig() to save the graph.

    Args:
        julian_day: Julian day of year i.e. 1 = first day of year, 365 = last day of year
        latitude: Latitude (degrees)
        wall_azimuth_angle: Wall azimuth angle (degrees)
        surface_tilt_angle: Surface tilt angle (degrees)
    """
    cos_angle_incds = [sol.cosine_angle_incidence(wall_azimuth_angle, surface_tilt_angle,
                                                  sol.altitude_angle(julian_day, hour, latitude),
                                                  sol.azimuth_angle(julian_day, hour, latitude))
                       for hour in range(1, 25)]
    fig, ax = plt.subplots()
    ax.plot(range(1, 25), cos_angle_incds, 'g-')
    ax.set_title('Hourly Cosine of the Angle of Incidence for Day {}'.format(julian_day))
    ax.set_xlabel('Time, Hours')
    ax.set_ylabel('Cosine of the Angle of Incidence')


def test_plots():
    plot_daily_declination_angles()
    plot_clock_solar_time_diff(-1, 0, -0.5, True)
    plot_daily_solar_day_length(52)
    plot_hourly_solar_altitude_angles(180, 52)
    plot_hourly_solar_azimuth_angles(180, 52)
    plot_hourly_cosine_angle_incidence(180, 52, 180, 90)


