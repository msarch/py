'''
#!/usr/bin/python
# -*- coding: utf-8
'''
# msarch@free.fr * jan 2015 * bw-rev113

##--- IMPORTS -----------------------------------------------------------------
from itertools import count

from utils.dump import dumpObj


_capsules=set()

##--- RULE CLASS --------------------------------------------------------------
class Capsule(object):
    new_id = count().next
    _actions=[]
    _shapes=[]
    _publish=[]

    def __init__(self, read_from=[],*args, **kwargs):
        self._id = chr((Capsule.new_id()%26)+97)  # converts int to letters
        for i in kwargs:
            setattr(self,i,kwargs[i])
        self._actions.append(self)
        self.setup()

        print "::"
        print ":: new agent :::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    def sort(self):
        pass
    
    def add(self,*args):
        '''
        Add items to the group list
        '''
        for sh in args:
            self.shapes.append(sh)  #add items
        print "::"
        print "GROUPED SHAPES"
        print "::"
        self.sort()
        
    def broadcast(self, message, cell):
        " Publish an event, no need to register it first."
        print 'message from :', self._id,':', message, cell,
        if not (message, cell) in _messages:
            _messages.add((message,cell))
        else:
            print '* message already registered *'
   
    @staticmethod
    def tick_capsules(dt):
        for k in _capsules:
            k.tick(dt)
            
    @staticmethod
    def draw_capsules(dt):
        for k in _capsules:
            k.draw(dt)
