"""
Copyright 2008 Joey Marshall

You can find an introduction to this course (HTPG) at http://arcticpaint.com/tutorials/

Lesson 1 - Mines
================

:author: Joey Marshall <web@joey101.net>
:date: Jan 5, 2008
:license: Everything with the exception of the Arctic Paint name and logo are licensed under the GPLv2 (see GPL.txt). If you wish to redistribute any part of this program THE COPYRIGHT NOTICE ON THE TOP AND BOTTOM OF THIS FILE MUST STAY!

In this lesson we will be making a simple Mines clone. It will have the most of the features but for the sake of simplicity we will leave out some stuff that isn't needed to play. Just read down and try to follow along :)
"""

from __future__ import division
import sys
import random
import rabbyt
from pyglet.clock import Clock
from pyglet.event import EventDispatcher
from pyglet.window import Window, mouse, key
from pyglet.text import Label

# We will be using this twice later on. It's just a list of all possible
# directions for finding adjacent blocks (A block being all the little boxes you
# click on that might be mines).
DIRECTIONS = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]

# The colors of our numbers on the blocks showing how many adjacent blocks are
# mines.
COLORS = {
    1: [0, 0, 178, 255],
    2: [0, 178, 0, 255],
    3: [102, 102, 25, 255],
    4: [0, 0, 0, 255],
    5: [178, 0, 204, 255],
    6: [127, 51, 51, 255],
    7: [178, 0, 0, 255],
    8: [178, 25, 76, 255]
}



class Game:
    """
    This Game class holds all the logic and variables (such as objects in a
    game) that is to be used in the game world. NO code used to display stuff on
    the screen should be put in here! You'll see why in later tutorials.
    """
    def __init__(self, size_xy, percent_mines):
        self.size_xy = size_xy
        self.percent_mines = percent_mines

        # This is where we will store all our blocks. The key being their xy
        # position and the value being the block itself. We have the key as the
        # xy to make it easy to look up a block at a certain position as we will
        # do later.
        self.blocks = {}

        self.setup()


    def setup(self):
        """
        This code could just as easily be put in the __init__ function but we
        separate it out here so we can "restart" the game later. What this
        code does is generate all the blocks and sets some of them to be mines.
        It then calculates for each block how many mines are next to it.
        """
        # We also want to have these variables cleared every time the game is
        # restarted.
        self.gameover = False
        self.won = False
        # This variable is used for keeping track of how many blocks have been
        # discovered (ie clicked on).
        self._num_discovered_blocks = 0

        # Generate all the blocks to fill out our grid.
        for x in range(self.size_xy[0]):
            for y in range(self.size_xy[1]):
                self.blocks[(x,y)] = GameBlock(x,y)

        # Here we set a specific number of the blocks to be mines.
        # At the risk of stating the obvious we are making our num_mines an int
        # so we don't get a floating point number. (which you can't validly use
        # with a range function anyway)
        self.num_mines = int(self.size_xy[0]*self.size_xy[1] * self.percent_mines)
        _tmp_blocks = self.blocks.values()
        for i in range(self.num_mines):
            b = random.choice(_tmp_blocks)
            b.is_mine = True
            _tmp_blocks.remove(b)

        # And now we take each block and count how many adjacent blocks are
        # mines. This is the first place were DIRECTIONS comes in handy.
        for b in self.blocks.values():
            for try_x, try_y in DIRECTIONS:
                try_xy = (b.x+try_x, b.y+try_y)
                if self.blocks.has_key(try_xy):
                    if self.blocks[try_xy].is_mine:
                        b.number_adjacent_mines += 1


    def press_block(self, block):
        """
        This function will be called when the player clicks on a block. We
        handle all the logic for win/lose conditions here.
        """
        self._num_discovered_blocks += 1
        block.discovered = True
        if block.is_mine:
            # Game over and player losses!
            self.gameover = True
            for b in self.blocks.values():
                b.discovered = True
        else:
            if block.number_adjacent_mines == 0:
                # As this block doesn't have any mines next to it we will
                # recursively go in all directions to find a block that does.
                # This is a great use for recursion!
                for try_x, try_y in DIRECTIONS:
                    try_xy = (block.x+try_x, block.y+try_y)
                    if self.blocks.has_key(try_xy):
                        b = self.blocks[try_xy]
                        # We want to make sure that the block we are about to
                        # try hasn't already been discovered as that would end
                        # up in an infinite recursion!
                        if not b.discovered:
                            self.press_block(b)

            # Here we check if the number of blocks discovered is equal to how
            # many there are that aren't mines. We have this here as the value
            # for this condition could only change if another block is
            # discovered.
            if self._num_discovered_blocks == (self.size_xy[0]*self.size_xy[1])\
                    - self.num_mines:
                self.gameover = True
                self.won = True


class GameBlock:
    """
    Here is a basic block class! Pretty simple eh? Notice its name is GameBlock.
    This code, like the game, should have nothing to do with receiving user
    input or displaying stuff.
    """
    def __init__(self, x, y):
        self.x, self.y = x,y
        self.is_mine = False
        self.number_adjacent_mines = 0
        self.discovered = False



