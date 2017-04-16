import os

print __file__


curdir = os.path.dirname(os.path.abspath(__file__))
mysubdir= os.sys.path.join((curdir,'scene/'))
print mysubdir
os.sys.path.append(os.path.join(curdir,'scene/'))
for module in os.listdir((os.path.join(curdir, 'scene/'))):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    print module
    __import__(module[:-3], locals(), globals())
del module


____________________________________________

import os

print __file__


curdir = os.path.dirname(os.path.abspath(__file__))
mysubdir= os.sys.path.join((curdir,'scene/'))
print mysubdir
os.sys.path.append(os.path.join(mysubdir)
for module in os.listdir(mysubdir):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    print module
    __import__(module[:-3], locals(), globals())
del module
