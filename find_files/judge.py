'''
    判断点的位置
'''
import numpy as np


class Point:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
        self.d = [0,0]

    def mult(self,x,p1,p2):
        x = np.array(x)
        p1 = np.array(p1)
        p2 = np.array(p2)
        ver_1 = p1 - x
        ver_2 = p1 - p2
        return ver_1[0] * ver_2[1] - ver_1[1] * ver_2[0]

    def intersect(self):
        if max(self.a[0],self.b[0]) < 0:
            return False
        if max(self.a[1],self.b[1]) < 0:
            return False
        if self.c[0] < min(self.a[0],self.b[0]):
            return  False
        if self.c[1] < min(self.a[1],self.b[1]):
            return  False
        if self.mult(self.c,self.a,self.b) * self.mult(self.d,self.a,self.b) >= 0:
            return False
        if self.mult(self.a,self.c,self.d) * self.mult(self.b,self.c,self.d) >= 0:
            return False
        return True