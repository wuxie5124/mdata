# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 10:51:03 2023

@author: Administrator
"""
import h5py
import pandas as pd
import numpy as np
import sys

catalogue = []
datasets = []

def GetS102Attribution(file):
    # file = h5py.File(filePath,"r")
    file.visit(prt)
    # file.close()

def prt(name):
    catalogue.append(name)
    # print(name)
    
def OutPutDataSetName(file):

    for item in catalogue:
        if isinstance(file[item],h5py._hl.dataset.Dataset):
            datasets.append(item)
            print(item)
      

if __name__ == '__main__':
    # a = []
    
    # for i in range(1, len(sys.argv)):
    #     a.append(sys.argv[i])
        
    # filePath = a[0]
    "104US00_ches_dcf1_20190703T00Z.h5"
    "104US00_ches_dcf2_20190606T12Z.h5"
    "104US00_ches_dcf3_20190606T12Z.h5"
    "104US00_ches_dcf7_20190606T12Z.h5"
    "104US00_ches_dcf8_20190703T00Z.h5"
        
    filePath = "D:\\qq文件\\1127434146\\FileRecv\\S104\\S104\\104US00_ches_dcf8_20190703T00Z.h5"
    
    file = h5py.File(filePath,"r")
    
    GetS102Attribution(file)
    OutPutDataSetName(file)
    
            
