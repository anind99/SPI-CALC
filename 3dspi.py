# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:07:32 2018

@author: anind
"""
import numpy as np


def spi3d(np.array) -> np.array:
    newarr = arr
    for x in range(len(newarr)):
        for y in range(len(newarr[x])):
            
            cell = newarr[x][y]
            modc = np.array([])
            for z in range(len(cell)):
                if cell[z] >= 0:
                   modc = np.append(modc,cell[z])
            
#            modc = use_spi(modc)
             modc = modc * 2
            
                           
            m = 0
            n = 0
            
            while m < len(cell) and n < len(modc):
                
                if cell[m] >= 0:
                    
                    cell[m] = modc[n]
                    n += 1
                m += 1
                
            newarr [x][y] = cell
            
    return newarr
    







