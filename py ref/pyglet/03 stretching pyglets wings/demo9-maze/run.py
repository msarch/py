#! python -O
"""
Demo 9
Create a maze, all rendered in one batch.draw() call.
Fill it with ghosts. Zoom the camera around a bit.
"""
from pyglet import app, clock
from pyglet.window import key, Window
from camera import Camera
from keyboard import Keyboard
from maze import Maze
from renderer import Renderer

def main():
    win = Window(fullscreen=True, visible=False)
    camera = Camera(win.width, win.height, (0, 0), 100)
    renderer = Renderer()
    maze = Maze()
    maze.create(50, 30, 300)
    keyboard = Keyboard()
    keyboard.key_handlers[key.ESCAPE] = win.close
    keyboard.key_handlers.update(camera.key_handlers)
    clock.schedule(maze.update)
    win.on_draw = lambda: renderer.on_draw(maze, camera, win.width, win.height)
    win.on_key_press = keyboard.on_key_press
    keyboard.print_handlers()
    win.set_visible()
    app.run()

if __name__ == "__main__":
    main()

