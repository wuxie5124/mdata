# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 19:44:15 2023

@author: Administrator
"""

import os
import numpy as np
# import h5py
import netCDF4 as nc
import pandas as pd
from osgeo import gdal,ogr
from osgeo import gdalconst
import sys
import totiff

if __name__ == "__main__":
    filePath = r"E:\\wrfout_d01_2021-11-08_00_00_00.nc"
    file = nc.Dataset(filePath,'r')
    # file = h5py.File(filePath,"r")
    lon = np.array(file["XLONG"][0])
    lat = np.array(file["XLAT"][0])
    value = np.array(file["U"][0][0])
    value = np.flipud(value) 
    west= lon.min()
    north = lon.max()
    cellsize = 0.1
    cols = len(value[0]) + 1
    rows = len(value)
    NcTotif = totiff.Totif("U.tif",value,len(value[0]),len(value),west,north,cellsize,cellsize,-1000)
    NcTotif.totif()
    print("成图")
    print("Success")