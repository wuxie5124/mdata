# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:56:39 2023

@author: zjm
"""
# 导出数据集为海图数据。dataset -> tif -> h5 or  dataset ->array->h5 暂定为前者

import h5py
from osgeo import ogr, gdalconst, gdal
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import ChartEnum as ce
import traceback

# strtype = h5py.special_dtype(vlen=str)
# strtype = h5py.vlen_dtype(str)
strtype2 = h5py.string_dtype(encoding="utf8")
strtype = h5py.vlen_dtype(str)


class tooChartS104():
    """
    导出海图数据的方法
    """

    def __init__(self, name, path, dcftype, info, time, coord, data):
        self.name = name
        self.path = path
        self.dcftype = dcftype
        self.info = info
        self.data = data
        self.time = time
        self.coord = coord
        """
        dcftype:
        1  ==  dcf1
        2  ==  dcf2
        3  ==  dcf3
        7  ==  dcf7
        8  ==  dcf8
        """

    def toChart(self):
        if(self.dcftype == 1):
            self.createdcf1()
        if(self.dcftype == 2):
            self.createdcf2()
        # if(self.dcftype == 3):
        #     self.createdf3()
        # if(self.dcftype == 7):
        #     self.createdf7()
        if(self.dcftype == 8):
            self.createdcf8()

    """
    创建 group -> dataset -> attrs
    """

    def createInfo(self, file):

        issueDate = datetime.now().strftime("%Y%m%d")
        issueTime = datetime.now().strftime("%H%M%SZ")

        fileName = ['eastBoundLongitude', 'geographicIdentifier', 'horizontalCRS', 'issueDate', 'issueTime', 'metadata', 'northBoundLatitude', 'productSpecification',
                    'southBoundLatitude', 'verticalCS', 'verticalCoordinateBase', 'verticalDatum', 'verticalDatumReference', 'waterLevelTrendThreshold', 'westBoundLongitude']
        fileValue = [self.eastlon, 'Chesapeake Bay', 4326, issueDate, issueTime,
                     'MD_104US00_ches_dcf1_20190703T00Z.XML', self.northlat, 'INT.IHO.S-104.1.0', self.southlat, 6499, 2, 12, 1, 0.2, self.westlon]

        file.attrs.create(fileName[0], fileValue[0], dtype="float64")
        file.attrs.create(fileName[1], fileValue[1], dtype=h5py.string_dtype(
            length=len(fileValue[1])))
        file.attrs.create(fileName[2], fileValue[2], dtype="int16")
        file.attrs.create(fileName[3], fileValue[3], dtype=h5py.string_dtype(
            length=len(fileValue[3])))
        file.attrs.create(fileName[4], fileValue[4], dtype=h5py.string_dtype(
            length=len(fileValue[4])))
        file.attrs.create(fileName[5], fileValue[5], dtype=h5py.string_dtype(
            length=len(fileValue[5])))
        file.attrs.create(fileName[6], fileValue[6], dtype="float64")
        file.attrs.create(fileName[7], fileValue[7], dtype=h5py.string_dtype(
            length=len(fileValue[5])))
        file.attrs.create(fileName[8], fileValue[8], dtype="float64")
        file.attrs.create(fileName[9], fileValue[9], dtype="int16")
        file.attrs.create(
            fileName[10], fileValue[10], dtype=ce.verticalCoordinateBase)
        file.attrs.create(fileName[11], fileValue[11], dtype="int16")
        file.attrs.create(
            fileName[12], fileValue[12], dtype=ce.verticalDatumReference)
        file.attrs.create(fileName[13], fileValue[13], dtype="float32")
        file.attrs.create(fileName[14], fileValue[14], dtype="float64")
        file["Group_F"]["WaterLevel"].attrs.create(
            "chunking", "0,0", dtype=h5py.string_dtype(length=len("0,0")))

    # 该方法只传递数据坐标，属性信息固定
    def createdcf1_old(self):
        productTime = datetime.now().strftime('%Y%m%dT%HZ')
        if self.name == None:
            self.name = "104US00_ches_" + "dcf1_" + productTime
        timecount = len(self.time)
        self.westlon = min(self.coord[:, 0])
        self.eastlon = max(self.coord[:, 0])
        self.southlat = min(self.coord[:, 1])
        self.northlat = max(self.coord[:, 1])
        maxValue = max(self.data)
        minValue = min(self.data)
        startTime = self.time[0]
        endTime = self.time[-1]

        Group_WaterLevel = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99', b'99.99', b'closedInterval'),
                                     (b'waterLevelTrend', b'Water level trend',
                                      b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'),
                                     (b'waterLevelTime', b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')],
                                    dtype=[('code', strtype), ('name', strtype), ('uom.name', strtype), ('fillValue', strtype), ('dataType', strtype), ('lower', strtype), ('upper', strtype), ('closure', strtype)])
        Group_featureCode = np.array(
            [b'WaterLevel'], dtype='|S10')
        geometryValues = np.array(self.coord,
                                  dtype={'names': ['longitude', 'latitude'], 'formats': ['<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
        uncertainty = np.array([(b'waterLevelHeight', -1.)],
                               dtype={'names': ['name', 'value'], 'formats': [strtype, '<f8'], 'offsets': [0, 8], 'itemsize': 64})
        axisNames = np.array([b'longitude', b'latitude '], dtype='|S9')
        dataset = np.array([(item, 0) for item in self.data],
                           dtype=[('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4')])

        WaterLevelName = ['commonPointRule', 'dataCodingFormat', 'dimension', 'horizontalPositionUncertainty', 'maxDatasetHeight',
                          'methodWaterLevelProduct', 'minDatasetHeight', 'numInstances', 'timeUncertainty', 'verticalUncertainty']

        WaterLevelValue = [4, 1, 2, -1.0, maxValue,
                           'pred, obsv, hcst, or fcst', minValue, 1, -1.0, -1.0]
        WaterLevel01Name = ['dateTimeOfFirstRecord', 'dateTimeOfLastRecord', 'eastBoundLongitude', 'northBoundLatitude',
                            'numGRP', 'numberOfStations', 'southBoundLatitude', 'typeOfWaterLevelData', 'westBoundLongitude']
        WaterLevel01Value = [
            startTime.strftime('%Y%m%dT%H%M%SZ'), endTime.strftime('%Y%m%dT%H%M%SZ'), self.eastlon, self.northlat, timecount, 1, self.southlat, 2, self.westlon]

        try:
            # group
            file = h5py.File(self.path + self.name + ".h5", "w")
            file.create_group("Group_F")
            file.create_group("WaterLevel")
            file["WaterLevel"].create_group("WaterLevel.01")
            for i in range(timecount):
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel"]["WaterLevel.01"].create_group(groupName)
            file["WaterLevel"]["WaterLevel.01"].create_group("Positioning")
            file["Group_F"]["WaterLevel"] = Group_WaterLevel
            file["Group_F"]["featureCode"] = Group_featureCode
            # dataset
            for i in range(timecount):
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel"]["WaterLevel.01"][groupName]["values"] = dataset[i]

            file["WaterLevel"]["WaterLevel.01"]["Positioning"]["geometryValues"] = geometryValues
            file["WaterLevel"]["WaterLevel.01"]["uncertainty"] = uncertainty
            file["WaterLevel"]["axisNames"] = axisNames
            # attrs
            self.createInfo(file)

            file["Group_F"]["WaterLevel"].attrs.create(
                "chunking", "0,0", dtype=h5py.string_dtype(length=len("0,0")))
            file["WaterLevel"].attrs.create(
                WaterLevelName[0], WaterLevelValue[0], dtype=ce.commonPointRule)
            file["WaterLevel"].attrs.create(
                WaterLevelName[1], WaterLevelValue[1], dtype=ce.dataCodingFormat)
            file["WaterLevel"].attrs.create(
                WaterLevelName[2], WaterLevelValue[2], dtype="int16")
            file["WaterLevel"].attrs.create(
                WaterLevelName[3], WaterLevelValue[3], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[4], WaterLevelValue[4], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[5], WaterLevelValue[5], dtype=h5py.string_dtype(length=len(WaterLevelValue[5])))
            file["WaterLevel"].attrs.create(
                WaterLevelName[6], WaterLevelValue[6], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[7], WaterLevelValue[7], dtype="int16")
            file["WaterLevel"].attrs.create(
                WaterLevelName[8], WaterLevelValue[8], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[9], WaterLevelValue[9], dtype="float32")

            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[0], WaterLevel01Value[0], dtype=h5py.string_dtype(length=len(WaterLevel01Value[0])))
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[1], WaterLevel01Value[1], dtype=h5py.string_dtype(length=len(WaterLevel01Value[1])))
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[2], WaterLevel01Value[2], dtype="float64")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[3], WaterLevel01Value[3], dtype="float64")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[4], WaterLevel01Value[4], dtype="int16")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[5], WaterLevel01Value[5], dtype="int16")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[6], WaterLevel01Value[6], dtype="float64")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[7], WaterLevel01Value[7], dtype=ce.typeOfWaterLevelData)
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[8], WaterLevel01Value[8], dtype="float64")

            for i in range(len(self.time)):
                pt = self.time[i]
                pointTimeStr = pt.strftime('%Y%m%dT%HZ')
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel/WaterLevel.01"][groupName].attrs.create(
                    "timePoint", pointTimeStr, dtype=h5py.string_dtype(length=16))
            file.close()
        except:
            file.close()
            raise ValueError('Wrong')
            """
            创建实例，没有交互
            """

        """
        固定站
        """
        producttime = datetime(2021, 12, 21, 14, 11)
        datatime = datetime(2019, 7, 3, 0, 0)

        productName = "104US00_ches_" + "dcf1_" + \
            datatime.strftime('%Y%m%dT%HZ') + ".h5"
        timecount = 25
        try:
            file = h5py.File(self.path + productName, "w")
            # create group
            file.create_group("Group_F")
            file.create_group("WaterLevel")
            file["WaterLevel"].create_group("WaterLevel.01")
            for i in range(timecount):
                # pt = datatime + timedelta(hours=i)
                # pointTimeStr = pt.strftime('%Y%m%dT%HZ')
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel"]["WaterLevel.01"].create_group(groupName)
            file["WaterLevel"]["WaterLevel.01"].create_group("Positioning")

            # create dateset
            file["Group_F"]["WaterLevel"] = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99', b'99.99', b'closedInterval'), (b'waterLevelTrend', b'Water level trend', b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'), (b'waterLevelTime',
                                                     b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')], dtype=[('code', strtype), ('name', strtype), ('uom.name', strtype), ('fillValue', strtype), ('dataType', strtype), ('lower', strtype), ('upper', strtype), ('closure', strtype)])
            file["Group_F"]["featureCode"] = np.array(
                [b'WaterLevel'], dtype='|S10')
            geometryValues = np.array([(-76.29, 39.250123), (-76.41, 38.74), (-76.33, 38.25),
                                       (-76.19, 38.21)],
                                      dtype={'names': ['longitude', 'latitude'], 'formats': ['<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
            axisNames = np.array([b'longitude', b'latitude '], dtype='|S9')
            uncertainty = np.array([(b'waterLevelHeight', -1.)],
                                   dtype={'names': ['name', 'value'], 'formats': [strtype, '<f8'], 'offsets': [0, 8], 'itemsize': 64})
            for i in range(timecount):
                groupName = "Group_" + "%03d" % (i+1)
                dataset = np.array([(1.325, 0), (1.324, 0), (1.238, 0), (1.825, 0)],
                                   dtype=[('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4')])
                file["WaterLevel"]["WaterLevel.01"][groupName]["values"] = dataset
            file["WaterLevel"]["WaterLevel.01"]["Positioning"]["geometryValues"] = geometryValues
            file["WaterLevel"]["WaterLevel.01"]["uncertainty"] = uncertainty
            file["WaterLevel"]["axisNames"] = axisNames

            # create attrs
            # 第一级
            fileName = ['eastBoundLongitude', 'geographicIdentifier', 'horizontalCRS', 'issueDate', 'issueTime', 'metadata', 'northBoundLatitude', 'productSpecification',
                        'southBoundLatitude', 'verticalCS', 'verticalCoordinateBase', 'verticalDatum', 'verticalDatumReference', 'waterLevelTrendThreshold', 'westBoundLongitude']
            fileValue = [-76.19, 'Chesapeake Bay', 4326, '20211221', '141100Z',
                         'MD_104US00_ches_dcf1_20190703T00Z.XML', 39.250123, 'INT.IHO.S-104.1.0', 38.21, 6499, 2, 12, 1, 0.2, -76.41]
            # for i in range(len(fileName)):
            #     file.attrs[fileName[i]] = fileValue[i]
            # # file.attrs[12].dtype = verticalDatumReference
            for i in range(len(fileName)):
                if fileName[i] == "verticalCoordinateBase":
                    file.attrs.create(
                        fileName[i],  fileValue[i], dtype=ce.verticalCoordinateBase)
                elif fileName[i] == "verticalDatumReference":
                    file.attrs.create(
                        fileName[i],  fileValue[i], dtype=ce.verticalDatumReference)
                elif fileName[i] == "waterLevelTrendThreshold":
                    file.attrs.create(
                        fileName[i],  fileValue[i], dtype="float32")
                elif isinstance(fileValue[i], int):
                    file.attrs.create(
                        fileName[i], fileValue[i], dtype="int16")
                elif isinstance(fileValue[i], float):
                    file.attrs.create(
                        fileName[i], fileValue[i], dtype="float")
                elif isinstance(fileValue[i], str):
                    file.attrs.create(
                        fileName[i],  fileValue[i], dtype=h5py.string_dtype(length=len(fileValue[i])))

            file["Group_F"]["WaterLevel"].attrs.create(
                "chunking", "0,0", dtype=h5py.string_dtype(length=len("0,0")))
            WaterLevelName = ['commonPointRule', 'dataCodingFormat', 'dimension', 'horizontalPositionUncertainty', 'maxDatasetHeight',
                              'methodWaterLevelProduct', 'minDatasetHeight', 'numInstances', 'timeUncertainty', 'verticalUncertainty']
            WaterLevelValue = [4, 1, 2, -1.0, 2.898,
                               'pred, obsv, hcst, or fcst', 0.039, 1, -1.0, -1.0]

            for i in range(len(WaterLevelName)):
                if WaterLevelName[i] == 'commonPointRule':
                    file["WaterLevel"].attrs.create(
                        WaterLevelName[i], WaterLevelValue[i], dtype=ce.commonPointRule)
                elif WaterLevelName[i] == 'dataCodingFormat':
                    file["WaterLevel"].attrs.create(
                        WaterLevelName[i], WaterLevelValue[i], dtype=ce.dataCodingFormat)
                elif isinstance(WaterLevelValue[i], int):
                    file["WaterLevel"].attrs.create(
                        WaterLevelName[i], WaterLevelValue[i], dtype="int16")
                elif isinstance(WaterLevelValue[i], float):
                    file["WaterLevel"].attrs.create(
                        WaterLevelName[i], WaterLevelValue[i], dtype="float32")
                else:
                    file["WaterLevel"].attrs.create(
                        WaterLevelName[i], WaterLevelValue[i], dtype=h5py.string_dtype(length=len(WaterLevelValue[i])))
            WaterLevel01Name = ['dateTimeOfFirstRecord',
                                'dateTimeOfLastRecord',
                                'eastBoundLongitude',
                                'northBoundLatitude',
                                'numGRP',
                                'numberOfStations',
                                'southBoundLatitude',
                                'typeOfWaterLevelData',
                                'westBoundLongitude']
            WaterLevel01Value = [
                '20190703T000000Z', '20190704T000000Z', -76.19, 39.250123, 4, 4, 38.21, 2, -76.41]
            for i in range(len(WaterLevel01Name)):
                if WaterLevel01Name[i] == "typeOfWaterLevelData":
                    file["WaterLevel/WaterLevel.01"].attrs.create(
                        WaterLevel01Name[i], WaterLevel01Value[i], dtype=ce.typeOfWaterLevelData)
                elif isinstance(WaterLevel01Value[i], int):
                    file["WaterLevel/WaterLevel.01"].attrs.create(
                        WaterLevel01Name[i], WaterLevel01Value[i], dtype="int16")
                elif isinstance(WaterLevel01Value[i], float):
                    file["WaterLevel/WaterLevel.01"].attrs.create(
                        WaterLevel01Name[i], WaterLevel01Value[i], dtype="float64")
                elif isinstance(WaterLevel01Value[i], str):
                    file["WaterLevel/WaterLevel.01"].attrs.create(
                        WaterLevel01Name[i], WaterLevel01Value[i], dtype=h5py.string_dtype(length=len(WaterLevel01Value[i])))
            for i in range(timecount):
                pt = datatime + timedelta(hours=i)
                pointTimeStr = pt.strftime('%Y%m%dT%HZ')
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel/WaterLevel.01"][groupName].attrs.create(
                    "timePoint", pointTimeStr, dtype=h5py.string_dtype(length=len(pointTimeStr)))
            file.close()
        except:
            file.close()
            raise ValueError('Wrong')

    def createdcf1(self):
        x = self.data['x'].tolist()
        y = self.data['y'].tolist()
        self.coord = [(x[index], y[index])for index in range(len(x))]
        eastBoundLongitude = max(x)
        westBoundLongitude = min(x)
        southBoundLatitude = min(y)
        northBoundLatitude = max(y)
        # 表记录属性

        geographicIdentifier = self.info[self.info["Name"] == 'geographicIdentifier']["Value"].tolist()[
            0]
        horizontalCRS = 4326
        issueDate = self.info[self.info["Name"] == 'issueDate']["Value"].tolist()[
            0]
        issueTime = self.info[self.info["Name"] == 'issueTime']["Value"].tolist()[
            0]
        metadata = self.info[self.info["Name"] == 'metadata']["Value"].tolist()[
            0]
        productSpecification = 'INT.IHO.S-104.1.0'
        verticalCS = int(self.info[self.info["Name"]
                         == 'verticalCS']["Value"].tolist()[0])
        verticalCoordinateBase = int(
            self.info[self.info["Name"] == 'verticalCoordinateBase']["Value"].tolist()[0])
        # verticalDatum = int(
        #     self.info[self.info['Name'] == 'verticalDatum']["Value"].tolist()[0])
        verticalDatum = 12
        verticalDatumReference = int(
            self.info[self.info["Name"] == 'verticalDatumReference']["Value"].tolist()[0])
        waterLevelTrendThreshold = float(
            self.info[self.info["Name"] == 'waterLevelTrendThreshold']["Value"].tolist()[0])
        # 固定内容
        Group_WaterLevel = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99', b'99.99', b'closedInterval'),
                                     (b'waterLevelTrend', b'Water level trend',
                                      b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'),
                                     (b'waterLevelTime', b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')],
                                    dtype=[('code', strtype), ('name', strtype), ('uom.name', strtype), ('fillValue', strtype), ('dataType', strtype), ('lower', strtype), ('upper', strtype), ('closure', strtype)])
        Group_featureCode = np.array(
            [b'WaterLevel'], dtype='|S10')
        # geometryValues = np.array(self.coord, dtype={'names': ['longitude', 'latitude'], 'formats': [
        #                           '<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
        uncertainty = np.array([(b'waterLevelHeight', -1.)],
                               dtype={'names': ['name', 'value'], 'formats': [strtype, '<f8'], 'offsets': [0, 8], 'itemsize': 64})

        axisNames = np.array([b'longitude', b'latitude '], dtype='|S9')
        try:
            print("创建group与数据集")
            file = h5py.File(self.path + "\\" + self.name + ".h5", "w")
            # group and dataset
            file.create_group("Group_F")
            file.create_group("WaterLevel")
            file["Group_F"].create_dataset("WaterLevel", data=Group_WaterLevel)
            file["Group_F"].create_dataset(
                "featureCode", data=Group_featureCode)
            file["WaterLevel"].create_dataset("axisNames", data=axisNames)
            waterLevel = list(set(self.data['waterlevel'].tolist()))
            waterLevel.sort()
            # print(waterLevel)
            for wl_item in waterLevel:
                waterlevelName = 'WaterLevel.' + '%02d' % wl_item
                file["WaterLevel"].create_group(waterlevelName)
                # 这里a是时间
                a = self.data[self.data['waterlevel']
                              == wl_item]['timepoint'].tolist()
                print(a)
                seta = list(set(a))
                # print(seta)
                for i in range(len(seta)):
                    groupName = "Group_" + "%03d" % (i+1)
                    file["WaterLevel"][waterlevelName].create_group(groupName)
                    aa = self.data[(self.data['waterlevel'] == wl_item) & (
                        self.data['timepoint'] == seta[i])][['height', 'trend']].values
                    dataset = np.array([(item[0], item[1])for item in aa], dtype=[
                                       ('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4')])
                    file["WaterLevel"][waterlevelName][groupName].create_dataset(
                        "values", data=dataset)
                    # print(i)
                    # print(seta[i])
                setcoorda = self.data[self.data['waterlevel'] == wl_item][['x', 'y']].values
                setcoord = list(set([(item[0], item[1])for item in setcoorda]))
                
                file["WaterLevel"][waterlevelName].create_group("Positioning")
                geometryValues = np.array(setcoord, dtype={'names': ['longitude', 'latitude'], 'formats': [
                                          '<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
                file["WaterLevel"][waterlevelName]["Positioning"].create_dataset(
                    "geometryValues", data=geometryValues)
                file["WaterLevel"][waterlevelName].create_dataset(
                    'uncertainty', data=uncertainty)
            # attrs
            file.attrs.create("eastBoundLongitude",
                              eastBoundLongitude, dtype="float64")
            file.attrs.create("geographicIdentifier", geographicIdentifier, dtype=h5py.string_dtype(
                length=len(geographicIdentifier)))
            file.attrs.create("horizontalCRS", horizontalCRS, dtype="int16")
            file.attrs.create("issueDate", issueDate, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("issueTime", issueTime, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("metadata", metadata, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("northBoundLatitude",
                              northBoundLatitude, dtype="float64")
            file.attrs.create("productSpecification", productSpecification, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("southBoundLatitude",
                              southBoundLatitude, dtype="float64")
            file.attrs.create("verticalCS", verticalCS, dtype="int16")
            file.attrs.create("verticalCoordinateBase",
                              verticalCoordinateBase, dtype=ce.verticalCoordinateBase)
            file.attrs.create("verticalDatum", verticalDatum, dtype="int16")
            file.attrs.create("verticalDatumReference",
                              verticalDatumReference, dtype=ce.verticalDatumReference)
            file.attrs.create("waterLevelTrendThreshold",
                              waterLevelTrendThreshold, dtype="float32")
            file.attrs.create("westBoundLongitude",
                              westBoundLongitude, dtype="float64")

            commonPointRule = int(
                self.info[self.info["Name"] == 'commonPointRule']['Value'].tolist()[0])
            dataCodingFormat = int(
                self.info[self.info["Name"] == 'dataCodingFormat']['Value'].tolist()[0])
            dimension = 2
            horizontalPositionUncertainty = -1.0
            maxDatasetHeight = max(self.data["height"].values)
            minDatasetHeight = min(self.data["height"].values)
            methodWaterLevelProduct = self.info[self.info["Name"] == 'methodWaterLevelProduct']['Value'].tolist()[
                0]
            numInstances = int(
                self.info[self.info["Name"] == 'numInstances']['Value'].tolist()[0])
            timeUncertainty = -1.0
            verticalUncertainty = -1.0
            file['WaterLevel'].attrs.create(
                "commonPointRule", commonPointRule, dtype=ce.commonPointRule)
            file['WaterLevel'].attrs.create(
                "dataCodingFormat", dataCodingFormat, dtype=ce.dataCodingFormat)
            file['WaterLevel'].attrs.create(
                "dimension", dimension, dtype="int16")
            file['WaterLevel'].attrs.create(
                "horizontalPositionUncertainty", horizontalPositionUncertainty, dtype="float32")
            file['WaterLevel'].attrs.create(
                "maxDatasetHeight", maxDatasetHeight, dtype="float32")
            file['WaterLevel'].attrs.create(
                "methodWaterLevelProduct", methodWaterLevelProduct, dtype=h5py.string_dtype(length=len(methodWaterLevelProduct)))
            file['WaterLevel'].attrs.create(
                "minDatasetHeight", minDatasetHeight, dtype="float32")
            file['WaterLevel'].attrs.create(
                "numInstances", numInstances, dtype="int16")
            file['WaterLevel'].attrs.create(
                "timeUncertainty", timeUncertainty, dtype="float32")
            file['WaterLevel'].attrs.create(
                "verticalUncertainty", verticalUncertainty, dtype="float32")
            for wl_item in waterLevel:
                waterlevelName = 'WaterLevel.' + '%02d' % wl_item
                rank = "WaterLevel/" + waterlevelName
                typeOfWaterLevelData = int(self.info[(self.info["Rank"] == rank) & (
                    self.info["Name"] == "typeOfWaterLevelData")]['Value'].tolist()[0])
                timepoint_str = self.data[self.data['waterlevel']
                                          == wl_item]['timepoint'].tolist()
                timepoint = [datetime.strptime(
                    item, "%Y%m%dT%H%M%SZ") for item in timepoint_str]

                dateTimeOfFirstRecord = min(
                    timepoint).strftime("%Y%m%dT%H%M%SZ")
                dateTimeOfLastRecord = max(
                    timepoint).strftime("%Y%m%dT%H%M%SZ")
                scoord = self.data[self.data['waterlevel']
                                   == wl_item][['x', 'y']].values
                print(scoord)
                setscoord = list(set([(item[0], item[1])for item in scoord]))

                eastBoundLongitude_secondary = max(scoord[:, 0])
                westBoundLongitude_secondary = min(scoord[:, 0])
                northBoundLatitude_secondary = max(scoord[:, 1])
                southBoundLatitude_secondary = min(scoord[:, 1])
                numGPR = numberOfStations = len(setscoord)

                file[rank].attrs.create("dateTimeOfFirstRecord", dateTimeOfFirstRecord,
                                        dtype=h5py.string_dtype(length=len(dateTimeOfFirstRecord)))
                file[rank].attrs.create("dateTimeOfLastRecord", dateTimeOfLastRecord, dtype=h5py.string_dtype(
                    length=len(dateTimeOfLastRecord)))
                file[rank].attrs.create(
                    "eastBoundLongitude", eastBoundLongitude_secondary, dtype="float64")
                file[rank].attrs.create(
                    "northBoundLatitude", northBoundLatitude_secondary, dtype="float64")
                file[rank].attrs.create("numGPR", numGPR, dtype="int16")
                file[rank].attrs.create(
                    "numberOfStations", numberOfStations, dtype="int16")
                file[rank].attrs.create(
                    "southBoundLatitude", southBoundLatitude_secondary, dtype="float64")
                file[rank].attrs.create(
                    "typeOfWaterLevelData", typeOfWaterLevelData, dtype=ce.typeOfWaterLevelData)
                file[rank].attrs.create(
                    "westBoundLongitude", westBoundLongitude_secondary, dtype="float64")
                for i in range(len(seta)):
                    groupName = "Group_" + "%03d" % (i+1)
                    rank_s = rank + "/" + groupName
                    timepoint_sub = seta[i]
                    file[rank_s].attrs.create(
                        "timePoint", timepoint_sub, dtype=h5py.string_dtype(length=len(timepoint_sub)))
            print("完成")
        except Exception as e:
            print(e)
            traceback.print_exc()

    def createdcf2(self):
        productTime = datetime.now().strftime('%Y%m%dT%HZ')
        if self.name == None:
            self.name = "104US00_ches_" + "dcf2_" + productTime
        timecount = len(self.time)
        self.westlon = min(self.coord[:, :, 0].reshape(1, -1))
        self.eastlon = max(self.coord[:, :, 0].reshape(1, -1))
        self.southlat = min(self.coord[:, :, 1].reshape(1, -1))
        self.northlat = max(self.coord[:, :, 1].reshape(1, -1))
        if timecount > 1:
            timeinterval = (self.time[1] - self.time[2]).seconds
        maxValue = max(self.data.reshape(1, -1))
        minValue = min(self.data.reshape(1, -1))
        startTime = self.time[0]
        endTime = self.time[-1]
        Group_WaterLevel = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99', b'99.99', b'closedInterval'),
                                     (b'waterLevelTrend', b'Water level trend',
                                      b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'),
                                     (b'waterLevelTime', b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')],
                                    dtype=[('code', strtype), ('name', strtype), ('uom.name', strtype), ('fillValue', strtype), ('dataType', strtype), ('lower', strtype), ('upper', strtype), ('closure', strtype)])
        Group_featureCode = np.array(
            [b'WaterLevel'], dtype='|S10')

        uncertainty = np.array([(b'waterLevelHeight', -1.)],
                               dtype={'names': ['name', 'value'], 'formats': [strtype, '<f8'], 'offsets': [0, 8], 'itemsize': 64})
        axisNames = np.array([b'longitude', b'latitude '], dtype='|S9')
        dataset = np.array([[[(item3, 0)for item3 in item2] for item2 in item1]for item1 in self.data],
                           dtype=[('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4')])

        WaterLevelName = ['commonPointRule', 'dataCodingFormat', 'dimension', 'horizontalPositionUncertainty', 'interpolationType', 'maxDatasetHeight',
                          'methodWaterLevelProduct', 'minDatasetHeight', 'numInstances', 'sequencingRule.scanDirection', 'sequencingRule.type', 'timeUncertainty', 'verticalUncertainty']

        WaterLevelValue = [4, 1, 2, -1.0, 5, maxValue, 'pred, obsv, hcst, or fcst',
                           minValue, 1, 'longitude,latitude',  1, -1.0, -1.0]
        WaterLevel01Name = ['dateTimeOfFirstRecord', 'dateTimeOfLastRecord', 'eastBoundLongitude', 'gridOriginLatitude', 'gridOriginLongitude', 'gridSpacingLatitudinal', 'gridSpacingLongitudinal', 'northBoundLatitude',
                            'numGRP', 'numPointsLatitudinal', 'numPointsLongitudinal', 'numberOfTimes', 'southBoundLatitude', 'startSequence', 'timeRecordInterval', 'typeOfWaterLevelData', 'westBoundLongitude']

        WaterLevel01Value = [
            startTime.strftime('%Y%m%dT%H%M%SZ'), endTime.strftime('%Y%m%dT%H%M%SZ'), self.eastlon, self.southlat, self.westlon, 0.25, 0.25, self.northlat, timecount, len(self.data), len(self.data[0]), timecount, 1, self.southlat, '0,0', timeinterval, 5, self.westlon]

        try:
            file = h5py.File(self.path + self.name + ".h5", "w")
            file.create_group("Group_F")
            file.create_group("WaterLevel")
            file["WaterLevel"].create_group("WaterLevel.01")
            for i in range(timecount):
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel"]["WaterLevel.01"].create_group(groupName)
            file["WaterLevel"]["WaterLevel.01"].create_group("Positioning")
            # dataset

            file["Group_F"]["WaterLevel"] = Group_WaterLevel
            file["Group_F"]["featureCode"] = Group_featureCode

            for i in range(timecount):
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel"]["WaterLevel.01"][groupName]["values"] = dataset[i]
            file["WaterLevel"]["WaterLevel.01"]["uncertainty"] = uncertainty
            file["WaterLevel"]["axisNames"] = axisNames
            # attrs
            self.createInfo(file)

            file["WaterLevel"].attrs.create(
                WaterLevelName[0], WaterLevelValue[0], dtype=ce.commonPointRule)
            file["WaterLevel"].attrs.create(
                WaterLevelName[1], WaterLevelValue[1], dtype=ce.dataCodingFormat)
            file["WaterLevel"].attrs.create(
                WaterLevelName[2], WaterLevelValue[2], dtype="int16")
            file["WaterLevel"].attrs.create(
                WaterLevelName[3], WaterLevelValue[3], dtype="float32")

            file["WaterLevel"].attrs.create(
                WaterLevelName[5], WaterLevelValue[5], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[6], WaterLevelValue[6], dtype=h5py.string_dtype(length=len(WaterLevelValue[6])))
            file["WaterLevel"].attrs.create(
                WaterLevelName[7], WaterLevelValue[7], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[8], WaterLevelValue[8], dtype="int16")
            file["WaterLevel"].attrs.create(
                WaterLevelName[9], WaterLevelValue[9], dtype=h5py.string_dtype(length=len(WaterLevelValue[9])))
            file["WaterLevel"].attrs.create(
                WaterLevelName[10], WaterLevelValue[10], dtype=ce.sequencingRuleType)
            file["WaterLevel"].attrs.create(
                WaterLevelName[11], WaterLevelValue[11], dtype="float32")
            file["WaterLevel"].attrs.create(
                WaterLevelName[12], WaterLevelValue[12], dtype="float32")

            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[0], WaterLevel01Value[0], dtype=h5py.string_dtype(length=len(WaterLevel01Value[0])))
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[1], WaterLevel01Value[1], dtype=h5py.string_dtype(length=len(WaterLevel01Value[1])))
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[2], WaterLevel01Value[2], dtype="float64")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[3], WaterLevel01Value[3], dtype="float64")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[4], WaterLevel01Value[4], dtype="int16")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[5], WaterLevel01Value[5], dtype="int16")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[6], WaterLevel01Value[6], dtype="float64")
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[7], WaterLevel01Value[7], dtype=ce.typeOfWaterLevelData)
            file["WaterLevel/WaterLevel.01"].attrs.create(
                WaterLevel01Name[8], WaterLevel01Value[8], dtype="float64")

            for i in range(len(self.time)):
                pt = self.time[i]
                pointTimeStr = pt.strftime('%Y%m%dT%HZ')
                groupName = "Group_" + "%03d" % (i+1)
                file["WaterLevel/WaterLevel.01"][groupName].attrs.create(
                    "timePoint", pointTimeStr, dtype=h5py.string_dtype(length=16))
            file.close()
        except:
            file.close()
            raise ValueError('Wrong')
        # def createdf3(self):

        # def createdf7(self):

            # 根据传入属性进行写入
    def createdcf8(self):
        # 此时data已经为dataFrame且coord已经在里面了
        # 部分固定属性信息存在info里面,也为dataFrame
        print("开始")
        # 数据属性
        try:
            x = self.data['x'].tolist()
            y = self.data['y'].tolist()
            self.coord = [(x[index], y[index])for index in range(len(x))]
            eastBoundLongitude = max(x)
            westBoundLongitude = min(x)
            southBoundLatitude = min(y)
            northBoundLatitude = max(y)
            # 表记录属性

            geographicIdentifier = self.info[self.info["Name"] == 'geographicIdentifier']["Value"].tolist()[
                0]
            horizontalCRS = 4326
            issueDate = self.info[self.info["Name"] == 'issueDate']["Value"].tolist()[
                0]
            issueTime = self.info[self.info["Name"] == 'issueTime']["Value"].tolist()[
                0]
            metadata = self.info[self.info["Name"] == 'metadata']["Value"].tolist()[
                0]
            productSpecification = 'INT.IHO.S-104.1.0'
            verticalCS = int(self.info[self.info["Name"]
                             == 'verticalCS']["Value"].tolist()[0])
            verticalCoordinateBase = int(
                self.info[self.info["Name"] == 'verticalCoordinateBase']["Value"].tolist()[0])
            # verticalDatum = int(
            #     self.info[self.info['Name'] == 'verticalDatum']["Value"].tolist()[0])
            verticalDatum = 12
            verticalDatumReference = int(
                self.info[self.info["Name"] == 'verticalDatumReference']["Value"].tolist()[0])
            waterLevelTrendThreshold = float(
                self.info[self.info["Name"] == 'waterLevelTrendThreshold']["Value"].tolist()[0])
            # 固定内容
            Group_WaterLevel = np.array([(b'waterLevelHeight', b'Water level height', b'metres', b'-9999.0', b'H5T_FLOAT', b'-99.99', b'99.99', b'closedInterval'),
                                         (b'waterLevelTrend', b'Water level trend',
                                          b' ', b'0', b'H5T_ENUM', b'1', b'1', b'1'),
                                         (b'waterLevelTime', b'Water level time', b'DateTime', b'1', b'H5T_STRING', b'19000101T000000Z', b'21500101T000000Z', b'closedInterval')],
                                        dtype=[('code', strtype), ('name', strtype), ('uom.name', strtype), ('fillValue', strtype), ('dataType', strtype), ('lower', strtype), ('upper', strtype), ('closure', strtype)])
            Group_featureCode = np.array(
                [b'WaterLevel'], dtype='|S10')
            # geometryValues = np.array(self.coord, dtype={'names': ['longitude', 'latitude'], 'formats': [
            #                           '<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
            uncertainty = np.array([(b'waterLevelHeight', -1.)],
                                   dtype={'names': ['name', 'value'], 'formats': [strtype, '<f8'], 'offsets': [0, 8], 'itemsize': 64})

            axisNames = np.array([b'longitude', b'latitude '], dtype='|S9')
            # ==================================================================================
            print("创建group与数据集")
            file = h5py.File(self.path + "\\" + self.name + ".h5", "w")
            # group and dataset
            file.create_group("Group_F")
            file.create_group("WaterLevel")
            file["Group_F"].create_dataset("WaterLevel", data=Group_WaterLevel)
            file["Group_F"].create_dataset(
                "featureCode", data=Group_featureCode)
            # file["Group_F"]["WaterLevel"] = Group_WaterLevel
            # file["Group_F"]["featureCode"] = Group_featureCode
            file["WaterLevel"].create_dataset("axisNames", data=axisNames)
            waterLevel = list(set(self.data['waterlevel'].tolist()))
            waterLevel.sort()
            print(waterLevel)
            for wl_item in waterLevel:
                waterlevelName = 'WaterLevel.' + '%02d' % wl_item
                file["WaterLevel"].create_group(waterlevelName)
                a = self.data[self.data['waterlevel']
                              == wl_item][['x', 'y']].values
                seta = list(set([(item[0], item[1])for item in a]))
                print(seta)
                for i in range(len(seta)):
                    # print(i)
                    # print(seta[i])
                    groupName = "Group_" + "%03d" % (i+1)
                    file["WaterLevel"][waterlevelName].create_group(groupName)
                    timeIntervalIndex = int(self.info[(self.info["Name"] == 'timeIntervalIndex') & (
                        self.info["Rank"] == "WaterLevel/" + waterlevelName + "/" + groupName)]["Value"].tolist()[0])
                    if(timeIntervalIndex == 1):
                        aa = self.data[(self.data['waterlevel'] == wl_item) & (self.data['x'] == seta[i][0]) & (
                            self.data['y'] == seta[i][1])][['height', 'trend']].values
                        dataset = np.array([(item[0], item[1])for item in aa], dtype=[
                                           ('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4')])
                        file["WaterLevel"][waterlevelName][groupName].create_dataset(
                            "values", data=dataset)
                    else:
                        aa = self.data[(self.data['waterlevel'] == wl_item) & (self.data['x'] == seta[i][0]) & (
                            self.data['y'] == seta[i][1])][['height', 'trend', 'timepoint']].values
                        dataset = np.array([(item[0], item[1], item[2])for item in aa], dtype=[
                                           ('waterLevelHeight', '<f4'), ('waterLevelTrend', '<i4'), ('waterLevelTime', strtype)])
                        file["WaterLevel"][waterlevelName][groupName].create_dataset(
                            "values", data=dataset)

                file["WaterLevel"][waterlevelName].create_group("Positioning")

                geometryValues = np.array(seta, dtype={'names': ['longitude', 'latitude'], 'formats': [
                                          '<f8', '<f8'], 'offsets': [0, 8], 'itemsize': 64})
                file["WaterLevel"][waterlevelName]["Positioning"].create_dataset(
                    "geometryValues", data=geometryValues)
                file["WaterLevel"][waterlevelName].create_dataset(
                    'uncertainty', data=uncertainty)
            # attrs
            file.attrs.create("eastBoundLongitude",
                              eastBoundLongitude, dtype="float64")
            file.attrs.create("geographicIdentifier", geographicIdentifier, dtype=h5py.string_dtype(
                length=len(geographicIdentifier)))
            file.attrs.create("horizontalCRS", horizontalCRS, dtype="int16")
            file.attrs.create("issueDate", issueDate, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("issueTime", issueTime, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("metadata", metadata, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("northBoundLatitude",
                              northBoundLatitude, dtype="float64")
            file.attrs.create("productSpecification", productSpecification, dtype=h5py.string_dtype(
                length=len(issueDate)))
            file.attrs.create("southBoundLatitude",
                              southBoundLatitude, dtype="float64")
            file.attrs.create("verticalCS", verticalCS, dtype="int16")
            file.attrs.create("verticalCoordinateBase",
                              verticalCoordinateBase, dtype=ce.verticalCoordinateBase)
            file.attrs.create("verticalDatum", verticalDatum, dtype="int16")
            file.attrs.create("verticalDatumReference",
                              verticalDatumReference, dtype=ce.verticalDatumReference)
            file.attrs.create("waterLevelTrendThreshold",
                              waterLevelTrendThreshold, dtype="float32")

            file.attrs.create("westBoundLongitude",
                              westBoundLongitude, dtype="float64")

            commonPointRule = int(
                self.info[self.info["Name"] == 'commonPointRule']['Value'].tolist()[0])
            dataCodingFormat = int(
                self.info[self.info["Name"] == 'dataCodingFormat']['Value'].tolist()[0])
            dimension = 2
            horizontalPositionUncertainty = -1.0
            maxDatasetHeight = max(self.data["height"].values)
            minDatasetHeight = min(self.data["height"].values)
            methodWaterLevelProduct = self.info[self.info["Name"] == 'methodWaterLevelProduct']['Value'].tolist()[
                0]
            numInstances = int(
                self.info[self.info["Name"] == 'numInstances']['Value'].tolist()[0])
            pickPriorityType = self.info[self.info["Name"] == 'pickPriorityType']['Value'].tolist()[
                0]
            timeUncertainty = -1.0
            verticalUncertainty = -1.0
            file['WaterLevel'].attrs.create(
                "commonPointRule", commonPointRule, dtype=ce.commonPointRule)
            file['WaterLevel'].attrs.create(
                "dataCodingFormat", dataCodingFormat, dtype=ce.dataCodingFormat)
            file['WaterLevel'].attrs.create(
                "dimension", dimension, dtype="int16")
            file['WaterLevel'].attrs.create(
                "horizontalPositionUncertainty", horizontalPositionUncertainty, dtype="float32")
            file['WaterLevel'].attrs.create(
                "maxDatasetHeight", maxDatasetHeight, dtype="float32")
            file['WaterLevel'].attrs.create(
                "methodWaterLevelProduct", methodWaterLevelProduct, dtype=h5py.string_dtype(length=len(methodWaterLevelProduct)))
            file['WaterLevel'].attrs.create(
                "minDatasetHeight", minDatasetHeight, dtype="float32")
            file['WaterLevel'].attrs.create(
                "numInstances", numInstances, dtype="int16")
            file['WaterLevel'].attrs.create(
                "pickPriorityType", pickPriorityType, dtype=h5py.string_dtype(length=len(pickPriorityType)))
            file['WaterLevel'].attrs.create(
                "timeUncertainty", timeUncertainty, dtype="float32")
            file['WaterLevel'].attrs.create(
                "verticalUncertainty", verticalUncertainty, dtype="float32")
            for wl_item in waterLevel:
                waterlevelName = 'WaterLevel.' + '%02d' % wl_item
                rank = "WaterLevel/" + waterlevelName
                typeOfWaterLevelData = int(self.info[(self.info["Rank"] == rank) & (
                    self.info["Name"] == "typeOfWaterLevelData")]['Value'].tolist()[0])
                timepoint_str = self.data[self.data['waterlevel']
                                          == wl_item]['timepoint'].tolist()
                timepoint = [datetime.strptime(
                    item, "%Y%m%dT%H%M%SZ") for item in timepoint_str]

                dateTimeOfFirstRecord = min(
                    timepoint).strftime("%Y%m%dT%H%M%SZ")
                dateTimeOfLastRecord = max(
                    timepoint).strftime("%Y%m%dT%H%M%SZ")
                scoord = self.data[self.data['waterlevel']
                                   == wl_item][['x', 'y']].values
                print(scoord)
                seta = list(set([(item[0], item[1])for item in scoord]))

                eastBoundLongitude_secondary = max(scoord[:, 0])
                westBoundLongitude_secondary = min(scoord[:, 0])
                northBoundLatitude_secondary = max(scoord[:, 1])
                southBoundLatitude_secondary = min(scoord[:, 1])
                numGPR = numberOfStations = len(seta)

                file[rank].attrs.create("dateTimeOfFirstRecord", dateTimeOfFirstRecord,
                                        dtype=h5py.string_dtype(length=len(dateTimeOfFirstRecord)))
                file[rank].attrs.create("dateTimeOfLastRecord", dateTimeOfLastRecord, dtype=h5py.string_dtype(
                    length=len(dateTimeOfLastRecord)))
                file[rank].attrs.create(
                    "eastBoundLongitude", eastBoundLongitude_secondary, dtype="float64")
                file[rank].attrs.create(
                    "northBoundLatitude", northBoundLatitude_secondary, dtype="float64")
                file[rank].attrs.create("numGPR", numGPR, dtype="int16")
                file[rank].attrs.create(
                    "numberOfStations", numberOfStations, dtype="int16")
                file[rank].attrs.create(
                    "southBoundLatitude", southBoundLatitude_secondary, dtype="float64")
                file[rank].attrs.create(
                    "typeOfWaterLevelData", typeOfWaterLevelData, dtype=ce.typeOfWaterLevelData)
                file[rank].attrs.create(
                    "westBoundLongitude", westBoundLongitude_secondary, dtype="float64")
                for i in range(len(seta)):
                    groupName = "Group_" + "%03d" % (i+1)
                    rank_s = rank + "/" + groupName
                    timepoint_group = self.data[(self.data['waterlevel'] == wl_item) & (
                        self.data['x'] == seta[i][0]) & (self.data['y'] == seta[i][1])]['timepoint'].tolist()
                    timepoint_grouplist = [datetime.strptime(
                        item, "%Y%m%dT%H%M%SZ") for item in timepoint_group]
                    endDateTime = max(timepoint_grouplist).strftime(
                        "%Y%m%dT%H%M%SZ")
                    numberOfTime = len(timepoint_grouplist)
                    startDateTime = min(timepoint_grouplist).strftime(
                        "%Y%m%dT%H%M%SZ")
                    stationIdentification = int(self.info[(self.info["Name"] == 'stationIdentification') & (
                        self.info["Rank"] == rank_s)]["Value"].tolist()[0])
                    stationName = self.info[(self.info["Name"] == 'stationName') & (
                        self.info["Rank"] == rank_s)]["Value"].tolist()[0]
                    timeIntervalIndex = int(self.info[(self.info["Name"] == 'timeIntervalIndex') & (
                        self.info["Rank"] == rank_s)]["Value"].tolist()[0])
                    file[rank_s].attrs.create(
                        "endDateTime", endDateTime, dtype=h5py.string_dtype(length=len(endDateTime)))
                    file[rank_s].attrs.create(
                        "numberOfTime", numberOfTime, dtype="int16")
                    file[rank_s].attrs.create(
                        "startDateTime", startDateTime, dtype=h5py.string_dtype(length=len(startDateTime)))
                    file[rank_s].attrs.create(
                        "stationIdentification", stationIdentification, dtype="int32")
                    file[rank_s].attrs.create(
                        "stationName", stationName, dtype=h5py.string_dtype(length=len(stationName)))
                    file[rank_s].attrs.create(
                        "timeIntervalIndex", timeIntervalIndex, dtype="int32")
                    if timeIntervalIndex == 1:
                        timeRecordInterval = int(self.info[(self.info["Name"] == 'timeRecordInterval') & (
                            self.info["Rank"] == rank_s)]["Value"].tolist()[0])
                        file[rank_s].attrs.create(
                            "timeRecordInterval", timeRecordInterval, dtype="int16")
            print("完成")
        except Exception as e:
            print(e)
            traceback.print_exc()
        # print("完成")


if __name__ == "__main__":
    toChart = tooChartS104(
        "this", r"C:\\Users\\zjm\\.spyder-py3\\mdata\\data\\", 1, None, None)
    toChart.toChart()
