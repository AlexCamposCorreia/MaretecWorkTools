import os
import sys

from pprint import pprint

from Common.extended_MHDF5_reader import ExtendedMHDF5Reader
from common_functions.density_calculator import calculate_model_densities 
from common_functions.write_to_csv import write_to_csv

if __name__ == '__main__':

    ### INPUT DATA ############################################################
    # stations coordinates
    # (lon lat)
    S1 = (-8.855261, 37.93272)
    S2 = (-8.850886, 37.92971)
    S2A = (-8.851303, 37.92932)
    S3 = (-8.847949, 37.92775)
    S4 = (-8.853503, 37.93137)
    S5 = (-8.843557, 37.92482)

    # campaign DateStrings
    # campaign 1
    cp1_date = '2018-06-29'

    cp1_S1_time = '12:15:00'
    cp1_S2_time = '13:15:00'
    cp1_S3_time = '14:00:00'
    cp1_S4_time = '12:30:00'

    # campaign 2
    cp2_date = '2018-10-25'

    cp2_S1_time = '13:45:00'
    cp2_S3_time = '12:00:00'

    # campaign 3
    cp3_date = '2019-03-12'

    cp3_S1_time = '13:45:00'
    cp3_S2A_time = '13:00:00'
    cp3_S3_time = '12:15:00'
    cp3_S5_time = '11:30:00'

    # campaign 4
    cp4_date = '2019-04-30'

    cp4_S1_time = '14:00:00'
    cp4_S2A_time = '11:45:00'
    cp4_S3_time = '12:15:00'
    cp4_S5_time = '13:00:00'

    # campaign 5
    cp5_date = '2019-05-23'

    cp5_S1_time = '11:45:00'
    cp5_S2A_time = '11:00:00'
    cp5_S3_time = '10:45:00'
    cp5_S5_time = '10:15:00'

    # campaign 6
    cp6_date = '2019-07-29'

    cp6_S1_time = ''
    cp6_S2A_time = ''
    cp6_S3_time = ''
    cp6_S5_time = ''
    ###########################################################################


    ### EXTRACTION FROM HDF5 FILES ############################################
    properties = ['temperature', 'salinity', 'oxygen', 'phytoplankton', 'ammonia', 'inorganic phosphorus']

    print('Working...')

    # campaign 1
    os.chdir('./campanha1_2018-06-29')
    HDF5directory = 'model_results/Sines4/Results_HDF/2018-06-29_2018-06-30'
    HDF5fileName = 'WaterProperties_1.hdf5'
    outputDirectory = 'model_results/profiles'
    a = ExtendedMHDF5Reader(HDF5fileName, HDF5directory)
    for prop_name in properties:
        try:
            depths, props = a.getDepthProfile(prop_name, S1[0], S1[1], a.getTimeIndexFromDateString(cp1_date+' '+cp1_S1_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S1.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S2[0], S2[1], a.getTimeIndexFromDateString(cp1_date+' '+cp1_S2_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S2.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S3[0], S3[1], a.getTimeIndexFromDateString(cp1_date+' '+cp1_S3_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S3.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S4[0], S4[1], a.getTimeIndexFromDateString(cp1_date+' '+cp1_S4_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S4.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
        except KeyError:
            print("[campaign 1]:: Couldn't find {} in {}/{}, ignoring.".format(prop_name, HDF5directory, HDF5fileName))
    stations = ['S1','S2','S3','S4']
    calculate_model_densities(outputDirectory+'/', stations)
    HDF5fileName = 'Hydrodynamic_1.hdf5'
    a = ExtendedMHDF5Reader(HDF5fileName, HDF5directory)
    prop_name = 'velocity modulus'
    depths, props = a.getDepthProfile(prop_name, S1[0], S1[1], a.getTimeIndexFromDateString(cp1_date+' '+'11:45:00'), forceTopAtZero=True, depthAsNegativeValues=True)
    write_to_csv('{}/{}S1_11h45.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
    depths, props = a.getDepthProfile(prop_name, S4[0], S4[1], a.getTimeIndexFromDateString(cp1_date+' '+'12:45:00'), forceTopAtZero=True, depthAsNegativeValues=True)
    write_to_csv('{}/{}S4_12h45.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
    depths, props = a.getDepthProfile(prop_name, S4[0], S4[1], a.getTimeIndexFromDateString(cp1_date+' '+'13:15:00'), forceTopAtZero=True, depthAsNegativeValues=True)
    write_to_csv('{}/{}S4_13h15.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
    depths, props = a.getDepthProfile(prop_name, S4[0], S4[1], a.getTimeIndexFromDateString(cp1_date+' '+'14:00:00'), forceTopAtZero=True, depthAsNegativeValues=True)
    write_to_csv('{}/{}S4_14h00.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
    os.chdir('..')
    
    # campaign 2
    os.chdir('./campanha2_2018-10-25')
    HDF5directory = 'model_results/Sines4/Results_HDF/2018-10-25_2018-10-26'
    HDF5fileName = 'WaterProperties_1.hdf5'
    outputDirectory = 'model_results/profiles'
    a = ExtendedMHDF5Reader(HDF5fileName, HDF5directory)
    for prop_name in properties:
        try:
            depths, props = a.getDepthProfile(prop_name, S1[0], S1[1], a.getTimeIndexFromDateString(cp2_date+' '+cp2_S1_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S1.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S3[0], S3[1], a.getTimeIndexFromDateString(cp2_date+' '+cp2_S3_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S3.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
        except KeyError:
            print("[campaign 2]:: Couldn't find {} in {}/{}, ignoring.".format(prop_name, HDF5directory, HDF5fileName))
    stations = ['S1','S3']
    calculate_model_densities(outputDirectory+'/', stations)
    os.chdir('..')
    
    # campaign 3
    os.chdir('./campanha3_2019-03-12')
    HDF5directory = 'model_results/Sines4/Results_HDF/2019-03-12_2019-03-13'
    HDF5fileName = 'WaterProperties_1.hdf5'
    outputDirectory = 'model_results/profiles'
    a = ExtendedMHDF5Reader(HDF5fileName, HDF5directory)
    for prop_name in properties:
        try:
            depths, props = a.getDepthProfile(prop_name, S1[0], S1[1], a.getTimeIndexFromDateString(cp3_date+' '+cp3_S1_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S1.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S2A[0], S2A[1], a.getTimeIndexFromDateString(cp3_date+' '+cp3_S2A_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S2A.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S3[0], S3[1], a.getTimeIndexFromDateString(cp3_date+' '+cp3_S3_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S3.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S5[0], S5[1], a.getTimeIndexFromDateString(cp3_date+' '+cp3_S5_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S5.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
        except KeyError:
            print("[campaign 3]:: Couldn't find {} in {}/{}, ignoring.".format(prop_name, HDF5directory, HDF5fileName))
    stations = ['S1','S2A','S3','S5']
    calculate_model_densities(outputDirectory+'/', stations)
    os.chdir('..')
    
    # campaign 4
    os.chdir('./campanha4_2019-04-30')
    HDF5directory = 'model_results/Sines4/Results_HDF/2019-04-30_2019-05-01'
    HDF5fileName = 'WaterProperties_1.hdf5'
    outputDirectory = 'model_results/profiles'
    a = ExtendedMHDF5Reader(HDF5fileName, HDF5directory)
    for prop_name in properties:
        try:
            depths, props = a.getDepthProfile(prop_name, S1[0], S1[1], a.getTimeIndexFromDateString(cp4_date+' '+cp4_S1_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S1.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S2A[0], S2A[1], a.getTimeIndexFromDateString(cp4_date+' '+cp4_S2A_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S2A.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S3[0], S3[1], a.getTimeIndexFromDateString(cp4_date+' '+cp4_S3_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S3.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S5[0], S5[1], a.getTimeIndexFromDateString(cp4_date+' '+cp4_S5_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S5.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
        except KeyError:
            print("[campaign 4]:: Couldn't find {} in {}/{}, ignoring.".format(prop_name, HDF5directory, HDF5fileName))
    stations = ['S1','S2A','S3','S5']
    calculate_model_densities(outputDirectory+'/', stations)
    os.chdir('..')
    
    # campaign 5
    os.chdir('./campanha5_2019-05-23')
    HDF5directory = 'model_results/Sines4/Results_HDF/2019-05-23_2019-05-24'
    HDF5fileName = 'WaterProperties_1.hdf5'
    outputDirectory = 'model_results/profiles'
    a = ExtendedMHDF5Reader(HDF5fileName, HDF5directory)
    for prop_name in properties:
        try:
            depths, props = a.getDepthProfile(prop_name, S1[0], S1[1], a.getTimeIndexFromDateString(cp5_date+' '+cp5_S1_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S1.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S2A[0], S2A[1], a.getTimeIndexFromDateString(cp5_date+' '+cp5_S2A_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S2A.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S3[0], S3[1], a.getTimeIndexFromDateString(cp5_date+' '+cp5_S3_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S3.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
            depths, props = a.getDepthProfile(prop_name, S5[0], S5[1], a.getTimeIndexFromDateString(cp5_date+' '+cp5_S5_time), forceTopAtZero=True, depthAsNegativeValues=True)
            write_to_csv('{}/{}S5.csv'.format(outputDirectory, prop_name), prop_name, depths, props)
        except KeyError:
            print("[campaign 5]:: Couldn't find {} in {}/{}, ignoring.".format(prop_name, HDF5directory, HDF5fileName))
    stations = ['S1','S2A','S3','S5']
    calculate_model_densities(outputDirectory+'/', stations)
    os.chdir('..')
    ###########################################################################
    
    print('Finshed.')
