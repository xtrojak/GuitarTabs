from PaintTones import *

SPACE = 50
POSITION = 60

# higher level of functions

def handleNote(string, row, bar, note, maximum):
	posX = 225*bar + (note + 1)*(225/(maximum + 1)) + 25
	posY = row*POSITION + SPACE*(row + 1) + string*10 - 5
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
			for note in range(len(data[row][bar])): # max is 10
				for (number, string) in data[row][bar][note]:
					if number is not None and string is not None:
						posX, posY = handleNote(string, row, bar, note, len(data[row][bar]))
						paintText(image, posX, posY, number, "black")
"""
Boundaries hints:
0: none
1: start
2: end
3: middle
"""
def drawComments(image, boundaries, texts):
	i = 0
	step = 50
	while i < len(texts):
		posX = step
		posY = POSITION*((i/4) + 1) + SPACE*(i/4) - 33
		if texts[i]:
			paintText(image, posX, posY, texts[i][:33], 'rgb(170,170,170)')
		step = (step + 225)%900
		i += 1

	i = 0
	step = 25
	while i < len(boundaries):
		if boundaries[i] != 0:
			fromX = step
			toX = step + 225
			Y = POSITION*((i/4) + 1) + SPACE*(i/4) - 30
			if boundaries[i] == 1:
				paintStartBoundary(image, fromX, toX, Y)
			elif boundaries[i] == 2:
				paintEndBoundary(image, fromX, toX, Y)
			elif boundaries[i] == 3:
				paintMiddleBoundary(image, fromX, toX, Y)
		step = (step + 225)%900
		i += 1
