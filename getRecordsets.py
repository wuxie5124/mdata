# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:11:54 2023

@author: zjm

dcf8的一个数据集就是一个group || 但是仍然得把所有数据集内容传入，不要重复修改h5(不清楚可行性) -> 
所以至少还得传入一个参数waterlevel0x(group则是可以通过坐标进行区分) -> 
检索waterlevel0x -- 检索坐标

dcf1的一个数据集则是一个waterlevel0x下的所有group

检索waterlevel0x 检索时间

"""

import sys
import pandas as pd
import numpy as np
import toHDF5

"===================="
"""弃用，对于名称不同数据不适用，同样的属性信息中的空格与，都得替换处理暂定为 # -> (' ') 和 & -> (',')  """
# if len(identifiers) != len(heights):
#     "倍数 time"
#     time = int(len(identifiers)/len(heights))
#     new_identifiers = []
#     for index in range(0,len(identifiers),time):
#         new_identifier = ""
#         for i in range(time):
#             new_identifier += identifiers[index + i] + " "
#         new_identifier = new_identifier[:-1]
#         new_identifiers.append(new_identifier)
#     identifiers = new_identifiers
# for item in identifiers:
#     print(item)
"==============="


if __name__ == "__main__":
    list_str = []
    for i in range(1, len(sys.argv)):
        # print(sys.argv[i])
        list_str.append(sys.argv[i].replace(",", ""))
    # list_str[0] = list_str[0].replace("[", "")
    # list_str[len(sys.argv) - 2] = list_str[len(sys.argv) - 2].replace("]", "")
    strr = ",".join(list_str)
    # print(strr)
    # 每个数组分开
    list_str = strr.split('][')
    list_str[0] = list_str[0].replace("[", "")
    list_str[len(list_str)-1] = list_str[len(list_str)-1].replace("]", "")
    xs = list(map(float, list_str[0].split(",")))
    ys = list(map(float, list_str[1].split(",")))
    heights = list(map(float, list_str[2].split(",")))
    trends = list(map(int, list_str[3].split(",")))
    identifiers = list_str[4].split(",")
    # print("1")
    identifiers = [item.replace('#', ' ')for item in identifiers]
    timePoints = list_str[5].split(",")
    waterlevel = list(map(int, list_str[6].split(",")))
    attrName = list_str[7].split(",")
    attrRank = list_str[8].split(",")
    attrValue = list_str[9].split(",")
    attrValue = [item.replace("#", " ").replace("&", ",")for item in attrValue]
    dcf = int(list_str[10])
    fileName = list_str[11]
    filePath = list_str[12]
    # xs = [1.1, 1.2, 1.1, 1.2]
    # ys = [2.1, 2.2, 2.1, 2.2]
    # heights = [3.5, 3.6, 3.5, 3.6]
    # trends = [2, 4, 2, 4]
    # identifiers = ['Chendu', 'Chongqing', 'Chendu', 'Chongqing']
    # timePoints = ['20190703T100000Z', '20190703T140000Z',
    #               '20190703T100000Z', '20190703T140000Z']
    # waterlevel = [1, 1, 2, 2]
    # attrName = ["geographicIdentifier","commonPointRule","typeOfWaterLevelData","endDateTime"]
    # attrRank = ["/","WaterLevel","WaterLevel/WaterLevel.01","WaterLevel/WaterLevel.01/Group_001"]
    # attrValue=["Chesapeake Bay","4","2","20190704T000000Z"]

    recordset = [(xs[index], ys[index], heights[index], trends[index],
                  identifiers[index], timePoints[index], waterlevel[index])for index in range(len(timePoints))]
    #
    coords = [(xs[index], ys[index])for index in range(len(xs))]
    coordsset = set(coords)
    recordset_df = pd.DataFrame(
        recordset, columns=['x', 'y', 'height', 'trend', 'identifier', 'timepoint', 'waterlevel'])
    waterlevelset = set(waterlevel)
    for waterle in waterlevelset:
        wrecordset = recordset_df[recordset_df['waterlevel'] == waterle]
        for co in coordsset:
            grouprecords = wrecordset[(wrecordset['x'] == co[0]) & (
                wrecordset['y'] == co[1])]
    tabular = [(attrName[index], attrRank[index], attrValue[index])
               for index in range(len(attrName))]
    tabular_df = pd.DataFrame(tabular, columns=["Name", "Rank", "Value"])
    too104 = toHDF5.tooChartS104(fileName, filePath, dcf, tabular_df, None, None, recordset_df)
    too104.toChart()
