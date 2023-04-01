# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 00:26:02 2023

@author: zjm
"""

import os
import numpy as np
import h5py
import sys

if __name__ == "__main__":
    a = []
    for i in range(1, len(sys.argv)):
        a.append(sys.argv[i])
    filePath = a[0]
    # filePath = r"D:\\qq文件\\1127434146\\FileRecv\\S104\\S104\\104US00_ches_dcf1_20190703T00Z.h5"
    file = h5py.File(filePath, "r")
    print(file['WaterLevel'].attrs["dataCodingFormat"])
    
    
    