##########################################################################################
# PyClim was developed by Prof. Darren Robinson (University of Sheffield, 2019).         #
# PyClim produces a range of graphs and statistics to support the analysis of climate    #
# data, to support architectural / engineering / technology students to develop their    #
# early-stage bioclimatic design concepts.                                               #
##########################################################################################


#THIS MODULE CONTAINS THE CLIMATE ANALYSIS FUNCTIONS, IN PARTICULAR RELATING TO
#SOLAR RADIATION, ILLUMINATION AND PSYCHROMETRIC PROCESSES. 

#imports the basic libraries
import math
import matplotlib.pyplot as plt
import numpy as np

pi = 3.141592654

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########
# HERE WE OPEN THE CLIMATE FILE AND ASSIGN COORDINATES
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########

file = open("./Finningley.csv", "r")
lat = 53.7
longitude = -1
timezone= 0
timeshift = -0.5 #for the hour-centred time convention

groundref=0.2

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########
# FUNCTIONS TO CALCULATE THE PSYCHROMETRIC PROPERTIES OF HUMID AIR
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########

def g(dbt, rh):
#calculates moisture content from dbt and rh
    psatvap=pss(dbt)
    mc=gss(fs(dbt),psatvap)
    lhs = rh*mc
    low=0.0001
    middle=100
    high=1
    errorlimit=0.00001
    error=1
    while error>errorlimit:
        middle=low+(high-low)/2
        rhmid=100*middle
        if lhs<rhmid:
            high=middle
        else:
            low=middle
        error=math.fabs(lhs-rhmid)
    g=middle
    return g


#def H(dbt,rh):
##Calculates the enthalpy of air
#    mc=g(dbt,rh)
#    if dbt>=0:
#        air_enthalpy = 1.007*dbt-0.026
#    else:
#        air_enthalpy=1.005*dbt
#    vapour_enthalpy=2501+1.84*dbt
#    H=air_enthalpy+mc*vapour_enthalpy
#    return H


def tsat(mc):
#Calculates saturation temperature from moisture content
    tstep=64
    tsathigh=60
    while tstep>0.05:
        told = tsathigh
        tsathigh=tsathigh-tstep
        gsat=g(tsathigh,100)
        if gsat<mc:
            tsathigh=told
        tstep=tstep/2
    tsat=tsathigh
    return tsat


def pss(t):
#Calculates the saturated vapour pressure (kPa) given the air temperature
    if t>=0:
        suf = 30.59051 - 8.2 * math.log10(t + 273.16) + 0.0024804 * (t + 273.16)
        suf = suf - 3142.31 / (t + 273.16)
        pss = 10 ** suf
    else:
        suf = 9.5380997 - 2663.91 / (t + 273.15)
        pss = 10 ** suf
    return pss


def gss(fs, pss):
#calculates moisture content of saturated vapour
    gss = 0.62197 * fs * pss / (101.325 - fs * pss)
    return gss


def fs(dbt):
#provides necessary interaction coefficients
    if dbt < 11:
        fs = -7.3E-06 * (dbt + 273.15) + 1.00444
    elif dbt >= 11 and dbt < 26:
        fs = 1.32E-05 * (dbt + 273.15) + 1.004205
    elif dbt >= 26 and dbt <= 60:
        fs = 4.05E-05 * (dbt + 273.15) + 1.003497
    return fs


def ps(g):
#calculates the vapour pressure of air at a given moisture content
    ps=101.325*g/(0.622+g)
    return ps


def rh(g,dbt):
#calculates rh given the moisture content and dry bulb tempature
    rh=100*(ps(g)/pss(dbt))
    return rh


def pvap(tdry, twet, screen):
#calculates the partial pressure of water vapour mixed with dry air (Pa),
#given dry-bulb and wet-bulb/screen temperature
    if twet >= 0 and screen == True:
        corr = 7.99
    if twet < 0 and screen == True:
        corr = 7.2
    if twet < 0 and screen == False:
        corr = 5.94
    else:
        corr = 6.66
    pssw = pss(twet)
    pvap = pssw - 101.325 * corr * 10**-4 * (tdry - twet)
    return pvap


def g_dry_wet(dbt,twet):
#calculates moisture content, given the dry and wet bulb temperatures
    pst=10*pvap(dbt,twet,False)
    mc = (0.62197 * fs(dbt) * pst / (1013.25 - fs(dbt) * pst))
    return mc


def twetrh(tdry, rh, screen):
#Calculates wet bulb or screen temperature (oC) given the dry bulb temperature and RH
    psuper = pss(tdry)
    Tstep = 64  
    twet = tdry
    while Tstep > 0.25:
        Told = twet
        twet = twet - Tstep
        ps = pvap(tdry, twet, screen)
        rhtwet = 100 * ps / psuper
        if rhtwet < rh:
            twet = Told
        Tstep = Tstep / 2
    twetrh = twet
    return twetrh


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########
# THIS FUNCTION CALCULATES THE GROUND TEMPERATURE
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########


