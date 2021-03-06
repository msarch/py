
import sys, os

import_error = None # lib import errors

try :
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
    from OpenGL.GL import *
except ImportError:
    import_error = 'pyOpenGL'

try: # only for importing the image files
    import pygame
except ImportError:
    import_error += ' pygame'

if import_error :
    print '*'*10
    print 'Mirra > graphics.py : ImportError, could not import %s . It must be installed in your system to run Mirra' % (import_error)
    print '*'*10
    import sys
    sys.exit() # quit

from utilities import *



""" Contains the OpenGL drawing funcitionality, renders and step() the graphicStack 
    Objects get rendered in the order they are in the stack, despite of their z location (Check Stack class at py)
    it knows how to render leaving trails and change the bgcolor of the window
"""    

# GLOBALS ###
graphicsStack = [] #Stack() # as global variable in this module because it needs to be accessed from Base class init method

textures = {} # class property. loaded textures dictionary
selectedObj = None
circleresolution = 60 # how many points form the circles, 60 seems to be ok for big ones
q = gluNewQuadric() # because if i do it as global there is an error on osx and linux, therefore it is a prop

bitmapFonts = {
    'typewriter': (
        (GLUT_BITMAP_8_BY_13, 13),
        (GLUT_BITMAP_9_BY_15, 15)
    ),
    'timesroman': (
        (GLUT_BITMAP_TIMES_ROMAN_10, 10),
        (GLUT_BITMAP_TIMES_ROMAN_24, 24)
    ),
    'helvetica': (
        (GLUT_BITMAP_HELVETICA_10, 10),
        (GLUT_BITMAP_HELVETICA_12, 12),
        (GLUT_BITMAP_HELVETICA_18, 18)
    )
}


###########################
# stack related functions

def newZ(newz, obj) :
    if obj in graphicsStack : remove(obj) # out
    addAt(newz, obj) # and back to new z

def remove(obj) : # called from objects when they end() !
    graphicsStack.pop(graphicsStack.index(obj)) 

def addAt(z, obj):
    """ looks for right place in stack for given objects Z loc
    Stack is orderer from bigger to smaller z index.
    Objects on the left side render on top of object on the right
    note that the object's z prop is not the same as its index in the list
    this just determines the hierarchy, given a stack with two objects A with z=1 and B
    with z=4000 , A would be the last to render because its z is lower, and B would be the first.
    If a 3rd object C is introduced it checks for the others z and gets inserted on the right location
    being C before any other object with same z prop (goes on top of its z)
    SO the rendering order is INVERSE to the number given by the z, the higher z number gets the 1st
    rendering location (bottom)
    """
    for o in graphicsStack : #find your place
        if o.z == z :
            i = graphicsStack.index(o) + 1 # where are you + 1?
            graphicsStack.insert(i, obj) # after this one
            return 
        elif o.z > z : # after because rendering left to right
            graphicsStack.insert(graphicsStack.index(o), obj) # in front of this one
            return 
    # bigger z than anyone, or stack was empty
    graphicsStack.append(obj) # just put it in the end



#############################
# texture functions

def loadTexture(path) :#name):
    """ load texture. to be acced from Bitmap and BitmayPoligon
    """
    if textures.has_key(path) :
        return textures[path] # import it only once

    surface = pygame.image.load(path) # need to remove dependency from pygame
    if surface.get_alpha is None:
       surface = surface.convert()
    else:
       surface = surface.convert_alpha()

    bin = pygame.image.tostring(surface, "RGBA", 1) # need to remove dependency from pygame
    w, h = surface.get_width(), surface.get_height()

####        # Wx code. Needs to pass alpha too
####        image = wx.Image(path, wx.BITMAP_TYPE_ANY)
######        image.ConvertAlphaToMask(220)
######        image = image.ConvertToBitmap()
####        bin = image.GetData()
####        w,h = image.GetWidth(), image.GetHeight()
####        if image.HasAlpha() :
####            alpha = image.GetAlpha()
######            print 'alpha', alpha
######        print 'bin', bin

    textid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textid)

