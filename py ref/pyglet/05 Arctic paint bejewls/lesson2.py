"""
Copyright 2008 Joey Marshall

If you have not read lesson 1 you can find it at http://arcticpaint.com/tutorials/

Lesson 2 - BeJewls
==================

:author: Joey Marshall <web@joey101.net>
:date: Jun 2, 2008
:license: Everything with the exception of the Arctic Paint name and logo are licensed under the GPLv2 (see GPL.txt). If you wish to redistribute any part of this program THE COPYRIGHT NOTICE ON THE TOP AND BOTTOM OF THIS FILE MUST STAY!

In lesson 2 we will be creating a game similar to bejeweled. The big thing I'll
be teaching here is animation and using a GUI to simplify input. Don't be scared
off by the length of this file... a good portion of it is comments! ;)
"""

from __future__ import division
import sys
import random
import rabbyt
from pyglet import clock

# We are going to be using a development version of snowui. Snowui is a small
# light weight GUI I made for use with pyglet. It's designed to be very
# simplistic and easy to extend.
# You can find the HG repo here: http://freehg.org/u/joey/snowui/
import snowui


# Let's start off with our Gem class. As you can see we are sub classing from
# snowui.Widget. The Widget class will give us a lot of functionality that we
# will need - primarily events as you will soon see.
#
# I strongly suggest you read the doc string for the Widget class in
# snowui/widget.py - it will really help you understand how snowui widgets work
# as I won't be going into detail about it here. Documentation is a bit scarce so
# you may want to read through the code too (it issn't very long).
class Gem(snowui.Widget, object):
    def __init__(self, client, id, x, y):

        # This looks a bit scary but it's pretty simple really.
        snowui.Widget.__init__(self,
                texture="data/gem%i.png"%id, # The image to use - gos
                                             # strait to rabbyt.Sprite

                rx=x*62.5+253+26, ry=y*62.5+52+26, # Relative x and y positions

                bounds="rect" # This is used for collision. Passing "rect" tells
                              # the widget to use a rectangular bounding box
                              # (default is a circle)
                )

        # This line needs an explanation. The Widget class will set the center
        # point on the sprite to be the bottom left corner. In this case we
        # don't want that. It's really pretty hackish but the widget saves it's
        # original shape to orig_shape. Here we are restoring it so that the
        # center point is back in the center of the sprite.
        self.shape.bottom, self.shape.left = self.orig_shape

        # It's important for us to save which type of gem this is... for obvious
        # reasons. :)
        self.id = id

        # We need to store where on the 8x8 grid this gem is. Because Widget
        # uses x and y for positioning the sprite we need to use something
        # else... like grid_x and grid_y!
        self.grid_x, self.grid_y = x, y

        self.client = client
        # When you look in the Client class further down you will see when we
        # define the gui. It's an instance of snowui.GUI (found in main.py).
        # It's a very simple class (less than 20 lines) but it manages all
        # our widgets. So all widgets, gems in our case, must be added and
        # removed from there.
        self.client.gui.add(self)


    # This might be a little bit confusing - especially if you don't understand
    # property. All this does is make it so you can read and set grid_x and
    # grid_y with grid_xy. Which is very helpful to be able to do.
    def _get_grid_xy(self):
        return self.grid_x, self.grid_y
    def _set_grid_xy(self, (x,y)):
        self.grid_x = x
        self.grid_y = y
    grid_xy = property(_get_grid_xy, _set_grid_xy)


    # This function is called by our sub classed Widget when the mouse is pressed
    # on this widget. Pretty simple.
    def handle_mouse_press(self, x, y, button, modifiers):
        # But we are going to pass this on to be handled by the client.
        self.client.handle_gem_click(self)

    # A simple function to see if this gem is next to another gem. This is used
    # to check when the player clicks on gems to see if the two can even be
    # attempted to flip.
    def is_next_to(self, other_gem):
        for (x,y) in [(-1,0), (0,1), (1,0), (0,-1)]:
            if other_gem.grid_xy == (self.grid_x+x, self.grid_y+y):
                return True
        return False

    # And here is where we flip two gems.
    def flip(self, gem):
        tmp_grid_xy = gem.grid_xy
        gem.grid_xy = self.grid_xy
        self.grid_xy = tmp_grid_xy

        self.client.game.gems[gem.grid_xy] = gem
        self.client.game.gems[self.grid_xy] = self

    # do_score sees if self (a gem remember) can score (by there being at least
    # three in a row).
    def do_score(self):
        # First we find all rows of the same gem type that this gem is in that
        # is (by default) at least three long.
        row = self.client.game.find_gems_row(self.grid_xy, self.id)
        if row:
            # As there is a row(s) we need to add self to it as the
            # find_gems_row function only checks and returns gems NEXT to this
            # one.
            row.add(self)
        else:
            return False

        # Ok, it is in a row! Now let's take each gem amd remove it. This is
        # where you would also put the scoring stuff - but for this example
        # we don't implement it.
        for gem in row:
            self.client.game.remove_gem(gem)

            # We don't want to remove this gem from the gui right away because
            # it would stop being drawn immediately - and we want to do some
            # cool fading effects :D
            # So we schedule with pyglet's clock to remove it is .7 seconds.
            clock.schedule_once(lambda dt:(self.client.gui.remove(gem)), .7)

            # And now we apply our fading and scaling effects... in exactly two
            # lines...
            gem.scale = rabbyt.lerp(end=0, startt=self.client.time+.5, dt=.2)
            gem.alpha = rabbyt.lerp(end=0, startt=self.client.time+.2, dt=.5)
            # HOLY COW THAT IS SO SIMPLE!1!! OMG!!!!1!1!11one!
            # For learning how rabbyt anims work and all you can do with them,
            # check out the online documentation for them at rabbyt's website:
            # http://matthewmarshall.org/projects/rabbyt/docs/rabbyt/anims/
            # That whole page is filled with all the awesomeness you can do
            # with the rabbyt anims.
        return True


