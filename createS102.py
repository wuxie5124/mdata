# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:01:12 2023

@author: zjm
"""

import os
import numpy as np
import h5py
import toShpPoint as sp
import pandas as pd
from osgeo import gdal, ogr
from osgeo import gdalconst

if __name__ == "__main__":
    #首先解析hdf5结构 - 读取
    # filePath = r"D:\qq文件\1127434146\FileRecv\S104\S104\104US00_ches_dcf1_20190703T00Z.h5"
    # file = h5py.File(filePath,"r")
    # filePath = r"data\new8H5.h5"
    # file = h5py.File(filePath,"w")
    # # imgData = np.zeros((30,3,128,256))
    # # file["2D"] = imgData
    # file["1D"] = range(0,100)
    # # file["STR"] = "This is new str"

    # file["1D"].attrs["1DAtrr"] = np.array([1,2,3])
    # file["1D"].attrs["1DAtrr2"] = "属性2"
    # file.close()

    # templatefilePath = r"D:\qq文件\1127434146\FileRecv\S104\S104\104US00_ches_dcf1_20190703T00Z.h5"
    # templatefile = h5py.File(templatefilePath,"r")
    dtype = h5py.special_dtype(vlen=str)
    filePath = r"data\supermap4ExportS104.h5"
    file = h5py.File(filePath, "w")
    file.create_group("Group_F")
    file.create_group("WaterLevel")
    file["Group_F"]["WaterLevel"] = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99', b'99.99', b'closedInterval'), (b'waterLevelTrend', b'Water level trend', b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'), (b'waterLevelTime',
                                             b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')], dtype=[('code', dtype), ('name', dtype), ('uom.name', dtype), ('fillValue', dtype), ('dataType', dtype), ('lower', dtype), ('upper', dtype), ('closure', dtype)])
    # file["Group_F"]["WaterLevel"] = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99',b'99.99', b'closedInterval'),(b'waterLevelTrend', b'Water level trend', b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'),(b'waterLevelTime', b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')],dtype=[('code', '|S9'), ('name', '|S9'), ('uom.name', '|S9'), ('fillValue', '|S9'), ('dataType', '|S9'), ('lower', '|S9'), ('upper', '|S9'), ('closure', '|S9')])
    file["Group_F"]["featureCode"] = np.array([b'WaterLevel'], dtype='|S10')
    file["WaterLevel"].create_group("WaterLevel.01")
    for i in range(1, 26):
        groupname = "Group_" + "%03d" % i
        file["WaterLevel"]["WaterLevel.01"].create_group(groupname)
        file["WaterLevel"]["WaterLevel.01"][groupname]["values"] = np.array([(1.325, 0), (1.324, 0), (1.238, 0), (1.825, 0)],
                                                                            dtype=[('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4')])
        file["WaterLevel"]["WaterLevel.01"][groupname].attrs["timePoint"] = "20190703T000000Z"
    file["WaterLevel"]["WaterLevel.01"].create_group("Positioning")
    file["WaterLevel"]["WaterLevel.01"]["Positioning"]["geometryValues"] = np.array([(-76.29, 39.250123), (-76.41, 38.74), (-76.33, 38.25), (-76.19, 38.21)], dtype={
                                                                                    'names': ['longitude', 'latitude'], 'formats': ['<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
    file["WaterLevel"]["WaterLevel.01"]["uncertainty"] = np.array([(b'waterLevelHeight', -1.)], dtype={
                                                                  'names': ['name', 'value'], 'formats': [dtype, '<f8'], 'offsets': [0, 8], 'itemsize': 64})
    file["WaterLevel"]["axisNames"] = np.array(
        [b'longitude', b'latitude '], dtype='|S9')
