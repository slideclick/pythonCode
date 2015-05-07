#! /usr/bin/env python
# -* - coding: UTF-8 -* -

import math, random, pylab
global numPai # = 1
global numPlayer #= 2
global numJudge
global numTimes #= 100


class deck():
    def __init__(self, numPai = 1):
        self.paiS = []
        self.i = 1
        for num in range(1,53):
            self.paiS.append(num)
    def getNext(self):
        if len(self.paiS) == 0:
            raise
        num =   random.choice( self.paiS )
        self.i += 1
        self.paiS.remove(num)
        num = num%13
        if num == 0:
            num = 13
        if num >= 10:
            num = 10
        return num
    def __test(self):
        i = 58
        while i > 0:
            print self.i, self.getNext()
            i -= 1
    def reset(self):
        pass

class player:
    def __init__(self,iJudge):
        self.pais = []
        self.win = 0
        self.fail = 0
        self.ping = 0
        self.iJudge =iJudge
    def newHand(self):
        self.pais = []
    def judgeYao(self):
        total = 0
        for n in self.pais:
            total += n
        if total > 21:
            #self.fail += 1
            return
        if total >= self.iJudge:
            return False
        else:
            return  True
    def getPai(self,num):
        if num == 1:
            num = 11
        self.pais.append(num)
    def getPoint(self):
        total = 0
        for n in self.pais:
            total += n
        if total > 21:
            #self.fail += 1
            return 0,total
        return len(self.pais), total

class dealer():
    def __init__(self):
        self.pais = []
        self.win = 0
        self.fail = 0
        self.ping = 0
    def newHand(self):
        self.pais = []
    def judgeYao(self):
        total = 0
        for n in self.pais:
            total += n
        if total > 21:
            #self.fail += 1
            return
        if total >= 17:
            return False
        else:
            return  True
    def getPai(self,num):
        if num == 1:
            num = 11
        self.pais.append(num)
    def getPoint(self):
        total = 0
        for n in self.pais:
            total += n
        if total > 21:
            #self.fail += 1
            return 0,total
        return len(self.pais), total


def oneTime(numPlayer, judge):

    de = deck()
    playlist = []
    for i in range(0,numPlayer):
        playlist.append(player(judge))
    delaer = dealer()
    while len(de.paiS) != 0:
        try:
            #print len(de.paiS)
            delaer.getPai(de.getNext())
            for p in playlist:
                p.getPai(de.getNext())

            delaer.getPai(de.getNext())
            for p in playlist:
                p.getPai(de.getNext())

            #print 'dealder: ',delaer.pais
            for p in playlist:
                #print 'player: ', p.pais
                while p.judgeYao() == True:
                    p.getPai(de.getNext())
                #print 'player: ', p.pais

            while delaer.judgeYao() == True:
                delaer.getPai(de.getNext())
            #print 'dealder: ',delaer.pais

            iDePai, iDeTotal = delaer.getPoint()
            for p in playlist:
                iPPai,iPTotal = p.getPoint()
                if iPPai == 2 and iPTotal == 21:
                    if iDePai == 2 and iDeTotal == 21:
                        delaer.ping += 1
                        p.ping += 1
                        #print 'ping'
                    else:
                        delaer.fail += 1
                        p.win += 1
                        #print 'player win'
                elif iPPai == 0:
                    p.fail += 1
                    delaer.win += 1
                    #print 'delaer win'
                elif iDePai == 2 and iDeTotal == 21:
                    p.fail += 1
                    delaer.win += 1
                    #print 'delaer win'
                elif  iDePai == 0l:
                    delaer.fail += 1
                    p.win += 1
                    #print 'player win'
                elif  iPTotal > iDeTotal:
                    delaer.fail += 1
                    p.win += 1
                    #print 'player win'
                elif  iPTotal == iDeTotal:
                    delaer.ping += 1
                    p.ping += 1
                    #print 'ping'
                else:
                    p.fail += 1
                    delaer.win += 1
                    #print 'delaer win'

                assert  delaer.ping == p.ping
                assert  delaer.fail == p.win
                assert delaer.win == p.fail
                delaer.newHand()
                for p in playlist:
                    p.newHand();
        except Exception as e:
            print e
            break

##    print 'dealer win: ', delaer.win
##    print 'dealer fail: ', delaer.fail
    pWintotal = 0
    pFailTotal = 0
    for p in playlist:
        #print 'player win: ', p.win
        pWintotal += p.win
        #print 'player fail: ', p.fail
        pFailTotal  += p.fail

    print de.paiS
    import math, operator as op
##    print 'player total win: ',pWintotal
##    print 'player total fail: ',pFailTotal
    assert delaer.fail == pWintotal #reduce(op.add,playlist)
    assert delaer.win == pFailTotal#reduce(op.add,playlist)
    return pWintotal,pFailTotal,delaer.fail,delaer.win

if __name__ == '__main__':
    global numTimes
    
    global numPlayer
    numPlayer = 1
    global numJudge
    judgelist = [12,16,21]    
    for j in judgelist:
        resultLine = [0.0]
        for i in range(20):
            numTimes = 100
            numJudge = 16# 16 is best. 22 WILL BE 0
            pTotal = 0
            dTotal = 0
            pTotalWin = 0
            dTotalWin = 0
            dtotalfail = 0
            while numTimes > 0:
                pWintotal,pFailTotal,delaerfail,delaerwin =oneTime(numPlayer,j)
                pTotal += (pWintotal+pFailTotal)
                dTotal += (delaerfail+delaerwin)
                assert pTotal == dTotal
                pTotalWin += pWintotal
                dTotalWin += delaerwin
                dtotalfail += delaerfail
                assert dtotalfail == pTotalWin
##                print 'player win percentage: ',float(pWintotal)/(pWintotal+pFailTotal)
##                print 'dealer win percentage: ',float(delaerwin)/(pWintotal+pFailTotal)
                numTimes -= 1
                
            #print  'player win percentage: ',float(pTotalWin)/pTotal
            #print  'dealer win percentage: ',float(dTotalWin)/dTotal
            resultLine.append(float(pTotalWin)/pTotal)
        pylab.plot(resultLine)
        pylab.show()
