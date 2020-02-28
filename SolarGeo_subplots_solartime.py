##########################################################################################
# PyClim was developed by Prof. Darren Robinson (University of Sheffield, 2019).         #
# PyClim produces a range of graphs and statistics to support the analysis of climate    #
# data, to support architectural / engineering / technology students to develop their    #
# early-stage bioclimatic design concepts.                                               #
##########################################################################################

#This module creates 3 sub-plots of daily: declination angle, equation of time, solar dayength.
#It also creates three hourly plots for a receiving surface: solar altitude, solar azimuth, cai.

############################################
# REVISE TO CREATE 2 SETS OF 2X2 SUBPLOTS, 1 ANNUAL AND 1 DAILY.
# ANNUAL TO INCLUDE: DEC, DAYLENGTH, EQT AND ... PERHAPS AN EMPTY SLOT or SKY CLEARNESS INDEX DISTRIBUTION.
# DAILY TO INCLUDE: WALL-SOLAR AZIMUTH, ALTITUDE, CAI AND IGBETA / IDBETA / IBBETA.
############################################


#imports the basic libraries
import math
import matplotlib.pyplot as plt

from ClimAnalFunctions import * 


lat = lat * pi / 180
DayChoice = 355
wallaz = 180 * pi /180
tilt = 90 * pi / 180
isotropic = True
EqTonly=False #this is a switch that corrects for longitude difference when finding the sun position
#groundref=0.2

day_list = []
dec_list = []
hour_list = []
solalt_list = []
solaz_list = []
timediff_list = []
cai_list = []
file_list = []
global_list = []
diffuse_list = []
day_global_list = []
day_diffuse_list = []
igbeta_list = []
daylength_list = []


#######################################
# THIS CODE WAS USED FOR PRODUCING AN IGBETA CHART
#######################################

#for a separate results window, type the following in the console
#matplotlib qt

##this reads climate data file
#for line in file:
#    line = line.rstrip('\n')
#    line = line.split(',')
#    file_list.append(line)
#file.close()


##this popuates global and diffuse lists with the corresponding solar data
#for i in range (3,len(file_list)):
#    global_list.append(float(file_list[i][5]))
#    diffuse_list.append(float(file_list[i][6]))


#This prompts the user to enter a day, to be later used to generate plots
#DayChoice = input('Choose a day that you would like hourly plots for: ')
#DayChoice = int(DayChoice)


#This is where the daily and hourly solar quantities are calculated, to be ;ater plotted
for i in range(1,365):
    day_list.append(i)
    dec_list.append(declin_angle(i))
    daylength_list.append(daylength(dec_list[i-1],lat))
    timediff_list.append(time_diff(i, EqTonly, longitude, timezone, timeshift))

    if i == DayChoice:
    #this loop populates lists for daynuber, solar altitude and solar azimuth for a user-defined day
        for j in range(1,24):
            hour_list.append(j)
            solalt_list.append(solar_altitude(i,j,lat, dec_list[i-1])*180/pi)
            solaz_list.append(solar_azimuth(i,j,lat, solalt_list[j-1]*pi/180, dec_list[i-1])*180/pi)
            cai_list.append(cai(wallaz,tilt,solalt_list[j-1]*pi/180,solaz_list[j-1]*pi/180))
#            day_global_list.append(global_list[24*(i-1)+j-1])
#            day_diffuse_list.append(diffuse_list[24*(i-1)+j-1])
#            igbeta_list.append(igbeta(cai_list[j-1],day_global_list[j-1],day_diffuse_list[j-1],solalt_list[j-1]*pi/180,tilt*pi/180))


#NEXT UP: SETUP DIFFUSE IRRADIANCE IRRADIANCE FUNCTIONS; CALCULATE INCIDENT GLOBAL
#IRRADIANCE ON TILTED SURFACE.
#WHEN COMPLETE, CALCULATE AND CREATE GLOBAL IRRADIATION SURFACE PLOT. 

#this plots the daily declination angles, as an OO figure
fig,axes = plt.subplots(3,2, figsize = (15,10))

axes[0,0].plot(day_list, dec_list, 'b-')
axes[0,0].set_title('Daily declination angles')
axes[0,0].set_xlabel('time, Julian days')
axes[0,0].set_ylabel('declination angle, degrees')

#this plots the clock-solar time difference for the selected day, as an OO figure
axes[0,1].plot(day_list, timediff_list, 'y-')
axes[0,1].set_title('Daily clock-solar time difference')
axes[0,1].set_xlabel('time, Julian days')
axes[0,1].set_ylabel('time difference, hours')

#this plots the clock-solar time difference for the selected day, as an OO figure
axes[1,0].plot(day_list, daylength_list, 'y-')
axes[1,0].set_title('Daily solar day length')
axes[1,0].set_xlabel('time, Julian days')
axes[1,0].set_ylabel('day length, hours')

#this plots the hourly solar altitude for the selected day, as an OO figure
axes[1,1].plot(hour_list, solalt_list, 'rx-')
axes[1,1].set_title('Hourly solar altitude angles for day ' + str(DayChoice))
axes[1,1].set_xlabel('time, hours')
axes[1,1].set_ylabel('solar altitude angle, degrees')

#this plots the hourly solar azimuth for the selected day, as an OO figure
axes[2,0].plot(hour_list, solaz_list, 'g-')
axes[2,0].set_title('Hourly solar azimuth angles for day ' + str(DayChoice))
axes[2,0].set_xlabel('time, hours')
axes[2,0].set_ylabel('solar azimuth angle, degrees')

#this plots the hourly solar azimuth for the selected day, as an OO figure
axes[2,1].plot(hour_list, cai_list, 'mo-')
axes[2,1].set_title('Hourly cosine of the angle of incidence for day ' + str(DayChoice))
axes[2,1].set_xlabel('time, hours')
axes[2,1].set_ylabel('CAI')

##this plots the hourly solar irradiance for the selected day, as an OO figure
#axes[3,0].plot(hour_list, igbeta_list, 'c.-')
#axes[3,0].set_title('Hourly incident global irradiance for day ' + str(DayChoice))
#axes[3,0].set_xlabel('time, hours')
#axes[3,0].set_ylabel('Ig_beta')


fig.tight_layout()
plt.show()