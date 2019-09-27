# GetMeteoPy
Python script to download, glue, and interpolate metereological model data in hdf5 format to be used as forcing in a MOHID model.

### Software requirements:
- a python 3 distribution
- pyyaml library

### Other requirements:
- `GetMeteoPy.dat` file with START and END dates in YYYY MM DD HH MM SS format
- `GetMeteoPy.yaml` file with the settings

Example `GetMeteoPy.dat`:
```yaml
START:                       2019 09 27 00 00 00
END:                         2019 09 27 00 00 00
```

#### `GetMeteoPy.yaml` keywords:
- `getMeteoPy`
  - `dontRunIfFileExists`: (0/1) if file already exists, doesn't run
  - `meteoModel`: (string) name of the meteo model, will be used to write the output file name
  - `meteoDirectory`: (string) location of the directory containing the hdf5 meteo files
  - `meteoName`: (string) prefix of the meteo hdf5 files
  - `domainName`: (string) domain name of the MOHID model, will be used to write the output file name
  - `bathymetry`: (string) location of the MOHID model domain bathymetry
  - `propertiesToInterpolate`: (python or yaml list) list of all the properties to interpolate

Example `GetMeteoPy.yaml`:
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
test 
