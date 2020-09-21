# Python Rework

This is reworked version of Python code, originally written by Prof. Darren Robinson from the University of Sheffield, by Kate Bobyn and Rob Bowland, as part of the second year Computer Science module - Software Hut (COM3420).

**Notes**:

*Completeness*:

Due to time limitations it was not possible to complete the refactoring of all graph generation files.
The following graphs remain incomplete:

- Ground Temperature Profile (solar_geo_subplots_solartime.py)
- Psychrometric Chart (psychrometrics.py)
- Wind Rose (wind_rose.py)
    - This function is actually complete, however I had doubt about its correct functioning and so it was not 
    included in the final product. Comments within the file explain.

*Documentation*:

Some documentation has been provided, but further documentation is needed. In these cases template docstrings have been provided for later completion.

*Additional*:

For use in this project it was necessary to make the Python code Python2 compatible. These changes were only minor and should not result in any functional changes when run on later versions of Python.


**File Structure Overview**:

> climateanalysis

This package contains reorganised and reworked functions originally stored within ClimAnalFunctions.py module.
These functions have been organised into a logical module based on the functions they perform.
Certain functions have been reworked to take additional parameters or parameters with different units. Where this has
occurred, relevant documentation is included as explanation.

