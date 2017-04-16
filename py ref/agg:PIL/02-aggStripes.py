import Image
import aggdraw as draw
 
def drawGraph(step_size=3, file_name="foo.png"):
	STEP_SIZE = step_size
	DURATION_SECONDS = 4
	LARGE_STEP_SIZE = STEP_SIZE * 5
	HEIGHT = STEP_SIZE * 5 * 4
	LS_PER_SECOND = 5 
	WIDTH = LS_PER_SECOND * DURATION_SECONDS * LARGE_STEP_SIZE
 
	img = Image.new("RGB", (WIDTH, HEIGHT), "#FFFFFF") 
	canvas = draw.Draw(img)
	black_pen = draw.Pen("black", 0.25)
	blue_pen = draw.Pen("red", 0.25)
 
	for x in range(0, WIDTH, STEP_SIZE): canvas.line((x,0,x,HEIGHT), blue_pen)
	for x in range(0, WIDTH, LARGE_STEP_SIZE): canvas.line((x,0,x,HEIGHT), black_pen)
	for y in range(0, HEIGHT, STEP_SIZE): canvas.line((0,y,WIDTH,y), blue_pen)
	for y in range(0, HEIGHT, LARGE_STEP_SIZE): canvas.line((0,y,WIDTH,y), black_pen)
	canvas.line((0,HEIGHT,WIDTH,HEIGHT), black_pen)
 
	canvas.flush().save(file_name, "PNG")
 
drawGraph()
drawGraph(6,"zoom.png")