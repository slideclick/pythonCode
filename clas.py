# -*- coding: UTF-8 -*-

#from __future__ import print_function

class Acnt(object):
    num=0
    def __init__(self,balance):
        self.balance = balance
        Acnt.num += 1
    def deposit(self,amt):
        self.balance += amt
    @classmethod
    def nums(cls):
        return cls.num
    @property
    def Balance(self):
        return self.balance
def withdraw(self,amt):
    self.balance -= amt
    
def Nums(cls):
        return cls.num

o=Acnt(10)
b=Acnt(20)
o.__dict__
Acnt.__dict__
Acnt.__dict__['num']