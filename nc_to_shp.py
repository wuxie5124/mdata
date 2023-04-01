# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:49:17 2023

@author: zjm
"""

# 根据传入参数转shp point。
import os
import numpy as np
import netCDF4 as nc
import toShpPoint as sp
import pandas as pd
from osgeo import gdal,ogr
from osgeo import gdalconst
import sys
import datetime 

# def createshp(filePath,shpPath,param,time,level,soil,ftp):
def createshp(filePath,shpPath,param,time,level):
    file = nc.Dataset(filePath,'r')
    lons = np.array(file["XLONG"][0]).astype(np.float64)
    lats = np.array(file["XLAT"][0]).astype(np.float64)
    if time != 0:
        if(level != 0):
            value = np.array(file[param][time-1][level-1])
        # elif(soil!=0):
        #     value = np.array(file[param][time-1][soil-1])
        # elif(ftp!=0):
        #    value = np.array(file[param][time-1][ftp-1])
        else:
            value = np.array(file[param][time-1])
        SP = sp.tooPoint(value, shpPath, param, [param], lons, lats)
        SP.toPoint();

if __name__ == "__main__":
    javaParam = []
    
    for i in range(1, len(sys.argv)):
         javaParam.append(sys.argv[i])
         
    Str_filePath = javaParam[0]
    Str_shpPath = javaParam[1]
    Str_param= javaParam[2]
    Str_time = javaParam[3]
    Str_level = javaParam[4]
    # Str_soil = javaParam[5]
    # Str_ftp = javaParam[6]
    
   
    filePaths = Str_filePath.split("#")[1:]
    shpPaths= Str_shpPath.split("#")[1:]
    params = Str_param.split("#")[1:]
    times = Str_time.split("#")[1:]
    levels = Str_level.split("#")[1:]
    # soils = Str_soil.split("#")[1:]
    # ftps = Str_ftp.split("#")[1:]

    

    for i in range(len(filePaths)):
        filePath = filePaths[i]
        shpPath = shpPaths[i]
        param = params[i]
        time = times[i]
        level = levels[i]
        # soil = soils[i]
        # ftp = ftps[i]
        print(filePath,shpPath,param,time,level)
        # createshp(filePath,shpPath,param,int(time),int(level),int(soil),int(ftp))
        createshp(filePath,shpPath,param,int(time),int(level))
        
    # filePath = r"D:\\work\\data\\wrfout_d01_2021-11-08_00_00_00.nc"
    # param = "U"
    # level = 1
    # time = 1  
    # shpPath = r"D:\\work\\data\\my.shp"
    # createshp(filePath,shpPath,param,time,level)
    
