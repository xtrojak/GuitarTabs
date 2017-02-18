import svgwrite

# basic functions

def paintLine(image, fromX, fromY, toX, toY):
	image.add(image.line((fromX, fromY), (toX, toY), stroke='rgb(170,170,170)'))

def paintText(image, posX, poY, text):
    image.add(image.text(text, insert=(posX, poY), fill="black", style = "font-size:16px; font-family:Arial"))

def createImage(fileName, size):
	image = svgwrite.Drawing(filename=fileName, size=(950, size), debug=True)
	image.add(image.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(255,255,255)'))
	return image

def saveImage(image):
	image.save()

# higher level of functions

def paintCell(image, position):
	space = 40*(position + 1)
	position *= 60
	for step in range(0,60,10):
		paintLine(image, 25, step + position + space, 925, step + position + space)

	for step in range(25,1150,225):
		paintLine(image, step, position + space, step, position + space + 50)
