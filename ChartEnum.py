# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:40:48 2023

@author: zjm
"""

import h5py
import numpy as np
import pandas as pd


verticalCoordinateBase = h5py.enum_dtype(
    {"seaSurface": 1, "verticalDatum": 2, "seaBottom": 3}, basetype='int8')
verticalDatumReference = h5py.enum_dtype(
    {"s100VerticalDatum": 1, "EPSG": 2}, basetype='int8')
dataCodingFormat = h5py.enum_dtype(
    {"fexedStations": 1, "regularGrid": 2, "ungeorectifiedGrid": 3,
     "movingPlatform": 4, "irregularedGrid": 5, "variablesCellSize": 6,
     "TIN": 7, "stationwiseFixed": 8}, basetype='int8')
commonPointRule = h5py.enum_dtype(
    {"average": 1, "low": 2, "high": 3, "all": 4}, basetype='int8')
typeOfWaterLevelData = h5py.enum_dtype(
    {"observation": 1, "astronomicalPrediction": 2, "analysisOrHybrid": 3, "hydrodynomicalHindcast": 4, "hydrodynomicalForecast": 5, "observedMinusPredicted": 6, "observedMinusAnalysis": 7, "observedMinusHindcaset": 8, "observedMinusForecast": 9, "forecastMinusPredicted": 10}, basetype='int8')
interplationType = h5py.enum_dtype({"nearestneighbor": 1, "linear": 2, "quadratic": 3, "cubic": 4,
                                   "bilinear": 5, "biquadratic": 6, "bicubic": 7, "lostarea": 8, "barycentric": 9, "discrete": 10})
sequencingRuleType = h5py.enum_dtype({"linear":1,"boustrophedonic":2,"CantorDiagonal":3,"spiral":4,"Morton":5,"Hilbert":6})