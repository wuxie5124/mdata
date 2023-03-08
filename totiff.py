# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:46:23 2023

@author: Administrator
"""

"""
转tif工具
"""

from osgeo import gdal,os,ogr
from osgeo import gdalconst
import numpy as np

class Totif():
    def __init__(self,tifPath,value,cols,rows,west,north,width,hight,nodataValue):
        self.value = value;
        self.tifPath  = tifPath
        self.west = west
        self.north = north
        self.width = width
        self.hight = hight
        self.cols = cols
        self.rows = rows
        self.nodataValue = nodataValue
       
    def totif(self):
        datatype = gdal.GDT_Float32
        driver = gdal.GetDriverByName("GTiff")
        rdband = 1
        dataset = driver.Create(self.tifPath, self.cols, self.rows, rdband, datatype)
        rdgeotrans = (self.west, self.width, 0, self.north, 0, -self.hight)
        dataset.SetGeoTransform(rdgeotrans)
        rdproj = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'
        dataset.SetProjection(rdproj)
        band = dataset.GetRasterBand(1)
        band.SetNoDataValue(self.nodataValue)
        band.WriteArray(self.value)
        dataset = None
        band = None
        

if __name__  == "__main__":
    print("test");
    