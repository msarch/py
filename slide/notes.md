

# nov 2016
----------
évolution des scenes:

    1- groupe de 1+4    
    2- les sliders epuvent laisser des traces (légèrement translucides
    3- les cellules peuvent se migrer et laisser des traces
    4- des bandes taille écran verticales et horiz glissent entre et sont modifiées

# aout 2016
-----------

recherche pour changement de couleurs:

   event system:
        - observer pattern
 

-------------------------------------------------------------------------------

- time is sliced into dt steps
- actions are rules applied every dt
- groups are lists of basic elements attached to actions
	(group of drawn elts : 
- basic elements :
	- groups NO-XYZ
 	- shapes XYZ
	- cells w. shapes XYZ
	- cells  w.o shape, i.e. a field NO-XYZ
- localised elements

         
- @rules : broadcast for next iteration
- @ shape , @ draw, @rules :NO LAYERS implement z instead

- TIMELINE ??? voir cocos (lifetime, blink...)


... /...

- record movement
- read svg
- scene manager (all dicts)+  parser (reads txt)
- PLY pour le polyhedre 
- 
# 25 nov 2014 / Event /  Model examples and discussion  
------------------------------------------------------
    ref : 
    - Events in Python
        http://www.valuedlessons.com/2008/04/events-in-python.html
    - Agents and Event Listeners for Python :
        http://blog.7co.cc/blog/2012/03/04/agents-and-event-listeners-for-python/
    - Simple event dispatcher in Python :
         http://www.expobrain.net/2010/07/31/simple-event-dispatcher-in-python/
         
         
*** Actors Model examples and discussion
-----------------------------------------

        T O D O
        

*** see cebas
--------------- 

from cebas, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, to search for the nearest/furthest particle within a specific radius

*** cebas thinking particles engine *
_____________________________________

ref: http://www.cebas.com/index.php?pid=product&prd_id=166&feature=1359


*** Rule-based Versus Event-driven Particle Systems
___________________________________________________  

- An event-driven particle system is based on "triggers" or events that must happen to activate an effect. This implies some kind of key frame related effects.
- thinkingParticles offers true Non Linear and procedural animation technology. Rules and conditions control the particle effects, regardless of the timing or number of frames that may change in an animation.


*** Rules
_________  

ThinkingParticles uses a 100% rule-based approach to create particle animations offering true Non Linear Animation (NLA). 

Example:
    To animate some cannons shooting at incoming targets. 
    How to do it - Rule based and with full use of NLA : 
         Create the cannon object
         Setup the shooting sequence of the cannon
         Create some targets
         Turn the cannons into particles
         Create a rule to aim at approaching targets when they are near
         Create a rule to shoot at the targets
         Create a rule to explode the targets when they get hit by a projectile


*** Object Access
_________________

A special operator, called ParamBlock enables the accessibility of all object parameters within thinkingParticles.  

The user may connect any particle parameter to an object parameter, or the other way around. In a scene, a particle may influence the position, color, size or segmentation of any 3ds Max object. It is possible to use the ParamBlock operator, to access every parameter of an object, and use it as an IDS (input data stream) or ODS (output data stream) connector. A radius of an object, for example, may control the particle speed or even age. A particle collision event, may control a Light On/Off parameter.


*** Memory Node
________________  

A memory node allows the storage of any kind of data.

The Memory node offers the storage of multiple variables along with multiple values per variable, on a "system-wide" basis. 

This means that every DynamicSet is able to access the stored values at any time, regardless of the number of nested DynamicSets used in a wired network. Values may be stored per particle or globally.


*** Condition Node
__________________

A powerful volume testing algorithm has been added to the thinkingParticles tool set. The InMesh condition node helps you to discover whether the particle is inside or outside a given mesh.


*** Advanced and powerful Nodes
_______________________________

like PSearch, open up a whole new world of particle effects that were never possible before. With the help of the PSearch node, it is an easy task to search for the nearest and furthest particle within a specific radius.

   !!! implement genral program struct with simplicity, more advanced behaviour is in world lmnts classes
  

# TICK *
________

    - depending on each lmn can have a simple struct with or w/o position and rotation or be a class with stored vertices and tick method followed by get_batch


*** From pybox2d : timeStep = 1.0 / 60 
**********************************************80


Typically we use a time step of 1/60 of a second (60Hz) and 6 velocity/2 position iterations. This provides a high quality simulation in most game scenarios.
 
**********************************************80
   
   DRAWING : as in spreading pyglets wings
   --------------------------------------- 
    - shapes are groups of primitives
    - shape.batch is collected with get_batch
    - drawing is done with batch.draw
    
            @QUESTION : 1 batch for each shape? multiple lmn with same batch @ diff pos? (
   
    @FUTURE 3 problemes
    -------------------
       1 input : svg files
            --> svgbatch 
       2 strorage of paths etc.. for transformation and then caching
            --> svgbatch 
                - better than svg from nodebox and than squirtle
                - clean
                - has path 
                - simple access to points
       3 combined kinematics (hinges)
            --> layers as in nodebox (+center of layer)
    
    
    SCENE is a folder
    -----------------
        actor1.py
            methods:
                draw()
                step()
                    listen()
                    update()
                    publish()
            fields : 
                alive
                startime / endtimr / cycle
        actor1.svg
                
**********************************************80

class Zulu:  Zulus objects ARE OBSOLETE ...........
--------------------------------------------------------------


# - zulus are NOT bodys, zulus may have bodys, one or a group
# - zulus may have bodies, and extra fields or values
# - zulus live ie : perform actions : ie have a step() method

    some parameters can be modified by rules

    STANDARD METHOD:

    STANDARD PARAMS :
        - self rules record
        - self Body
            - self shapes
                - self vertexes (ordered?)
        - position is GPU managed with OpenGL matrix translation
        - rotation is GPU managed with OpenGL matrix rotation
        - same parameters also at step+1

    OTHER OTIONAL RECORDS :
        - acceleration,
        - speed,
        - rotational speed and acc
        - any on demand
    """
    
    
#Superfolia code from NODEBOX
___________________________________________________________________     
**********************************************80

from math import sqrt
from math import sin, cos, radians
 
def radial_gradient(colors, x, y, radius, steps=300):
 
    """ Radial gradient using the given list of colors.
    """
 
    def _step(colors, i, n):
        l = len(colors)-1
        a = int(1.0*i/n*l)
        a = min(a+0, l)
        b = min(a+1, l)
        base = 1.0 * n/l * a
        d = (i-base) / (n/l)
        r = colors[a].r*(1-d) + colors[b].r*d
        g = colors[a].g*(1-d) + colors[b].g*d
        b = colors[a].b*(1-d) + colors[b].b*d
        return color(r, g, b)
 
    for i in range(steps):
        fill(_step(colors, i, steps))
        oval(x+i, y+i, radius-i*2, radius-i*2)  
 
def root(x, y, angle=0, depth=5, alpha=1.0, decay=0.005):
    
    """ Recursive root branches to smaller roots.
    """
    
    w = depth*6
    for i in range(depth*random(10,20)):
 
        v = float(depth)/5
        alpha -= i*decay
        alpha = max(0, alpha)
        
        if alpha > 0:
            
            # Next direction to grow in.,
            # e.g. between -60 and 60 degrees of current heading.
            angle += random(-60, 60)
            dx = x + cos(radians(angle)) * w
            dy = y + sin(radians(angle)) * w
            
            # Oval dropshadow.
            nostroke()
            fill(0, 0, 0, alpha*0.25)
            oval(x-w/6+depth, y-w/6+depth, w/3, w/3)
 
            # Line segment to next position.
            nofill()
            stroke(0.8-v*0.25, 0.8, 0.8-v, alpha)
            strokewidth((depth+1)*0.5)            
            line(x, y, dx, dy)
            
            # Colored oval.
            strokewidth((depth+1)*0.25)
            fill(0.8-v*0.25, 0.8, 0.8-v, alpha*0.5)
            oval(x-w/6, y-w/6, w/3, w/3)
            
            # Create a branching root.
            if random() > 0.8 and depth > 0:
                root(x, y, angle, depth-1, alpha)
            
            x = dx
            y = dy
    
    # Continue growing at less alpha and depth.
    if depth > 0:
        root(x, y, angle, depth-1, alpha)
 
size(600, 600)
radial_gradient(
    [color(0.05, 0.06, 0.0), color(0.125, 0.150, 0.0)],
    -150, -150,
    radius=900
) 
root(300, 300, angle=-90, depth=6)

**********************************************80

#Tendril code from NODEBOX
___________________________________________________________________   
 
**CODE:** 
   
    size(600, 600)
    from math import pi, sin, cos, radians
     
    class Tendril:
        
        def __init__(self, x, y, width=15):
            """ A new sinewy tendril at location x and y.
            Its segment width will gradually become smaller as it grows.
            """
            self.x = x
            self.y = y
            self.width = width
            self.angle = random(2*pi) - pi # random angle in radians.
            self.segments = []
            self.v = 0
     
        def grow(self, distance=3.0, curl=1.0, step=0.02):
            """ Tendril segment growth using fluid, spiral sine functions,
            taken from the ART+COM Tendrils class for Processing.
            """
            # Think of a tendril having a steering compass.
            # For each new segment, the compass shifts a bit left or right.
            self.x += cos(self.angle) * distance
            self.y += sin(self.angle) * distance
            self.v += random(-step, step)
            self.v *= 0.9 + curl*0.1
            self.angle += self.v
            self.segments.append(
                (self.x, self.y, self.angle)
            )
            
        def draw(self, path=None):
            """ Draws all the segments in the tendril,
            as separate ovals or as a single path if one is supplied.
            """
            n = len(self.segments)
            for i, (x, y, angle) in enumerate(self.segments):
                r = (1-float(i)/n) * self.width # size gradually decreases.
                if path != None:
                    path.oval(x, y, r, r)
                else:
                    oval(x, y, r, r)
            
    class Plant:
        
        def __init__(self, x, y, tendrils=30, width=15):
            """ A collection of tendrils.
            """
            self.x = x
            self.y = y
            self.tendrils = []
            for i in range(tendrils): 
                self.tendrils.append(
                    Tendril(self.x, self.y, width)
                )
        
        def grow(self, distance=3.0, curl=1.0, step=0.02):
            """ Grow a new segment on each of the plant's tendrils.
            """
            for b in self.tendrils:
                b.grow(distance, curl, step)
                
        def draw(self):
            """ Draw the plant.
            """
            for tendril in self.tendrils:
                tendril.draw()
            
        def path(self):
            """ Return the plant as a path consisting of ovals.
            """
            path = BezierPath()
            for tendril in self.tendrils:
                tendril.draw(path)
            return path
     
    background(0.12, 0.12, 0.06)
    nofill()
    stroke(1, 0.5)
    strokewidth(0.5)
     
    plant = Plant(WIDTH/2, HEIGHT/2, tendrils=20)
    for i in range(200): 
        plant.grow(curl=1.0, step=0.02)
     
    plant.draw()

**********************************************80

#Reférences
___________________________________________________________________

- components extra DATA fields --> **grease/base.py**
    - extra fields could be in RULE's field
- batch.draw(), background first, then bodies --> **spreading pyglet's wings**
- --> **nodebox**
- --> http://nodebox.net/code/index.php/Core_Image

**********************************************80

#TODO dec 2013
___________________________________________________________________

- BAKE FUNCTION
    - objects can be 'baked' after transformation
    - and maybe moved to a still group (no glmove) for optimization
- OPTIMISATION:
    - staticmethod optim
    - render with functions inlieu of classes methods?
- SHADERS
    - implement shaders (from nodebox graphics
- SPLINES & OTHER GEOM PRIMITIVES
    - use path for splines and oher bodys. Unify draw mode(shoebot/ nodebox /
    - text


##  @ ZULUS -------------------------------------------------------
# TODO ANCHORS
# bodys have an anchor to which displacements are applied

# TODO : ZULU CLASS
# anchor point and rot(or align-to  or look-at point) are zulu level,
# colors + linestyle are bodys (superclass) level
# zulus have a set of points
#   - one (number 0) is anchor
#   - others are geom(4 for recs, 3 for tri, 2 for lines etc..,
#   - extras are 'pegs' to anchor other geometries thus NO GROUPS are needed

# TODO : GROUPS
# implement groups similar to nobgl layers

##  TO DO SORTED ----------------------------------------------------

# 1 focus on input, animation and render(png,pdf, openGL) with RECTS only
# 2 zulus have points :
# 3 app structure : ZULU CLASS, ANCHORS, BAKE, COLOR STROKE & FILL
# 4 performance and render issues : VERTEX LISTS, 25 IMAGES/S, EXPORT
# 99 later : SHADERS, SUBPIXEL, SPLINES & OTHER bodyS

- REMOVED ----------------------------------------------------------
# CAMERA : useless, complicated, camera mvt not needed yet

##  TO DO OTHER  ------------------------------------------------------
- COLOR STROKE & FILL
# use named colors module -->ie styles module?
# kwd : program style

    
utiliser une table de correspondance rule/zulu
--------------------------------------------------------------------80
links : matrix or table use  (type 'gx' to open url)
http://stackoverflow.com/questions/15312273/traverse-a-graph-represented-in-an-adjacency-matrix?rq=1
http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch20s05.html

**********************************************80

--------------------------------------------------------------------80
SVG READ
--------------------------------------------------------------------80
#!/usr/bin/env python
"""\
Usage: drawsvg.py file
file  - one SVG file (from Inkscape!) that is all simple paths

"""
##    svg2py Copyright  (C)  2007 Donn.C.Ingle
##    http://cairographics.org/svgtopycairo/
##    Contact: donn.ingle@gmail.com - I hope this email lasts.
##
SVG paths can be parsed and turned into a seqence of cairo commands that re-draw them.

This took a while, the pyparsing had me in knots, but now it's short and sweet.
A fuller implementation of what can be done in SVG would be really nice. (Hint...)

Make sure you pass it a very simple SVG file (from Inkscape is best)
-- one that has had all the shapes reduced to paths.
Oh, and keep your canvas 400 by 400 or it may draw clear off the screen.

Depends on

elementree: import elementree as myDearWatson :) It's a great module for slicing through XML.
pyparsing: This module is deeply wonderful. I won't pretend to savvy even 1% of it, but it really does the job. They have a great mailing list where I got a lot of help. It let's you parse strings into lists and that is no small feat.
SVG Path element

To briefly explain, inside an svg file (which is just xml) you'll find a tag named 'g' and under that one or more tags named 'path'. Inside path there is an element called 'd'; that's the actual path. It's formed like this: "COMMAND NUMBER COMMA NUMBER Optionally[NUMBER COMMA NUMBER a few more times]", where COMMAND is M for move, L for line, C for curve and Z for close path. There may be others, but that's what I tackled. Have a look at the pyparsing grammar which makes it fairly clear how different commands have different numbers behind them.##

import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo
from pyparsing import *
import os, sys
from elementtree import ElementTree as et

# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def run(Widget):
    window = gtk.Window()
    window.set_size_request(400, 400)
    window.connect("delete-event", gtk.main_quit)
    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

## Do the drawing ##

class Shapes(Screen):
    def draw(self, ctx, width, height):

        #Build a string of cairo commands
        cairo_commands = ""
        command_list = []
        for tokens in paths:
            for command,couples in tokens[:-1]: #looks weird, but it works :)
                c = couples.asList()
                if command == "M":
                    cairo_commands += "ctx.move_to(%s,%s);" % (c[0],c[1])
                if command == "C":
                    cairo_commands += "ctx.curve_to(%s,%s,%s,%s,%s,%s);" % (c[0],c[1],c[2],c[3],c[4],c[5])
                if command == "L":
                    cairo_commands += "ctx.line_to(%s,%s);" % (c[0],c[1])
                if command == "Z":
                    cairo_commands += "ctx.close_path();"

            command_list.append(cairo_commands) #Add them to the list
            cairo_commands = ""
        #Draw it. Only stroked, to fill as per the SVG drawing is another whole story.
        ctx.set_source_rgb(1,0,0)
        for c in command_list:
            exec(c)
        ctx.stroke()

***************************************************************##

#Check args:
if len(sys.argv) < 2:
    raise SystemExit(__doc__)
file = sys.argv[1]

***************************************************************##

## Pyparsing grammar:
## With HUGE help from Paul McGuire <paul@alanweberassociates.com>
## Thanks!
dot = Literal(".")
comma = Literal(",").suppress()
floater = Combine(Optional("-") + Word(nums) + dot + Word(nums))
## Unremark to have numbers be floats rather than strings.
#floater.setParseAction(lambda toks:float(toks[0]))
couple = floater + comma + floater
M_command = "M" + Group(couple)
C_command = "C" + Group(couple + couple + couple)
L_command = "L" + Group(couple)
Z_command = "Z"
svgcommand = M_command | C_command | L_command | Z_command
phrase = OneOrMore(Group(svgcommand))

## Find and open the svg file
xml_file = os.path.abspath(__file__)
xml_file = os.path.dirname(xml_file)
xml_file = os.path.join(xml_file, file)

tree = et.parse(xml_file)

ns = "http://www.w3.org/2000/svg" #The XML namespace.
paths = []
for group in tree.getiterator('{%s}g' % ns):
    for e in group.getiterator('{%s}path' % ns):
        p = e.get("d")
        tokens = phrase.parseString(p.upper())
        paths.append(tokens) # paths is a global var.

run(Shapes)

**********************************************80

*** fonction sinus améliorée
___________________________  

def cos_sin_deg(deg):
    """Return the cosine and sin for the given angle
    in degrees, with special-case handling of multiples
    of 90 for perfect right angles
    """
    deg = deg % 360.0
    if deg == 90.0:
        return 0.0, 1.0
    elif deg == 180.0:
        return -1.0, 0
    elif deg == 270.0:
        return 0, -1.0
    rad = math.radians(deg)
    return math.cos(rad), math.sin(rad)


**********************************************80

*** NOTES oct 2013
__________________  

TODO :
------
- read code from PARTICLE ENGINES, ruels, update sequence,force fields?



**********************************************80

*** sept 2013
_____________  

animation 2
-----------


# TODO #1
# Every zulu folows a scenario that schedules a number of rules for a period of time.
# Moving in a direction is a rule
# Boucing on an obstacle is a rule
# Changing color at some moment, appearing and disapearing are rules

# TODO #2
# ajust the general scale of objects relative to screen center
# adjust the general speed of movements




**********************************************80

animation
---------
all zulus properties may have an 'animate' or 'update' method overriding the zulu class empty update method

r1=zulu()
r1.shape
   def update()
      shape = f(t)
r1.pos=(x=0,y=0,z=0)
   def update()
     x = f(t), y= f(t)
r1.movement_function=
    def update(dt)
        x,y=(a*t, sin(t))
r1.color
   def update(dt)
      color = f(t)

Questions:
----------

Regler le pb d'update des AABB pour les objets après leur transformation
Among their many advantages, managed attributes are used 
	- to protect an attribute from changes or 
	- to automatically update the values of a dependant attribute.

Logiques possibles en animation.
    - comportements individuels
        --> gérer les collisions ou non 
        --> orientation 'jeu video' et 'automates'
    - gérer des scenarios en fonction du temps écoulé
        --> implémenter une variable temps total
        --> voir grease: world est une variable globale
    - solution mixte : semi-autonomie + events scénarisés

@ version 1.0 slim
------------------
    - gerer de façon simple la sortie d'ecran 
        - test position
        - ou longueur max 
        --> remove element from list
    - implém. les'autres elts navigateurs
    - regrouper dans 1 fichier unique pour 'distrib'
@ futur
-------
    - ce ne sont pas les shapes mais une super-classe qui sont les elts de base
        - ces elts ont des attributs : shape, comportements etc..
        - par ex.ne pas structurer : 
               - shape
                    - bool 'en_vie'
                    - speed
                    - color
        mais :
                - entity
                    - shape
                    - bool 'en_vie'
                    - speed
                    - color



    - gerer le temps :
        - component is aging each dt: age += dt, then check if dead
    - gerer des élements déclencheurs
    - autonomie des mobiles
    - unifier les representations avec Vec2d, arrays, 
    - les elements mobiles ou pas ont une methode step ou pas
---
# Looking at Casey Duncan's 'Grease' code
*******************************************************************************


Ref :
----
http://pythonhosted.org/grease/index.html

Time tracking
-------------

[docs]	def tick(self, dt):
		"""Tick the mode's clock, but only if the world is currently running
		
		:param dt: The time delta since the last tick
		:type dt: float
		"""
		if self.running:
			super(World, self).tick(dt)
	

[docs]	def step(self, dt):
		"""Execute a time step for the world. Updates the world `time`
		and invokes the world's systems.
		
		Note that the specified time delta will be pinned to 10x the
		configured step rate. For example if the step rate is 60,
		then dt will be pinned at a maximum of 0.1666. This avoids 
		pathological behavior when the time between steps goes
		much longer than expected.

		:param dt: The time delta since the last time step
		:type dt: float
		"""
		dt = min(dt, 10.0 / self.step_rate)
		for component in self.components:
			if hasattr(component, "step"):
				component.step(dt)
		for system in self.systems:
			if hasattr(system, "step"):
				system.step(dt)

[docs]	def on_draw(self, gl=pyglet.gl):
		"""Clear the current OpenGL context, reset the model/view matrix and
		invoke the `draw()` methods of the renderers in order
		"""
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
		gl.glLoadIdentity()
		for renderer in self.renderers:
			renderer.draw()
Collision :
-----------
There are two major steps to collision handling in Grease:
    collision detection and 
    collision response. 
    
The detection step happens within the collision system. 

A set of pairs of the currently colliding entities can be found in the collision_pairs attribute of the collision system. Applications are free to use collision_pairs directly, but they can also register one or more handlers for more automated collision response. 

Collision handlers are simply functions that accept the collision system they are configured for as an argument. 

The handler functions are called each time step to deal with collision response.

---
# Looking at Casey Duncan's 'Planar'
*******************************************************************************





---
# Computational Geometry : 2D Afine Transformation matrixes
*******************************************************************************

Ref:
---
http://en.wikipedia.org/wiki/Transformation_matrix

- Affine transformations preserve collinearity and relative distancing :
	- points on a line will remain in a line after an affine transformation 
	- parallel lines remain parallel 
	- relative spacing or distancing,
        (may scale, but will always maintain at a consistent ratio.)
- Affine transformations allow for repositioning, scaling, skewing and rotation. 
- Things they cannot do include tapering or distorting with perspective.
- Toutes les transformations affines peuvent se calculer avec des matrices.


Normalement pour un point 2d à deux coordonnées (x,y):
	- L¿homothétie et la rotation se calculent par multiplication de matrices
		[x']   [a b]   [x]
		[y'] = [c d] * [y]
	- La translation se calcule par addition de matrices
		[x']   [Tx]   [x]
		[y'] = [Ty] + [y]
alors que pour un point 3d toutes les operations affines sont de la forme :
		[x']   [a b c]   [x]
		[y'] = [d e f] * [y]
		[z']   [g h i]   [z]
		
A trois coordonnées, avec des matrices qui sont toujours carrées,
on peut composer plusieur transformations en multipliant les matrices 
correspondant à chaque opération DANS UN ORDRE PRECIS.

Si le point 2D devient artificielement un vecteur à 3 coordonne¿es (x,y,z) 
(par défaut on fixe z=1), la matrice générale des transformations 2d devient :
		[x']   [a b m]   [x]   [ax + by + mz]   [ax + by + mz]
		[y'] = [c d n] * [y] = [cx + dy + nz] = [cx + dy + nz] 
		[z']   [0 0 1]   [z]   [0x + 0y + 1z]	   [     1      ]

Nous quittons maintenant le domaine de la ge¿ome¿trie euclidienne pour 
entrer dans celui de la ge¿ome¿trie projective, outil géométrique très puissant.

Matrice type de mise a¿ l'e¿chelle 
--------------------------------
		[Sx  0  0]
		[ 0 Sy  0]
		[ 0  0  1]
Matrice de rotation
------------------
		[ cos¿ ¿sin¿    0] 
		[ sin¿  cos¿    0]
		[   0     0     1]
Matrice de Translation
----------------------
		[ 1  0  dx]
		[ 0  1  dy]
		[ 0  0   1]
		
Re¿flexion d'un point par rapport a¿ un axe (transformation miroir)
-----------------------------------------------------------------
- Par rapport à l¿axe des y :
		[-1  0  0] 
		[ 0  1  0]
		[ 0  0  1]
		
- Par rapport à l¿axe des x :
		[ 1  0  0] 
		[ 0 ¿1  0]
		[ 0  0  1]
		
- Par rapport a¿ l¿origine :
		[¿1  0  0] 
		[ 0 ¿1  0]
		[ 0  0  1]
		
		
Composition is accomplished by matrix multiplication. 
If A and B are the matrices of two linear transformations,
then the effect of applying first A and then B to a vector x is given by:
	B(Ax) = (BA)x
	
Rotation autour d'un point arbitraire
-------------------------------------
- La rotation autour d'un point arbitraire s'exprime comme une combinaison de:
    ¿ Une translation du point arbitraire vers l'origine 
	¿ Une rotation autour de l'origine
	¿ Une translation de l'origine vers le point arbitraire

Homothe¿tie par rapport a¿ un point arbitraire
--------------------------------------------
L'homothe¿tie (ou changement d'e¿chelle) par rapport a¿ un point arbitraire
se de¿compose :	- Translation du point arbitraire vers l'origine
	- Homothe¿tie par rapport a¿ l'origine
	- Translation inverse de l'origine vers le point arbitraire

multiplication de matrices carrées 3x3:
--------------------------------------
		[a b c]   [A B C]   [aA+bD+cG  aB+bE+cH  aC+bF+cI]
		[d e f] * [D E F] = [dA+eD+fG  dB+eE+fH  dC+eF+fI]
		[g h i]   [G H I]   [gA+hD+iG  gB+hE+iH  gC+hF+iI]


The identity matrix 
-------------------
An important matrix is the identity matrix:

	  | 1 0 0 |
	I=| 0 1 0 |
	  | 0 0 1 |
It transforms a point to itself: P1=P2=I·P1

This can be interpreted as

- translation with (0,0)
- rotation with 0 degrees, since cos (0)=1 and sin (0) =0
- scaling with (1,1)


In python :
-----------
Nested lists are often used to represent matrices. For example, the matrix:
		[a b c]
		[d e f]
		[g h i]
might be represented as a list with three elements, where each element 
is a row of the matrix. 
>>> matrix = [[a, b, c], [d, e, f], [g, h, i]]

The identity matrix would be :
>>> matrix = [[1, 0, c], [0, 1, 0], [0, 0, 1]]

In OpenGL
---------
To understand how OpenGL's transformations work, we have to take a closer
look at the concept: current transformation matrix. It means that OpenGL
always multiply coordinate values in drawing commands with the current matrix,
before they are processed further and eventually, after more transformations,
are rendered onto the screen. The basic drawing command in OpenGL, 
for plane and space respectively:

  glVertex2(x,y)
  glVertex3(x,y,z)
	
The position vector which are described by the parameters is multiplied 
with the current transformation matrix, before it is processed further on
its way to the screen. glVertex is in principle the only basic drawing
primitive in OpenGL.

The identity matrix doesn't do anything with the coordinates. 
In OpenGL there is ALWAYS a current model matrix that all of the 
points are multiplied with. To avoid any unwanted transformation, 
the identity matrix must be set to be the current transformation matrix with :
  glLoadIdentity()
	
OpenGL has three basic functions that make up the current transformations
matrix, in addition to glLoadIdentity():

  glTranslate()
  glRotate()
  glScale()
	
When we call one of these the current transformations matrix is affected 
by the new transformation matrix that is multiplied with it.

The example with rotation around another point than the origin, can be 
realized like this in OpenGL: 
	  Geometric operation	 / OpenGL-call	 /  Current matrix M
	- Reset the transformations	 / glLoadIdentity() / M=I
	- Translate origin to a	 /  gltranslate(1,1,0) / M =I·T1
	- Rotate /  glRotate(90,0,0,1)	/ M= I·T1·R
	- Translate origin back	 / gltranslate(-1,-1,0)  / M= I·T1·R·T2
	- 
We see that the rotation function has parameters that both gives the 
rotation and the rotation axis.


---
# Computational Geometry : Detecting Whether Two AABB Boxes Overlap
*******************************************************************************

from : http://gamemath.com/2011/09/detecting-whether-two-boxes-overlap/

The acronym AABB is often used for axially-aligned bounding box.
¿axially-aligned¿ means that the sides are parallel to the x- and y-axes; 

With very high frequency one answers with the incorrect solution discussed below, work through some examples, and arrive at the correct one. 

Most experienced web/GUI programmers have worked with 2D boxes and have encountered the problem, and should know the proper solution. However, they often do not immediately perceive the principle that extends the idea beyond AABB¿s to arbitrarily-oriented boxes. In summary, it¿s a problem with a deceptively simple starting point and many branching points depending on the skill of the applicant, which is precisely why it¿s a great interview question.

Let¿s say that we have basic 2D vector and bounding box classes such as:

// Simple 2D vector class
struct Vec2D
{
    float x,y;
};
 
// 2D axially-aligned bounding box.
struct Box2D
{
    Vec2D min, max;
};


So the goal of the question is a function with a prototype such as

bool BoxesIntersect(const Box2D &a, const Box2D &b);
When faced with this problem, inexperienced programmers produce a particular solution that doesn¿t work with such regularity, that it is worth mentioning. They suggest to check the four corners of box A, to see if any are containing within box B, and also check B¿s corners to see if they are contained within A. But this approach fails in the following example.



The correct approach is to work by process of eliminating situations when the two AABB¿s do not intersect? 
The boxes cannot intersect if :
	- if A is completely to the left of B, 
	- or completely to the right 
	- or completly above 
	- or completly below. 

Are there any other cases to consider? No. If A is completely to the left or right of B, then the vertical positions of the boxes do not matter. If two boxes do not intersect, they will fit into at at least one of the four cases just mentioned. 


This is the correct answer:

bool BoxesIntersect(const Box2D &a, const Box2D &b)
{
    if (a.max.x < b.min.x) return false; // a is left of b
    if (a.min.x > b.max.x) return false; // a is right of b
    if (a.max.y < b.min.y) return false; // a is above b
    if (a.min.y > b.max.y) return false; // a is below b
    return true; // boxes overlap
}

# Python modules and scripts used for reference:
*******************************************************************************

    - 'planar'
    - 'matrix' from kai chang (http://www.syntagmatic.net)
    - 'nodebox'
        - 'nodebox.graphics.geometry' --> 2d geometry operations, classes
        - 'nodebox.graphics.context'  --> interface w/pyglet
    - 'pyglet' --> opengl



*** first notes
_______________  

@REFERENCES
-----------
- pyglet tutorial
- pyglet programming guide
- nodebox GL
- Casey Duncan, Planar lib
- Casey Reas, structures
- Kay Chang, matrix multiplication in python
- Langton's ants


@FUTURE
-------
gr1=actor
gr1.shape=star(size=2,n=5)
gr1.pos=(x=0,y=0,z=0)
gr1 has no color 
gr1.movement.path= "line, 
gr1.movement.speed= 3
gr1.movement.duration= 10000
gr1.interactions = canvas_collision( 

@QUESTIONS
-----------

Logiques possibles en animation.

    - comportements individuels pré-programmés
        --> gérer les collisions ou non
        --> orientation 'jeu video' et 'automates'
        
    - gérer des scenarios en fonction du temps écoulé
        --> implémenter une variable temps total
        --> voir grease: world est une variable globale
        
    - solution mixte : semi-autonomie + events scénarisés