class Client:
    """
    While we aren't networking this game it's better to learn this structure now
    rather than later. Even if you never plan on learning how to network your
    games this is still a very good architecture to use.

    This Client class should be considered completely separate from the Game. It
    is just a way of interacting with the game. The game should not depend on
    anything in this class. Working like this will help you keep your code much
    cleaner and, as stated before, networkable. You could also make multiple
    clients using different technologies. In our case we are using pyglet and
    rabbyt libraries, but it wouldn't be difficult to make a client using pygame
    or even just the consol (for a text mode).
    """
    def __init__(self, game):
        # While the game needs to work independently of the client the client
        # can't work independently of the game. The client will be sending
        # input to the game as well as looking up different elements (such as
        # all the blocks so we can draw them and tell the game when we click on
        # one).
        self.game = game

        # Setup our pyglet window.
        self.window = Window(width=self.game.size_xy[0]*20,
                height=self.game.size_xy[1]*20+50)
        self.window.set_caption("Mines")
        self.window.on_close = sys.exit
        # The default pyglet OpenGL display is setup a bit different than how
        # rabbyt would like, thus rabbyt.set_default_attribs
        rabbyt.set_default_attribs()

        # Using pyglet for input is really easy. When you get further down
        # you'll see GameContorl inherits from EventDispatcher. That's how
        # window.push_handlers does the magic as we'll see further down.
        self.ctrl = GameContorl(self)
        self.window.push_handlers(self.ctrl)


        # Here we have some sprites we are going to use for the client. For
        # bigger games I think it's better to separate stuff like this out;
        # but this is quite small and not an issue.
        self.smile_face = rabbyt.Sprite("data/smile.png")
        self.smile_face.x = self.window.width/2
        self.smile_face.y = self.window.height-25

        self.dead_face = rabbyt.Sprite("data/smile_dead.png")
        self.dead_face.xy = self.smile_face.xy

        self.won_face = rabbyt.Sprite("data/smile_won.png")
        self.won_face.xy = self.smile_face.xy
        # That sprite stuff was pretty self explanatory. It is also very basic.
        # I'm not going to be going into much depth with rabbyt in these
        # tutorials so you may want to check out the rabbyt documentation from
        # http://matthewmarshall.org/projects/rabbyt/
        # Very cool and elegant stuff there. Check it out!

        self.clock = Clock()
        self.clock.set_fps_limit(20)
        self.window.push_handlers(self.clock)
        self.time = 0
        self.clock.schedule(self._add_time)

        self.setup()


    def setup(self):
        """
        Just like the setup in the Game class this one fills out the block data.
        But wait, why do we have to do this again? Remeber how in the GameBlock
        we only had stuff related to the game engine; no display stuff? Well,
        we need display stuff for the client - that's why we have ClientBlock!
        As you'll see soon the ClientBlock sorta wraps the GameBlock to provide
        the graphical stuff we need.
        """
        self.blocks = {}
        for key,b in self.game.blocks.items():
            self.blocks[key] = ClientBlock(self, b)


    def _add_time(self, dt):
        """
        This is kept track of so we can pass it onto rabbyt (so animation works)
        """
        self.time += dt


    def loop(self):
        """
        And here is our main game loop! In case you are new to game programming
        this is what is called every frame. This is where we will handle the
        display and stuff.
        """
        # clock.tick is used for keeping track of time and limiting the frame
        # rate.
        self.clock.tick()
        self.window.dispatch_events()
        # And this is where that mysterious "time" comes in. This way rabbyt
        # knows how much time has passed and can do the awesome animations.
        rabbyt.set_time(self.time)

        # If you are new to this sort of thing rabbyt.clear clears the screen
        # (erases what was drawn last loop). We pass white as the color that we
        # want to clear it with.
        rabbyt.clear((1,1,1,1))

        # And now we draw our blocks and smile face.
        for b in self.blocks.values():
            b.draw()

        if self.game.gameover == True:
            if self.game.won == False:
                self.dead_face.render()
            else:
                self.won_face.render()
        else:
            self.smile_face.render()

        # This draws the buffer onto the screen. Without this we would be
        # staring at a blank screen.
        self.window.flip()


    def press_block(self, block):
        """
        This is called by the Control as we will see later. Pretty simple and
        even unneeded. But this is where you could add cool effects for when
        you click on a block if you wannted to. (That's the reasion I have it)
        """
        self.game.press_block(block.gameblock)


    def retry(self):
        """
        Re-sets up the game.
        """
        self.game.setup()
        self.setup()




