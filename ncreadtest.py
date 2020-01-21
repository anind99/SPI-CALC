# -*- coding: utf-8 -*-
"""
Created on Wed May 16 12:26:33 2018

@author: anind
"""

from PIL import Image
import os
from netcdfNCL import aggregateRastersMonthly
import numpy
im = Image.open('data/Rainf_tavg/20010101.tif')

imarray = numpy.array(im)
imarray.shape
imarray1 = imarray
imarray += imarray1

im2 = Image.fromarray(imarray)
im2.show()
directory_in_str = 'data'
d2 = 'data/spicalcs'
aggregateRastersMonthly(directory_in_str,d2,'sum')


 
directory = os.fsencode(directory_in_str)

directory = os.fsencode(directory_in_str)
random.choice(directory).show()


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tif"): 
         
         continue
for file in os.listdir('data'):
    filename = os.fsdecode(file)
    if filename.endswith(".tif"):
        im = Image.open(filename)
        nfilarr = np.array(im)
        narr = np.dstack(narr,nfilarr)

l = [1,2,3,4]
m = [-9999.99, 4, 6,2, -9999.99, 3,2,-9999.99]
i = 0
j = 0
while i < len(m) and j < len(l):
    if m[i] >= 0:
        m[i] = l[j]
        j += 1
    i+=1


