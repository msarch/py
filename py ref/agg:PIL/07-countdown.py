# countdown animation
import aggdraw,os,time,numpy
from PIL import Image, ImageDraw, ImageFont

# user variables
#resolution = (xres, yres) = (4096, 2304)
resolution = (xres, yres) = (1920, 1080)
#resolution = (xres, yres) = (1280, 720)
framerate = 30.
countdown = 10 # time in seconds
bgcolor = "black" # set colors
fgcolor = "white"

background = Image.new("RGB", resolution, bgcolor) # create PIL image
foreground = Image.new("RGB", resolution, fgcolor) # create PIL image

# properties calculated
r = 9 * yres / 20 # radius of circle
font = aggdraw.Font("white", "Arial.ttf", size=yres/3.05, opacity=255)
print 'About', int((countdown + 26) * framerate), 'frames will be rendered:',

# make new dir
maindir=os.getcwd()
dirname = time.strftime("Frames_%Y%m%d_%H%M%S", time.localtime())
newdir = maindir + '\\' + dirname
os.mkdir(newdir)
os.chdir(newdir)


def display(seconds): # return int tulple (hours, minutes, seconds)
    if seconds < 60.00001:
        return str(int(seconds+0.9999))
    if seconds < 3601:
        s = seconds+0.9999
        m, s = divmod(s, 60)
        return "%d:%02d" % (m, s)
    s = seconds+0.99999
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%d:%d:%d" % (h, m, s)


# create background with marks
x, y = (xres / 2, yres / 2)
backg = background.copy()
draw = aggdraw.Draw(backg) # use aggdraw on the PIL image
# minutes
marks = int(countdown/60) + 1 # number of marks
step = 2 * numpy.pi / countdown * 60 # angle between marks
angles = [numpy.pi / 2] # angles of marks, beginning with top
[ angles.append(angles[-1] + step) for n in range(1, marks) ]
# marks coordinates
mark = [] # (x1, y1, x2, y2)
rr = 1.1 # default minute mark length
if countdown > 600:
    rr = 1.05 # smaller minute marks
for angle in angles:
    mark.append((x + r/rr * numpy.cos(angle), \
         y - r/rr * numpy.sin(angle),\
        x + r/1.0 * numpy.cos(angle),\
                y - r/1.0 * numpy.sin(angle)))
p = aggdraw.Pen(fgcolor, width=xres/600., opacity=255)
for tup in mark:
    draw.line([tup[0], tup[1], tup[2], tup[3]], p)
draw.flush() # draw!
if countdown < 600:
    # seconds
    marks = int(countdown) + 1 # number of marks
    step = 2 * numpy.pi / countdown # angle between marks
    angles = [numpy.pi / 2] # angles of marks, beginning with top
    [ angles.append(angles[-1] + step) for n in range(1, marks) ]
    # marks coordinates
    mark = [] # (x1, y1, x2, y2)
    for angle in angles:
        mark.append((x + r/1.05 * numpy.cos(angle), \
             y - r/1.05 * numpy.sin(angle),\
            x + r/1.0 * numpy.cos(angle),\
                    y - r/1.0 * numpy.sin(angle)))
    p = aggdraw.Pen(fgcolor, width=xres/600., opacity=255)
    for tup in mark:
        draw.line([tup[0], tup[1], tup[2], tup[3]], p)
    draw.flush() # draw!


frame = 1
precount = 5 # set countdown delay in seconds
seconds = float(precount)
running = True
while running:
    print frame,
    mask1 = Image.new("L", resolution, "black") # create circle mask
    mask2 = Image.new("L", resolution, "black") # create circle mask
    drawmask1 = aggdraw.Draw(mask1) # use aggdraw on the PIL image
    drawmask2 = aggdraw.Draw(mask2) # use aggdraw on the PIL image
    b = aggdraw.Brush("white", 255)
    circle = (xres/2 - r-2, yres/2 - r-2, xres/2 + r+2, yres/2 + r+2)
    angle = 90 - 360 * (precount - seconds) / float(precount) # in degrees
    if framerate > 13: # mark animation if framerate is smooth enough
        drawmask1.pieslice(circle, angle, 90, b)
        drawmask1.flush()
        i = Image.composite(backg, background, mask1)
    else: i = backg
    # draw text
    x = xres / 2 - drawmask1.textsize(display(seconds), font)[0] / 2
    y = yres / 2 - drawmask1.textsize(display(seconds), font)[1] / 2
    drawmask2.text((x,y), display(seconds), font) # create text
    drawmask2.flush()
    i = Image.composite(foreground, i, mask2)
    i.save ( 'Frame_'+str(frame)+'.png') # save in new dir
    frame += 1
    seconds -= 1. / framerate
    if seconds < 1. / framerate:
        running = False

seconds = float(countdown)
running = True
while running:
    print frame,
    # create images
    fg = Image.new("RGB", resolution, "white") # create PIL image
    mask1 = Image.new("L", resolution, "black") # create text mask
    mask2 = mask1.copy() # create circle mask
    drawmask1 = aggdraw.Draw(mask1) # use aggdraw on the PIL image
    drawmask2 = aggdraw.Draw(mask2) # use aggdraw on the PIL image
    #draw text
    x = xres / 2 - drawmask1.textsize(display(seconds), font)[0] / 2
    y = yres / 2 - drawmask1.textsize(display(seconds), font)[1] / 2
    drawmask1.text((x,y), display(seconds), font) # create text
    drawmask1.flush()
    # draw circle
    b = aggdraw.Brush("white", 255)
    circle = (xres/2 - r, yres/2 - r, xres/2 + r, yres/2 + r)
    angle = 90 - 360 * (countdown - seconds) / float(countdown) # in degrees
    drawmask2.pieslice(circle, angle, 90, b)
    drawmask2.flush()
    i = Image.composite(foreground, backg, mask1) # paste text
    i = Image.composite(foreground, i, mask2) # paste circle
    mask3 = Image.composite(mask1, Image.new("L", resolution, "black"), \
                            mask2).convert("L")
    i = Image.composite(background, i, mask3)
    i.save ( 'Frame_'+str(frame)+'.png') # save in new dir
    
    seconds -= 1. / framerate
    if seconds <= -1./framerate:
        running = False
    frame += 1

# created inverted image
i2 = Image.composite(background, foreground, mask2) # paste circle
i2 = Image.composite(foreground, i2, mask1) # paste text

step = framerate / 6.
if step % 2:
    step += 0.5 
for n in range(step-1):
    i.save ( 'Frame_'+str(frame)+'.png')
    frame += 1
    print frame,
for m in range(5):
    if not m % 2:
        for n in range(step):
            i2.save ( 'Frame_'+str(frame)+'.png')
            frame += 1
            print frame,
    if m % 2:
        for n in range(step):
            i.save ( 'Frame_'+str(frame)+'.png')
            frame += 1
            print frame,
for n in range(framerate * 20):
    i.save ( 'Frame_'+str(frame)+'.png')
    frame += 1
    print frame,

os.chdir(maindir)

    
