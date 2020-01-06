# GetMeteoPy
Python script to download, glue, and interpolate metereological model data in hdf5 format to be used as forcing in a MOHID model.


## Requirements
### Software:
- a python 3 distribution
- PyYAML library ([pip](https://pypi.org/project/PyYAML/), [conda](https://anaconda.org/conda-forge/pyyaml))
- h5py ([pip](https://pypi.org/project/h5py/), [conda](https://anaconda.org/conda-forge/h5py))
- ConvertToHDF5 tool from [MOHID](https://github.com/Mohid-Water-Modelling-System/Mohid)

### File requirements:
- `GetMeteoPy.dat` file with START and END dates in YYYY MM DD HH MM SS format
- `GetMeteoPy.yaml` file with the desired settings


## How does it work
GetMeteoPy uses the ConvertToHDF5 MOHID tool with the action [GLUES HDF5 FILES](http://wiki.mohid.com/index.php?title=ConvertToHDF5#GLUES_HDF5_FILES) to glue the meteo hdf5 files, then it uses the action [INTERPOLATE GRIDS](http://wiki.mohid.com/index.php?title=ConvertToHDF5#INTERPOLATE_GRIDS) or the action [PATCH HDF5 FILES](http://wiki.mohid.com/index.php?title=ConvertToHDF5#PATCH_HDF5_FILES) to interpolate the results to the MOHID model bathymetry

## Keywords
### List of keywords used in the `GetMeteoPy.yaml` file:
- `convertToHDF5exe`: (string) location of the ConvertToHDF5 tool
- `bathymetry`: (string) location of the bathymetry of your MOHID Water or Land domain
- `typeOfInterpolation`: (integer)(1,2,3 or 4) option of interpolation used by the INTERPOLATE GRIDS and PATCH HDF5 FILES actions, see the [MOHID documentation](http://wiki.mohid.com/index.php?title=ConvertToHDF5#INTERPOLATE_GRIDS)
- `outputDirectory`: (string) directory to save the output of the program
- `outputPrefix`: (string) used to write the name of the HDF5 output file

- `meteoModels`: block of metereologic models to be used in the interpolation
  - `modelName1`: block of the first metereologic model, name is arbitrary but duplicates are not allowed
    - `meteoDirectory`: (string) directory where your metereologic HDF5 files are stored, program will search inside subdirectories
    - `meteoFileFormat`: (string) name of the files to be searched in the directory, dates are specified using [python datetime string codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) at least year, month and day are expected. Given 2 sets of dates it's assumed to be the start and end of the HDF5 file. Given just 1 date it's assumed to be the start of the HDF5 file.
    - `meteoFileTotalSeconds`: (integer) if given just 1 date in `meteoFileFormat` it's necessary to give the number of sconds between the final and first instant of the HDF5 file.
    - `meteoRemoveStartupSeconds`: (integer)(optional) if your HDF5 files contains startup instant that you don't want to use, use this keyword with the amount of time in seconds to be discarded counting from the begining of the files.
    - `meteoDatFile`: (string) location of the bathymetry file of your metereologic model
    - `level`: (integer) if given more than 1 metereologic model use this keyword to specify the priority (smaller numbers are higher priority)
  - `modelName2`
    - `...`
    - `...`
- `propertiesToInterpolate`: (optional) if you don't want to interpolate all the properties present in the metereologic HDF5 files use this block with a list of properties to interpolate.
  - `...`
  - `...`
- `mohidKeywords`:
  -`GLUES HDF5 FILES`:
    -`...`: `...`
  -`INTERPOLATE GRIDS`:
    -`...`: `...`
  -`PATCH HDF5 FILES`:
    -`...`: `...`


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

GLUES HDF5 FILE action:
```
<begin_file>

ACTION                        : GLUES HDF5 FILES
OUTPUTFILENAME                : D3.hdf5

START                         : 2019 09 01 00 00 00
END                           : 2019 09 02 00 00 00

<<begin_list>>
D3_2019083119_2019090100.hdf5
D3_2019090101_2019090106.hdf5
D3_2019090107_2019090112.hdf5
D3_2019090113_2019090118.hdf5
D3_2019090119_2019090200.hdf5
<<end_list>>

<end_file>
```

INTERPOLATE GRIDS action:
```
<begin_file>

ACTION                        : INTERPOLATE GRIDS
TYPE_OF_INTERPOLATION         : 3
OUTPUTFILENAME                : MM5_Sines1_2019-09-01_2019-09-02.hdf5
NEW_GRID_FILENAME             : ../../../../GeneralData/Bathymetry/Bathymetry_Sines1.dat

START                         : 2019 09 01 00 00 00
END                           : 2019 09 02 00 00 00

<<begin_father>>
FATHER_FILENAME               : D3.hdf5
FATHER_GRID_FILENAME          : D3.dat
<<end_father>>

<<BeginFields>>
air temperature
albedo
downward long wave radiation
mean sea level pressure
pbl height
precipitation
relative humidity
solar radiation
wind velocity X
wind velocity Y
<<EndFields>>

<end_file>
```

Output:

`MM5_Sines1_2019-09-01_2019-09-02.hdf5`
