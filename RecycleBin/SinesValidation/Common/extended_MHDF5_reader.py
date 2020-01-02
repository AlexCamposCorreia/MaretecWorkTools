from datetime import datetime

import numpy as np

from Common.MHDF5_reader import MHDF5Reader
from Common.grid_to_center_cells import lonlat_grid_to_center_cells


class ExtendedMHDF5Reader(MHDF5Reader):

    def __init__(self, fileName, directory):
        super().__init__(fileName, directory, mandatoryMesh=False)
    
    #returns the time step corresponding to a dateString
    def getTimeIndexFromDateString(self, dateString):
        date = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
        if date < datetime.strptime(self.getDateStr(1), "%Y-%m-%d %H:%M:%S") or date > datetime.strptime(self.getDateStr(self.getNumbTimeSteps()), "%Y-%m-%d %H:%M:%S"):
            print('- [MHDF5Reader::getTimeIndexFromDateString]: date provided is not present in HDF5 file range')
            exit(1)
        for n in range(1, self.getNumbTimeSteps()+1):
            if date == datetime.strptime(self.getDateStr(n), "%Y-%m-%d %H:%M:%S"):
                return n
        print('- [MHDF5Reader::getTimeIndexFromDateString]: the specific date provided is not present in the HDF5 file')
        exit(1)
    #returns the longitude horizontal grid array
    def getLonHorizontalGrid(self):
        return self.f['Grid']['Longitude'][:]

    #returns the latitude horizontal grid array
    def getLatHorizontalGrid(self):
        return self.f['Grid']['Latitude'][:]

    #returns
    def getLonHorizontalGridCenterCells(self):
        return lonlat_grid_to_center_cells(self.getLonHorizontalGrid(), self.getLatHorizontalGrid())[0]

    def getLatHorizontalGridCenterCells(self):
        return lonlat_grid_to_center_cells(self.getLonHorizontalGrid(), self.getLatHorizontalGrid())[1]
    
    #returns the bathymetry 2D array
    def getBathymetry(self):
        if self.hasBathymetry():
            return self.f['Grid']['Bathymetry'][:]
        else:
            print('- [MHDF5Reader::getBathymetry]: hdf file has no Bathymetry attribute')
            exit(1)
    
    #returns the results array of a given property
    def getPropertyResults(self, propertyName, timeIndex):
        if propertyName in self.f['Results'].keys():
            propertyArray = self.f['Results'][propertyName][propertyName+'_'+str(timeIndex).zfill(5)][:]
            return propertyArray
        else:
            print('- [MHDF5Reader::getPropertyResults]: {} not found in hdf file'.format(propertyName))
            print('try:', self.f['Results'].keys())
            exit(1)
    
    #returns the open points array
    def getOpenPoints(self, timeIndex):
        if 'OpenPoints' in self.f['Grid'].keys():
            openPointsArray = self.f['Grid']['OpenPoints']['OpenPoints_'+str(timeIndex).zfill(5)][:]
            return openPointsArray
        else:
            print('- [MHDF5Reader::getOpenPoints]: OpenPoints not found in hdf file')
            exit(1)

    #returns the value of a given property at a long, lat, depth point
    def getPointValue(self, propertyName, longitude, latitude, depth, timeIndex):
        latGrid1D = self.getLatHorizontalGrid()[0,:]
        if latitude < latGrid1D[0] or latGrid1D[-1] < latitude: 
            print('- [MHDF5Reader::getPointValue]: latitude: {} is outside the hdf file range of [{}, {}]'.format(latitude, latGrid1D[0], latGrid1D[-1]))
            exit(1)

        lonGrid1D = self.getLonHorizontalGrid()[:,0]
        if longitude < lonGrid1D[0] or lonGrid1D[-1] < longitude: 
            print('- [MHDF5Reader::getPointValue]: latitude: {} is outside the hdf file range of [{}, {}]'.format(longitude, lonGrid1D[0], lonGrid1D[-1]))
            exit(1)

        i = 0
        while True:
            if latGrid1D[i] < latitude < latGrid1D[i+1]:
                break
            else:
                i += 1
        
        j = 0
        while True:
            if lonGrid1D[j] < longitude < lonGrid1D[j+1]:
                break
            else:
                j += 1

        verticalGrid1D = self.f['Grid']['VerticalZ']['Vertical_'+str(timeIndex).zfill(5)][:,j,i]
        lenBeforeTrim = len(verticalGrid1D)-1
        verticalGrid1D = list(filter(lambda x: x > -9.8e15, verticalGrid1D))
        lenAfterTrim = len(verticalGrid1D)-1
        k = lenBeforeTrim - lenAfterTrim
        if depth < verticalGrid1D[-1] or verticalGrid1D[0] < depth:
            print('- [MHDF5Reader::getPointValue]: depth: {} is outside the hdf file range of [{}, {}]'.format(depth, verticalGrid1D[-1], verticalGrid1D[0]))
            exit(1)
        
        k_aux = 0
        while True:
            if verticalGrid1D[k_aux] > depth > verticalGrid1D[k_aux+1]:
                break
            else:
                k_aux += 1
        k = k + k_aux

        print('i:', i+1)
        print('j:', j+1)
        print('k:', k+1)

        return self.getPropertyResults(propertyName, timeIndex)[k,j,i]

    #returns the depth profile of a given property at a long, lat location
    def getDepthProfile(self, property_name, longitude, latitude, timeIndex, forceTopAtZero=False, depthAsNegativeValues=False):
        latGrid1D = self.getLatHorizontalGrid()[0,:]
        i = 0
        while True:
            if latGrid1D[i] < latitude < latGrid1D[i+1]:
                break
            else:
                i += 1
        
        lonGrid1D = self.getLonHorizontalGrid()[:,0]
        j = 0
        while True:
            if lonGrid1D[j] < longitude < lonGrid1D[j+1]:
                break
            else:
                j += 1

        verticalGrid = self.f['Grid']['VerticalZ']['Vertical_'+str(timeIndex).zfill(5)][:,j,i]
        verticalGrid = list(filter(lambda x: x > -9.8e15, verticalGrid))
        verticalGrid.reverse()

        verticalCenterCells = []
        aux = 0
        while aux < len(verticalGrid)-1:
            verticalCenterCells.append((verticalGrid[aux] + verticalGrid[aux+1]) / 2)
            aux += 1

        property1Dvertical = self.f['Results'][property_name][property_name+'_'+str(timeIndex).zfill(5)][:,j,i]
        property1Dvertical = list(filter(lambda x: x > -9.8e15, property1Dvertical))
        property1Dvertical.reverse()
        property1Dvertical = property1Dvertical[:len(verticalCenterCells)]

        if forceTopAtZero is True:
            top = verticalGrid[0]
            verticalCenterCells = list(map(lambda x: x-top, verticalCenterCells))

        if depthAsNegativeValues is True:
            verticalCenterCells = list(map(lambda x: -x, verticalCenterCells))

        return verticalCenterCells, property1Dvertical


if __name__ == '__main__':
    a = ExtendedMHDF5Reader('Hydrodynamic.hdf5', '.')

    lon = -10.229544
    lat = 39.048503
    depth = 1.24

    #print(a.getTimeIndexFromDateString('2019-08-01 12:00:00'))
    #print(a.getPropertyResults('velocity modulus', timeIndex=a.getTimeIndexFromDateString('2019-08-01 12:00:00')))
    #print(a.getDepthProfile('velocity modulus', lon, lat, timeIndex=5, forceTopAtZero=True, depthAsNegativeValues=True))
    print(a.getPointValue('velocity modulus', longitude=lon, latitude=lat, depth=depth, timeIndex=5))
