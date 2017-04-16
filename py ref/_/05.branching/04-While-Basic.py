#!/usr/bin/env python
#coding:utf-8

y=0
x=3
itersLeft = 5
while(itersLeft>0):
    y=y+x
    itersLeft = itersLeft - 1
    print 'y =',y,',itersLeft=',itersLeft
print y

x = 10
i=1
while(i<x):
    if x%i==0:
        print 'divisor ',i
    i = i +1
