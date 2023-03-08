# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 11:40:06 2022

@author: Administrator
"""


import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from osgeo import gdal
from osgeo import gdalconst
import ogr
import os
import sys

# f = h5py.File("C:\\Users\\Administrator\\Desktop\\zjk-21811.h5", 'r')

# h5 = pd.read_hdf("C:\\Users\\Administrator\\Desktop\\zjk-21811.h5",key ="BathymetryCoverage")
# aDataset = f["BathymetryCoverage"]

# }

def toTif(f, path):
    listhdf5 = list(f["BathymetryCoverage"]["BathymetryCoverage.01"].attrs.items())
    east  = listhdf5[0][1]
    west  = listhdf5[11][1]
    north = listhdf5[5][1]
    south = listhdf5[9][1]
    
    width = listhdf5[4][1]
    hight = listhdf5[3][1]
    
    data = f["BathymetryCoverage"]["BathymetryCoverage.01"]["Group_001"]["values"][:]
    
    zerodata = np.zeros([503,543])
    zerodataunc1 = np.zeros([503,543])
    zerodataunc2 = np.zeros([503,543])
    
    for i in range(len(zerodata)):
        for j in range(len(zerodata[i])):
            zerodata[i][j] = data[i][j][0]
    datatype = gdal.GDT_Float32
    driver = gdal.GetDriverByName("GTiff")
    rdband= 1

    dataset = driver.Create(path, 543,503, rdband, datatype)
    rdgeotrans = (west,width,0,north,0,-hight)
    dataset.SetGeoTransform(rdgeotrans)
    rdproj ='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'
    dataset.SetProjection(rdproj)
    band  = dataset.GetRasterBand(1)
    band.SetNoDataValue(1000000)
    band.WriteArray(zerodata)
    dataset = None
    band = None
    
def toTif2(f,path):
    
    east  = f["WaterLevel"]['WaterLevel.01'].attrs["eastBoundLongitude"]
    west  = f["WaterLevel"]['WaterLevel.01'].attrs["westBoundLongitude"]
    south = f["WaterLevel"]['WaterLevel.01'].attrs["southBoundLatitude"]
    north = f["WaterLevel"]['WaterLevel.01'].attrs["northBoundLatitude"]
    
    width = f["WaterLevel"]['WaterLevel.01'].attrs["gridSpacingLongitudinal"]
    hight = f["WaterLevel"]['WaterLevel.01'].attrs["gridSpacingLatitudinal"]
    
    
    for item in list(f["WaterLevel"]['WaterLevel.01'].keys()):
    # item = 'Group_001'
        data = f["WaterLevel"]['WaterLevel.01'][item]["values"][:]
        npzeros = np.zeros([8,4])
        for i in range(len(data)):
            for j in range(len(data[i])):
                npzeros[i][j] = data[i][j][0]
        
        datatype = gdal.GDT_Float32
        driver = gdal.GetDriverByName("GTiff")
        rdband= 1
        
        dataset = driver.Create(path + item + ".tif", 4,8, rdband, datatype)
        rdgeotrans = (west,width,0,north,0,-hight)
        dataset.SetGeoTransform(rdgeotrans)
        rdproj ='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'
        dataset.SetProjection(rdproj)
        band  = dataset.GetRasterBand(1)
        band.SetNoDataValue(-9999)
        band.WriteArray(npzeros)
        dataset = None
        band = None
                   
                   
               

if __name__ == '__main__':
    
    filePath = "C:\\Users\\Administrator\\Desktop\\S104\\104US00_ches_dcf2_20190606T12Z.h5"
    model = "r"; #"W"
    
    outfile0 = "C:\\Users\\Administrator\\Desktop\\S104\\104US00_ches_dcf2_20190606T12Z"
    
    file = h5py.File(filePath,model)
    a = list(file["WaterLevel"]['WaterLevel.01'].keys())
    # for aitem in a:
    #     print(file["WaterLevel"]['WaterLevel.01'][aitem].attrs["timePoint"])
    # toTif2(file,outfile0)
    # toTif(file,outfile0)


    
    