from PaintLibrary import *
import collections

def prepareOutputPicture(num):
    sizeY = 50*(num-1) + 60*(num + 1)
    Image = createImage('tabs.svg', 950, sizeY)
    for i in range(num):
        paintCell(Image, i)
    return Image, sizeY

def parseNote(note): # max is tab/string
    return tuple(map(int, note.split("/")))

def parseNotes(notes): # max is 6
    notes = notes.split(".")
    return map(lambda note: parseNote(note), notes)[:6]

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

def flatten(x):
    if isinstance(x, tuple):
        return [x]
    elif isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

def getTones(data):
    tones = flatten(data)
    tones = set(filter(lambda (bar, string): bar < 13, tones))
    size, iterate, tonesBox, tuning = getGuitarAttributes()
    scale = []
    for (bar, string) in tones:
        scale.append(tonesBox[string - 1][bar - 1])
    return list(set(scale))

def checkBorders(inputText):
    print 'run'
    outputErrors = []
    splittedText = inputText.split('\n\n')
    for block in range(len(splittedText)):
        lines = splittedText[block].split("\n")
        for lineNum in range(len(lines)):
            if lineNum >= 4:
                outputErrors.append(sum([len(splittedText[i]) for i in range(0, block)]) + \
                                    sum([len(lines[i]) for i in range(0, lineNum)]) + 1)
            else:
                tones = lines[lineNum].split()
                if len(tones) > 8:
                    outputErrors.append(sum([len(splittedText[i]) for i in range(0, block)]) + \
                                        sum([len(lines[i]) for i in range(0, lineNum)]) + \
                                        sum([len(tones[i]) + 1 for i in range(0,7)]))
    return outputErrors