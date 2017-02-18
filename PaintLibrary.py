import svgwrite

SPACE = 50
POSITION = 60

# basic functions

def paintLine(image, fromX, fromY, toX, toY):
	image.add(image.line((fromX, fromY), (toX, toY), stroke='rgb(170,170,170)'))

def paintText(image, posX, poY, text):
    image.add(image.text(text, insert=(posX, poY), fill="black", style = "font-size:13px; font-family:Arial"))

def createImage(fileName, size):
	image = svgwrite.Drawing(filename=fileName, size=(950, size), debug=True)
	image.add(image.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(255,255,255)'))
	return image

def saveImage(image):
	image.save()

# higher level of functions

def handleNote(string, row, bar, note):
	posX = 225*bar + (note + 1)*25 + 20
	posY = row*POSITION + SPACE*(row + 1) + (int(string))*10 - 5
	return posX, posY

def writeTitle(title):
	return

def paintCell(image, position):
	space = SPACE*(position + 1)
	position *= POSITION
	for step in range(0, POSITION, 10):
		paintLine(image, 25, step + position + space, 925, step + position + space)

	for step in range(25, 1150, 225):
		paintLine(image, step, position + space, step, position + space + SPACE)

def paintTabs(image, data):
	for row in range(len(data)):
		for bar in range(len(data[row])): # max is 4
			for note in range(len(data[row][bar])): # max is 8
				for (number, string) in data[row][bar][note]:
					posX, posY = handleNote(string, row, bar, note)
					paintText(image, posX, posY, number)