#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev112
'''

##--- IMPORTS -----------------------------------------------------------------
import weakref
from pyglet.clock import schedule_interval
from utils.dump import dumpObj
from shapes.shapes import dummy

##--- CONSTANTS AND VARIABLES -------------------------------------------------
_broadcasts_record=set()
_conditional = set()
_oneshot = set()
_periodic = set()
_persistent = set()

##--- RULE CLASS --------------------------------------------------------------
class Rule(object):
    def __init__(self, *args, **kwargs):
        self._items=set()
        if args:
            self._items.update(args)
        else:
            self._items.add(dummy)
        for i in kwargs:
            setattr(self,i,kwargs[i])
        if not hasattr (self,'ruletype'):
            self.ruletype='persistent'
        # default ruletype
        if self.ruletype == 'persistent':
            _persistent.add(weakref.ref(self))
        # periodic rules, of course rule must have a 'period' attribute
        elif self.ruletype == 'periodic':
            _periodic.add(weakref.ref(self))  # is this necessary ?
            schedule_interval(self,self.period) # or schedule a oneshot rule ?
        # will run only once, then erased from list
        elif self.ruletype == 'oneshot':
            _oneshot.add(weakref.ref(self))
        # of course rule must have a 'condition' attribute
        elif self.ruletype == 'conditional':
            _conditional.add(weakref.ref(self))
        else:
            print ':: unrecognized type of rule'
        self.setup()
        print "::"
        print ":: new rule :::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    def setup(self):
        pass

    def tick(self,dt, group):  # this is the method that defines the action
        pass


#--- FUNCS --------------------------------------------------------------------
def tick(dt):
    # first : check for conditions
    # second: one shot rules are executed once and then deleted
    # regular rule comes last
    for rule in _conditional:
        for item in rule()._items:
            if (rule().condition) in _broadcasts_record:
                rule().tick(dt)
    _broadcasts_record.clear()
    for rule in _oneshot: rule().tick(dt)
    _oneshot.clear()
    for rule in _persistent: rule().tick(dt)

def broadcast(eventname, cell):
    " Publish an event, no need to register it first."
    print ' << broadcasting :', eventname, cell, '>>',
    if not (eventname, cell) in _broadcasts_record:
        _broadcasts_record.add((eventname,cell))
    else:
        print '** duplicate event :', eventname, cell