######        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
######        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
######        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, bin )
    
    gluBuild2DMipmaps(GL_TEXTURE_2D, 4, w, h, GL_RGBA, GL_UNSIGNED_BYTE, bin)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE) # GL_MODULATE, GL_DECAL, GL_BLEND, or GL_REPLACE
##        >>>> GL_MODULATE # to get bitmap blended (Tom) # replace works ok but no image blend 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # GL_CLAMP
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # GL_CLAMP

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    textures[path] = textid
    return textid


def deleteTexture(txt):
    # TO DO : need to check if any one is still using it before deleting it
    if textures.has_key(txt) : # if there
        try :
            p = textures.get(txt)
            textures.pop(p)
        except :
            pass # already deleted or non existent txt
        glDeleteTextures(txt)

###########################



##    def screenshot( path_prefix='.', format='PNG'):
##        """Saves a screenshot of the current frame buffer.
##        The save path is <path_prefix>/.screenshots/shot<num>.png
##        The path is automatically created if it does not exist.
##        Shots are automatically numerated based on how many files
##        are already in the directory."""
##        import Image, os
##        dir = os.path.join(path_prefix, '.screenshots')
##        if not os.path.exists(dir):
##            os.makedirs(dir)
##        index = len(os.listdir(dir))
##        path = os.path.join(dir, 'shot' + str(index) + '.png')
##        glPixelStorei(GL_PACK_ALIGNMENT, 1)
##        data = glReadPixels(0, 0,
##            width, height, GL_RGB, GL_UNSIGNED_BYTE)
##        image = Image.fromstring("RGB",
##            (width, height), data)
##        image = image.transpose( Image.FLIP_TOP_BOTTOM)
##        image.save(path, format)
##        print 'Image saved to %s'% (os.path.abspath(path))

    
def checkMouseIntersection( x, y, flag ) : 
    """ checks for intersection between mouseloc and interactive objects on graphicStack. If there is a hit it
    tries to trigger the event defined on the argument flag
    """
    global selectedObj
    hit = None  # reset first
    
    if selectedObj is None : # if none already selected check for intersections
##        for obj in graphicsStack.stack[:][::-1] : # copy and reverse
        for obj in graphicsStack[:][::-1] : # copy and reverse
            if obj.interactiveState > 0 : #and obj.visible : # only the ones visible and listening to the mouse
                if obj.intersects(x,y):
                    hit = obj # this is the one, exit loop
                    break
    else:
        hit = selectedObj # there was one already selected


    if hit : # there has been a click,
        if flag == "mouseDown":
            if hit.mouseDown(x,y) == -1 :
                return None # pass mousedown event to background
            else :
                selectedObj = hit
        elif flag == "mouseUp":
            if hit.mouseUp(x,y) == -1 :
                return None # pass mouseup event to background
            else :
                hit.mouseUp(x,y)
                selectedObj = None
        elif flag == "mouseDragged":
            hit.mouseDragged(x,y)
##        elif flag == "mouseMoved": # it is too much to test for mouseenter all the time
##           hit.mouseEntered(x,y)
        elif flag == "rightMouseDown":
            hit.rightMouseDown(x,y)
            selectedObj = hit
        elif flag == "rightMouseUp":
            hit.rightMouseUp(x,y)
            selectedObj = None
        # elif flag is "mouseDClick":
        #   hit.mouseDClick(x,y)
        return hit
    elif selectedObj :
        selectedObj.mouseDragged(x,y) # there is one clicked
        return selectedObj
    else:
        return None # clicked on stage


###########

def start( s=(640,480), c=(1,1,1,0), t=0, sm=0, m='2D' ) :
    """ inits main Engine instance's variables
    """
    global mode, size, trails, smooth,  bgColor
    
    mode = m
    smooth = sm
    size = s # w and h
    trails = t # leave trails

    if len(c) == 4 :
        bgColor = c
    else :
        bgColor = c[0], c[1], c[2], 0
        
    restart() # set opengl stuff

    glutInit([]) # avoid problem on Linux when drawing text --  ERROR:  Function <glutBitmapCharacter> called without first calling 'glutInit'.

    

