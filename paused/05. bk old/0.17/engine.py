#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: engine :: rev 16 :: 01.2014 :: msarch@free.fr

##---IMPORTS ------------------------------------------------------------------
import pprint
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key


##---NOTES---------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''

##---PYGLET ENGINE-------------------------------------------------------------
class Engine(pyglet.window.Window):

    def __init__(self, **options):
        for opt in options:
                setattr(self, opt,options[opt])
        print 'Options :'
        pprint.pprint(options)


        self.chrono=0.0 # keeps track of total time elapsed
        self.frame_number=0 # frame counter
        self.paused=False
        self.fps_on=True
        self.fps_display = pyglet.clock.ClockDisplay()
        pyglet.window.Window.__init__(self,vsync = True)
        # set size depending on choosen mode
        if self.MODE=='FULL':
            self.set_fullscreen(True)
            self.get_display_size()
        elif self.MODE in ('EXPORT','PREVIEW'): #export or preview  mode
            self.xmax = self.PREVIEW_SIZE[0]
            self.ymax = self.PREVIEW_SIZE[1]
            self.set_size(self.xmax,self.ymax)
        else:
            print 'error : undefined mode'
            exit()
        self.key_setup()
        self.print_keys()
        self.gl_setup()
        self.mouse_setup()


    #---key handling-----------------------------------------------------------
    def key_setup(self):
        self.key_actions = {
        key.ESCAPE: lambda: exit(),
        #key.PAGEUP: lambda: self.camera.zoom(2),
        #key.PAGEDOWN: lambda: self.camera.zoom(0.5),
        #key.LEFT: lambda: self.camera.pan(self.camera.scale, -1.5708),
        #key.RIGHT: lambda: self.camera.pan(self.camera.scale, 1.5708),
        #key.DOWN: lambda: self.camera.pan(self.camera.scale, 3.1416),
        #key.UP: lambda: self.camera.pan(self.camera.scale, 0),
        key.SPACE : lambda: self.toggle_pause(),
        key.F : lambda: self.toggle_fps_on(),
        key.I : lambda: self.save_a_frame(),
        }

    def print_keys(self):
        print "keys to try:"
        [pprint.pprint(key.symbol_string(k)) for k in self.key_actions.keys()]

    def on_key_press(self,symbol, modifiers): #override pyglet window's
        if symbol in self.key_actions:
            self.key_actions[symbol]()

    def toggle_pause(self):
        self.paused=(True,False)[self.paused]

    def toggle_fps_on(self):
        self.fps_on=(True,False)[self.fps_on]


    #---mouse handling---------------------------------------------------------
    def mouse_setup(self):
        self.set_mouse_visible(False)

    #---GL stuff---------------------------------------------------------------
    def gl_setup(self):
        # Set the window color, this will be transparent in saved images.
        glClearColor(*self.BGCOLOR)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

    def get_display_size(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmax = screen.width
        self.ymax = screen.height

    #--- FRAME EXPORT LOOP ----------------------------------------------------
    def save_a_frame(self):
            file_num=str(self.frame_number).zfill(5)
            file_t=str(self.chrono)
            filename="scene "+self.scene+"-frame "+file_num+ " -@ "+file_t+'sec.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
            print 'image file writen : ',filename

    def export_loop(self,dt):
        constant_interval=1.0/PicPS
        if self.chrono<END_TIME:
            # tick at a constant dt, regardless of real time
            # so that even if refresh is slow no frame should be missing
            # self.frame_(PicPS)
            self.tick(constant_interval)
            self.frame_paint(dt)
            self.frame_number+=1
            self.save_a_frame()
        else:
            exit()

    #--- SCREEN MODE LOOP -----------------------------------------------------
    def frame_paint(self,dt):
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `()` methods of the zulus
        """
        if not self.paused:
            self.gl_clear()

            self.scene.paint()

            if self.fps_on:
                glColor4ub(255, 0, 0, 255)
                pyglet.clock.ClockDisplay().draw()
                self.fps_display.draw()


    def tick(self,dt):
        if not self.paused:
            self.chrono+=dt
            print self.chrono
            if self.chrono > self.duration:
                exit()
            for actor in self.actor_registry:
                actor.tick(dt)
        else:
            pass


    #---dynamic scene handling ------------------------------------------------
    def get_actors(self):
        self.scene_folder ='scene'
        self.fl=[] # file list
        self.actor_registry = []
        self.rule_registry = []

        modules = {}
        for path in glob.glob('scene/[!_]*.py'):
            name, ext = os.path.splitext(os.path.basename(path))
            modules[name] = imp.load_source(name, path)
        print modules


##---MAIN----------------------------------------------------------------------
def main():
        # schedule pyglet  loop at max framerate
        # and the tick function at more than fps
        # frame / time driven loop
    options = {
    'DEBUG': 1,
    'PREVIEW_SIZE': (800, 600),
    'BGCOLOR': (0.95, 0.95, 0.95, 0),  # background
    'FPS': 60,  # display max framerate
    'PicPS': 25,  # images per second for movie export
    'MODE': 'PREVIEW',  # options are: 'FULL'; 'PREVIEW'; 'EXPORT'
    'DURATION' : 3,
    'SCENE_FOLDER' : 'scene',
    }

    engine = Engine(**options)

    #---run loop options-------------------------------------------------------
    if  engine.MODE in ('FULL','PREVIEW'):
        clock.schedule_interval(engine.frame_paint,1.0/engine.FPS)
        clock.schedule_interval_soft(engine.tick, 1.0/(1.0*engine.FPS))
    elif engine.MODE == 'EXPORT': # export loop
        # try (soft) to run export method at final anim speed,
        clock.schedule_interval_soft(engine.export_loop,1.0/engine.PicPS)
        # while (soft) run the preview at good rate
        #clock.schedule_interval_soft(self.frame_, 1.0/self.FPS,scene)

    pyglet.app.run()


##-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