def Tground(t_mean,t_swing,cum_monthdaynum,dayofminmean,depth):
#Eq 2 in: Labs, K. "Regional analysis of ground and above-ground climate conclusion",
#Underground Space Vol.7 pp037-65, 1982  
    #approx ground thermophysical properties
    Conductivity = 1.21
    Density = 1960
    Cp = 840
    Diff = 8.64*10**4*Conductivity/(Density*Cp)#m^2/day
    Decrement = math.exp(-depth*(pi/(365*Diff))**0.5)
    Lag = 0.5*(365/(pi*Diff))**0.5
    Tground = t_mean - t_swing*Decrement*math.cos(2*pi*(cum_monthdaynum-dayofminmean-depth*Lag)/365)
    return Tground


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########
# FUNCTIONS TO CALCULATE THE POSITION OF THE SUN
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########

#Exception handling for arcsine and arccosine functions: only necessary
#when using exclusively solar time
def arccos(x):
    if x>=1:
        arccos=0
    elif x<=-1:
        arccos= pi
    else:
        arccos = math.atan(-x / (-x * x + 1)**0.5) + 2 * math.atan(1)
    return arccos


def arcsin(x):
    if x >= 1:
        arcsin = pi / 2
    elif x <= -1: 
        arcsin = -pi / 2
    else:
        arcsin = math.atan(x / (-x * x + 1)**0.5)
    return arcsin


#Calculates the sunrise and sunset times
def sunrise_time(dec, lat, jday):
    DL = daylength(dec,lat)
    SStime = 12+DL/2
    SRtime = 12-DL/2
    return SStime, SRtime


#this function calculates the declination angle in radians
def declin_angle(jday):
    tau = 2*pi*(jday-1)/365
    declin_angle = 0.006918 - 0.399912 * math.cos(tau) + 0.070257 * math.sin(tau) - 0.006758 * math.cos(2 * tau) + 0.000907 * math.sin(2 * tau) - 0.002697 * math.cos(3 * tau) + 0.00148 * math.sin(3 * tau)
    return declin_angle


#this function calculates the solar altitude in radians
def solar_altitude(jday, hour, latitude, Declin):
    Hourangle = pi * hour / 12
    solar_altitude = arcsin(math.sin(latitude) * math.sin(Declin) - math.cos(latitude) * math.cos(Declin) * 	math.cos(Hourangle))
    if solar_altitude < 0:
        solar_altitude = 0
    return solar_altitude


#this function calculates the solar azimuth
def solar_azimuth(jday, hour, latitude, solalt, declin):
    Hourangle = pi * hour / 12
    if Hourangle < pi:
        solar_azimuth = arccos((-math.sin(latitude) * math.sin(solalt) + math.sin(declin)) / (math.cos(latitude) * math.cos(solalt)))
    else:
        solar_azimuth = ((2 * pi) - arccos((-math.sin(latitude) * math.sin(solalt) + math.sin(declin)) / (math.cos(latitude) * math.cos(solalt))))    
    return solar_azimuth


#this function calculates the cosine of the angle of incidence on a tilted plane
def cai(wallaz, tilt, solalt, solaz):
    wallsolaz = math.fabs(solaz-wallaz)
    CAI = math.cos(solalt)*math.cos(wallsolaz)*math.sin(tilt)+math.sin(solalt)*math.cos(tilt)
    if CAI<0:
        CAI=0
    return CAI


#this function calculates the difference between solar time and clock time
def time_diff(jday, EqTonly, longitude, timezone, timeshift):
    B = 2 * pi * (jday-1)/365
    #The term on the left below, converts from radians, through degrees, to minutes: Earth takes 4minutes to rotate one degree.
    EqT = (4*180/pi) * (0.000075 + 0.001868 * math.cos(B) - 0.032077 * math.sin(B) - 0.014615 * math.cos(2 * B) - 0.040849 * math.sin(2 * B))
    if EqTonly==False:
        #NB: timeshift accounts for the climate file time convention: hour-centred corresponds to +/-30mins
        deltaT = 4 * longitude - 60 * timezone + (60*timeshift) + EqT
    else:
        deltaT = EqT
    #conversion to hours:
    time_diff = deltaT / 60
    return time_diff 


#this function calculates the number of hours that the sun is above the horizon
def daylength(dec, lat):
    daylength=24*arccos(-math.tan(lat)*math.tan(dec))/pi
    return daylength


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########
# FUNCTION TO CALCULATE THE INCIDENT GLOBAL IRRADIANCE
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########


