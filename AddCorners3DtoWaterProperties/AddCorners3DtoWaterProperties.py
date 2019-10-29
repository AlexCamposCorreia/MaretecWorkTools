import h5py

hydrodynamic_file = 'Hydrodynamic_1.hdf5'
waterproperties_file = 'WaterProperties_1.hdf5'

f = h5py.File(hydrodynamic_file, 'r')
Corners3D_Latitude = f['Grid']['Corners3D']['Latitude'][:,:,:]
Corners3D_Longitude = f['Grid']['Corners3D']['Longitude'][:,:,:]
Corners3D_Vertical = f['Grid']['Corners3D']['Vertical'][:,:,:]
f.close()


f = h5py.File(waterproperties_file, 'a')
try:
    f.create_dataset('/Grid/Corners3D/Latitude', data=Corners3D_Latitude)
except RuntimeError:
    pass
try:
    f.create_dataset('/Grid/Corners3D/Longitude', data=Corners3D_Longitude)
except RuntimeError:
    pass
try:
    f.create_dataset('/Grid/Corners3D/Vertical', data=Corners3D_Vertical)
except RuntimeError:
    pass
f.close()
