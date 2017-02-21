from PaintTones import *

SPACE = 50
POSITION = 60

# higher level of functions

def handleNote(string, row, bar, note):
	posX = 225*bar + (note + 1)*25 + 20
	posY = row*POSITION + SPACE*(row + 1) + (int(string))*10 - 5
	return posX, posY

def writeTitle(image, title):
	posX = 475 - len(title)*3
	posY = 20
	paintText(image, posX, posY, title, "black")

def drawBarNumbers(image, num):
	number = 1
	for i in range(num):
		for step in range(30, 930, 225):
			posX = step
			posY = POSITION*(i + 1) + SPACE*i - 15
			paintText(image, posX, posY, number, 'rgb(170,170,170)')
			number += 1

def paintCell(image, position):
	space = SPACE*(position + 1)
	position *= POSITION
	for step in range(0, POSITION, 10):
		paintLine(image, 25, step + position + space, 925, step + position + space, 'rgb(170,170,170)')

	for step in range(25, 1150, 225):
		paintLine(image, step, position + space, step, position + space + SPACE, 'rgb(170,170,170)')

def paintTabs(image, data):
	for row in range(len(data)):
		for bar in range(len(data[row])): # max is 4
			for note in range(len(data[row][bar])): # max is 8
				for (number, string) in data[row][bar][note]:
					posX, posY = handleNote(string, row, bar, note)
					paintText(image, posX, posY, number, "black")