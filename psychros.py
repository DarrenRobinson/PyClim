##########################################################################################
# PyClim was developed by Prof. Darren Robinson (University of Sheffield, 2019).         #
# PyClim produces a range of graphs and statistics to support the analysis of climate    #
# data, to support architectural / engineering / technology students to develop their    #
# early-stage bioclimatic design concepts.                                               #
##########################################################################################


#////////////////////////////////////////////////////////////////////////////////////
# CREATE A CLASS TO CREATE THE CHART, AND PASS ARRAYS WITH THE DATA TO BE PLOTTED
#////////////////////////////////////////////////////////////////////////////////////


#This module creates a psychrometric chart for the plotting of climate data
#It also creates a second chart with data translated along the wet bulb line 
#to a defined fraction of the wbtd, to mimic adiabatic (evaporative) cooling.

#imports the basic libraries
import math
import matplotlib.pyplot as plt
import numpy as np

from ClimAnalFunctions import * 

file = open("./Phoenix.csv", "r")


file_list = []
temp_list = []
rh_list = []
g_list = []
PlotMonthly=True

PlotEvapCool = True
LLdbt = 25 #lower limit of temperature: above which data is shifted
MartinezLimit = True
EvapCoolEff = 0.7 #Proportion of wbtd thar data s shifted to.
Screen = False #so that wbt not t_screen is calculated


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#READ IN THE CLIMATE DATA TO PLOT
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#this reads climate data file

numhours=0
for line in file:
    line = line.rstrip('\n')
    line = line.split(',')
    file_list.append(line)
    numhours=numhours+1
file.close()


#this popuates lists with the corresponding data
for i in range (3, len(file_list)):
    temp_list.append(float(file_list[i][3]))
    rh_list.append(float(file_list[i][4]))

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#NOW: CREATE THE PSYCHROMETRIC CHART
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

plt.figure(figsize=(12, 8), tight_layout=True)

temp_x_list = []
g_y_list = []

for rh in range (10,110,10):
    for temp in range (-10,61):
        temp_x_list.append(temp)
        g_y_list.append(g(temp,rh))
    plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
    temp_x_list.clear()
    g_y_list.clear()

mc=0
while mc<=0.03:
    mc=mc+0.005
    temp_x_list.append(tsat(mc))
    g_y_list.append(mc)
    temp_x_list.append(60)
    g_y_list.append(mc)
    plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
    temp_x_list.clear()
    g_y_list.clear()

for temp in range(-10,60,5):
    gsat=g_dry_wet(temp,temp)
    if gsat>=0.3:
        gsat=0.3
    temp_x_list.append(temp)
    g_y_list.append(0)
    temp_x_list.append(temp)
    g_y_list.append(gsat)
    plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
    temp_x_list.clear()
    g_y_list.clear()

for wbt in range (-10,40,5):
    for dbt in range (-10, 61, 1):
        mc = g_dry_wet(dbt,wbt)
        if dbt>=wbt:
            temp_x_list.append(dbt)
            g_y_list.append(mc)
    plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
    temp_x_list.clear()
    g_y_list.clear()


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#NOW: PLOT THE DATA
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

if PlotMonthly==False:
    for plotpoints in range (0,len(temp_list)):
        g_list.append(g(temp_list[plotpoints],rh_list[plotpoints]))
    plt.scatter(temp_list,g_list, c='red', alpha=0.5, s=5)
else:
    cumhour=0
    Colour_list = ['firebrick', 'salmon', 'darkorange', 'orange', 'gold', 'yellow', 'yellowgreen', 'green', 'olive', 'cyan', 'skyblue', 'blue']
    Month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    daynum_list = [31,28,31,30,31,30,31,31,30,31,30,31]
    Monthly_g = []
    Monthly_t = []
    for month in range (1,13):
        for days in range (0, daynum_list[month-1]):
            for hours in range(1,25):
                Monthly_g.append(g(temp_list[cumhour],rh_list[cumhour]))
                Monthly_t.append(temp_list[cumhour])
                cumhour=cumhour+1
        plt.scatter(Monthly_t, Monthly_g, c=Colour_list[11-month], label = (Month_list[month-1]), s=6, alpha=0.9)
        Monthly_t.clear()
        Monthly_g.clear()


plt.ylim(0,0.03)
plt.xlim(-10,60)
plt.xlabel('Dry bulb temperature, $^o$C')
plt.ylabel('Moisture content, kg/kg (dry air)')

plt.axvline(x=60, color='lightgrey')
#plt.axis('off')
plt.title('Hourly climate data plotted on a psychrometric chart', loc='center')
plt.legend(loc = 'upper left', frameon=False)

plt.show()


if PlotEvapCool == True:
    
    #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    #RE-CREATE THE PSYCHROMETRIC CHART AND PLOT EVAP-COOLED DATA
    #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    plt.figure(figsize=(12, 8), tight_layout=True)
    
    temp_x_list = []
    g_y_list = []
    for rh in range (10,110,10):
        for temp in range (-10,61):
            temp_x_list.append(temp)
            g_y_list.append(g(temp,rh))
        plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
        temp_x_list.clear()
        g_y_list.clear()
    
    mc=0
    while mc<=0.03:
        mc=mc+0.005
        temp_x_list.append(tsat(mc))
        g_y_list.append(mc)
        temp_x_list.append(60)
        g_y_list.append(mc)
        plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
        temp_x_list.clear()
        g_y_list.clear()
    
    for temp in range(-10,60,5):
        gsat=g_dry_wet(temp,temp)
        if gsat>=0.3:
            gsat=0.3
        temp_x_list.append(temp)
        g_y_list.append(0)
        temp_x_list.append(temp)
        g_y_list.append(gsat)
        plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
        temp_x_list.clear()
        g_y_list.clear()
    
    for wbt in range (-10,40,5):
        for dbt in range (-10, 61, 1):
            mc = g_dry_wet(dbt,wbt)
            if dbt>=wbt:
                temp_x_list.append(dbt)
                g_y_list.append(mc)
        plt.plot(temp_x_list,g_y_list, lw=1, color='darkgray')
        temp_x_list.clear()
        g_y_list.clear()

    
    shifted_temp_list = []
    shifted_g_list = []
    
    for plotpoints in range (0,len(temp_list)):
        g_list.append(g(temp_list[plotpoints],rh_list[plotpoints]))
        tdry = temp_list[plotpoints]
        twet = twetrh(temp_list[plotpoints], rh_list[plotpoints], Screen)
        wbtd = tdry-twet
        
        if MartinezLimit==True:
            LLdbt = 29 + g_list[plotpoints] / -0.0055 #where -0.0055 = dy/dx of PDEC line
        
        if tdry>=LLdbt:
            tdry = tdry - (EvapCoolEff * wbtd)
            shifted_temp_list.append(tdry)
            shifted_g_list.append(g_dry_wet(tdry,twet))
        else:
            shifted_temp_list.append(temp_list[plotpoints])
            shifted_g_list.append(g_list[plotpoints])
    plt.scatter(shifted_temp_list,shifted_g_list, c='red', alpha=0.5, s=5)
    
    plt.ylim(0,0.03)
    plt.xlim(-10,60)
    plt.xlabel('Dry bulb temperature, $^o$C')
    plt.ylabel('Moisture content, kg/kg (dry air)')
    
    plt.axvline(x=60, color='lightgrey')
    #plt.axis('off')
    plt.title('Hourly climate data plotted on a psychrometric chart', loc='center')
    
    plt.show()
















