# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 08:54:13 2023

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
def trans(lons,lats):
    #网格范围确定
    lon_max = lons.max()
    lon_min= lons.min()
    lat_max = lats.max()
    lat_min = lats.min()
    
    cellsize = 0.1 #对应10000m
    num_lon =  (lon_max- lon_min)// cellsize
    num_lat =  (lat_max- lat_min)// cellsize
    if (lon_max- lon_min) % cellsize != 0 :
        num_lon+=1
    if (lat_max- lat_min) % cellsize !=0:
        num_lat+=1
    # value_x  value_y 记录 矩阵对应的位置
    # value_x = np.zeros([num_lat , num_lon]) - 1000  # -1000为nodata
    # value_y = np.zeros([num_lat , num_lon]) - 1000
    gridxy = []
    for i in range(0, int(num_lat)):
        gridy = []
        for j in range(0, int(num_lon)):
            lon = lon_min + j * cellsize
            lat = lat_max - i * cellsize
            gridx = find(lon,lat,lons,lats,cellsize)
            gridy.append(gridx)
        gridxy.append (gridy)
    return gridxy,lon_min,lat_max,cellsize
        
def find(lon,lat,lons,lats,cellsize):
    xy = [];
    for i in range(len(lats)):
        for j in range(len(lats[0])):
            la = lats[i][j]
            lo = lons[i][j]
            if(lo >= lon and lo < (lon + cellsize)) and (la <= lat and la > (lat - cellsize)):
                xy.append([i,j])
    return xy

def getValue(xy,values):
    y = len(xy)
    x = len(xy[0])
    valueresult = np.zeros([y,x]) - 10000
    for i in range(y):
        for j in range(x):
            if(len(xy[i][j]) != 0):
                val = 0;
                for z in range(len(xy[i][j])): 
                    yy = xy[i][j][z][0]  
                    xx = xy[i][j][z][1]
                    val += values[yy][xx]
                valueresult[i][j] = val/len(xy[i][j])
    return valueresult

if __name__ == "__main__":
    filePath = r"E:\\wrfout_d01_2021-11-08_00_00_00.nc"
    file = nc.Dataset(filePath,'r')
    # file = h5py.File(filePath,"r")
    lon = np.array(file["XLONG"][0])
    lat = np.array(file["XLAT"][0])
    xyarrys,west,north,cellsize = trans(lon,lat)
    
    value = getValue(xyarrys,np.array(file["XLONG"][0]))
    NcTotif = totiff.Totif("Lon.tif",value,len(value[0]),len(value),west,north,cellsize,cellsize)
    NcTotif.totif()
    print("Success")