##    def getSmooth(self): return __smooth
##    def setSmooth( b):
##        __smooth = b
##        if b :
##            glPushAttrib(GL_COLOR_BUFFER_BIT | GL_ENABLE_BIT);
##            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
##            glEnable(GL_LINE_SMOOTH);
##            glEnable(GL_BLEND);
##            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
##        else :
##            glPopAttrib()
##    smooth = property(getSmooth, setSmooth)


def restart() :
    """ inits GL modes
    # about depth : i could either render all on same Z (needs depth buffer) and then remode the z from all objects
    # another way is to have the loc signed by the render loop, depth not needed as they all render in diff layers
    # finally i could let z be set by their z propt then i need to have depth
    """
    glDepthFunc(GL_LEQUAL) # GL_LESS
    glEnable(GL_DEPTH_TEST) # enable depth buffer

    glClearDepth(1.0)
    glClearColor(bgColor[0], bgColor[1], bgColor[2], 0) # bg color, no blend
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear color and depth buffer
    
    glDisable(GL_DITHER)  # improves performance
    glShadeModel(GL_FLAT) # improves performance
    
    glMatrixMode(GL_PROJECTION)     # set to proyection mode
    glLoadIdentity()                # load identity matrix -> reset 3D world view

    if mode=='2D' :
        # set proyection to screen size to allow 1:1 mapping and (0,0) to be on left bottom
        glOrtho(0, size[0],  size[1], 0, 5000, 0) # glOrtho(left, right, bottom, top, zNear, zFar)
    else :# 3D
        # glFrustum(left, right, bottom, top, zNear, zFar)
        # gluPerspective(fovy, aspect, zNear, zFar) 
##            glFrustum(0, size[0], size[1], 0, 5000, 1)
        gluPerspective(10, size[0]/float(size[1]), 5000, 0) 
        
    glMatrixMode(GL_MODELVIEW)  # back to modeling mode
    glLoadIdentity()  # again

    glEnable(GL_BLEND) # enable blend before render blended objects (all should be)
##        glDepthMask(GL_FALSE) #!
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # GL_ONE # GL_DST_ALPHA

##def step() : pass
##        for o in graphicsStack : 
##            o.step()        

def end():
    for o in graphicsStack : 
        o.end()

def render() : #, fcount):
    """ clears blackground and loops the stack passing position in list and reference to engine (self).
        All shapes are now blended.
        Note : two choices. 1- disable depth and render all in diff z position
        2 - enable blend and render all in same z position.
        need to make some tests
    """
####        if smooth :
####    glPushAttrib(GL_COLOR_BUFFER_BIT | GL_ENABLE_BIT);
##    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
##    glEnable(GL_LINE_SMOOTH);
##    glEnable(GL_BLEND);
##    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
##        glClearDepth(1.0)
    glClearColor(bgColor[0], bgColor[1], bgColor[2], 1) 

    if trails : # and fcount > 3 : # make sure it cleans buffer
        glClear(GL_DEPTH_BUFFER_BIT) # leave trails
    else: # GL_ACCUM_BUFFER_BIT | GL_STENCIL_BUFFER_BIT
         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for o in graphicsStack : 
        o.render() 
        o.step()    

##        if smooth :
##    glPopAttrib()
            


######################
    
    
def drawText( text='', x=0, y=0, z=0, font="helvetica", size=10, color=(0,0,0,1)):
    """ Draw text at position, with font, size and with color.
    available font are
    typewriter 13 and 15
    timesroman 10 and 24
    helvetica 10,12 and 18
    TO_DO : rotation
    """
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)

##        glPushMatrix() # remember previous matrix state before translating, rotating
    glRasterPos3f(x, y, -z)

    current = GLUT_BITMAP_8_BY_13
    if bitmapFonts.has_key(font): # this type
        for s in bitmapFonts[font]:
            if s[1] == size : # this size
                current = s[0] # get the font

    for c in text:
        glutBitmapCharacter(current, ord(c))

