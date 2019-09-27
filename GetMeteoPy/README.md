# GetMeteoPy
Python script to download, glue, and interpolate metereological model data in hdf5 format to be used as forcing in a MOHID model.


## Requirements
### Software:
- a python 3 distribution
- [PyYAML](https://pyyaml.org/) library
- ConvertToHDF5 tool from [MOHID](https://github.com/Mohid-Water-Modelling-System/Mohid)

### File requirements:
- `GetMeteoPy.dat` file with START and END dates in YYYY MM DD HH MM SS format
- `GetMeteoPy.yaml` file with the desired settings
- `History` folder on the same directory that GetMeteoPy.py is called on


## Keywords
### List of keywords used in the `GetMeteoPy.yaml` file:
- `getMeteoPy`
  - `dontRunIfFileExists`: (0/1) if file already exists, doesn't run
  - `meteoModel`: (string) name of the meteo model, will be used to write the output file name
  - `meteoDirectory`: (string) location of the directory containing the hdf5 meteo files
  - `meteoName`: (string) prefix of the meteo hdf5 files
  - `domainName`: (string) domain name of the MOHID model, will be used to write the output file name
  - `bathymetry`: (string) location of the MOHID model domain bathymetry
  - `propertiesToInterpolate`: (python or yaml list) list of all the properties to interpolate

## Example usage:
`GetMeteoPy.dat` file:
```yaml
START:                       2019 09 01 00 00 00
END:                         2019 09 02 00 00 00
```

`GetMeteoPy.yaml` file:
```yaml
getMeteoPy:
  dontRunIfFileExists: 1
  meteoModel: "MM5"
  meteoDirectory: "//MWDATA/Storage01/Meteo/MM5/MM5_D2_D3_6h/"
  meteoName: "D3"
  domainName: "Sines1"
  bathymetry: "../../../../GeneralData/Bathymetry/Bathymetry_Sines1.dat"
  propertiesToInterpolate:
    - "air temperature"
    - "albedo"
    - "downward long wave radiation"
    - "mean sea level pressure"
    - "pbl height"
    - "precipitation"
    - "relative humidity"
    - "solar radiation"
    - "wind velocity X"
    - "wind velocity Y"
```

Output:

`MM5_Sines1_2019-09-01_2019-09-02.hdf5`


## How does it work
GetMeteoPy uses the ConvertToHDF5 MOHID tool with the action [GLUES HDF5 FILES](http://wiki.mohid.com/index.php?title=ConvertToHDF5#GLUES_HDF5_FILES) to glue the meteo hdf5 files, then it uses the action [INTERPOLATE GRIDS](http://wiki.mohid.com/index.php?title=ConvertToHDF5#INTERPOLATE_GRIDS) to interpolate the results to the MOHID model bathymetry