# Now for our Client class. When reading through you need to keep in mind that
# it uses parts from the Game class which is right below this one.
class Client:
    def __init__(self):
        clock.set_fps_limit(35)
        self.time = 0

        self.window = snowui.Window((800,600))
        # snowui.GUI is a Widget just like anything else; so it can have a
        # texture just like anything else!
        self.gui = snowui.GUI(texture="data/bg.png")
        self.window.push_handlers(self.gui)

        # This is a nice gradient that we put over our game. We won't in this
        # tutorial but we could do some pretty cool fading stuff with it to
        # change the mood of the game. (such as for levels)
        self.bg_overlay = rabbyt.Sprite("data/bg_overlay.png")
        self.bg_overlay.left = 0
        self.bg_overlay.bottom = 0
        self.bg_overlay.rgba = 0,.7,1,.1

        # snowui has a pre-made Button class because it is so common. It also
        # makes a really good example for how to extend the Widget to do what
        # you want it to do.
        quit_button = snowui.Button(texture="data/exit_button.png",
                rx=5, ry=5,
                default_color=(1,1,1,.7),
                hover_color=(.7,0,0,1),
                callback=sys.exit)
        self.gui.add(quit_button)

        # Notice that we aren't using the snowui Button but our own. It is at
        # the bottom of this tutorial and you'll see how cool it is down there.
        restart_button = RestartButton(texture="data/restart_button.png",
                rx=75, ry=24,
                default_color=(1,1,1,.7),
                hover_color=(0,1,0,1),
                shape=(-20,20,20,-20),
                bounds="rect",
                callback=self.restart_game)
        self.gui.add(restart_button)
        # If you are unsure how all this works take a look at the Button class
        # in snowui/button.py

        # And now for our Happy Glacier icon. If you haven't seen arctic paint
        # you need to check it out at arcticpaint.com! Chance are you got this
        # tutorial from there though.
        hg_icon = snowui.Button(texture="data/hg_icon.png",
                rx=800-89, ry=600-46,
                hover_color=(.7,.7,1,1),
                fade_time=.1,
                bounds="rect")
        self.gui.add(hg_icon)

        # Here is where we store the running game. The Game keeps track of all
        # the gems on the playing field and functions for moving them around and
        # junk like that. You'll see soon.
        self.game = Game(self)

        self.selected_gem = None
        self.selection_marker = rabbyt.Sprite("data/selection_marker.png")
        self.selection_marker.alpha = 0

    # This is the callback for the restart button. It is quite simple and...
    # restarts the game! Should I even be writing this comment?
    def restart_game(self):
        for g in self.game.gems.values():
            self.gui.remove(g)
        self.game = Game(self)

    # If you'll remember back in the Gem class, this is the function that is
    # called by the gem when it is clicked.
    def handle_gem_click(self, gem):
        if self.selected_gem and gem.is_next_to(self.selected_gem):
            # Alright, we have a gem selected and the player clicked on another
            # gem that is right next to it. Now this is where everything starts
            # happening!

            # First we are going to flip it. If it is invalid we will flip it
            # back later. But it is import that we do it like this for our
            # checking functions to work properly.
            gem.flip(self.selected_gem)

            # Remember calling find_gems_row? Here we are checking to see if
            # either of the two gems we just flipped cause us to score.
            if self.game.find_gems_row(self.selected_gem.grid_xy,
                    self.selected_gem.id) or\
                    self.game.find_gems_row(gem.grid_xy, gem.id):

                # Yeah! We can SCORE!!! So let's visually flip them here.
                tmp_xy = gem.xy
                gem.xy = rabbyt.ease_out(end=self.selected_gem.xy, dt=.5)
                self.selected_gem.xy = rabbyt.ease_out(end=tmp_xy, dt=.5)
                # Oh yeah, that awesome anim stuff again!

                # And now the do_score. If you don't remember what it all does
                # go back and check in the Gem class.
                gem.do_score()
                self.selected_gem.do_score()

                # In .7 seconds (which is the time we need to allow for the
                # awesome disappearing animation stuff to finish) we drop the
                # gems to fill in the empty spaces.
                clock.schedule_once(lambda dt:(self.game.drop_gems()), .7)

            else:
                # It didn't match, flip back.
                gem.flip(self.selected_gem)

                # And as it didn't match we want a cool animation where they
                # start switching places but swing back around to where they
                # were.
                tmp_xy = gem.xy
                gem.xy = rabbyt.chain(
                        rabbyt.ease_out(end=self.selected_gem.xy, dt=.5),
                        rabbyt.ease_out(end=gem.xy, dt=.5),
                        )
                self.selected_gem.xy = rabbyt.chain(
                        rabbyt.ease_out(end=tmp_xy, dt=.5),
                        rabbyt.ease_out(end=self.selected_gem.xy, dt=.5),
                        )

            # Alright, everything is said and done. Deselect our gem.
            self.selected_gem = None
            self.selected_marker = None
            self.selection_marker.alpha = 0

        elif gem != self.selected_gem:
            # What happened here is that they had a gem selected and clicked on
            # another one that wassn't next to this one. We want to simply
            # select the new gem.
            self.selected_gem = gem
            self.selection_marker.xy = gem.xy
            self.selection_marker.alpha = 1


    # This is our infinite loop that runs the game. It's very simple thanks to
    # using snowui and there isn't much to do here. It should all be pretty
    # self explanatory.
    def loop(self):
        dt = clock.tick()
        self.time += dt

        self.window.dispatch_events()
        rabbyt.set_time(self.time)
        rabbyt.clear()

        self.gui.render()
        self.bg_overlay.render()
        self.selection_marker.render()

        self.window.flip()
        return True


