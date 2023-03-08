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

if __name__ =="__main__":
    # a = []
    # for i in range(1, len(sys.argv)):
    #     a.append(sys.argv[i])     
    # filePath = a[0]
    
    filePath = r"D:\\work\\wrfout_d01_2021-11-08_00_00_00"
    file = nc.Dataset(filePath,'r')
    Params = list(file.variables.keys())
    for Param in Params:
        dim = list(file[Param].dimensions)
        if ("west_east" in dim or  "west_east_stag" in dim) and ()
        
    
    
    
    
    