class ClientBlock:
    """
    And here is our ClientBlock! Handles all of the graphical stuff that the
    GameBlock didn't.
    """
    def __init__(self, client, gameblock):
        self.gameblock = gameblock
        self.client = client

        # You know when you right click on a block how it places a flag? That's
        # what this is. We have it here and not in the GameBlock because it
        # only effects the client (weather or not it can be clicked/discovered).
        self.flagged = False

        # Here are all the sprites we use for our block. This COULD be optimized
        # to run faster... but quite frankly, we don't need to (and it's more
        # complicated). If we had 5000 blocks on the screen we would probably
        # consider it.
        self.sprite = rabbyt.Sprite("data/block_hidden.png")
        self.sprite.x = self.gameblock.x*20
        self.sprite.y = self.gameblock.y*20
        # I'm not going to go into detail about rabbyt sprites (you can read
        # the documentation for that) but just so you aren't clueless is tells
        # the sprite that the anchor point for x and y is on the bottom left
        # of the sprite and not the center (default).
        self.sprite.shape.left = 0
        self.sprite.shape.bottom = 0

        self.sprite2 = rabbyt.Sprite("data/block_discovered.png")
        self.sprite2.xy = self.sprite.xy
        self.sprite2.shape = self.sprite.shape

        if self.gameblock.is_mine:
            self.minesprite = rabbyt.Sprite("data/mine.png")
            self.minesprite.xy = self.sprite.xy
            self.minesprite.shape = self.sprite.shape

        self.flag_sprite = rabbyt.Sprite("data/flag.png")
        self.flag_sprite.xy = self.sprite.xy
        self.flag_sprite.shape = self.sprite.shape

        # Here we create the number that will be shown on the block when it is
        # descovered (if it is supposed to have one).
        # NOTE: Drawing pyglet Text is really slow - it would be better to
        # render the text onto a rabbyt sprite (which would go really fast) but
        # we'll just do this for now as that would make this tutorial more
        # complicated than it needs to be.
        if not gameblock.is_mine and gameblock.number_adjacent_mines > 0:
            self.text = Label(str(self.gameblock.number_adjacent_mines),
                    x = self.sprite.x + 5,
                    y = self.sprite.y + 5,
                    color = COLORS[self.gameblock.number_adjacent_mines])



    def draw(self):
        if self.gameblock.discovered:
            self.sprite2.render()
            if self.gameblock.is_mine:
                self.minesprite.render()
            elif self.gameblock.number_adjacent_mines > 0:
                self.text.draw()
        else:
            self.sprite.render()
            if self.flagged:
                self.flag_sprite.render()


    def hover_in(self):
        # I was going to do a bit of animation stuff but decided to save it
        # for a later tutorial as this one is more on structuring a game.
        self.sprite.alpha = 0.5

    def hover_out(self):
        self.sprite.alpha = 1


# Yikes! This tutorial getting long! And whats scary is that they will just be
# getting longer. Just bare with me a little longer, we are almost done here :)


class GameContorl(EventDispatcher):
    """
    Remember when we created an instance of this class and pushed it as a
    handler to our pyglet window? What that does is allows us to just define
    function such as on_mouse_press that are automatically called when the mouse
    is pressed for example.
    """
    def __init__(self, client):
        EventDispatcher.__init__(self)
        self.client = client

        # We need to keep track of which block we are pressing (if any). This
        # way we can have it so you have to press on and let up on a block
        # before it registers. (which is important as that's how people's
        # software works and how they expect the game to work)
        self.pressed_block = None

    def find_block_from_xy(self, x, y):
        """
        This function takes the x,y coordinates and finds which block it is
        hovering over.
        """
        # The // syntax is something that is new in python 3000. It means to
        # devide and have the result be an integer (apposed to only one slash
        # which would be a float). We do that first import at the top of this
        # file to make it work like it will in pythin 3k
        xy = x//20, y//20
        if self.client.blocks.has_key(xy):
            return self.client.blocks[xy]

    def on_mouse_press(self, x, y, button, modifiers):
        """ This is called from pyglet when a mouse button is pressed down. """
        b = self.find_block_from_xy(x,y)
        if b and not b.gameblock.discovered:
            self.pressed_block = b
            b.hover_in()

    def on_mouse_release(self, x, y, button, modifiers):
        """ This is called from pyglet when a mouse button is released. """
        if not self.pressed_block:
            if self.client.game.gameover:
                self.client.retry()
        else:
            b = self.find_block_from_xy(x,y)
            if b == self.pressed_block:
                if button == mouse.LEFT and b.flagged == False:
                    self.client.press_block(b)
                elif button == mouse.RIGHT:
                    # This may look a bit funny. flagged is a boolean. This is
                    # just setting itself to the opposite of what it was.
                    b.flagged = not b.flagged
            self.pressed_block.hover_out()
            self.pressed_block = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        This is called when the mouse is moved while a button is being held
        down.
        """
        if not self.pressed_block: return
        b = self.find_block_from_xy(x,y)
        if b != self.pressed_block:
            self.pressed_block.hover_out()
        else:
            self.pressed_block.hover_in()


# And that's it for all those classes! Now we create the game and client:
game = Game(size_xy=(30,10), percent_mines=0.15)
client = Client(game)

# And begin the infinite loop!
while True:
    client.loop()


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