##        glPopMatrix() # back to previous matrix state



def drawPixel( x, y, z=0, color=(0,0,0,1)):
    """ drawPixel( x, y, z=0, color=(0,0,0,1))
        Draws a pixel at a given x and y with given color .
        Color = 3 or 4 arg tuple. RGB values from 0 to 1 being 1 max value (1, 1, 1) would be white
    """
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)
        
    glPushMatrix() # remember previous matrix state before translating, rotating
    glTranslatef(x, y, -z) # translate to point to draw

    glBegin(GL_POINTS) # draw point
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    glPopMatrix() # back to previous matrix state


def drawLine( p1, p2, z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
    """ drawLine( p1, p2, z=0, color=(0,0,0,1), stroke=0, rotation=0.0)
        p1, p2 are two tuple points and color is tuple rgb, values range 0 to 1
        Rotation in degrees. clockwise.
    """
    x = abs(p1[0] + (p2[0] - p1[0]) * 0.5) # calc loc point
    y = abs(p1[1] + (p2[1] - p1[1]) * 0.5) 
        
    p1x = x - p1[0] # calc pixels points relative to loc pixel point
    p1y = y - p1[1] 
    p2x = x - p2[0]
    p2y = y - p2[1]

    drawLineRel(x, y, (p1x,p1y), (p2x,p2y), z, color, stroke, rotation, style)


def drawLineRel( x, y, p1, p2, z=0, color=(0,0,0,1), stroke=1, rotation=0.0, style=0):
    """ drawLine(  x, y, p1, p2, z=0, color=(0,0,0,1), stroke=0, rotation=0.0)
        p1, p2 are two tuple points RELATIVE to x,y
        Rotation in degrees. clockwise.
    """
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)
           
    glPushMatrix()

    glTranslatef(x, y, -z) # translate to GL loc ppint
    glRotatef(rotation, 0, 0, 0.1)

    if style :
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, style)
        
    if stroke <= 0: stroke = 1
    glLineWidth(stroke)

    glBegin(GL_LINES)
    glVertex2fv(p1)
    glVertex2fv(p2)
    glEnd()

    if style : glDisable(GL_LINE_STIPPLE)
    
    glPopMatrix()


def drawVertex( x, y,  z=0, v=(), color=(0,0,0,1), stroke=0, rotation=0.0,
               style=0):
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)
        
    glPushMatrix()

    glTranslatef(x, y, -z)
    glRotatef(rotation, 0, 0, 0.1)

    if style :
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, style)
##        else :
##            glDisable(GL_LINE_STIPPLE)
##            0xF0F0 # dashed line
##            0xF00F # long dashed line
##            0x8888 # dotted lines
##        glRect(x1,y,1,x1,x2)
##        glRectiv(v1,v2) # oposite vertex of rectangle
    # -- start drawing
    if stroke : # outlined polygon
        glLineWidth(stroke)
        glBegin(GL_LINE_LOOP)
    else: # filled polygon
        if   len(v) == 4 : glBegin(GL_QUADS)
        elif len(v)  > 4 : glBegin(GL_POLYGON)
        else :                 glBegin(GL_TRIANGLES) # which type of polygon are we drawing?

##        for i, p in enumerate(v):
##            glVertex2fv(p)  # draw each vertex
    for p in v :
        glVertex2fv(p)  # draw each vertex

    glEnd()
    # -- end drawing
    
    if style : glDisable(GL_LINE_STIPPLE)
    
    glPopMatrix()
    


def drawTexturedVertex( x, y,  z=0, v=(), rotation=0.0, texID=None, texCoord=[]):
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)        
    glPushMatrix()

    glTranslatef(x, y, -z)
    glRotatef(rotation, 0, 0, 0.1)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texID)

    # -- start drawing
    if   len(v) == 4 : glBegin(GL_QUADS)
    elif len(v)  > 4 : glBegin(GL_POLYGON)
    else :                glBegin(GL_TRIANGLES) # which type of polygon are we drawing?

    for i, p in enumerate(v) :
        glTexCoord2dv(texCoord[i])    # set vertex texture coordinate
        glVertex2fv(p)  # draw each vertex

    glEnd()
    # -- end drawing
            
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D) # disable in case it was on
    

