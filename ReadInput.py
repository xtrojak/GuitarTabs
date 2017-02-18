from PaintLibrary import *

def prepareOutputPicture(num):
	size = 50*(num-1) + 60*(num + 1)
	Image = createImage('pic.svg', size)
	for i in range(num):
		paintCell(Image, i)
	return Image

def parseNotes(notes): # max is 6
	notes = notes.split(".")
	return map(lambda note: tuple(note.split("/")), notes)[:6]

def parseBar(bar): # max is 8
	bar = bar.split()
	return map(lambda notes: parseNotes(notes), bar)[:8]

def parseLine(line): # max is 4
	return map(lambda bar: parseBar(bar), line)[:4]

def parseInput(inputFile):
	bars = []
	lineNum = 1
	with open(inputFile) as lines:
		toParse = []
		for line in lines:
			line = line.rstrip().replace("\"", "")
			if not line:
				lineNum += 1
				bars.append(parseLine(toParse))
				toParse = []
			else:
				toParse.append(line)
		bars.append(parseLine(toParse))
	return bars, lineNum