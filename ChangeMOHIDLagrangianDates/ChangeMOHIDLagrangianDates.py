# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2002-03-06

# This script finds the lines that specify the start and end of a MOHIDLagrangian settings .xml file
# and replaces the date values by what is specified in a .dat file.
#

# intrinsic python libraries
import os
import sys
import shutil
import logging
from datetime import datetime

# user made code
sys.path.append('../')
from mohid_reader import mohid_dat_reader


def change_dates(dat):
    with open(dat['MOHID_XML_FILE'], 'r') as f:
        ls = f.readlines()

    f = open(dat['MOHID_XML_FILE'], 'w')
    for l in ls:
        if l.find('parameter') != -1 and l.find('"Start"') != -1:
            f.write(l[:l.find('value')+7]+datetime.strftime(dat['START'],'%Y %m %d %H %M %S'))
            l = l[l.find('value')+5:]
            l = l[l.find('"')+1:]
            l = l[l.find('"'):]
            f.write(l)
        elif l.find('parameter') != -1 and l.find('"End"') != -1:
            f.write(l[:l.find('value')+7]+datetime.strftime(dat['END'],'%Y %m %d %H %M %S'))
            l = l[l.find('value')+5:]
            l = l[l.find('"')+1:]
            l = l[l.find('"'):]
            f.write(l)
        else:
            f.write(l)

    f.close()


def main():
    dat = mohid_dat_reader.get_mohid_dat('ChangeMOHIDLagrangianDates.dat')
    change_dates(dat)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
