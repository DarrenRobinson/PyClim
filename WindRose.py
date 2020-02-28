##########################################################################################
# PyClim was developed by Prof. Darren Robinson (University of Sheffield, 2019).         #
# PyClim produces a range of graphs and statistics to support the analysis of climate    #
# data, for architectural / engineering / technology students to develop their           #
# early-stage bioclimatic design concepts.                                               #
##########################################################################################

#THIS MODULE SIMPLY CREATES A POLAR WIND ROSE PLOT.

import math
import matplotlib.pyplot as plt
import numpy as np

from ClimAnalFunctions import * 

#in the future: provide the option to plot using the Beaufort scale

########################################################
#The following control the format of the windrose
########################################################

#This determines whether the radial axis goes from centre outwards or vice-versa
invert_radialaxis=False
#This sets the number of azimuthal sectors to plot
numsectors = 16
#These set the lower and upper bounds of the colormap
upper_percentile_limit = 80
lower_percentile_limit  = 20
#This determines whether temperature or wind speed is plotted
PlotTemp = True
#Wind speeds are potted at 1m/s intervals: TempInterval sets the temperature intervals
TempInterval = 2.5

#this reads climate data file
winspeed_list= []
windir_list = []
temp_list = []
file_list = []

for line in file:
    line = line.rstrip('\n')
    line = line.split(',')
    file_list.append(line)
file.close()


#this popuates lists with the corresponding data
for i in range (3, len(file_list)):
    temp_list.append(float(file_list[i][3]))
    winspeed_list.append(float(file_list[i][7]))
    windir_list.append(float(file_list[i][8]))

maxspeed = int(max(winspeed_list))
maxtemp = int(max(temp_list))
mintemp = int(min(temp_list))

azimuth_list  = np.linspace(0, 360, (numsectors+1))
zenith_list = np.linspace(0,maxspeed+1,(maxspeed+1))
tempzen_list = np.linspace(mintemp,maxtemp+1,(maxtemp-mintemp+1))
value_list = [[0 for i in range(numsectors+1)] for j in range(maxspeed+1)]
tempval_list = [[0 for i in range(numsectors+1)] for j in range(maxtemp-mintemp+1)]

for j in range (0,8760):        
    sectornum = int(windir_list[j]/(360/numsectors))
    speednum=int(winspeed_list[j])
    tempnum=int(temp_list[j])
    zval = value_list[speednum][sectornum]
    zpval = tempval_list[tempnum][sectornum]
    value_list[speednum][sectornum] = zval+1
    tempval_list[tempnum][sectornum] = zpval+1

value_list[0][0]=0

fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))

azimuth_list = np.radians(azimuth_list)

if PlotTemp == False:
    #NB: The jet cmap gives very good discrimination:
    cp = ax.pcolormesh(azimuth_list, zenith_list, value_list, cmap='jet') #'plasma', 'magma', 'jet' and 'viridis' are good cmaps
    
    ax.set_title('Annual Wind Rose: with wind speed in radial sectors')
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim([int(np.percentile(winspeed_list,lower_percentile_limit)), int(np.percentile(winspeed_list,upper_percentile_limit))])
    
    if invert_radialaxis==True:
        ax.set_ylim(plt.ylim()[::-1])
    fig.colorbar(cp, label = 'Annual hours: wind approaching from ith direction at jth speed')
else:
    cp = ax.pcolormesh(azimuth_list, tempzen_list, tempval_list, cmap='jet')
    
    ax.set_title('Annual Wind Rose: with temperature in radial sectors')
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim([int(np.percentile(temp_list,lower_percentile_limit)), int(np.percentile(temp_list,upper_percentile_limit))])
    
    if invert_radialaxis==True:
        ax.set_ylim(plt.ylim()[::-1])
#    ax.set_yticklabels([])
    fig.colorbar(cp, label = 'Annual hours: wind approaching from ith direction at jth temperature')

plt.tight_layout()
plt.show()
