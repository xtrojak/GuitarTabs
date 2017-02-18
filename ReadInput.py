from PaintLibrary import *

def getNumberOfLines(): 
	return # according to count number of lines

def prepareOutputPicture(num):
	size = 40*(num-1) + 60*(num + 1)
	Image = createImage('pic.svg', size)
	for i in range(num):
		paintCell(Image, i)
	return Image

def parseInput():
	return

def paintTabs(image):
	return
	#call something from paintLib