from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *
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

def checkNumOfTones(inputText):
    outputErrors = []
    lines = inputText.split("\n")
    sectionNum = 0
    for lineNum in range(len(lines)):
        if lines[lineNum]:
            sectionNum += 1
        else:
            sectionNum = 0

        expression = QRegExp("([0-9]+\/[0-9]+)(\.[0-9]+\/[0-9]+)*")
        tones = lines[lineNum].split()
        for tone in tones:
            if not expression.exactMatch(tone):
                return sum([len(lines[i]) + 1 for i in range(0,lineNum)]), "syntaxError"
        if sectionNum > 4:
            return sum([len(lines[i]) + 1 for i in range(0,lineNum)]), "tooManyBars"
        
        if len(tones) > 8:
            return sum([len(lines[i]) + 1 for i in range(0,lineNum)]), "tooManyTones"

    return None, None