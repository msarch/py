*********************************MAZES**********************************

By: Benjamin Debski <benjamin.debski@gmail.com>
Date started: 16th?/October/2008
Description: Mazes is a 2D puzzle platfromer game writtin in python using pyglet and pybox2d.

Controls:
Arrow keys = move
Space = jump
Esc = menu
F12 = fullscreen/window
F11 = screenshot
F8 = display FPS counter
` = console

Code guide:
R00. Game objects interaction self contained
R01. If 50% of vars in an instance stay the same, make it permenant
R02. If a variable is needed by more than 50% of objects globalise

Code todo:
-Consider using tags in the map loader e.g. movable walls that generate opengl commands
-Stop player from climbing up steep slopes by calculating normals or using sensors
-Alarm(timer) system
-Link system for switches(remote triggers)
-Add optimized reload method to SVG2B2D
-When returning from menu/console check caller __class__ to decide were to push handlers
-GameConsole logging in the background?
-Change config.txt format into a python script that is executed like in HL/Quake series?

Aesthetics todo:
-Color themes: Original/paper(black on white), Retro(green on black), Candy(pink on black)
-When the Player dies, set the body to sensor so that it falls through the floor like Sonic death ani.