def drawPolygon( v=[], z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
    """ drawPolygon( v=[], z=0, color=(0,0,0,1), stroke=0, rotation=0.0, texID=None, texCoord=[])
        v is an array with tuple points like [(x, y), (x2, y2), (x3, y3)]
        min vertex number to draw a polygon is 3
        stroke=0 to fil with color the inside of the shape or stroke=N just to draw N-px thick outline.
        Note. It doesnt work with non covex polygons, need to implement tesselation yet
    """
    l,t,r,b = calcPolygonRect(v)
    x,y = calcRectCenter(l,t,r,b)
    drawVertex(x, y, z, [(i[0] - x, i[1] - y) for i in v], color, stroke, rotation, style)


def drawRect( x=1, y=1, z=0, width=10, height=10, color=(0,0,0,1), stroke=0,
             rotation=0.0, style=000000):
    """ drawRect( x=1, y=1, z=0, width=10, height=10, color=(0,0,0,1), stroke=0, rotation=0.0, texID=None, texCoord=[])
        draws a rect, uses drawPolygon passing the vertex list calculated from loc, width and height
    """
    v = [ (i[0] - x, i[1] - y) for i in calcRectQuad(x, y, width, height) ]
    drawVertex(x, y, z, v, color, stroke, rotation, style)


def drawCircle( x, y, z=0, radius=1, color=(0,0,0,1), stroke=0, rotation=0.0,
               texID=None, texCoord=[], style=GLU_FILL): 
    """ drawCircle( x, y, z=0, radius=5, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL)
        x, y, z, width in pixel, rotation, color and line width in px
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
        TO DO : textured circles
    """
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)
        
    glPushMatrix()

    glTranslatef(x, y, -z)
    glRotatef(rotation, 0, 0, 0.1)

    if radius < 1 : radius = 1

    if stroke :
        inner = radius - stroke # outline width
        if inner < 0: inner=0
    else :
         inner = 0 # filled
    
    gluQuadricDrawStyle(q, style)

    gluDisk(q, inner, radius, circleresolution, 1) # gluDisk(quad, inner, outer, slices, loops)
        
    glPopMatrix()
    

def drawArc( x, y, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke = 0,
            rotation=0.0, texID=None, texCoord=[], style=GLU_FILL) :
    """ drawArc( x, y, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke = 0, rotation=0.0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)

    glPushMatrix()

    glTranslatef(x, y, -z)
    glRotatef(rotation, 0, 0, 0.1)

    if stroke : 
        inner = radius - stroke
        if inner < 0: inner=0
    else :
        inner = 0 # full, no inner
    start -= 180
    
    gluQuadricDrawStyle(q, style)
    
    gluPartialDisk(q, inner, radius, circleresolution, 1, start, sweep)
    
    glPopMatrix()



## glLineStipple	
## glPolygonStipple

##glReadPixels(x, y, 1, 1, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)

##    glBitmap draw a bitmap
##    glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv draw a rectangle


    

def drawEllipse( x, y, z=0, width=10, height=10, color=(0,0,0,1), stroke=0, rotation=0.0,
               texID=None, texCoord=[], style=GLU_FILL) :
##    print 'ellipse'
##        if glGetFloatv(GL_CURRENT_COLOR) != color : glColor4fv(color)
    glColor4fv(color)

    glPushMatrix()

    glTranslatef(x, y, -z)
    glRotatef(rotation, 0, 0, 0.1)

    if stroke : 
        inner = radius - stroke
        if inner < 0: inner=0
    else :
        inner = 0 # full, no inner
    
    gluQuadricDrawStyle(q, style)
    glScalef(width, height, 1)
    gluDisk(q, inner, radius, circleresolution, 1) # gluDisk(quad, inner, outer, slices, loops)
    
    glPopMatrix()
                  




