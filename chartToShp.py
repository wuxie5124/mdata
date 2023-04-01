# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:06:54 2023

@author: zjm
"""

# 导入S104所有数据为数据集

import os
import numpy as np
import h5py
import toShpPoint as sp
import pandas as pd
from osgeo import gdal, ogr
from osgeo import gdalconst
import sys
from datetime import datetime, timedelta


class ChartTo():
    def __init__(self, filePath, dcf, datasource, expdir):
        self.filePath = filePath
        self.dcf = dcf
        self.datasource = datasource
        self.expdir = expdir
        # self.namepro = filePath.split('\\')[-1].split(".")[0][13:]

    def toshp(self):
        if dcf == 1:
            self.dcf1toshp()
        # elif dcf == 2 :
        #     dcf2toshp(self)
        elif dcf == 8:
            self.dcf8toshp()

    def dcf1toshp(self):
        file = h5py.File(self.filePath, "r")

        dataInfo = []
        geographicIdentifier = file.attrs["geographicIdentifier"]
        issueDate = file.attrs["issueDate"]
        issueTime = file.attrs["issueTime"]
        metadata = file.attrs["metadata"]
        verticalCS = file.attrs["verticalCS"]
        verticalCoordinateBase = file.attrs['verticalCoordinateBase']
        verticalDatumReference = file.attrs["verticalDatumReference"]
        waterLevelTrendThreshold = file.attrs['waterLevelTrendThreshold']

        commonPointRule = file['WaterLevel'].attrs["commonPointRule"]
        dataCodingFormat = file['WaterLevel'].attrs["dataCodingFormat"]
        methodWaterLevelProduct = file['WaterLevel'].attrs["methodWaterLevelProduct"]
        numInstances = file['WaterLevel'].attrs["numInstances"]
        dataInfo.append(['geographicIdentifier', "/", geographicIdentifier])
        dataInfo.append(['issueDate', "/", issueDate])
        dataInfo.append(['issueTime', "/", issueTime])
        dataInfo.append(['metadata', "/", metadata])
        dataInfo.append(["verticalCS", "/", verticalCS])
        dataInfo.append(["verticalCoordinateBase",
                        "/", verticalCoordinateBase])
        dataInfo.append(['verticalDatumReference',
                        "/", verticalDatumReference])
        dataInfo.append(["waterLevelTrendThreshold",
                        "/", waterLevelTrendThreshold])

        dataInfo.append(['commonPointRule', "WaterLevel", commonPointRule])
        dataInfo.append(['dataCodingFormat', "WaterLevel", dataCodingFormat])
        dataInfo.append(['methodWaterLevelProduct',
                        "WaterLevel", methodWaterLevelProduct])
        dataInfo.append(['numInstances', "WaterLevel", numInstances])

        # typeOfWaterLevelData = file['WaterLevel']['WaterLevel.01'].attrs["typeOfWaterLevelData"]
        waterlevel0List = list(file["WaterLevel"])
        waterlevel0List.remove('axisNames')
        # 名称为首个waterlevel的starttime 拼凑
        self.namepro = "S104_dcf1_"+ str(file['WaterLevel'][waterlevel0List[0]].attrs['dateTimeOfFirstRecord'],encoding="utf-8")
        for waterLevel0 in waterlevel0List:
            typeOfWaterLevelData = file['WaterLevel'][waterLevel0].attrs["typeOfWaterLevelData"]
            dataInfo.append(
                ["typeOfWaterLevelData", "WaterLevel/" + waterLevel0, typeOfWaterLevelData])
            groupList = list(file['WaterLevel'][waterLevel0])
            coord = file["WaterLevel"][waterLevel0]['Positioning']["geometryValues"][:]
            groupList.remove('Positioning')
            groupList.remove('uncertainty')
            # coordnp = np.array([[item[0], item[1]]for item in coord])
            # lons = coordnp[:, 0]
            # lats = coordnp[:, 1]
            lonall = []
            latall = []
            value_all = []
            fieldsName = ["Height", "Trend", "identifier", "timePoint"]
            for group in groupList:
                value = file["WaterLevel"][waterLevel0][group]["values"][:]
                # shpPath = self.expdir + waterLevel0 + "_" + group + "_value" + ".shp"
                timePoint = file["WaterLevel"][waterLevel0][group].attrs['timePoint']
                for i in range(len(value)):
                    value_all.append((value[i][0], value[i][1], str(
                        geographicIdentifier, encoding='utf-8'), str(timePoint, encoding='utf-8')))
                # value_2 = [(item[0], item[1], str(geographicIdentifier, encoding='utf-8'),
                #             str(timePoint, encoding='utf-8'))for item in value]
                for i in range(len(coord)):
                    lonall.append(coord[i][0])
                    latall.append(coord[i][1])
            shpPath = self.expdir + self.namepro + "_" + \
                waterLevel0.split('.')[-1] + "_value" + ".shp"
            ToPoint = sp.tooPoint(
                value_all, shpPath, waterLevel0, fieldsName, np.array(lonall), np.array(latall))
            print(shpPath + "#" + self.datasource + "#" + "0")
            ToPoint.toPoint()
            """存属性表"""
            dataInfonp = np.array(dataInfo)
            dataInfoDf = pd.DataFrame(
                dataInfonp, columns=['Name', "Rank", "Value"])
            xlsxPath = self.expdir + \
                self.namepro + ".xlsx"
            write = pd.ExcelWriter(xlsxPath)
            dataInfoDf.to_excel(write, sheet_name="Sheet1", index=False)
            write.close()
            print(xlsxPath + "#" + self.datasource + "#" + "1")

    def dcf8toshp(self):

        file = h5py.File(self.filePath, "r")
        dataInfo = []
        geographicIdentifier = file.attrs["geographicIdentifier"]
        issueDate = file.attrs["issueDate"]
        issueTime = file.attrs["issueTime"]
        metadata = file.attrs["metadata"]
        verticalCS = file.attrs["verticalCS"]
        verticalCoordinateBase = file.attrs['verticalCoordinateBase']
        verticalDatumReference = file.attrs["verticalDatumReference"]
        waterLevelTrendThreshold = file.attrs['waterLevelTrendThreshold']

        commonPointRule = file['WaterLevel'].attrs["commonPointRule"]
        dataCodingFormat = file['WaterLevel'].attrs["dataCodingFormat"]
        methodWaterLevelProduct = file['WaterLevel'].attrs["methodWaterLevelProduct"]
        numInstances = file['WaterLevel'].attrs["numInstances"]
        pickPriorityType = file['WaterLevel'].attrs['pickPriorityType']
        dataInfo.append(['geographicIdentifier', "/", geographicIdentifier])
        dataInfo.append(['issueDate', "/", issueDate])
        dataInfo.append(['issueTime', "/", issueTime])
        dataInfo.append(['metadata', "/", metadata])
        dataInfo.append(["verticalCS", "/", verticalCS])
        dataInfo.append(["verticalCoordinateBase",
                        "/", verticalCoordinateBase])
        dataInfo.append(['verticalDatumReference',
                        "/", verticalDatumReference])
        dataInfo.append(["waterLevelTrendThreshold",
                        "/", waterLevelTrendThreshold])

        dataInfo.append(['commonPointRule', "WaterLevel", commonPointRule])
        dataInfo.append(['dataCodingFormat', "WaterLevel", dataCodingFormat])
        dataInfo.append(['methodWaterLevelProduct',
                        "WaterLevel", methodWaterLevelProduct])
        dataInfo.append(['numInstances', "WaterLevel", numInstances])
        dataInfo.append(["pickPriorityType", 'WaterLevel', pickPriorityType])

        waterlevel0List = list(file["WaterLevel"])
        waterlevel0List.remove('axisNames')
        fieldsName = ["Height", "Trend", "identifier", "timePoint"]
        self.namepro = "S104_dcf8_"+ str(file['WaterLevel'][waterlevel0List[0]].attrs['dateTimeOfFirstRecord'],encoding="utf-8")
        for waterLevel0 in waterlevel0List:
            typeOfWaterLevelData = file['WaterLevel'][waterLevel0].attrs["typeOfWaterLevelData"]
            dataInfo.append(
                ["typeOfWaterLevelData", "WaterLevel/" + waterLevel0, typeOfWaterLevelData])
            groupList = list(file['WaterLevel'][waterLevel0])
            coord = file["WaterLevel"][waterLevel0]['Positioning']["geometryValues"][:]
            groupList.remove('Positioning')
            groupList.remove('uncertainty')
            coord = file["WaterLevel"][waterLevel0]['Positioning']["geometryValues"][:]
            for i in range(len(groupList)):
                group = groupList[i]
                endDateTime = file["WaterLevel"][waterLevel0][group].attrs["endDateTime"]
                numberOfTime = file["WaterLevel"][waterLevel0][group].attrs["numberOfTimes"]
                startDateTime = file["WaterLevel"][waterLevel0][group].attrs["startDateTime"]
                stationIdentification = file["WaterLevel"][waterLevel0][group].attrs["stationIdentification"]
                stationName = file["WaterLevel"][waterLevel0][group].attrs["stationName"]
                timeIntervalIndex = file["WaterLevel"][waterLevel0][group].attrs["timeIntervalIndex"]
                dataInfo.append(
                    ["endDateTime", "WaterLevel/" + waterLevel0 + "/" + group, endDateTime])
                dataInfo.append(
                    ["numberOfTime", "WaterLevel/" + waterLevel0 + "/" + group, numberOfTime])
                dataInfo.append(
                    ["startDateTime", "WaterLevel/" + waterLevel0 + "/" + group, startDateTime])
                dataInfo.append(["stationIdentification", "WaterLevel/" +
                                waterLevel0 + "/" + group, stationIdentification])
                dataInfo.append(
                    ["stationName", "WaterLevel/" + waterLevel0 + "/" + group, stationName])
                dataInfo.append(["timeIntervalIndex", "WaterLevel/" +
                                waterLevel0 + "/" + group, timeIntervalIndex])
                if timeIntervalIndex == 1:
                    timeRecordInterval = file["WaterLevel"][waterLevel0][group].attrs["timeRecordInterval"]
                    dataInfo.append(
                        ["timeRecordInterval", "WaterLevel/" + waterLevel0 + "/" + group, timeRecordInterval])
                    startime = datetime.strptime(
                        str(startDateTime, encoding='utf-8'), "%Y%m%dT%H%M%SZ")
                    endtime = datetime.strptime(
                        str(endDateTime, encoding='utf-8'), "%Y%m%dT%H%M%SZ")
                    value_all = []
                    timeall = []
                    lonall = []
                    latall = []
                    for j in range(numberOfTime):
                        currentTime = startime + j * \
                            timedelta(seconds=int(timeRecordInterval))
                        "字符串形式时间"
                        currentDataTime = currentTime.strftime(
                            "%Y%m%dT%H%M%SZ")
                        timeall.append(currentDataTime)
                    value = file["WaterLevel"][waterLevel0][group]["values"][:]
                    for j in range(len(value)):
                        value_all.append((value[j][0], value[j][1], str(
                            geographicIdentifier, encoding='utf-8'), timeall[j]))
                elif timeIntervalIndex == 0:
                    lonall = []
                    latall = []
                    value = file["WaterLevel"][waterLevel0][group]["values"][:]
                    value_all = [(item[0], item[1], str(geographicIdentifier, encoding='utf-8'),
                                  str(item[2], encoding='utf-8'))for item in value]

                for j in range(len(value)):
                    lonall.append(coord[i][0])
                    latall.append(coord[i][1])

                shpPath = self.expdir + self.namepro + \
                    "_" + waterLevel0.split('.')[-1] + \
                    "_" + group + "_value" + ".shp"
                ToPoint = sp.tooPoint(
                    value_all, shpPath, waterLevel0, fieldsName, np.array(lonall), np.array(latall))
                print(shpPath + "#" + self.datasource + "#" + "0")
                ToPoint.toPoint()
        """存属性表"""
        dataInfonp = np.array(dataInfo)
        dataInfoDf = pd.DataFrame(
            dataInfonp, columns=['Name', "Rank", "Value"])
        xlsxPath = self.expdir + \
            self.namepro + ".xlsx"
        write = pd.ExcelWriter(xlsxPath)
        dataInfoDf.to_excel(write, sheet_name="Sheet1", index=False)
        write.close()
        print(xlsxPath + "#" + self.datasource + "#" + "1")


if __name__ == "__main__":
    # filePath = "D:\\DATA\\海图\\S104\\104US00_ches_dcf8_20190703T00Z.h5"
    # dcf = 8
    # datasource = "mydatasource"
    # exportfiledir = "D:\\DATA\\海图\\shpAndExcel\\"
    a = []
    for i in range(1, len(sys.argv)):
        a.append(sys.argv[i])
    filePath_str = a[0]
    dcf_str = a[1]
    datasource_str = a[2]
    exportfiledir = a[3]

    filePaths = filePath_str.split("#")[1:]
    dcfs = dcf_str.split("#")[1:]
    datasources = datasource_str.split("#")[1:]
    for i in range(len(filePaths)):
        filePath = filePaths[i]
        dcf = int(dcfs[i])
        datasource = datasources[i]
        CT = ChartTo(filePath, dcf, datasource, exportfiledir)
        CT.toshp()
