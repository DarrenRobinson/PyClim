##########################################################################################
# PyClim was developed by Prof. Darren Robinson (University of Sheffield, 2019).         #
# PyClim produces a range of graphs and statistics to support the analysis of climate    #
# data, to support architectural / engineering / technology students to develop their    #
# early-stage bioclimatic design concepts.                                               #
##########################################################################################

#This module creates a stereographic sunpath diagram,given a user-defined latitude, and 
#specification of solar or clock time. It can also create shading protractors.

#imports the basic libraries
import math
import matplotlib.pyplot as plt
import numpy as np

from ClimAnalFunctions import * 

lat = 52
lat = lat*pi/180

AzimuthIncrement = 10
HorizontalProtractor = True
VerticalProtractor = True
WallAzimuth = 185
ClockTime = True

EqTonly = True

circles_x = []
circles_y = []
spokes_x = []
spokes_y = []


Hemisphere = "N"
if lat<0:
    Hemisphere="S"


#working backwards from the winter solstice
SunpathDay_list = [355,325,294,264,233,202,172,141,111,80,52,21]
azi_list = []
alt_list = []
sunpath_x = []
sunpath_y = []

Colour_list = ['firebrick', 'darkorange', 'orange', 'gold', 'green', 'cyan', 'blue']
Month_list = ['Dec', 'Nov/Jan', 'Oct/Feb', 'Sep/Mar', 'Aug/Apr', 'Jul/May', 'Jun']
plt.figure(figsize=(9, 9))

#######################################
# THIS PLOTS THE ISO-ALTITUDE CIRCLES AND RADIAL AZIMUTH LINES
#######################################

for circle in range (90,0,-10):
    for orientation in range (0,360+AzimuthIncrement, AzimuthIncrement):
        circles_x.append(circle*math.sin(orientation*pi/180))
        circles_y.append(circle*math.cos(orientation*pi/180))
        if circle==80:
            spokes_x.append(90*math.sin(orientation*pi/180))
            spokes_y.append(90*math.cos(orientation*pi/180))
            spokes_x.append(0*math.sin(orientation*pi/180))
            spokes_y.append(0*math.cos(orientation*pi/180))
        if circle==90 and orientation < 360:
            plt.text(95*math.sin(orientation*pi/180),95*math.cos(orientation*pi/180),str(orientation)+ '$^o$', c = 'darkgray', horizontalalignment='center', fontsize=8)
    if circle<90 and circle!=0:
        plt.text((circle+1)*math.sin(5*pi/180),(circle+1)*math.cos(orientation*pi/180),str(90-circle)+ '$^o$', c = 'darkgray', horizontalalignment='center', fontsize=8)

    plt.plot(circles_x,circles_y, lw=1, color='darkgray')
    plt.plot(spokes_x,spokes_y, lw=1, color='darkgray')
    circles_x.clear()
    circles_y.clear()
    spokes_x.clear()
    spokes_y.clear()

for month in range (1,8):
    position=0
    day = SunpathDay_list[month-1]
    dec = declin_angle(day)
    ss,sr = sunrise_time(dec,lat,day)
    
    if ss<24:
        #in this case we need to plot from the non-integer sunrise time, through to sunset
        alt_list.append(solar_altitude(day,sr,lat,dec)*180/pi)    
        azi_list.append(solar_azimuth(day,sr,lat,alt_list[0]*pi/180,dec))
        sunpath_x.append((90-alt_list[0])*math.sin(azi_list[0]))
        sunpath_y.append((90-alt_list[0])*math.cos(azi_list[0]))
    
        for hour in range(math.ceil(sr),int(sr)+2*(12-int(sr))):
            position=position+1
            alt_list.append(solar_altitude(day,hour,lat,dec)*180/pi)    
            azi_list.append(solar_azimuth(day,hour,lat,alt_list[position]*pi/180,dec))
            sunpath_x.append((90-alt_list[position])*math.sin(azi_list[position]))
            sunpath_y.append((90-alt_list[position])*math.cos(azi_list[position]))
            
        alt_list.append(solar_altitude(day,ss,lat,dec)*180/pi)    
        azi_list.append(solar_azimuth(day,ss,lat,solar_altitude(day,ss,lat,dec)*pi/180,dec))
        sunpath_x.append(90*math.sin(azi_list[position+1]))
        sunpath_y.append(90*math.cos(azi_list[position+1]))
    else:
        #in this case we simply need to plot for the entire 24h period
         for hour in range(0,25):
            alt_list.append(solar_altitude(day,hour,lat,dec)*180/pi)    
            azi_list.append(solar_azimuth(day,hour,lat,alt_list[position]*pi/180,dec))
            sunpath_x.append((90-alt_list[position])*math.sin(azi_list[position]))
            sunpath_y.append((90-alt_list[position])*math.cos(azi_list[position]))
            position=position+1

    plt.plot(sunpath_x, sunpath_y, c=Colour_list[7-month], label = (Month_list[month-1]), marker='o')
    
    alt_list.clear()
    azi_list.clear()
    sunpath_x.clear()
    sunpath_y.clear()