# Almost done! JUST KIDDING! Now for the hard confusing parts.
class Game:
    def __init__(self, client):
        self.client = client

        # Generate our board.
        self.gems = {}
        # empty_slot stores all the vertical rows as lists. This makes it easy
        # to make the rows drop later on.
        self.empty_slots = {}
        ids = [0,1,2,3,4,5,6]
        for x in range(8):
            self.empty_slots[x] = []
            for y in range(8):
                random.shuffle(ids)
                for id in ids:
                    # Make sure we aren't putting any 2 gems right next to each
                    # other of the same type.
                    row = self.find_gems_row((x,y),id,2)
                    if not row:
                        break
                gem = Gem(self.client, id=id, x=x, y=y)
                self.gems[(x,y)] = gem

    # Alright, this may get a bit confusing, but who said making games was easy?
    def drop_gems(self):

        # We need to keep track of all gems that have moved so we can detect
        # chain reaction scores.
        moved_gems = set()

        # Here we go through all the columns to see if they need to be dropped.
        for k,row in self.empty_slots.items():
            if not row:
                # This row is devoid of emptiness. Skip it.
                continue

            # We sort the row so that the bottom most empty slot on this column
            # is first in the list. The row is structured with x being the key
            # and the value being a list of all the empty coordinates on the
            # board that need filled.
            row.sort(key=lambda obj:obj[1])
            # We are only interested in the bottom most one.
            empty_xy = row[0]

            # We are going to start at the bottom most one and move the next
            # closest gem that is above it to be right on top of it. We then
            # work our way up until we have filled all empty spots in this
            # column (or row as the variable calls it).
            while True:
                if not self.gems.has_key(empty_xy):
                    # Oops, we passed the top! This is it for this row.
                    break

                if self.gems[empty_xy] is None:
                    # This spot is empty so let's drop the closest one above it!
                    # First step is to find it.
                    ng = self.find_next_gem_up(empty_xy)

                    # Move the gem we are dropping. Notice that where the ng gem
                    # used to be it is now empty. That is one reason we work our
                    # way up and not down!
                    self.gems[ng.grid_xy] = None
                    ng.grid_xy = empty_xy
                    self.gems[empty_xy] = ng

                    # Move the gem vissually. Above we just moved it in the
                    # game's gem store.
                    ng.y = rabbyt.lerp(end=ng.grid_y*62.5+52+26, dt=.6)

                    moved_gems.add(ng)

                # Now we prepare for the next loop to check the slot about this
                # one.
                empty_xy = (empty_xy[0], empty_xy[1]+1)

            # This row is full!
            self.empty_slots[k] = []

        # Don't be thrown off by this; we are still in the drop_gems function!
        # This is what's called a factory. This is probably one of the most
        # confusing places. What we are doing here is waiting until all our gems
        # have dropped and then checking to see if there are any chain reaction
        # scoring. If there is we drop it all over again.
        def _score(dt):
            _s = False
            for g in moved_gems:
                if g.do_score():
                    _s = True
            if _s:
                clock.schedule_once(lambda dt:(self.drop_gems()), .4)
        clock.schedule_once(_score, .6)


    def find_next_gem_up(self, (x,y)):
        # How this works is we start at the given xy position and work our way
        # up until we find a gem (and then we return it) or the top of the board
        # (and then we create a new gem and add it to the game).
        while True:
            y += 1
            if self.gems.has_key((x,y)):
                if self.gems[(x,y)]:
                    return self.gems[(x,y)]
            else:
                g = Gem(self.client, random.randint(0,6), x, y-1)
                g.alpha = rabbyt.lerp(start=0, end=1, dt=1)
                self.gems[g.grid_xy] = g
                return g


    def remove_gem(self, gem):
        self.empty_slots[gem.grid_x].append(gem.grid_xy)
        self.gems[gem.grid_xy] = None


    # Now for our longest function yet! I wish it could be shorter but this is
    # the way it is. There isn't much I can say to make it any clearer...
    # good luck!
    def find_gems_row(self, (x,y), id, row_length=3):
        """
        If xy on the board were gem id would it be a row of 3 or more? If so
        which gems would be in the row.
        """

        all_gems = set()

        # Check left and right.
        x_gems = set()
        txl = x
        while True:
            txl -= 1
            if self.gems.has_key((txl,y)) and self.gems[(txl,y)] and\
                    self.gems[(txl,y)].id == id:
                x_gems.add(self.gems[(txl,y)])
            else:
                break

        txr = x
        while True:
            txr += 1
            if self.gems.has_key((txr,y)) and self.gems[(txr,y)] and\
                    self.gems[(txr,y)].id == id:
                x_gems.add(self.gems[(txr,y)])
            else:
                break

        if len(x_gems) >= row_length-1:
            all_gems.update(x_gems)

        # Check up and down.
        y_gems = set()
        tyl = y
        while True:
            tyl -= 1
            if self.gems.has_key((x,tyl)) and self.gems[(x,tyl)] and\
                    self.gems[(x,tyl)].id == id:
                y_gems.add(self.gems[(x,tyl)])
            else:
                break

        tyr = y
        while True:
            tyr += 1
            if self.gems.has_key((x,tyr)) and self.gems[(x,tyr)] and\
                    self.gems[(x,tyr)].id == id:
                y_gems.add(self.gems[(x,tyr)])
            else:
                break

        if len(y_gems) >= row_length-1:
            all_gems.update(y_gems)

        return all_gems



# And here is our restart button that spins really awesomely when hovered! As
# you can see we are sub classing snowui.Button. All we do is define our own
# animations when it is hovered (or as the function calls it, "faded").
class RestartButton(snowui.Button):
    def do_fade(self, start_rgba, end_rgba):
        snowui.Button.do_fade(self, start_rgba, end_rgba)
        if self.is_hovering:
            # We are fading out.
            self.rot = rabbyt.lerp(end=0, dt=.2)
        else:
            self.rot = rabbyt.ease_out(end=-180, dt=1, extend="repeat",
                    method="bounce")


client = Client()
while True:
    client.loop()
# And here we start the game. And that is it! I hope you learned a lot and had
# fun! I sure did have fun... I guess I learned something too. :)
# That's one of the great things about programming; always learning something
# new!
#
#
# ------------------------------------------------------------------------------
# This tutorial is copyright 2008 by Joey Marshall and his company Arctic Paint
# http://arcticpaint.com
# Everything with the exception of the Arctic Paint name and logo are licensed
# under the GPLv2 (see GPL.txt)
# If you wish to redistribute this tutorial I politely demand that the copyright
# notice on the top and bottom of this file be left intact and unmodified.
# Thank you!
# Joey Marshall
# ------------------------------------------------------------------------------
