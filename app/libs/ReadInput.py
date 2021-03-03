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
    if note == "-":
        return (None, None)
    return tuple(map(int, note.split("/")))

def parseNotes(notes): # max is 6
    notes = notes.split(".")
    return map(lambda note: parseNote(note), notes)[:6]

def parseBar(bar): # max is 10
    bar = bar.split()
    return map(lambda notes: parseNotes(notes), bar)

def parseLine(line): # max is 4
    return map(lambda bar: parseBar(bar), line)[:4]

def parseInput(inputData):
    bars = []
    toParse = []
    comments = []
    lineNum = 1
    for line in str(inputData).split("\n"):
        if not line:
            lineNum += 1
            bars.append(parseLine(toParse))
            while len(comments) % 4 != 0:
                comments.append(None)
            toParse = []
        else:
            parts = line.split("#")
            toParse.append(parts[0])
            if len(parts) > 1:
                comments.append(parts[1])
            else:
                comments.append(None)

    bars.append(parseLine(toParse))
    return bars, lineNum, comments

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
        if bar is not None and string is not None:
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

        if sectionNum > 4:
            return sum([len(lines[i]) + 1 for i in range(0,lineNum)]), "tooManyBars"

        expression = QRegExp("([0-9]+\/[0-9]+)(\.[0-9]+\/[0-9]+)*|\-")
        tones = lines[lineNum].split("#")[0].split(" ")

        for i in range(len(tones)):
            if tones[i]:
                if not expression.exactMatch(tones[i]):
                    startOfLine = sum([len(lines[j]) + 1 for j in range(0,lineNum)])
                    previousTones = sum([len(tones[j]) + 1 for j in range(0, i)])
                    return (startOfLine + previousTones, len(tones[i])), tones[i]

        tones = lines[lineNum].split("#")[0].split()
        if len(tones) > 11:
            return sum([len(lines[i]) + 1 for i in range(0,lineNum)]), "tooManyTones"

    return None, None

def computeAnnotations(comments):
    boundaries, texts = [], []
    insideBoundary = False
    for comment in comments:
        if not comment:
            if insideBoundary:
                boundaries.append(3)
            else:
                boundaries.append(0)
            texts.append(None)
        elif comment[0] == "!":
            insideBoundary = True
            boundaries.append(1)
            texts.append(comment[1:])
        elif comment[0] == "?":
            insideBoundary = False
            boundaries.append(2)
            texts.append(comment[1:])
        else:
            if insideBoundary:
                boundaries.append(3)
                texts.append(comment)
            else:
                boundaries.append(0)
                texts.append(comment)
    return boundaries, texts