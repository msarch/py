#!/usr/bin/python

# list all files in directory tree by recursion
# shows full file path of all files in subdirectories too
# works with Python2 and Python3

import os

def mylister(startdir, mylist=[]):
    # default mylist becomes static
    print( "looking at %s" % startdir)
    for file in os.listdir(startdir):

        # add directory to filename
        path = os.path.join(startdir, file)
        if not os.path.isdir(path):
            #print(path)
            mylist.append(path)
        else:
            # recurse into subdirs
            mylister(path)
    return mylist

# this allows the module mylister to be tested


curdir = os.path.dirname(os.path.abspath(__file__))
print 'currrent directory -->', curdir
path_list = mylister(curdir)
print '\n'
for path in path_list:
    print(path)

