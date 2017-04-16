import os
curdir = os.path.dirname(os.path.abspath(__file__))
print curdir


mysubdir= "/".join((curdir,'data'))

print mysubdir
