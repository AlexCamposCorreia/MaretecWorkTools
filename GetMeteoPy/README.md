# GetMeteoPy
Python script to download, glue, and interpolate metereological model data to be used as forcing in a MOHID model.

### Software requirements:
- a python 3 distribution
- pyyaml library

### Other requirements:
- `GetMeteoPy.dat` file with START and END dates in YYYY MM DD HH MM SS format
- `GetMeteoPy.yaml` file with the settings

Example `GetMeteoPy.dat`:

> START: 2019 09 27 00 00 00
>
> END: 2019 09 27 00 00 00

Example `GetMeteoPy.yaml`:
```getMeteoPy:
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
    - "wind velocity Y"```
    
    test
