"""
Description goes here
"""

import numpy as np
from scipy import interpolate, stats
from scipy.constants import g
from math import sqrt
import os
from common_functions.get_data import get_data
from common_functions.equation_of_state import EOS80_Fofonoff as EOS, extrapolate_rho


def calculate_density(folder, station):
    
    arr_t = get_data(folder +'temperature'+station+'.csv')

    arr_s = get_data(folder +'salinity'+station+'.csv')

    atm_pressure = 1.03 # bar

    rho = EOS(arr_t[0,1], arr_s[0,1])
    #rho = EOS(arr_t[0,1], arr_s[0,1])

    arr_rho = np.array([[arr_t[0,0], rho]])

    for n in range(1, len(arr_t[:,0])):

        try:
            last_rho = extrapolate_rho(arr_rho[-2,0], arr_rho[-2,1], arr_rho[-1,0], arr_rho[-1,1], arr_t[n,0])
            avg_rho = (arr_rho[0,1] + last_rho) / 2
            #print(last_rho)
        except IndexError:
            avg_rho = (arr_rho[0,1] + arr_rho[-1,1]) / 2

        water_pressure = avg_rho * g * -1*arr_t[n,0] * 1E-5
        total_pressure = atm_pressure + water_pressure

        rho = EOS(arr_t[n,1], arr_s[n,1], water_pressure)
        #rho = EOS(arr_t[n,1], arr_s[n,1])

        arr_rho = np.append(arr_rho, [[arr_t[n,0], rho]], axis=0)

    np.savetxt(folder +'density'+station+'.csv', arr_rho, delimiter=',', header='depth,density')


def calculate_model_densities(folder, stations):

    for station in stations:

        calculate_density(folder, station)


if __name__ == '__main__':
    stations = ['S1', 'S2A', 'S3', 'S5']
    calculate_model_densities('campanha5_2019-05-23/model_results/profiles/', stations)
