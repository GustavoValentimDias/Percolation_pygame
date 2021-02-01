# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 15:15:40 2020

@author: gusta
"""

from percolation import Percolation
import numpy as np
import random
import math
                 
class PercolationStats:
    '''Classe utilizada para estimar o limiar de percolação.
    '''
    def __init__(self, shape, T):
        self.T = T
        if type(shape) == int:
            a = shape
            b = shape
        elif type(shape) == tuple:
            a = shape[0]
            b = shape[1]
        self.abertos = np.zeros(T, dtype = int)
        self.limiares = np.zeros(T)
        for i in range (0, T):
            p = Percolation(shape)
            n = 0
            while p.percolates() != True:
                v = p.get_grid()
                lin = random.randint(0, a - 1)
                col = random.randint(0, b - 1)
                if v[lin][col] == 0:
                    p.open(lin, col)
                    n = n + 1
                self.abertos[i] = n
            self.limiares[i] = self.abertos[i]/(a*b)
    
    def no_abertos(self):
        return self.abertos.copy()
        
    def mean(self):
        return np.mean(self.limiares)
        
    def stddev(self):
        return np.std(self.limiares, ddof = 1)
        
    def confidenceLow(self):
        return (self.mean() - (1.96*self.stddev()/(math.sqrt(self.T))))
        
    def confidenceHigh(self):
        return (self.mean() + (1.96*self.stddev()/(math.sqrt(self.T))))