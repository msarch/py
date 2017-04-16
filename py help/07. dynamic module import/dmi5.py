
# To load a file from the directory of the *imported* module

# When you import a module the working directory is still the working
# directory of the main module:
# say this file is in c:\py_progs

import sys
sys.path.append(r'C:\py_progs\modules')
import my_module

# This is my_module in c:\py_progs\modules
# Even though my_module is in the modules directory and gets correctly
# imported, the working directory is still C:\py_progs.

import os
print(os.getcwd)

# then to load the file from within the submodule
import os
mypath = os.path.dirmane(__file__)
pygame.image.load(os.path.join(mypath, image_name))

