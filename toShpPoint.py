# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:22:20 2023

@author: Administrator
"""

import os
import numpy as np
import pandas as pd
from osgeo import gdal,osr,ogr
from osgeo import gdalconst
import sys


class tooPoint():
    def __init__(self,value,shpPath,layername,fieldnames,lons,lats):
        self.value = value
        self.shpPath = shpPath
        self.layername = layername
        self.fieldnames = fieldnames
        self.lons = lons
        self.lats = lats
        
    def toPoint(self):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        data_source = driver.CreateDataSource(self.shpPath) ## shp文件名称
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326) ## 空
        layer = data_source.CreateLayer(self.layername , srs, ogr.wkbPoint)
        
        for fieldname in self.fieldnames:      
            layer.CreateField(ogr.FieldDefn(fieldname, ogr.OFTReal))
        if self.lons.ndim == 1:
            for i in range(len(self.lons)):
                feature = ogr.Feature(layer.GetLayerDefn())
                for fieldindex in range(len(self.fieldnames)):
                     feature.SetField(self.fieldnames[fieldindex], str(self.value[i][fieldindex]))       
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(self.lons[i],self.lats[i])
                feature.SetGeometry(point)  ## 设置点
                layer.CreateFeature(feature)  ## 添加点    
                feature.Destroy()
        elif(self.lons.ndim == 2):
            for i in range(len(self.lons)):
                for j in range(len(self.lons[i])):
                    feature = ogr.Feature(layer.GetLayerDefn())
                    for fieldindex in range(len(self.fieldnames)):
                         feature.SetField(self.fieldnames[fieldindex], str(self.value[i][j]))       
                    point = ogr.Geometry(ogr.wkbPoint)
                    point.AddPoint(self.lons[i][j],self.lats[i][j])
                    feature.SetGeometry(point)  ## 设置点
                    layer.CreateFeature(feature)  ## 添加点    
                    feature.Destroy()
        data_source.Destroy()
        data_source = None
            

        
        