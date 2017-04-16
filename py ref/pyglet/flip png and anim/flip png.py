#!usr/bin/python
import pyglet
window = pyglet.window.Window()
counter=.0

def load_anim():
    arrImages=[]
    for i in range(2):
        tmpImg=pyglet.resource.image("step"+str(i)+".png")
        arrImages.append(tmpImg)
    return arrImages

def update_frames(dt):
    global counter
    counter=(counter+dt)%2

@window.event
def on_draw():
    print counter
    pyglet.gl.glClearColor(0,0,0,0)
    window.clear()
    frames[int(counter)].blit(320,200,0,
                              frames[int(counter)].width,
                              frames[int(counter)].height)

frames = load_anim()
pyglet.clock.schedule_interval(update_frames,1/10.0)
pyglet.app.run()

#
#
#I use my own sprite class, which has an timer variable which accumulates the dtime in the update_frames() message. By this you have an exact timestamp and can easily change the image based on certain timings.I do not have a source available but I will add this later, if needed
#
#Update: Here is a small piece of code: It loads two frames and displays flip flop it after a second. This will be done in update_frames(dt) (counter is a float between [0-2[, you can also multiply dt to have different timings )
#
#Note that the print in on_draw will print on each frame, but count changes only 10 times a second, configured in pyglet.clock.schedule_interval(update_frames,1/10.0) (play with this value, you will see the duration of the animation will not change)