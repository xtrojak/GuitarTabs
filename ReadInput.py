from PaintLibrary import *

def prepareOutputPicture(num):
	sizeY = 50*(num-1) + 60*(num + 1)
	Image = createImage('tabs.svg', 950, sizeY)
	for i in range(num):
		paintCell(Image, i)
	return Image, sizeY

def parseNotes(notes): # max is 6
	notes = notes.split(".")
	return map(lambda note: tuple(note.split("/")), notes)[:6]

def parseBar(bar): # max is 8
	bar = bar.split()
	return map(lambda notes: parseNotes(notes), bar)[:8]

def parseLine(line): # max is 4
	return map(lambda bar: parseBar(bar), line)[:4]

def parseInput(inputData):
	bars = []
	toParse = []
	lineNum = 1
	for line in str(inputData).split("\n"):
		if not line:
			lineNum += 1
			bars.append(parseLine(toParse))
			toParse = []
		else:
			toParse.append(line)
	bars.append(parseLine(toParse))
	return bars, lineNum

def getTones(data):
	return ["a", "c", "d", "e", "f"]