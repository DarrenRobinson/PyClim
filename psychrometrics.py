import matplotlib as plt
from climateanalysis import psychrometric as psy
#  TODO
#           Required graphs:          Done?     Data Lists just from Files:                         Calculated[From] Data Lists:
#       - Psychrometric Charrt         []         Dry Bulb Temperatures, Relative Humidities                 X
#   INCOMPLETE


# Would need A LOT of refactoring to make it readable
def psychrometric_chart(dry_bulb_temperatures, relative_humidity_values, lower_temp_limit, evap_cooled_efficiency, plot_monthly=False, plot_evap_cooled=False):
    # Create chart for plotting
    plt.figure(figsize=(12, 8), tight_layout=True)

    g_list = []
    temp_x_list = []
    g_y_list = []

    for rh in range(10, 110, 10):
        for temp in range(-10, 61):
            temp_x_list.append(temp)
            g_y_list.append(psy.moisture_content(temp, rh))
        plt.plot(temp_x_list, g_y_list, lw=1, color='darkgray')
        del temp_x_list[:]
        del g_y_list[:]
    mc = 0
    while mc <= 0.03:
        mc = mc + 0.005
        temp_x_list.append(psy.saturation_temp(mc))
        g_y_list.append(mc)
        temp_x_list.append(60)
        g_y_list.append(mc)
        plt.plot(temp_x_list, g_y_list, lw=1, color='darkgray')
        del temp_x_list[:]
        del g_y_list[:]

    for temp in range(-10, 60, 5):
        gsat = psy.g_dry_wet(temp, temp)
        if gsat >= 0.3:
            gsat = 0.3
        temp_x_list.append(temp)
        g_y_list.append(0)
        temp_x_list.append(temp)
        g_y_list.append(gsat)
        plt.plot(temp_x_list, g_y_list, lw=1, color='darkgray')
        del temp_x_list[:]
        del g_y_list[:]

    for wbt in range(-10, 40, 5):
        for dbt in range(-10, 61, 1):
            mc = psy.g_dry_wet(dbt, wbt)
            if dbt >= wbt:
                temp_x_list.append(dbt)
                g_y_list.append(mc)
        plt.plot(temp_x_list, g_y_list, lw=1, color='darkgray')
        del temp_x_list[:]
        del g_y_list[:]
    # Plot the data on the chart

    if plot_monthly == False:
        for plotpoints in range(0, len(dry_bulb_temperatures)):
            g_list.append(psy.moisture_content(dry_bulb_temperatures[plotpoints], relative_humidity_values[plotpoints]))
        plt.scatter(dry_bulb_temperatures, g_list, c='red', alpha=0.5, s=5)
    else:
        cumhour = 0
        Colour_list = ['firebrick', 'salmon', 'darkorange', 'orange', 'gold', 'yellow', 'yellowgreen', 'green', 'olive',
                       'cyan', 'skyblue', 'blue']
        Month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        daynum_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        Monthly_g = []
        Monthly_t = []
        for month in range(1, 13):
            for days in range(1, daynum_list[month - 1]):
                for hours in range(1, 25):
                    Monthly_g.append(psy.moisture_content(dry_bulb_temperatures[cumhour], relative_humidity_values[cumhour]))
                    Monthly_t.append(dry_bulb_temperatures[cumhour])
                    cumhour = cumhour + 1
            plt.scatter(Monthly_t, Monthly_g, c=Colour_list[11 - month], label=(Month_list[month - 1]), s=6, alpha=0.9)
            del Monthly_t[:]
            del Monthly_g[:]

    if plot_evap_cooled:
        shifted_temp_list = []
        shifted_g_list = []
        if plot_monthly:
            cumhour = 0
            Colour_list = ['firebrick', 'salmon', 'darkorange', 'orange', 'gold', 'yellow', 'yellowgreen', 'green',
                           'olive',
                           'cyan', 'skyblue', 'blue']
            Month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            daynum_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            Monthly_g = []
            Monthly_t = []
            for month in range(1, 13):
                for days in range(1, daynum_list[month - 1]):
                    for hours in range(1, 25):
                        Monthly_g.append(
                            psy.moisture_content(dry_bulb_temperatures[cumhour], relative_humidity_values[cumhour]))
                        tdry = dry_bulb_temperatures[cumhour]
                        twet = psy.twetrh(dry_bulb_temperatures[cumhour], relative_humidity_values[cumhour], True)
                        wbtd = tdry - twet
                        if tdry > lower_temp_limit:
                            tdry = tdry - (evap_cooled_efficiency * wbtd)
                            shifted_temp_list.append(tdry)
                            shifted_g_list.append(psy.g_dry_wet(tdry, twet))
                        else:
                            shifted_temp_list.append(tdry)
                            shifted_g_list.append(Monthly_g[cumhour])
                        cumhour = cumhour + 1
                plt.scatter(shifted_temp_list, shifted_g_list, c=Colour_list[11 - month], label=(Month_list[month - 1]),
                            s=6, alpha=0.9)
                del Monthly_t[:]
                del shifted_temp_list[:]
                del shifted_g_list[:]
        else:
            for plotpoints in range(0, len(dry_bulb_temperatures)):
                g_list.append(psy.moisture_content(dry_bulb_temperatures[plotpoints], relative_humidity_values[plotpoints]))
                tdry = dry_bulb_temperatures[plotpoints]
                twet = psy.twetrh(dry_bulb_temperatures[plotpoints], relative_humidity_values[plotpoints], True)
                wbtd = tdry - twet
                if tdry > lower_temp_limit:
                    tdry = tdry - (evap_cooled_efficiency * wbtd)
                    shifted_temp_list.append(tdry)
                    shifted_g_list.append(psy.g_dry_wet(tdry, twet))
                else:
                    shifted_temp_list.append(tdry)
                    shifted_g_list.append(g_list[plotpoints])
            plt.scatter(shifted_temp_list, shifted_g_list, c='red', alpha=0.5, s=5)

    plt.ylim(0, 0.03)
    plt.xlim(-10, 60)
    plt.xlabel('Dry bulb temperature, $^o$C')
    plt.ylabel('Moisture content, kg/kg (dry air)')

    plt.axvline(x=60, color='lightgrey')
    # plt.axis('off')
    plt.title('Hourly climate data plotted on a psychrometric chart', loc='center')
    plt.legend(loc='upper left', frameon=False)

