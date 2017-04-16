#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Author:  msarch@free.fr
# Purpose: draws a square room from a list of measurements
# Created:   .  .2012
# License: MIT License

foo= 65
lignes= 3
colonnes = 5

# Declare and initialize a 2d list (actually nested list)

# You need to append values into the lists
a = []
for i in xrange(lignes):
    a.append([])
    for j in xrange(colonnes):
        a[i].append(foo)

print a


# You can use a list comprehension:
a = [[foo for i in range(lignes)] for j in range(colonnes)]

print a

a = []
count=1
for i in xrange(lignes):
    a.append([])
    for j in xrange(colonnes):
        a[i].append(count)
        count = count+1

print a
print a[1][4] # = ligne 2 colonne 5
#Usually when you want multidimensional arrays you
#don't want a list of lists, but rather a numpy array
#or possibly a dict.
#For example, with numpy you would do something like :

#import numpy
#a = numpy.empty((10, 10))
#a.fill(foo)
#share|improve this answer
#edited Mar 7 '10 at 17:36

#Although numpy is great, I think it might be a bit of overkill for a beginner. – voyager Mar 7 '10 at 17:42
#numpy provides a multidimensional array type.
#Building a good multidimensional array out of lists is possible
#but less useful and harder for a beginner than using numpy.
#Nested lists are great for some applications,
#but aren't usually what someone wanting a 2d array would be best off with

#If it's a sparsely-populated array, you might be better off using a dictionary keyed with a tuple:

#dict = {}
#key = (a,b)
#dict[key] = value
#...
#

# The Difference Between Extend and Append

li = ['a', 'b', 'c'] 
li.extend(['d', 'e', 'f'])                         
print li 

print len(li)                                            

print li[-1] 

li = ['a', 'b', 'c'] 
li.append(['d', 'e', 'f'])                        

print li 

print len(li)                                            

print li[-1] 