time_curve_x = []
time_curve_y = []
for hour in range (0,25):
    for day in range(1,366):
        #if the sun is below the horizon during the summer solstice for this hour then skip
        if Hemisphere=="N":
            summerday = 172
        else:
            summerday = 355
        if solar_altitude(summerday,hour,lat,declin_angle(summerday))>0:
            #this controls whether solar time curves of the analemma are plotted
            if ClockTime == True:
                EqT = time_diff(day, EqTonly, 0, 0, 0)
            else:
                EqT = 0
            Dec = declin_angle(day)
            Solalt = solar_altitude(day,hour+EqT,lat, Dec)
            if Solalt>0:
                Solaz = solar_azimuth(day,hour+EqT,lat,Solalt,Dec)
                time_curve_x.append((90-(Solalt*180/pi))*math.sin(Solaz))
                time_curve_y.append((90-(Solalt*180/pi))*math.cos(Solaz))
    plt.plot(time_curve_x, time_curve_y, c='darkblue')
    time_curve_x.clear()
    time_curve_y.clear()
#WEIRD PROBLEM: EQT FOR FIRST HOUR IN (ANT)ARCTIC CIRCLE ISN'T CORRECT (IT MIRRORS ABOUT THE HALF YEAR).


#######################################
# THIS PLOTS THE SHADING PROTRACTORS
#######################################

Protractor_x = []
Protractor_y = []
if HorizontalProtractor == True:
    for Theta in range (10, 90, 10):
        for Orientation in range (WallAzimuth-90, WallAzimuth+100, 10):
            ThetaAdjusted = math.atan(math.tan(Theta*pi/180) * math.cos(math.fabs(Orientation-WallAzimuth)*pi/180)) * 180/pi            
            Protractor_x.append((90-ThetaAdjusted)*math.sin(Orientation*pi/180))
            Protractor_y.append((90-ThetaAdjusted)*math.cos(Orientation*pi/180))
        plt.plot(Protractor_x, Protractor_y, c='darkorange', lw=2, linestyle=':')
        Protractor_x.clear()
        Protractor_y.clear()
if VerticalProtractor == True:
    for Orientation in range (WallAzimuth-90, WallAzimuth+100, 10):
        Protractor_x.append(90*math.sin(Orientation*pi/180))
        Protractor_y.append(90*math.cos(Orientation*pi/180))
        Protractor_x.append(0*math.sin(Orientation*pi/180))
        Protractor_y.append(0*math.cos(Orientation*pi/180))        
        plt.plot(Protractor_x, Protractor_y, c='darkorange', lw=2, linestyle=':')
        Protractor_x.clear()
        Protractor_y.clear()

plt.title('Stereographic sunpath diagram, for latitude: ' + str(int(180*math.fabs(lat)/pi)) +'$^o$' + str(Hemisphere), loc='center')
plt.legend(loc = 'lower left', frameon=False)
plt.axis('off')
plt.tight_layout()

plt.show()

