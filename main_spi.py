# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:04:44 2018

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



directory_name = "C:\\Users\\anind\\SpiCalc\\data"
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

filetype = 'tif'
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
            if (cell[0] < 0) or (cell[0] == np.nan) or (not isinstance(cell[0],float)):
                arr[x][y] == np.nan
                now = time.time()
                print(str(x)+' , '+str(y) + ' : ' + str(now-st) + '  nan')
            else:
                try:
                
                
                    cell = use_spi(cell)
                    arr[x][y] = cell
                    now = time.time()
                    print(str(x)+' , '+str(y) + ' : ' + str(now-st))
                except:
                    arr[x][y][:] = np.nan
                    now = time.time()
                    print(str(x)+' , '+str(y) + ' : ' + str(now-st)+"  nan")
                    
            
#            cell = arr[x][y]
#            lis = []
#            
#            mlist = []
#            for z in range(len(cell)):
#                if cell[z] > -0.00000000000000001:
#                   #print(cell[z]) 
#                   mlist.append(cell[z])
#                   
#                   lis.append(z)
#                else:
#                    arr[x][y][z] = np.nan
##                   
##            lis = [i for i in range(len(arr[x][y])) if arr[x][y][i] >= 0.00000000001]
##            mlist = [i for i in arr[x][y] if i >= 0.00000000001]
#            
#            
#            modc = np.array(mlist)
#            try:
#                modc = use_spi(modc)            
#    
#                for k in range(len(modc)):
#                    pos = lis[k]
#                    arr[x][y][pos] = modc[k]
#                now = time.time()
#                print(str(x)+' , '+str(y) + ' : ' + str(now-st))
#            except:
#                arr[x][y][:] = np.nan
#                now = time.time()
#                print(str(x)+' , '+str(y) + ' : ' + str(now-st)+"  nan")
            
                    
                
#            newarr [x][y] = cell 
    en = time.time()
    print(en-st)
    arr = np.swapaxes(arr,2,0)
    arr = np.swapaxes(arr,1,2)
            
    return arr


def tiffolder_spi(inputfolder,outputfolder):
    
    arr = tiffolder_to_3darr(inputfolder)
    arr = spi3d(arr)
    
    arr = np.swapaxes(arr,2,0)
    arr = np.swapaxes(arr,1,2)
    
    names = gettypefilelist(inputfolder)
    
    
    outdir = outputfolder
    
    for i in range(len(arr)):
        location = outdir + "\\" + names[i]
        im = Image.fromarray(arr[i])
        im.save(location)

def gtfifarr(loc, topleftN, topleftE, BottomrightN, BottomrightE, store):
    
    l = sorted(os.listdir(loc))
    
    new_l = [a for a in l if a[-4:] == '.tif']
    
    total = []
    
    month = []
    
    start = new_l[0][:6]
    
    for i in range(len(new_l)):
        if new_l[i][:6] == start:
            month.append(new_l[i])
        else:
            total.append(month)
            month = []
            start = new_l[i][:6]
            month.append(new_l[i])
    total = sorted(total)
    
    sizeget = new_l[0]
    
    sample = loc + '\\' + sizeget
    
    inDs = gdal.Open(sample)
    
    band = inDs.GetRasterBand(1)
    NDV = band.GetNoDataValue()
    arr = band.ReadAsArray()
    
    gt = inDs.GetGeoTransform()
#    minx = gt[0]
#    newx = 0
#    maxy = gt[3]
#    newy = 0
#    
#    while not minx >= topleftE:
#        minx += gt[1] # W=E pixel resolution
#        newx += 1
#    
#    while not maxy <= topleftN:
#        maxy += gt[5]
#        newy += 1
#        
#    minx = minx - gt[1]
#    newx = newx - 1
#    maxy = maxy - gt[5]
#    newy = newy - 1
#    
#    maxx = minx
#    miny = maxy
#    newx2 = newx
#    newy2 = newy
#    
#    while not maxx >= BottomrightE:
#        maxx += gt[1]
#        newx2 += 1
#    while not miny <= BottomrightN:
#        miny += gt[5]
#        newy2 += 1
    
    narr = arr[:]
    newgt = gt
    wkt = inDs.GetProjection()
        
        # setting spatial reference of output raster 
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    
    inDs = None
    
    
    
    [rows,cols] = narr.shape
    
    driver = gdal.GetDriverByName("GTiff")
    
    raster = np.zeros((rows,cols), dtype=np.float32)

    files = []
    allfiles = []
    
    
    for i in range(len(total)):
        
        month = total[i][0][:6]
            
        nfile = month + '.tif'
        
        storeloc = store + '\\' + nfile
        
        for j in range(len(total[i])):
            
            file = total[i][j]
        
            files.append(file)
        
            file_loc = loc + '\\' + file
            
            inDs = gdal.Open(file_loc)
        
            band = inDs.GetRasterBand(1)
            
            arr = band.ReadAsArray()
            
            narr = arr[:]
            
            raster = raster + narr
            
            inDs = None
        
        
        
            
            
            
        
        allfiles.append(files)
        files = []
        #print(file)
        #count = 0
        
        
        raster = raster / len(total[i])
        
        raster[raster<0] = np.nan
    
        dst_ds = driver.Create(storeloc, 
                           cols, 
                           rows, 
                           1, 
                           gdal.GDT_Float32)
        
       
        

        dst_ds.SetProjection( srs.ExportToWkt() )
        
                  
        dst_ds.SetGeoTransform(newgt)
        
        dst_ds.GetRasterBand(1).SetNoDataValue(NDV)
        
        
        
        
        dst_ds.GetRasterBand(1).WriteArray(raster)
        
        #dst_ds.GetRasterBand(1).WriteArray( narr ) 
        
        dst_ds.FlushCache()
        dst_ds = None
        
        print(nfile)
            
    
    
    
    #writting output raster
