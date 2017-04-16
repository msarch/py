#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''


_events = {}

def subscribe(rule, requisite, cells):
    " Subscribe to an event, even if it doesn't exist yet."
    _events[eventname] = []
    listeners = _events[eventname]
    print '** subscribed'
    print _events
    listeners.append(rule.name)



def publish(eventname, *args, **kwargs):
    " Publish an event, no need to register it first."
    print '** raising', eventname
    if not eventname in _events:
        _events[eventname] = []
        listeners = _events[eventname]
        print "** EVENT %s (%d listeners, possibly dead) %s" % (eventname, len(listeners), str(args))
        i = 0
        while i < len(listeners):
            obj = listeners[i]
            listener = obj()
            if listener:
                fn = getattr(listener, 'OnEvent')
                print '** calling : ', fn
                fn(eventname, *args, **kwargs)
                i += 1
            else:
                print "** Removing %s from %s" % (str(obj), eventname)
                listeners.remove(obj)



