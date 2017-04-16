from PIL import Image
from aggdraw import Draw, Brush
transBlack = (0, 0, 0, 0)         # shows your example with visible edges
solidBlack = (0, 0, 0, 255)       # shows shape on a black background
transWhite = (255, 255, 255, 0)
solidWhite = (255, 255, 255, 255)

im = Image.new("RGBA", (600, 600), solidBlack)

draw = Draw(im)

brush = Brush("yellow")

draw.polygon(
             (
              50, 50,
              550, 60,
              550, 550,
              60, 550,
             ),
             None, brush
            )

draw.flush()
im.save("squar.png")
im.show()