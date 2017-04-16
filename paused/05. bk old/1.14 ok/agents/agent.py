#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
'''

##--- IMPORTS -----------------------------------------------------------------
from itertools import count, chain
from pyglet.clock import schedule_interval
from utils.dump import dumpObj
from shapes.rectangle import dummy

##--- CONSTANTS AND VARIABLES -------------------------------------------------
_broadcasts_record=set()
_conditional = set()
_oneshot = set()
_periodic = set()
_persistent = set()

##--- RULE CLASS --------------------------------------------------------------
class Agent(object):

    new_id = count().next

    def __init__(self, *args, **kwargs):
        self._id = chr((Agent.new_id()%26)+97)  # converts int to letters
        self._items=set()
        if args:
            self._items.update(args)
        else:
            self._items.add(dummy)
        for i in kwargs:
            setattr(self,i,kwargs[i])
        if not hasattr (self,'agenttype'):
            self.agenttype='persistent'
        # default agenttype
        if self.agenttype == 'persistent':
            _persistent.add(self)
        # periodic agents, of course agent must have a 'period' attribute
        elif self.agenttype == 'periodic':
            _periodic.add(self)  # is this necessary ?
            schedule_interval(self.tick,self.period) # or schedule a oneshot agent ?
        # will run only once, then erased from list
        elif self.agenttype == 'oneshot':
            _oneshot.add(self)
        # of course agent must have a 'condition' attribute
        elif self.agenttype == 'conditional':
            _conditional.add(self)
        else:
            print ':: unrecognized type of agent'
        self.setup()
        print "::"
        print ":: new agent :::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    def setup(self):
        pass

    def tick(self,dt, group):  # this is the method that defines the action
        pass


#--- FUNCS --------------------------------------------------------------------
def cycle(dt):
    print
    print 'cycle',
    # first : check for conditions
    # second: one shot agents are executed once and then deleted
    # regular agent comes last
    for agent in _conditional:
        print agent._id,
        for item in agent._items:
            if (agent.condition) in _broadcasts_record:
                agent.tick(dt)
    _broadcasts_record.clear()
    for agent in _oneshot:
        print agent._id,
        agent.tick(dt)
    _oneshot.clear()
    for agent in _persistent:
        print agent._id,
        agent.tick(dt)

def broadcast(eventname, cell):
    " Publish an event, no need to register it first."
    print ' << broadcasting :', eventname, cell, '>>',
    if not (eventname, cell) in _broadcasts_record:
        _broadcasts_record.add((eventname,cell))
    else:
        print '** duplicate event :', eventname, cell
