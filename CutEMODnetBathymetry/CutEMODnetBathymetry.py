# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2002-03-06

# This script crops a bathymetry file from the EMODnet bathymetry service. Will probably work for 
# other sources of bathymetry but was not tested.
# At the moment assumes data comes in the following order: lon, lat, Z or X, Y, Z
#

lon_min = -9.6055
lon_max = -8.5892
lat_min = 37.3720
lat_max = 38.3821
# intrinsic python libraries
import sys

# user made code
sys.path.append('../')
from mohid_reader import mohid_dat_reader


def crop_bathymetry(dat):
    input_file = dat['INPUT_FILE']
    output_file = dat['OUTPUT_FILE']

    lon_min = float(dat['LON_MIN'])
    lon_max = float(dat['LON_MAX'])
    lat_min = float(dat['LAT_MIN'])
    lat_max = float(dat['LAT_MAX'])

    input_separator = dat['INPUT_SEPARATOR']

    if 'OUTPUT_SEPARATOR' in dat.keys():
        output_separator = dat['OUTPUT_SEPARATOR']
    else:
        output_separator = ' '

    if 'WRITE_MOHID_XYZ_BLOCK' in dat.keys() and dat['WRITE_MOHID_XYZ_BLOCK']:
        MOHIDxyzBlock = True
    else:
        MOHIDxyzBlock = False

    f1 = open(input_file, 'r')
    f2 = open(output_file, 'w')

    if MOHIDxyzBlock:
        f2.write('<begin_xyz>\n')

    while True:
        l = f1.readline()
        if l == '':
            break
        l = l.strip()
        if l.endswith(input_separator):
            l = l.rstrip(input_separator)
        l = l.strip('\n')
        l = l.split(input_separator)
        l = list(map(lambda x: float(x), l))
        if lon_min <= l[0] <= lon_max and lat_min <= l[1] <= lat_max:
            l = list(map(lambda x: str(x), l))
            f2.write(output_separator.join(l) + '\n')

    if MOHIDxyzBlock:
        f2.write('<end_xyz>\n')

    f1.close()
    f2.close()


def main():
    print('Working...')
    dat = mohid_dat_reader.get_mohid_dat('CutEMODnetBathymetry.dat')
    print(dat)
    crop_bathymetry(dat)
    print('Finished.')


if __name__ == '__main__':
    main()