#! /usr/bin/env python
# -* - coding: UTF-8 -* -
import math, random, pylab
class location(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    def getCoords(self):#如果是极坐标方式构造，也可以返回
        return self.x, self.y
    def getDist(self, other):#self距离某点多远，而不是 计算两点距离
        ox, oy = other.getCoords()
        xDist = self.x - ox
        yDist = self.y - oy
        return math.sqrt(xDist**2 + yDist**2)
    def __add__(self, other):#处理 += 的能力
        return location(self.x + other.x,self.y +other.y)#functional
    def __str__(self):
        return str(self.x)+'   '+str(self.y)
import operator as op;a =[location(3,3),location(4,5)];print reduce (op.add ,a)

class drunk(object):
    possibles = ('N', 'S', 'E', 'W')
    def __init__(self, name,orloc):
        self.name = name
        self.loc = orloc
        self.orgLoc = orloc
    @property
    def dist(self):
        return self.loc.getDist(self.orgLoc)

    def move(self,dist):
        self.pt = (random.choice(drunk.possibles))
        if self.pt == 'N': self.loc  += location(0, dist)
        elif self.pt == 'S': self.loc  += location(0, -dist)
        elif self.pt == 'E': self.loc  += location (dist, 0)
        elif self.pt == 'W': self.loc  += location (-dist, 0)
        #return self.loc#非functional

class field(object):
    orgloc = location(0,0)    
    def perform(self,num):
        distances = [0.0]
        dr = drunk('simon',field.orgloc)
        for t in range(1,num+1):
            dr.move(1) #newloc = 
            #dist = newloc.getDist(field.orgloc)#而不是 CalcDistance(p1,p1)这个全局函数
            distances.append(dr.dist)
        return  distances

def main():
    f = field()# static main()一般先 class obj = new Class()
    distances = f.perform(10)# obj->message(para)
    pylab.plot(distances)#分离数据与UI
    pylab.show()

if __name__ == '__main__':
   main()
   
