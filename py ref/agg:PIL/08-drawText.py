import Image
import aggdraw

im = Image.new("RGBA", (200, 200), 'white')
draw = aggdraw.Draw(im)

# note that the color is specified in the font constructor in aggdraw
font = aggdraw.Font((0,0,0), "Arial.ttf")
draw.text((100, 100),"hello, world")


draw.flush() # don't forget this to update the underlying PIL image!

im.show()