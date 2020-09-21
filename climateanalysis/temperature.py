""" This Module ..."""
from __future__ import division
import math


def Tground(t_mean, t_swing, cum_monthdaynum, dayofminmean, depth):
    """
    Reference:
        Eq 2 in: Labs, K. "Regional analysis of ground and above-ground climate conclusion",
        Underground Space Vol.7 pp037-65, 1982

    Args:
        t_mean:
        t_swing:
        cum_monthdaynum:
        dayofminmean:
        depth:

    Returns:

    """
    # approx ground thermophysical properties
    Conductivity = 1.21
    Density = 1960
    Cp = 840
    Diff = 8.64 * 10 ** 4 * Conductivity / (Density * Cp)  # m^2/day
    Decrement = math.exp(-depth * (math.pi / (365 * Diff)) ** 0.5)
    Lag = 0.5 * (365 / (math.pi * Diff)) ** 0.5
    Tground = t_mean - t_swing * Decrement * math.cos(2 * math.pi * (cum_monthdaynum - dayofminmean - depth * Lag) / 365)
    return Tground
