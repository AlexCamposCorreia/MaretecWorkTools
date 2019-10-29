import os
from shutil import copy2
import numpy as np
import h5py


def SinesMM5QuickFix(file):
    f = h5py.File(file, 'r+')
    timeIndex = 1

    while True:
        try:

            str_timeIndex = str(timeIndex).zfill(5)
            air_temp_array = np.asarray(f['Results/air temperature/air temperature_{}'.format(str_timeIndex)])

            J = 16

            for I in range(13, 20):
                print(air_temp_array[J,I])
                air_temp_array[J,I] = air_temp_array[J-1,I]
                air_temp_array[J+1,I] = air_temp_array[J-1,I]
                print(air_temp_array[I,J])
                print('-------------')

            temp_dset = f['Results/air temperature'].create_dataset_like(
                name=None,
                other=f['Results/air temperature/air temperature_{}'.format(str_timeIndex)],
                data=air_temp_array)

            attr_list = list(f['Results/air temperature/air temperature_{}'.format(str_timeIndex)].attrs.keys())

            for a in attr_list:
                temp_dset.attrs.create(
                    name=a,
                    data=f['Results/air temperature/air temperature_{}'.format(str_timeIndex)].attrs[a],
                    dtype=f['Results/air temperature/air temperature_{}'.format(str_timeIndex)].attrs[a].dtype)

            
            del f['Results/air temperature/air temperature_{}'.format(str(timeIndex).zfill(5))]
            f['Results/air temperature/air temperature_{}'.format(str(timeIndex).zfill(5))] = temp_dset

            timeIndex += 1
        
        except KeyError:
            break
    
    f.close()


if __name__ == '__main__':
    print('Working...')
    SinesMM5QuickFix('./D3.hdf5')
    print('Finished.')