#this function calculates incident irradiance, for either an isotropic or an anisotropic sky
def igbeta(jday, cai, igh, idh, solalt, tilt, isotropic, DiffuseOnly):
    if solalt>0:
        ibn=(igh-idh)/math.sin(solalt)
    else:
        ibn=0
    if isotropic==True:
        idbeta=idh*(1+math.cos(tilt))/2
    else:
        idbeta=0
        if idh>0:
            idbeta=idh_perez(jday, cai, solalt, idh, ibn, tilt)
    if DiffuseOnly==True:
        igbeta=idbeta
    else:
        iground=igh*groundref*(1-math.cos(tilt))/2
        ibbeta=ibn*cai
        igbeta=ibbeta+idbeta+iground
    return igbeta


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########
# FUNCTIONS TO CALCULATE THE INCIDENT DIFFUSE / GLOBAL ILLUMINANCE / IRRADIANCE
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX########


#This calculates the luminous efficacy
def LumEff(globaleff, jday, solalt, idh, ibn):
    amc = 2
    brightness = PerezBrightness(jday, solalt, idh)
    clearness = PerezClearness(solalt, idh, ibn)
    LumEff = LumEffCoeffs(globaleff, clearness, amc, solalt, brightness)
    return LumEff


def LumEffCoeffs(globaleff, clearness, amc, solalt, brightness):
    if globaleff == True:
        LA_list = [96.6251, 107.5371, 98.7277, 92.721, 86.7266, 88.3516, 78.624, 99.6452]
        LB_list = [-0.4703, 0.7866, 0.6972, 0.5591, 0.9763, 1.3891, 1.4699, 1.8569]
        LC_list = [11.501, 1.7899, 4.4046, 8.3579, 7.1033, 6.0641, 4.9305, -4.4555]
        LD_list = [9.1555, -1.1892, -6.9483, -8.3063, -10.9361, -7.5967, -11.3703, -3.1465]
    else:
        LA_list = [97.2375, 107.2129, 104.996, 102.3945, 100.71, 106.42, 141.88, 152.23]
        LB_list = [-0.4597, 1.1508, 2.9605, 5.589, 5.94, 3.83, 1.9, 0.35]
        LC_list = [11.962, 0.584, -5.5334, -13.951, -22.75, -36.15, -53.24, -45.27]
        LD_list = [-8.9149, -3.949, -8.7793, -13.9052, -23.74, -28.83, -14.03, -7.98]
    LumEff = LA_list[clearness-1]+LB_list[clearness-1]*amc+LC_list[clearness-1]*math.sin(solalt)+LD_list[clearness-1]*math.log(brightness)
    return LumEff


#this function calculates the Perez Clearness number, for use in the Perz Coefficients function
def PerezClearness(solalt, idh, ibn):
    ThetaZ=((pi/2)-solalt)*180/pi
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


#Calculates the Perez brightness coefficient
def PerezBrightness(jday, solalt, idh):
    IextraT = 1367*(1+0.033*math.cos((360*jday/365)*pi/180))  
    airmass = 1 / math.sin(solalt)
    PerezBrightness = airmass*idh/IextraT
    return PerezBrightness


#this function calculates the Perez coefficients for use in the Perez tilted surface model
def PerezCoefficients(clearness):
    F11_list = [-0.0083, 0.1299, 0.3297, 0.5682, 0.873, 1.1326, 1.0602, 0.6777]
    F12_list = [0.5877, 0.6826, 0.4869, 0.1875, -0.392, -1.2367, -1.5999, -0.3273]
    F13_list = [-0.0621, -0.1514, -0.2211, -0.2951, -0.3616, -0.4118, -0.3589, -0.2504]
    F21_list = [-0.0596, -0.0189, 0.0554, 0.1089, 0.2256, 0.2878, 0.2642, 0.1561]
    F22_list = [0.0721, 0.066, -0.064, -0.1519, -0.462, -0.823, -1.1272, -1.3765]
    F23_list = [-0.022, -0.0289, -0.0261, -0.014, 0.0012, 0.0559, 0.1311, 0.2506]
    F11 = F11_list[clearness-1]
    F12 = F12_list[clearness-1]
    F13 = F13_list[clearness-1]
    F21 = F21_list[clearness-1]
    F22 = F22_list[clearness-1]
    F23 = F23_list[clearness-1]
    return F11, F12, F13, F21, F22, F23


#these functions calculates diffuse irradiance on a tilted plane using the Perez model
def idh_perez(jday, cai, solalt, idh, ibn, tilt):
    if solalt<(5*pi/180):
        solalt=5*pi/180
    F11, F12, F13, F21, F22, F23 = PerezCoefficients(PerezClearness(solalt, idh, ibn))
    thetaz = (pi/2)-solalt
    brightness = PerezBrightness(jday, solalt, idh)
    F1 = F11+F12*brightness+F13*thetaz
    if F1 < 0:
        F1 = 0
    F2 = F21+F22*brightness + F23*thetaz
    a1 = math.sin(solalt)
    if a1<math.sin(5*pi/180):
        a1=math.sin(5*pi/180)
    idh_perez = idh*((1-F1)*(1+math.cos(tilt))/2+F1*cai/a1+F2*math.sin(tilt))
    return idh_perez

