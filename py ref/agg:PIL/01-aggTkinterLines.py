import aggdraw
import random
import Tkinter

root = Tkinter.Tk()
import Image
 
img = Image.new("RGB", (1000,2000), "#FFFFFF")
 
import aggdraw as draw
 
canvas = draw.Draw(img)
 
pen = draw.Pen("black", 0.5)
 
canvas.line((5,20,200,100), pen)
 
canvas.line((0,500,500,0), draw.Pen("blue", 0.7))
 
canvas.flush()
 
img.save("love.png", "PNG")
 
img.save("love.gif", "GIF")