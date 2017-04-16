#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''

event.py, an event manager using
    publish
    subscribe
    weakrefs

Any function can publish any event without registering it first,
and any object can register interest in any event, even if it doesn't exist yet.

The event manager uses weakrefs, so lists of listeners won't stop them
from being garbage collected when they're deleted.
'''

import weakref

_events = {}

def Subscribe(eventname, self):
    " Subscribe to an event, even if it doesn't exist yet."
    eventname = eventname.lower()
    eventname = eventname.replace(' ', '')
    if not eventname in _events:
        _events[eventname] = []
        listeners = _events[eventname]
        obj = weakref.ref(self)
        if not obj in listeners:
            listeners.append(obj)

def Unsubscribe(eventname, self):
    " Unsubscribe from an event, even if it never existed."
    eventname = eventname.lower()
    eventname = eventname.replace(' ', '')
    if not eventname in _events:
        return
    listeners = _events[eventname]
    obj = weakref.ref(self)
    if obj in listeners:
        print "Removing listener %s from event %s" % (str(self), eventname)
    listeners.remove(obj)

def Raise(eventname, *args, **kwargs):
    " Publish an event, no need to register it first."
    eventname = eventname.lower()
    eventname = eventname.replace(' ', '')
    if not eventname in _events:
        _events[eventname] = []
        listeners = _events[eventname]
        print "EVENT %s (%d listeners, possibly dead) %s" % (eventname, len(listeners), str(args))
        i = 0
        while i < len(listeners):
            obj = listeners[i]
            listener = obj()
            if listener:
                fnname = 'On' + eventname[0].upper() + eventname[1:].lower()
                fn = getattr(listener, fnname, None)
            if fn == None:
                fn = getattr(listener, 'OnEvent')
                fn(eventname, *args, **kwargs)
                i += 1
            else:
                print "Removing %s from %s" % (str(obj), eventname)
                listeners.remove(obj)


class Listener:
    '''
    Objects that want to be notified of events.
    They should have an 'OnEventname' function for
    every event they're interested in, or a single
    function called 'OnEvent' to receive all events.
    '''

    _listen = []

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        for eventname in self._listen:
            Subscribe(eventname, self)
            print "*** %s is interested in %s" % (self.name, eventname)

    def OnEvent(self, eventname, *args, **kwargs):
        print "*** %s(%s, %s)" % (eventname, str(args), str(kwargs))

    def __str__(self):
        return str(self.__dict__)

    def __del__(self):
        print "*** %s is dead." % self.name



def main():

    class Dog(Listener):
        name = 'Dog'
        _listen = ['Bone', 'Ball']
        def OnEvent(self, eventname, *args, **kwargs):
            if eventname == 'bone':
                print "*** %s slobbers on the bone" % self.name
            elif eventname == 'ball':
                print "*** %s noses the ball forward" % self.name

    class Cat(Listener):
        name = 'Cat'
        _listen = ['Ball', 'Yarn', 'Fluffy chick']

        def OnBall(self, *args, **kwargs):
            print "*** %s chases the ball" % self.name

        def OnYarn(self, *args, **kwargs):
            print "*** %s bats at the yarn." % self.name

        def OnFluffychick(self, *args, **kwargs):
            print "*** %s eats the fluffy chick." % self.name

    Raise('INIT', 'No one is interested in this event')
    Raise('BALL', 'Look! A ball, but no one is watching.')
    dog = Dog(name = 'Fido')
    Raise('BALL', 'Another ball! Watch, Fido!')
    del dog
    Raise('BALL', 'No one is watching because Fido is dead.')
    cat = Cat(name = 'Snowball')
    dog = Dog(name = 'Spot')
    Raise('BONE', "Only dogs eat bones.")
    Raise('BALL', "Cats and dogs both love this one!")
    Raise('YARN', "ball of pink yarn")
    Raise('RAKING', 'Humans working in the yard')
    Raise('Fluffy chick', 'Ooh, how cute! An Easter leftover walking in the yard.')
    Unsubscribe('fluffy chick', cat)
    Raise('Fluffy chick', 'The cat is full and no longer interested in chicks.')
    del cat
    del dog
    Raise('BALL', 'Ball anyone? Fluffy? Spot? Fido?')


    print "Done!"

if __name__ == '__main__':
    main()

