""" This Module ..."""
from __future__ import division
import math


def luminous_coefficients(globaleff, clearness, amc, solar_alt, brightness):
    """

    Args:
        globaleff:
        clearness:
        amc:
        solar_alt:
        brightness:

    Returns:

    """
    if globaleff:
        LA_list = [96.6251, 107.5371, 98.7277, 92.721, 86.7266, 88.3516, 78.624, 99.6452]
        LB_list = [-0.4703, 0.7866, 0.6972, 0.5591, 0.9763, 1.3891, 1.4699, 1.8569]
        LC_list = [11.501, 1.7899, 4.4046, 8.3579, 7.1033, 6.0641, 4.9305, -4.4555]
        LD_list = [9.1555, -1.1892, -6.9483, -8.3063, -10.9361, -7.5967, -11.3703, -3.1465]
    else:
        LA_list = [97.2375, 107.2129, 104.996, 102.3945, 100.71, 106.42, 141.88, 152.23]
        LB_list = [-0.4597, 1.1508, 2.9605, 5.589, 5.94, 3.83, 1.9, 0.35]
        LC_list = [11.962, 0.584, -5.5334, -13.951, -22.75, -36.15, -53.24, -45.27]
        LD_list = [-8.9149, -3.949, -8.7793, -13.9052, -23.74, -28.83, -14.03, -7.98]
    LumEff = LA_list[clearness - 1] + LB_list[clearness - 1] * amc + LC_list[clearness - 1] * math.sin(solar_alt) + \
             LD_list[clearness - 1] * math.log(brightness)
    return LumEff

def luminous_efficacy(globaleff, jday, solar_alt, idh, ibn):
    """
    Calculates the luminous efficacy

    Args:
        globaleff:
        jday: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        solar_alt:
        idh:
        ibn:

    Returns:

    """
    amc = 2
    brightness = perez_brightness(jday, solar_alt, idh)
    clearness = perez_clearness(solar_alt, idh, ibn)
    return luminous_coefficients(globaleff, clearness, amc, solar_alt, brightness)


def perez_clearness(solar_alt, idh, ibn):
    """
    Calculates the Perez Clearness number, for use in the Perez Coefficients function

    Args:
        solar_alt:
        idh:
        ibn:

    Returns:

    """
    ThetaZ = ((math.pi / 2) - solar_alt) * 180 / math.pi
    clearness = (((idh + ibn) / idh) + 5.535 * 10 ** -6 * ThetaZ ** 3) / (1 + 5.535 * 10 ** -6 * ThetaZ ** 3)
    if (1 <= clearness) and (clearness < 1.065):
        PerezClearness = 1
    elif (1.065 < clearness) and (clearness < 1.23):
        PerezClearness = 2
    elif (1.23 < clearness) and (clearness < 1.5):
        PerezClearness = 3
    elif (1.5 < clearness) and (clearness < 1.95):
        PerezClearness = 4
    elif (1.95 < clearness) and (clearness < 2.8):
        PerezClearness = 5
    elif (2.8 < clearness) and (clearness < 4.5):
        PerezClearness = 6
    elif (4.5 < clearness) and (clearness < 6.2):
        PerezClearness = 7
    else:
        PerezClearness = 8
    return PerezClearness


def perez_brightness(jday, solar_alt, idh):
    """
    Calculates the Perez brightness coefficient.

    Args:
        jday: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        solar_alt:
        idh:

    Returns:

    """
    IextraT = 1367 * (1 + 0.033 * math.cos((360 * jday / 365) * math.pi / 180))
    airmass = 1 / math.sin(solar_alt)
    PerezBrightness = airmass * idh / IextraT
    return PerezBrightness


def perez_coefficients(clearness):
    """
    Calculates the Perez coefficients for use in the Perez tilted surface model.

    Args:
        clearness:

    Returns:

    """
    F11_list = [-0.0083, 0.1299, 0.3297, 0.5682, 0.873, 1.1326, 1.0602, 0.6777]
    F12_list = [0.5877, 0.6826, 0.4869, 0.1875, -0.392, -1.2367, -1.5999, -0.3273]
    F13_list = [-0.0621, -0.1514, -0.2211, -0.2951, -0.3616, -0.4118, -0.3589, -0.2504]
    F21_list = [-0.0596, -0.0189, 0.0554, 0.1089, 0.2256, 0.2878, 0.2642, 0.1561]
    F22_list = [0.0721, 0.066, -0.064, -0.1519, -0.462, -0.823, -1.1272, -1.3765]
    F23_list = [-0.022, -0.0289, -0.0261, -0.014, 0.0012, 0.0559, 0.1311, 0.2506]
    F11 = F11_list[clearness - 1]
    F12 = F12_list[clearness - 1]
    F13 = F13_list[clearness - 1]
    F21 = F21_list[clearness - 1]
    F22 = F22_list[clearness - 1]
    F23 = F23_list[clearness - 1]
    return F11, F12, F13, F21, F22, F23


def idh_perez(jday, cos_angle_inc, solar_alt, idh, ibn, tilt):
    """
    calculates diffuse irradiance on a tilted plane using the Perez model
    Args:
        jday:
        cos_angle_inc:
        solar_alt:
        idh:
        ibn:
        tilt:

    Returns:

    """
    if solar_alt < (5 * math.pi / 180):
        solar_alt = 5 * math.pi / 180
    F11, F12, F13, F21, F22, F23 = perez_coefficients(perez_clearness(solar_alt, idh, ibn))
    thetaz = (math.pi / 2) - solar_alt
    brightness = perez_brightness(jday, solar_alt, idh)
    F1 = F11 + F12 * brightness + F13 * thetaz
    if F1 < 0:
        F1 = 0
    F2 = F21 + F22 * brightness + F23 * thetaz
    a1 = math.sin(solar_alt)
    if a1 < math.sin(5 * math.pi / 180):
        a1 = math.sin(5 * math.pi / 180)
    idh_perez = idh * ((1 - F1) * (1 + math.cos(tilt)) / 2 + F1 * cos_angle_inc / a1 + F2 * math.sin(tilt))
    return idh_perez


def igbeta(jday, cai, igh, idh, solalt, tilt, isotropic, DiffuseOnly):
    """

    Args:
        jday: Julian Day of the year i.e 1 = first day of year, 365 = last day of year
        cai:
        igh:
        idh:
        solalt:
        tilt:
        isotropic:
        DiffuseOnly:

    Returns:

    """
    groundref = 0.2
    if solalt > 0:
        ibn = (igh - idh) / math.sin(solalt)
    else:
        ibn = 0
    if isotropic == True:
        idbeta = idh * (1 + math.cos(tilt)) / 2
    else:
        idbeta = 0
        if idh > 0:
            idbeta = idh_perez(jday, cai, solalt, idh, ibn, tilt)
    if DiffuseOnly == True:
        igbeta = idbeta
    else:
        iground = igh * groundref * (1 - math.cos(tilt)) / 2
        ibbeta = ibn * cai
        igbeta = ibbeta + idbeta + iground
    return igbeta