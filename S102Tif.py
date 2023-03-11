# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 15:41:36 2023

@author: Administrator
"""
import os
import numpy as np
import h5py
import pandas as pd
from osgeo import gdalconst,gdal,osr,ogr
import sys


def toTif(f, path, var, isRemoveNoise, isOverlayUncer):
    listhdf5 = list(f["BathymetryCoverage/BathymetryCoverage.01"].attrs.items())
    east  = listhdf5[0][1]
    west  = listhdf5[11][1]
    north = listhdf5[5][1]
    south = listhdf5[9][1]
    
    width = listhdf5[4][1]
    hight = listhdf5[3][1]
    data = np.array(f[var][:])
    row = len(data[0])
    colunm = len(data)
    
    datazeros = np.zeros([colunm,row])
    datauncertain = np.zeros([colunm,row])
    if(isOverlayUncer):
        for i in range(len(datazeros)):
             for j in range(len(datazeros[i])):
                 datauncertain[i][j] =  data[i][j][1]
        pathUncertain = path[:-4] + "_UC" + path[-4:]          
        tooTif(datauncertain,pathUncertain,row,colunm,west,north,width,hight)
                 
                 
    # else:
    #     for i in range(len(datazeros)):
    #          for j in range(len(datazeros[i])):
    for i in range(len(datazeros)):
         for j in range(len(datazeros[i])):
             datazeros[i][j] =  data[i][j][0]   
                 
    # resultvalue = datazeros
    datavalue = np.copy(datazeros)
    datavalue[datavalue>1000]=0
    if(isRemoveNoise):
       datazeros1 =  arrayRemoveNosie(datazeros,datavalue,colunm,row)
       path2 = path[:-4] + "_RN" + path[-4:]
       tooTif(datazeros1,path2, row, colunm,west,north,width,hight)
    tooTif(datazeros,path,row,colunm,west,north,width,hight)

def tooTif(datazeros,path, row, colunm,west,north,width,hight):
    datatype = gdal.GDT_Float32
    driver = gdal.GetDriverByName("GTiff")
    rdband= 1
    # 上下转换
    zerodataT = np.flipud(datazeros)

    dataset = driver.Create(path, row, colunm, rdband, datatype)
    rdgeotrans = (west,width,0,north,0,-hight)
    dataset.SetGeoTransform(rdgeotrans)
    rdproj ='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'
    dataset.SetProjection(rdproj)
    band  = dataset.GetRasterBand(1)
    band.SetNoDataValue(1000000)
    band.WriteArray(zerodataT)
    dataset = None
    band = None
def arrayRemoveNosie(datazeros,datavalue,colunm,row):
    for i in range(len(datazeros)):
        for j in range(len(datazeros[i])):
            if datazeros[i][j] >1000:
                a = 1
                if i+a > colunm-1:
                    if j+a> row-1:
                        tempvalue = (datavalue[i][j-a] +datavalue[i-a][j] +datavalue[i-a][j-a])/3
                    elif j-a<0:
                        tempvalue = (datavalue[i][j+a] +datavalue[i-a][j+a] +datavalue[i-a][j+a])/3
                    else:
                        tempvalue = (datavalue[i-a][j-a] +datavalue[i-a][j] +datavalue[i-a][j+a] +datavalue[i][j-a] +datavalue[i][j+a] )/5
                elif i-a<0:
                    if j+a>row-1:
                       tempvalue = (datavalue[i][j-a] +datavalue[i+a][j-a] +datavalue[i+a][j])/3
                    elif j-a<0:
                        tempvalue = (datavalue[i][j+a] +datavalue[i+a][j] +datavalue[i+a][j+a])/3    
                    else:
                        tempvalue = (datavalue[i+a][j-a] +datavalue[i+a][j] +datavalue[i+a][j+a] +datavalue[i][j-a] +datavalue[i][j+a] )/5
                else:
                    if j+a>row-1:
                       tempvalue = (datavalue[i-a][j-a] +datavalue[i][j-a]+datavalue[i+a][j-a] +datavalue[i-a][j]+ datavalue[i+a][j])/5
                    elif j-a<0:
                        tempvalue = (datavalue[i-a][j-a] +datavalue[i][j-a]+datavalue[i+a][j-a] +datavalue[i-a][j]+ datavalue[i+a][j])/5
                    else:
                        tempvalue = (datavalue[i-a][j-a] +datavalue[i][j-a]+datavalue[i+a][j-a] +datavalue[i-a][j]+ datavalue[i+a][j] + datavalue[i-a][j+a] +datavalue[i][j+a]+datavalue[i+a][j+a])/8      
                datazeros[i][j]  =  tempvalue
                
    return datazeros

def toShp(f, path, var ,isOverlayUncer):
    listhdf5 = list(f["BathymetryCoverage/BathymetryCoverage.01"].attrs.items())
    east  = listhdf5[0][1][0]
    west  = listhdf5[11][1][0]
    north = listhdf5[5][1][0]
    south = listhdf5[9][1][0]
    print(east)
    width = listhdf5[4][1][0]
    hight = listhdf5[3][1][0]
    data = np.array(f[var][:])
    col = len(data[0])
    row = len(data)
    name = path.split("/")[-1][:-4]
    
    datazeros = np.zeros([row,col])
    datauncertain = np.zeros([row,col])
    
    driver = ogr.GetDriverByName("ESRI Shapefile")
    path = path[:-4] + ".shp"
    print(col,row,name,path,var)
    data_source = driver.CreateDataSource(path) ## shp文件路径
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326) ## 空
    
    layer = data_source.CreateLayer(name , srs, ogr.wkbPoint)
        
    if isOverlayUncer:
        layer.CreateField(ogr.FieldDefn(name, ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("Uncertainty", ogr.OFTReal))
        for i in range(row):
            for j in range(col):
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetField(name, str(data[i][j][0]))
                feature.SetField("Uncertainty", str(data[i][j][1]))
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(west + j*width ,south + i * hight)
                feature.SetGeometry(point)  ## 设置点
                layer.CreateFeature(feature)  ## 添加点
                feature.Destroy()  
        data_source.Destroy()
    else:
        layer.CreateField(ogr.FieldDefn(name, ogr.OFTReal))
        for i in range(row):
            for j in range(col):
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetField(name, str(data[i][j][0]))
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(west + j*width ,south + i * hight)
                feature.SetGeometry(point)  ## 设置点
                layer.CreateFeature(feature)  ## 添加点
                feature.Destroy()  
        data_source.Destroy()

if __name__ == '__main__':
    # file = h5py.File(r"D:\qq文件\1127434146\FileRecv\zjk-21811.h5","r")
    # toShp(file,r"C:\Users\zjm\Desktop\test\张.tif","BathymetryCoverage/BathymetryCoverage.01/Group_001/values",False)
    
     javaParam = []
     for i in range(1, len(sys.argv)):
          javaParam.append(sys.argv[i])
     #a = ["C:\\Users\\Administrator\\Desktop\\zjk-21811.h5","C:\\Users\\Administrator\\Desktop\\s102\\DEPTH.tif","1"]
        
     Str_filePath = javaParam[0]
        
     Str_tifPath = javaParam[1]
    
     Str_varable = javaParam[2]
    
     Str_isNoiseRedution = javaParam[3]
     # bool(int(a[3]))
    
     Str_isOverlayUncertainty = javaParam[4]
    
     Str_isImportRaster = javaParam[5]
    
     filePath = Str_filePath.split("#")[1:]
     tifPath = Str_tifPath.split("#")[1:]
     varable = Str_varable.split("#")[1:]
     isNoiseRedution = Str_isNoiseRedution.split("#")[1:]
     isOverlayUncertainty = Str_isOverlayUncertainty.split("#")[1:]
     isImportRaster = Str_isImportRaster.split("#")[1:]

     for i in range(len(filePath)):
         file = h5py.File(filePath[i],"r")
         if bool(int(isImportRaster[i])):
             toTif(file,tifPath[i],varable[i],bool(int(isNoiseRedution[i])),bool(int(isOverlayUncertainty[i])))
         toShp(file,tifPath[i],varable[i],bool(int(isOverlayUncertainty[i])))
        
     print("There is No Problem")