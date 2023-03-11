# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:11:26 2023

@author: a
"""

import os
import numpy as np
import h5py
import pandas as pd
from osgeo import gdal,osr,ogr
from osgeo import gdalconst
import sys

def toPoint(file,shpPath,var):
    Positionvar = var.split("/")[0] +  "/" + var.split("/")[1]
    level = list(file[Positionvar])
    isGrid = True
    for lev in level:
        if(lev == "Positioning"):
            isGrid = False;
            break;
    if(isGrid):
        west = list(file[Positionvar].attrs.items())[16][1]
        north= list(file[Positionvar].attrs.items())[7][1]
        width= list(file[Positionvar].attrs.items())[6][1]
        heigh= list(file[Positionvar].attrs.items())[5][1]
        widthnum = list(file[Positionvar].attrs.items())[10][1]
        heighnum = list(file[Positionvar].attrs.items())[9][1]
        coordinatearray = []
        for i in range(0,heighnum):
            column = []
            for j in range(0,widthnum):
                column.append((west+j*width,north-i*heigh))
            coordinatearray.append(column)
        coordinate = np.array(coordinatearray)
    else:
        coordinate = file[Positionvar + "/Positioning/geometryValues"][:]
    
    value = file[var][:]
    
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(shpPath) ## shp文件路径
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326) ## 空
    layer = data_source.CreateLayer(var.split("/")[0] , srs, ogr.wkbPoint)
    layer.CreateField(ogr.FieldDefn("Height", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("Trend", ogr.OFTReal))
    if(coordinate.ndim == 1):
        for i in range(len(coordinate)):
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("Height", str(value[i][0]))
            feature.SetField("Trend", str(value[i][1]))
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(coordinate[i][0],coordinate[i][1])
            feature.SetGeometry(point)  ## 设置点
            layer.CreateFeature(feature)  ## 添加点
            feature.Destroy()
        data_source.Destroy()
    elif(coordinate.ndim > 2):
        for i in range(len(coordinate)):
                for j in range(len(coordinate[i])):
                    feature = ogr.Feature(layer.GetLayerDefn())
                    feature.SetField("Height", str(value[i][j][0]))
                    feature.SetField("Trend", str(value[i][j][1]))
                    point = ogr.Geometry(ogr.wkbPoint)
                    point.AddPoint(coordinate[i][j][0],coordinate[i][j][1])
                    feature.SetGeometry(point)  ## 设置点
                    layer.CreateFeature(feature)  ## 添加点
                    feature.Destroy()  
        data_source.Destroy()

if __name__ == '__main__':
    javaParam = []
    for i in range(1, len(sys.argv)):
          javaParam.append(sys.argv[i])
         
    Str_filePath= javaParam[0];
    Str_shpPath = javaParam[1]
    Str_varable = javaParam[2]
     
    filePath = Str_filePath.split("#")[1:]
    shpPath = Str_shpPath.split("#")[1:]
    varable = Str_varable.split("#")[1:]
    # filePath = ["C:\\Users\\Public\\Nwt\\cache\\recv\\2016-20180\\海图\\S104\\S104\\104US00_ches_dcf1_20190703T00Z.h5"]
    # shpPath = ["s104.shp"]
    # varable = ["WaterLevel/WaterLevel.01/Group_001/values"]

    for i in range(len(filePath)):
        file = h5py.File(filePath[i],"r")
        toPoint(file,shpPath[i],varable[i])
     
    print("There is No Problem")