# Potentially allows plotting of monthly evap-cooled data
# I think this is right
# TODO - write a test to be certain
    if plot_evap_cooled:
        shifted_temp_list = []
        shifted_g_list = []
        if not plot_monthly:
            for plotpoints in range(0, len(dry_bulb_temperatures)):
                g_list.append(psy.moisture_content(dry_bulb_temperatures[plotpoints], relative_humidity_values[plotpoints]))
                tdry = dry_bulb_temperatures[plotpoints]
                twet = psy.twetrh(dry_bulb_temperatures[plotpoints], relative_humidity_values[plotpoints], True)
                wbtd = tdry - twet
                if tdry > lower_temp_limit:
                    tdry = tdry - (evap_cooled_efficiency * wbtd)
                    shifted_temp_list.append(tdry)
                    shifted_g_list.append(psy.g_dry_wet(tdry, twet))
                else:
                    shifted_temp_list.append(tdry)
                    shifted_g_list.append(g_list[plotpoints])
            plt.scatter(shifted_temp_list, shifted_g_list, c='red', alpha=0.5, s=5)
        else:
            cumhour = 0
            Colour_list = ['firebrick', 'salmon', 'darkorange', 'orange', 'gold', 'yellow', 'yellowgreen', 'green', 'olive',
                           'cyan', 'skyblue', 'blue']
            Month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            daynum_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            Monthly_g = []
            Monthly_t = []
            for month in range(1, 13):
                for days in range(1, daynum_list[month - 1]):
                    for hours in range(1, 25):
                        Monthly_g.append(psy.moisture_content(dry_bulb_temperatures[cumhour], relative_humidity_values[cumhour]))
                        tdry = dry_bulb_temperatures[cumhour]
                        twet = psy.twetrh(dry_bulb_temperatures[cumhour], relative_humidity_values[cumhour], True)
                        wbtd = tdry - twet
                        if tdry > lower_temp_limit:
                            tdry = tdry - (evap_cooled_efficiency * wbtd)
                            shifted_temp_list.append(tdry)
                            shifted_g_list.append(psy.g_dry_wet(tdry, twet))
                        else:
                            shifted_temp_list.append(tdry)
                            shifted_g_list.append(Monthly_g[cumhour])
                        cumhour = cumhour + 1
                plt.scatter(shifted_temp_list, shifted_g_list, c=Colour_list[11 - month], label=(Month_list[month - 1]), s=6, alpha=0.9)
                del Monthly_t[:]
                del shifted_temp_list[:]
                del shifted_g_list[:]
