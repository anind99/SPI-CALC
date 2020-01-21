# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:06:00 2018

@author: anind
"""
import numpy as np

def addtwoarrays (ar1: np.array()) -> list:
    rval = []
    for i in range(len(ar1)):
        for j in range(ar1[i]):
            rval.append(ar1[i][j][0])
    return rval
    