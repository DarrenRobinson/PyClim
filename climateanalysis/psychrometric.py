"""
This Module ...
NOTE: Many docstrings are incomplete. They are left here as a template for completion.
"""
from __future__ import division
import math


def moisture_content(dry_bulb_temp, rel_humidity):
    """
    Calculates moisture content from dry bulb temperature and relative humidity

    Args:
        dry_bulb_temp: The Dry Bulb Temperature (degrees C) for a certain time-point
        rel_humidity: The Relative Humidity (%) for a certain time-point

    Returns:
        The calculated moisture content
    """
    # calculates moisture content from dbt and rh
    psatvap = saturated_vapour_pressure(dry_bulb_temp)
    mc = saturated_vapour_moisture_content(fs(dry_bulb_temp), psatvap)
    lhs = rel_humidity * mc
    low = 0.0001
    middle = 100
    high = 1
    errorlimit = 0.00001
    error = 1
    while error > errorlimit:
        middle = low + (high - low) / 2
        rhmid = 100 * middle
        if lhs < rhmid:
            high = middle
        else:
            low = middle
        error = math.fabs(lhs - rhmid)
    g = middle
    return g


def saturation_temp(moisture_cont):
    """
    Calculates saturation temperature from moisture content.

    Args:
        moisture_cont: The moisture content () for a certain time-point

    Returns:
        The calculated saturation temperature
    """
    tstep = 64
    tsathigh = 60
    while tstep > 0.05:
        told = tsathigh
        tsathigh = tsathigh - tstep
        gsat = moisture_content(tsathigh, 100)
        if gsat < moisture_cont:
            tsathigh = told
        tstep = tstep / 2
    tsat = tsathigh
    return tsat


def saturated_vapour_pressure(air_temp):
    """
    Calculates the saturated vapour pressure (kPa) given the air temperature.

    Args:
        air_temp: The Air Temperature (degrees C) for a certain time-point

    Returns:
        The calculated saturated vapour pressure
    """
    if air_temp >= 0:
        suf = 30.59051 - 8.2 * math.log10(air_temp + 273.16) + 0.0024804 * (air_temp + 273.16)
        suf = suf - 3142.31 / (air_temp + 273.16)
        pss = 10 ** suf
    else:
        suf = 9.5380997 - 2663.91 / (air_temp + 273.15)
        pss = 10 ** suf
    return pss


def saturated_vapour_moisture_content(fs, pss):
    """
    Calculates moisture content of saturated vapour.

    Args:
        fs:
        pss:

    Returns:

    """
    gss = 0.62197 * fs * pss / (101.325 - fs * pss)
    return gss


def fs(dry_bulb_temp):
    """
    Provides necessary interaction coefficients

    Args:
        dry_bulb_temp: The Dry Bulb Temperature (degrees C) for a certain time-point

    Returns:

    """
    if dry_bulb_temp < 11:
        fs = -7.3E-06 * (dry_bulb_temp + 273.15) + 1.00444
    elif 11 <= dry_bulb_temp < 26:
        fs = 1.32E-05 * (dry_bulb_temp + 273.15) + 1.004205
    elif 26 <= dry_bulb_temp <= 60:  # may want remove 60 upper bound
        fs = 4.05E-05 * (dry_bulb_temp + 273.15) + 1.003497
    return fs


def vapour_pressure(moisture_cont):
    """
    Calculates the vapour pressure of air at a given moisture content.

    Args:
        moisture_cont: The moisture content () for a certain time-point

    Returns:

    """
    return 101.325 * moisture_cont / (0.622 + moisture_cont)


def relative_humidity(moisture_cont, dry_bulb_temp):
    """
    Calculates relative humidity given the moisture content and dry bulb temperature
    Args:
        moisture_cont: The moisture content () for a certain time-point
        dry_bulb_temp: The Dry Bulb Temperature (degrees C) for a certain time-point

    Returns:
        (Union[int,float]):
    """
    # calculates rh given the moisture content and dry bulb tempature
    return 100 * (vapour_pressure(moisture_cont) / saturated_vapour_pressure(dry_bulb_temp))


def pvap(dry_bulb_temp, wet_bulb_temp, screen):
    """
    Calculates the partial pressure of water vapour mixed with dry air (Pa), given dry-bulb and wet-bulb/screen
    temperature.

    Args:
        dry_bulb_temp: The Dry Bulb Temperature (degrees C) for a certain time-point
        wet_bulb_temp:
        screen:

    Returns:

    """
    # calculates the partial pressure of water vapour mixed with dry air (Pa),
    # given dry-bulb and wet-bulb/screen temperature
    if wet_bulb_temp >= 0 and screen is True:
        corr = 7.99
    elif wet_bulb_temp < 0 and screen is True:
        corr = 7.2
    elif wet_bulb_temp < 0 and screen is False:
        corr = 5.94
    else:
        corr = 6.66
    pssw = saturated_vapour_pressure(wet_bulb_temp)
    pvap = pssw - 101.325 * corr * 10 ** -4 * (dry_bulb_temp - wet_bulb_temp)
    return pvap


def g_dry_wet(dry_bulb_temp, wet_bulb_temp):
    """
    Calculates moisture content, given the dry and wet bulb temperatures.

    Args:
        dry_bulb_temp:
        wet_bulb_temp:

    Returns:
        (float):
    """
    pst = 10 * pvap(dry_bulb_temp, wet_bulb_temp, False)
    mc = (0.62197 * fs(dry_bulb_temp) * pst / (1013.25 - fs(dry_bulb_temp) * pst))
    return mc


def twetrh(dry_bulb_temp, _relative_humidity, screen):  # screen is a boolean
    """
    Calculates wet bulb or screen temperature (oC) given the dry bulb temperature and relative humidity.

    Args:
        dry_bulb_temp: The Dry Bulb Temperature (degrees C) for a certain time-point
        _relative_humidity: The Relative Humidity (%) for a certain time-point
        screen:

    Returns:
        :
    """
    psuper = saturated_vapour_pressure(dry_bulb_temp)
    Tstep = 64
    twet = dry_bulb_temp
    while Tstep > 0.25:
        Told = twet
        twet = twet - Tstep
        ps = pvap(dry_bulb_temp, twet, screen)
        rhtwet = 100 * ps / psuper
        if rhtwet < _relative_humidity:
            twet = Told
        Tstep = Tstep / 2
    twetrh = twet
    return twetrh
