import os
from shutil import copy2
import numpy as np
import h5py


def SolarRadiationFilter(file, max_value):
    f = h5py.File(file, 'r+')
    timeIndex = 1

    while True:
        try:
            dset_path = 'Results/solar radiation/solar radiation_{}'.format(str(timeIndex).zfill(5))

            solar_radiation_array = np.asarray(f[dset_path])

            solar_radiation_array = np.where(solar_radiation_array > max_value, max_value, solar_radiation_array)

            temp_dset = f['Results/solar radiation'].create_dataset_like(
                name = None,
                other=f[dset_path],
                data=solar_radiation_array)

            attr_list = list(f[dset_path].attrs.keys())

            for a in attr_list:
                temp_dset.attrs.create(
                    name=a,
                    data=f[dset_path].attrs[a],
                    dtype=f[dset_path].attrs[a].dtype)

            
            del f[dset_path]
            f[dset_path] = temp_dset

            timeIndex += 1
        
        except KeyError:
            break
    
    f.close()


if __name__ == '__main__':
    print('Working...')
    SolarRadiationFilter('./MM5_Sines1_2018-06-29_2018-06-30.hdf5', 900)
    print('Finished.')
