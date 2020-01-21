# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:48:01 2018

@author: anind
"""
from spi import SPI
import numpy as np
import os, random
from PIL import Image
import time
import gdal
import osr
from math import isnan



spi = SPI()
    
spi.set_rolling_window_params(
    span=1, window_type=None, center=True)

    # Set distribution parameters
spi.set_distribution_params(dist_type='gam')


def use_spi(arr: np.array) -> np.array:

    
    data = spi.calculate(arr, starting_month=1)
    data = data.flatten()    
    #Calculate and return 1d array
    return data

def tiffolder_to_3darr(directory_name) -> np.array:
    '''Returns a 3d array from a directory containing tiff images of
       equal shape.
       For ex: if each image is of shape (460,640) and there are 200 images,
       the returned array will have shape (460,640,200)
     '''
    start = time.time()
    sizeget = ''
    while sizeget[-3:] != 'tif':
         
        sizeget = random.choice(os.listdir(directory_name))
    location = directory_name + "\\" + sizeget
    im = Image.open(location)
    arr = np.array(im)
    
    y = np.size(arr,1)
    x = np.size(arr,0)
    #getting size of an image (it should match the other images)
    mainarr = np.zeros((x,y,0))
    for file in os.listdir(directory_name):
        #appending arrays of tif file to 3darray
        if file[-3:] == 'tif':
            location = directory_name + "\\" + file
            im = Image.open(location)
            arr = np.array(im)              
            mainarr = np.dstack((mainarr,arr))
            print('added')
    end = time.time()
    print(end - start)
    return mainarr 

def gettypefilelist(directory_name, filetype) -> list:
    lis = []
    for file in os.listdir(directory_name):
        if file.endswith(filetype):
            lis.append(file)
    return lis

def spi3d(arr: np.array) -> np.array:
#    newarr = arr
    st = time.time()
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            
            cell = arr[x][y]
            lis = []
            
            mlist = []
            for z in range(len(cell)):
                if cell[z] > -0.00000000000000001:
                   #print(cell[z]) 
                   mlist.append(cell[z])
                   
                   lis.append(z)
                else:
                    arr[x][y][z] = np.nan
#                   
#            lis = [i for i in range(len(arr[x][y])) if arr[x][y][i] >= 0.00000000001]
#            mlist = [i for i in arr[x][y] if i >= 0.00000000001]
            
            
            modc = np.array(mlist)
            try:
                modc = use_spi(modc)            
    
                for k in range(len(modc)):
                    pos = lis[k]
                    arr[x][y][pos] = modc[k]
                now = time.time()
                print(str(x)+' , '+str(y) + ' : ' + str(now-st))
            except:
                arr[x][y][:] = np.nan
                now = time.time()
                print(str(x)+' , '+str(y) + ' : ' + str(now-st)+"  nan")
                    
                
#            newarr [x][y] = cell 
    en = time.time()
    print(en-st)
    
    arr = np.swapaxes(arr,2,0)
    arr = np.swapaxes(arr,1,2)
            
    return arr


def output(loc: str, arr: np.array, l: list, store: str):
    '''loc : location of rainfall files
       arr: 3d array containing spi values
       l: list containing names of files in the same order
       store: store location of spi files
    '''
    sizeget = l[0]
    
    sample = loc + '\\' + sizeget
    
    inDs = gdal.Open(sample)
    
    band = inDs.GetRasterBand(1)
    NDV = band.GetNoDataValue()
    
    wkt = inDs.GetProjection()
        
        # setting spatial reference of output raster 
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    
    gt = inDs.GetGeoTransform()
    
    inDs = None
    
    [rows,cols] = arr[0].shape
    
    driver = gdal.GetDriverByName("GTiff")
    
    
    
    for i in range(len(arr)):
        raster = np.zeros((rows,cols), dtype=np.float32)
        a = arr[i]
        raster = raster + a
        storeloc = store + '\\' + l[i]
        dst_ds = driver.Create(storeloc, 
                           cols, 
                           rows, 
                           1, 
                           gdal.GDT_Float32)
        

        dst_ds.SetProjection( srs.ExportToWkt() )
        
                  
        dst_ds.SetGeoTransform(gt)
        
        dst_ds.GetRasterBand(1).SetNoDataValue(NDV)
        
        
        
        
        dst_ds.GetRasterBand(1).WriteArray(raster)
        
        #dst_ds.GetRasterBand(1).WriteArray( narr ) 
        
        dst_ds.FlushCache()
        dst_ds = None
        
        print(l[i])
        
        
    



