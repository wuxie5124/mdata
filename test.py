# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:50:39 2023

@author: zjm
"""

# 测试能否调用自己的库
# 感觉不能  no 可以

# 枚举类能否写入h5py

import toShpPoint as sp
from enum import Enum
import sys


class Week(Enum):
    Monday = 0,
    Tuesday = 1,
    wednesday = 2,
    Thursday = 3,
    Friday = 4,


if __name__ == "__main__":
    list_str = []
    list_float = []
    # print(sys.argv[0])
    for i in range(1, len(sys.argv)):
        # print(sys.argv[i])
        list_str.append(sys.argv[i].replace(",", ""))
    list_str[0] = list_str[0].replace("[", "")
    list_str[len(sys.argv) - 2] = list_str[len(sys.argv) - 2].replace("]", "")
    strr = ",".join(list_str)
    list_str = strr.split('][')
    xs = list_str[0].split(",")
    ys = list_str[1].split(",")
    heights = list_str[2].split(",")
    trends = list_str[3].split(",")
    identifiers = list_str[4].split(",")
    timePoints = list_str[5].split(",")
    waterLevel = list_str[6].split(",")
    for item in waterLevel:
        print(item)
    # for item in list_str:
    #     print(item)
    # a = []
    # for i in range(1, len(sys.argv)):
    #     a.append(sys.argv[i])
    # for item in a:
    #     print(item)

    # for day in Week:
    #     print(day)

    # print("No Problem")
