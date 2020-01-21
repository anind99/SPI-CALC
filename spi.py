# -*- coding: utf-8 -*-
"""
Created on Wed May 16 10:30:47 2018

@author: anind
"""

from basemod import BaseStandardIndex


class SPI(BaseStandardIndex):

    def set_distribution_params(self, dist_type='gengamma', **kwargs):
        super(SPI, self).set_distribution_params(dist_type=dist_type, **kwargs)
