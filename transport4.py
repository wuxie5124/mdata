# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:19:37 2023

@author: Administrator
"""

"""
nc  -  point ||   --tif 桌面处理
"""

import os
import numpy as np
import netCDF4 as nc
import toShpPoint as sp
import pandas as pd
from osgeo import gdal,ogr
from osgeo import gdalconst
import sys
import datetime 
if __name__ == "__main__":
    timestart =datetime.datetime.now()
    filePath = r"D:\\work\\wrfout_d01_2021-11-08_00_00_00"
    file = nc.Dataset(filePath,'r')
    # file = h5py.File(filePath,"r")
    lons = np.array(file["XLONG"][0]).astype(np.float64)
    lats = np.array(file["XLAT"][0]).astype(np.float64)
    value = np.array(file["U"][0][0])
    shpPath = "U6.shp"
    layername = "windU" 
    fieldnames = ["u"]
    
    toshpPoint = sp.tooPoint(value, shpPath, layername, fieldnames, lons, lats)
    toshpPoint.toPoint();
    print(datetime.datetime.now() - timestart)
    