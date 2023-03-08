# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:31:10 2023

@author: Administrator
"""

import os
import numpy as np
import netCDF4 as nc
import pandas as pd
from osgeo import gdal,ogr
from osgeo import gdalconst
import sys
import totiff

def GeomtryCal(lons,lats):
    lon_max = lons.max()
    lon_min= lons.min()
    lat_max = lats.max()
    lat_min = lats.min()
    
    cellsize = 0.1 #对应10000m
    num_lon =  int((lon_max- lon_min)// cellsize) +1
    num_lat =  int((lat_max- lat_min)// cellsize) +1
    # if (lon_max- lon_min) % cellsize != 0 :
    #     num_lon+=1
    # if (lat_max- lat_min) % cellsize !=0:
    #     num_lat+=1
    print(num_lon,num_lat)
    # value_x  value_y 记录 矩阵对应的位置
    value_x = np.zeros([num_lat , num_lon]) - 1000  # -1000为nodata
    value_y = np.zeros([num_lat , num_lon]) - 1000
    print(value_x.shape)

    for i in range(0, len(lons)):
        a11 = []
        for j in range(0, len(lons[i])):
            lo = lons[i][j]
            la = lats[i][j]
            x =  int((lo  - lon_min)//cellsize)
            y =  int((lat_max  - la)//cellsize)
            # if (lat_max  - la)%cellsize != 0:
            #     y += 1
            value_x[y][x] = i
            value_y[y][x] = j
    return    value_x,value_y,num_lon,num_lat

def cal(xs,ys,num_lon,num_lat,value):
     result = np.zeros([num_lat , num_lon]) - 1000   
     for i in range(len(xs)):
         for j in range(len(xs[0])):
             if xs[i][j] != -1000:
                 result[i][j] = value[int(xs[i][j])][int(ys[i][j])]
 
     return result
                 
if __name__ == "__main__":
    filePath = r"E:\\wrfout_d01_2021-11-08_00_00_00.nc"
    file = nc.Dataset(filePath,'r')
    # file = h5py.File(filePath,"r")
    lon = np.array(file["XLONG"][0])
    lat = np.array(file["XLAT"][0])
    value = np.array(file["U"][0][0])
    value_x,value_y,num_lon,num_lat  = GeomtryCal(lon,lat)
    resultval = cal(value_x,value_y,num_lon,num_lat,value)
    west= lon.min()
    north = lon.max()
    cellsize = 0.1
    cols = len(value[0]) 
    rows = len(value)
    NcTotif = totiff.Totif("U2.tif",resultval,len(resultval[0]),len(resultval),west,north,cellsize,cellsize,-1000)
    NcTotif.totif()
    