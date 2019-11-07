import os
from shutil import copy2
import numpy as np
from netCDF4 import Dataset

print('Working...')

original_files_dir = './CMEMS_IBI_HOURLY'
formated_files_dir = './CMEMS_IBI_formated'

files = list(os.walk(original_files_dir))[0][2]
netcdf_files = list(filter(lambda x: x.endswith('.nc'), files))


for netcdf_file in netcdf_files:

    print(netcdf_file)

    copy2(original_files_dir+'/'+netcdf_file, formated_files_dir+'/'+netcdf_file)

    f = Dataset(formated_files_dir+'/'+netcdf_file, 'r+')

    time_stamps = np.asarray(f.variables['time'][:])
    new_time_stamps = time_stamps * 3600

    f['time'].units = 'seconds since 1950-01-01 00:00:00'
    f['time'].valid_min = np.min(new_time_stamps)
    f['time'].valid_max = np.max(new_time_stamps)
    f.variables['time'][:] = new_time_stamps

    f.close()

print('Finished.')
