# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 00:34:46 2020

@author: gusta
"""

import numpy as np
 
#-------------------------------------------------------------------------- 
# constantes
BLOCKED = 0  # sítio bloqueado
OPEN    = 1  # sítio aberto
FULL    = 2  # sítio cheio
 
#-------------------------------------------------------------------------- 
 
class Percolation:
 
    def __init__(self, shape):
        #verificação se tem alguma coisa errada
        cond1 = not isinstance(shape , tuple) and not isinstance(shape, int)
        if cond1:
            print('ERRO')
            return None
        elif isinstance(shape , tuple):
            cond2 = isinstance(shape[0], int) and isinstance(shape[1], int)
            cond3 = shape[0] > 0 and shape[1] > 0
            if not cond2 or not cond3:
                print('ERRO')
                return None
        #inicialização
        if isinstance(shape, int):
            self.shape = (shape, shape)
        else:
            self.shape = shape
        self.data=np.full(self.shape, BLOCKED)
 
    def __str__(self):
        #coisa horrorosa, nem tente entender o que está acontecendo
        s1 = '+'+'---+'*self.shape[1]+'\n'
        s2 = '|'+'   |'*self.shape[1]
        s3 = s1+(s2+'\n'+s1)*self.shape[0]
        s3 = s3[:len(s3)-1]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                k=(2+4*self.shape[1])*(2*i+1)+4*j+2
                if self[i,j] == OPEN:
                    s3 = s3[:k]+'o'+s3[k+1:]
                elif self[i,j] == FULL:
                    s3 = s3[:k]+'x'+s3[k+1:]
        s4 = f'grade de dimensão: {self.shape[0]}x{self.shape[1]}'
        s5 = f'no. sítios abertos: {self.no_open()}'
        s6 = f'percolou: {self.percolates()}'
        return s3+'\n'+s4+'\n'+s5+'\n'+s6+'\n'
 
    def __getitem__(self, pos):
        return self.data[pos]
    
    def __setitem__(self, pos , valor):
        self.data[pos]=valor
 
    def is_open(self, lin, col):
        cond1 = lin < 0 or lin >= self.shape[0]
        cond2 = col < 0 or col >= self.shape[1]
        if cond1 or cond2:
            print(f'posição [{lin},{col}] está fora da grade')
            ret = None
        else: 
            ret = self[lin, col] == OPEN or self[lin, col] == FULL
        return ret
 
    def is_full(self, lin, col):
        cond1 = lin < 0 or lin >= self.shape[0]
        cond2 = col < 0 or col >= self.shape[1]
        if cond1 or cond2:
            print(f'posição [{lin},{col}] está fora da grade')
            ret = None
        else:
            ret = self[lin, col] == FULL
        return ret
 
    def no_open(self):
        a=self.shape[0]*self.shape[1]
        return a-np.count_nonzero(self.data == BLOCKED)
 
    def percolates(self):
        return np.count_nonzero(self.data[self.shape[0]-1 , :] == FULL ) > 0    
    
    def __sweep(self, i,j):
        #Este é o algoritmo scanline fill, peguei pronto na net e só adaptei
        self.max_depth = 0
        stack = [(j,i)]
        w = self.shape[1]
        h = self.shape[0]
        while stack:
            self.max_depth = max(self.max_depth , len(stack))
            cur_point = stack.pop()
            x1 , y1 = cur_point
            while x1 >= 0 and self[y1,x1] == OPEN:
                x1 -= 1
            x1 += 1
            above = False
            below = False
            while x1 < w and self[y1,x1] == OPEN:
                self[y1 , x1] = FULL
                if not above and y1 > 0 and self[ y1-1 ,x1] == OPEN:
                    stack.append((x1 , y1-1))
                    above = True
                elif above and y1 < h-1 and self[y1-1 , x1] != OPEN:
                    above = False
                if not below and y1 < h-1 and self[y1+1,x1] == OPEN:
                    stack.append((x1,y1+1))
                    below = True
                elif below and y1 < h-1 and self[y1+1, x1] != OPEN:
                    below = False
                x1 +=1
 
    def open(self, lin, col): 
        cond1 = lin < 0 or lin >= self.shape[0]
        cond2 = col < 0 or col >= self.shape[1]
        if cond1 or cond2:
            print(f'posição [{lin},{col}] está fora da grade')
 
        elif self[lin, col] == BLOCKED:
            self[lin, col] = OPEN
            #alguns booleanos para deixar os testes mais limpos
            c1 = lin>0
            c2 = col>0
            c3 = lin<self.shape[0]-1
            c4 = col<self.shape[1]-1       
            #a seguir excluímos uns casos para não usar o sweep de forma 
            #redundante, preenchendo o site se necessário ou deixando open
            vizinhos=[] #lista de como são os elementos vizinhos
            if c1:
                vizinhos.append(self[lin-1, col])
            if c2:
                vizinhos.append(self[lin, col-1])
            if c3:
                vizinhos.append(self[lin+1, col])
            if c4:
                vizinhos.append(self[lin, col+1])
            #mais alguns booleanos para deixar os testes mais limpos
            c5 = (FULL in vizinhos and not (OPEN in vizinhos))
            c6 = (not c1) and (not (OPEN in vizinhos))
            c7 = (OPEN in vizinhos) and (FULL in vizinhos)
            if c5 or c6:
                self[lin, col] = FULL
            elif c7 or (not c1):
                self.__sweep(lin, col)            
            #ainda teria um caso de else aqui, mas ele não faz nada, apenas
            #mantém o site OPEN, então nem precisa escrever            
 
    def get_grid(self):
        return self.data.copy()