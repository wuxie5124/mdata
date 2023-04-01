# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:51:45 2023

@author: zjm
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import toHDF5

if __name__ == "__main__":

    # data = pd.read_excel(
    #     r"D:\qq文件\1309756024\FileRecv\潮-20220125_20220127\潮-20220125_20220127分表.xlsx", sheet_name='Sheet3', index_col=1)
    # startDateTime = data.keys()[0]
    # data = data.drop(data.keys()[0], axis=1)
    # thistimedelta = timedelta(minutes=5)
    # datav = data.values
    # value = datav.reshape(1, -1)[0]
    # # for i in range(len(value)):
    #     currentDateTime = startDateTime + thistimedelta*i

    value = np.zeros([5, 8, 4])+25
    startDateTime = datetime(2023, 1, 1)
    thistimedelta = timedelta(hours=5)
    name = "excelToChats104dcf2_0127"
    path = "C:\\Users\\zjm\\.spyder-py3\\mdata\\data\\"
    dcftype = 2
    timelist = [startDateTime + i*thistimedelta for i in range(len(value))]
    # coordinate = np.array([[107.25, 23.41]])
    lon = np.arange(107.2, 107.24, 0.01)
    lat = np.arange(23.1, 23.18, 0.01)
    coordinate = np.zeros([8, 4, 2])
    for i in range(len(lat)):
        for j in range(len(lon)):
            coordinate[i][j][0] = lon[j]
            coordinate[i][j][1] = lat[i]    
    tc104 = toHDF5.tooChartS104(
        name, path, dcftype, None, timelist, coordinate, value)
    tc104.toChart()