def output(loc: str, arr: np.array, l: list, store: str):
    '''loc : location of files
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
        
    

def get_netcdf_info(filename,var_name):

    nc_file = gdal.Open(filename)

    if nc_file is None:
        sys.exit()

    #There are more than two variables, so specifying the lwe_thickness variable

    
    subdataset = 'NETCDF:"'+filename+'":'+var_name #Specifying the subset name
    src_ds_sd = gdal.Open(subdataset) #Reading the subset
    NDV = src_ds_sd.GetRasterBand(1).GetNoDataValue() #Get the nodatavalues
    xsize = src_ds_sd.RasterXSize #Get the X size
    ysize = src_ds_sd.RasterYSize #Get the Y size
    GeoT = src_ds_sd.GetGeoTransform() #Get the GeoTransform
    Projection = osr.SpatialReference() #Get the SpatialReference
    Projection.ImportFromWkt(src_ds_sd.GetProjectionRef()) #Setting the Spatial Reference
    src_ds_sd = None #Closing the file
    nc_file = None #Closing the file

    return xsize,ysize,GeoT,Projection,NDV #Return data that will be used to convert the shapefile

def getdecadlylist(loc) -> list:
    l = [a for a in os.listdir(loc) if a.endswith('.tif')]
    new_l = []
    r = []
    month = l[0][4:6]
    for i in range(len(l)):
        if i == len(l) - 1:
            new_l.append(l[i])
            r.append(new_l)
            new_l = []
            
        elif l[i+1][4:6] != month:
            month = l[i+1][4:6]
            new_l.append(l[i])
            r.append(new_l)
            new_l = []
            
        elif l[i][6:8] == '10':
            new_l.append(l[i])
            r.append(new_l)
            new_l = []
        elif l[i][6:8] == '20':
            new_l.append(l[i])
            r.append(new_l)
            new_l = []
        
        else:
            new_l.append(l[i])
    a = []
    name = r[0][0][:6] + '01'
    for dec in r:
        name1 = dec[0][:6]
        if name1 == name[:6]:
            num = int(name[7]) + 1
            name1 = name1 + '0' + str(num)
            name = name1
        else:
            name = name1 + '01'
        a.append(name)
    b = [q +'.tif' for q in a]
    return r , b
            



def aggregateDecadlyRainCount(loc, store, filenames: list, naming):
    sizeget = filenames[0][0]
    
    sample = loc + '\\' + sizeget
    
    location = loc + "\\" + sizeget
    im = Image.open(location)
    arr = np.array(im)
    
    inDs = gdal.Open(sample)
    
    band = inDs.GetRasterBand(1)
    NDV = band.GetNoDataValue()
    
    wkt = inDs.GetProjection()
        
        # setting spatial reference of output raster 
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    
    gt = inDs.GetGeoTransform()
    
    inDs = None
    
    [rows,cols] = arr.shape
    
    driver = gdal.GetDriverByName("GTiff")


    for i in range(len(filenames)):
        raster = np.zeros((rows,cols), dtype=np.float32)
        storeloc = store + "\\" + naming[i]
        
        for j in range(len(filenames[i])):
            location = loc + "\\" + filenames[i][j]
            im = Image.open(location)
            a = np.array(im)
            a[a>0] = 1
            raster += a
            
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
        
        print(naming[i])
        
            
            

    
    
    
        
        
        

    
    
    
    
    
    
            
            
            
    










    