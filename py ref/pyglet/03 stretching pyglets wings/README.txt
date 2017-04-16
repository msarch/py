Stretching pyglet's Wings

    A presentation and demo code written for PyCon UK 2008. The most up-to-date
    version can be found at http://tartley.com/?p=378

    Dependencies are Python 2.5, pyglet 1.1.1.

    The intent of the presentation and demos is to start with something very
    close to a minimal pyglet application, as seen at the start of the
    programming guide, and add one feature at a time until it demonstrates a
    reasonable 2D vector graphics system for a game with a fairly minimal,
    clean-lined aesthetic.

To Run

	Run each demo using 'python -O run.py'

    The '-O' flag can sometimes speed things up a lot (eg. factor of five under
    some circumstances, esp on Linux.) It skips some error checking pyglet
    normally does.

Keyboard

    In all demos:

        escape - quit

    In demos 2-6:

        up, down, left, right - pan camera
        pgup, pgdown - zoom in/out
        comma,period - tilt camera

    In demo 4, keys 1 and 2 trigger a popup ghost or a chase.

    In demo 5, the following keys switch the rendering method, so you can
    compare framerates:
        1 - render individual vertices with glVertex calls
        2 - render individual primitives with pyglet.graphics.draw
        3 - render each primitive with pyglet.graphics.vertex_list
        4 - render an entire shape (eg. a ghost) with pyglet.graphics.batch

Known Issues

    For reasons unknown, in demo5, graphics.draw is somewhat slower than
    glVertex calls. Also, graphics.vertex_list seems to be no faster.
    Probably we are not seeing the full benefit of these techniques here, with
    such low numbers of vertices, but I'm not sure why they are actually
    slower.

    Demos 7 & 8, which demonstrate fast vertex lists using the pyglet openGL
    bindings, are included instead.

    All demos are 2 to 4 times faster on Linux than Windows on my hardware
    (a Thinkpad T60 lappy with at ATIsomething or other), for reasons unknown.

Contact

    Jonathan Hartley
    tartley@tartley.com

