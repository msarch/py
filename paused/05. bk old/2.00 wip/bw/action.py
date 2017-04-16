#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
'''

##--- IMPORTS -----------------------------------------------------------------
from itertools import count
from utils.dump import dumpObj

_messages=set()

##--- RULE CLASS --------------------------------------------------------------
class Action(object):
    new_id = count().next
d
    def __init__(self, *args, **kwargs):
        self._id = chr((Action.new_id()%26)+97)  # converts int to letters
        for i in kwargs:
            setattr(self,i,kwargs[i])
        self._actions.append(self)
        self.setup()

        print "::"
        print ":: new agent :::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    def setup(self):
        pass

    def tick(self,dt, group):  # this is the method that defines the action
        pass

    def broadcast(self, message, cell):
        " Publish an event, no need to register it first."
        print 'message from :', self._id,':', message, cell,
        if not (message, cell) in _messages:
            _messages.add((message,cell))
        else:
            print '* message already registered *'
   
    @staticmethod
    def tick_all(dt):
        print
        # first : check for conditions
        # second: one shot actions are executed once and then deleted
        # regular action comes last
        for action in Action._actions:
            if hasattr(action,'condition'):
                for target in action.targets:
                    if (action.condition) in _messages:
                        action.tick(dt)
                        print 'cycle',
                        print action._id
                _messages.clear()
            elif hasattr(action, 'lifespan'):
                # check if dead or alive
                pass
            else:
                action.tick(dt)
                print 'cycle',
                print action._id





