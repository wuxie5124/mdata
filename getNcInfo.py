# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 16:05:47 2023

//获取nc数据的信息，以传递回JAVA，包括params，time ，level 

@author: zjm
"""

import os
import numpy as np
import netCDF4 as nc
import sys

if __name__ == "__main__":
    a = []
    for i in range(1, len(sys.argv)):
        a.append(sys.argv[i])
    filePath = a[0]
    # filePath = r"D:\\work\\wrfout_d01_2021-11-08_00_00_00.nc"
    file = nc.Dataset(filePath, 'r')
    Params = list(file.variables.keys())
    for Param in Params:
        dim = list(file[Param].dimensions)
        # print(Param)
        if ("west_east" in dim or "west_east_stag" in dim) and ("south_north" in dim or "south_north_stag" in dim):
            time = "0"
            level = "0"
            soil = "0"
            ftp = "0"
            if("Time" in dim):
                time = str(file.dimensions["Time"].size)
            if("bottom_top_stag" in dim):
                level = str(file.dimensions["bottom_top_stag"].size)
            if("bottom_top" in dim):
                level = str(file.dimensions["bottom_top"].size)
            # if("soil_layers_stag" in dim):
            #     soil = str(file.dimensions["soil_layers_stag"].size)
            # if("pft_fraction_stag" in dim):
            #     ftp = str(file.dimensions["pft_fraction_stag"].size)
            # print(Param + "#" + time + "#" + level + "#" + soil + "#" + ftp)
            print(Param + "#" + time + "#" + level)
