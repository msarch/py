#!/usr/bin/env python

from mirra import main
from mirra.graphics import *
from mirra import utilities

""" Mirra : 2D graphic engine in OpenGL by www.ixi-software.net
    Check out documentation files
"""


class MirraApp(main.App):
    """ the basic idea is that there is a txt file with python commands. Those commands are executed by python
    when readSetUpPrefs() or readOtherPrefs() are called. We need to keep setUp preferences separated from other
    preferences by a comment line with 'others' keyword on it. Check prefs.txt for format example. Each of the functions
    will read its part of the file. SetUp prefs need to be executed from setUp() function and others can be executed and
    any time after setUp, for example start() is a good moment.
    """
    
    def setUp(self):
        # all setup values are taken from the prefs.txt file
        self.readSetUpPrefs('prefs.txt') # prefs.txt file must be next to this file

        
    def start(self):
        self.circlesize = 0 # this variable will get a value on the prefs file
        # background color will also read from that file        
        self.readOtherPrefs('prefs.txt') # prefs.txt file must be next to this file

        self.Circle = Circle(200, 200, 1, self.circlesize, color=(1,0,0))
        






if __name__ == '__main__': MirraApp() # init always here your main app class that extends main.App




