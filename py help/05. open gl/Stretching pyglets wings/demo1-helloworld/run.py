#! python -O
"""
Demo1
Pyglet provides OpenGL bindings. This script calls glColor and glVertex to
render a triangle, and uses Pyglet's font.Text object to render 'Hello World'
"""
from sys import stdout
from pyglet import app, clock, font
from pyglet.window import key, Window
from pyglet.gl import *
from pyglet.graphics import draw

win = Window(fullscreen=True, visible=False)
clockDisplay = clock.ClockDisplay()
glClearColor(0.1, 0.2, 0.3, 0) # color of background. RG & B between 0 and 1.
text = font.Text(
    font.load('Helvetica', win.width/10),
    'Hello, World!',
    x=win.width / 2, y=win.height / 2,
    halign=font.Text.CENTER, valign=font.Text.CENTER,
    color=(1, 1, 0, 0.5),
)

verts = (
    win.width * 0.9, win.height * 0.9,
    win.width * 0.5, win.height * 0.1,
    win.width * 0.1, win.height * 0.9,
)
colors = (
    255, 000, 000,
    000, 255, 000,
    000, 000, 255,
)

# since this demo has no movement, we just let pyglet call on_draw when it
# wants to, which by default is in response to events like window open,
# mouse move, keyboard, etc. This results in a very low fps and low cpu load.
@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    draw(3, GL_TRIANGLES,
        ('v2f', verts),
        ('c3B', colors),
    )
    text.draw()
    clockDisplay.draw()

print "press ESC to exit"
stdout.flush()
win.set_visible()
app.run()

