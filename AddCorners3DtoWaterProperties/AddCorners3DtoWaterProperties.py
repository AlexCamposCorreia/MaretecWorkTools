import numpy as np
import h5py

hydrodynamic_file = './Hydrodynamic.hdf5'
waterproperties_file = './WaterProperties.hdf5'

f1 = h5py.File(hydrodynamic_file, 'r')
f2 = h5py.File(waterproperties_file, 'a')

f2.create_group('Grid/Corners3D')

attr_list = list(f1['Grid/Corners3D'].attrs.keys())
for attr in attr_list:
    f2['Grid/Corners3D'].attrs.create(
        name=attr,
        data=f1['Grid/Corners3D'].attrs[attr],
        dtype=f1['Grid/Corners3D'].attrs[attr].dtype)

for prop in (list(f1['Grid/Corners3D'].keys())):
    f2['Grid/Corners3D'].create_dataset_like(
        name=prop,
        other=f1['Grid/Corners3D/'+prop],
        data=np.asarray(f1['Grid/Corners3D/'+prop]))
    
    attr_list = list(f1['Grid/Corners3D/'+prop].attrs.keys())
    for attr in attr_list:
        f2['Grid/Corners3D/'+prop].attrs.create(
            name=attr,
            data=f1['Grid/Corners3D/'+prop].attrs[attr],
            dtype=f1['Grid/Corners3D/'+prop].attrs[attr].dtype)

f1.close()
f2.close()
