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
class Agent(object):
    new_id = count().next
    _agents=[]

    def __init__(self, *args, **kwargs):
        self._id = chr((Agent.new_id()%26)+97)  # converts int to letters
        for i in kwargs:
            setattr(self,i,kwargs[i])
        self._agents.append(self)
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
        print 'cycle',
        # first : check for conditions
        # second: one shot agents are executed once and then deleted
        # regular agent comes last
        for agent in Agent._agents:
            print agent._id,
            if hasattr(agent,'condition'):
                for target in agent.targets:
                    if (agent.condition) in _messages:
                        agent.tick(dt)
                        print agent._id
                _messages.clear()
            elif hasattr(agent, 'lifespan'):
                # check if dead or alive
                pass
            else:
                agent.tick(dt)
                print agent._id





