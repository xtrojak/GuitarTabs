import svgwrite

# basic functions

def paintLine(image, fromX, fromY, toX, toY, color):
    image.add(image.line((fromX, fromY), (toX, toY), stroke=color))

def paintText(image, posX, posY, text, color):
    image.add(image.text(text, insert=(posX, posY), fill=color, style = "font-size:13px; font-family:Arial"))

def createImage(fileName, sizeX, sizeY):
    image = svgwrite.Drawing(filename=fileName, size=(sizeX, sizeY), debug=True)
    image.add(image.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='white'))
    return image

def saveImage(image):
    image.save()

# higher level of functions

def paintVerticalLine(image, size, i):
    paintLine(image, 50 + (i+1)*80, 50, 50 + (i+1)*80, size, "black")

def paintHorizontalLine(image, i):
    paintLine(image, 50, 50 + (i+1)*50, 1010, 50 + (i+1)*50, "black")

def paintTone(image, i, j, tone):
    paintText(image, 85 + i*80, 30 + (j + 1)*50, tone, "red")

def writeBarNumber(image, i):
    paintText(image, 80 + i*80, 30, str(i+1), "black")

def writeBaseTone(image, i, tone, color):
    paintText(image, 30, 80 + i*50, tone, color)

def writeTextUnderPicture(image, i, tones):
    paintText(image, 50, i, "tones: " + ", ".join(sorted(set(tones))), "black")

def getGuitarAttributes():
    tones = [['f', 'f#', 'g', 'g#', 'a', 'a#', 'h', 'c', 'c#', 'd', 'd#', 'e'],
             ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'h'],
             ['g#', 'a', 'a#', 'h', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g'],
             ['d#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'h', 'c', 'c#', 'd'],
             ['a#', 'h', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a'],
             ['f', 'f#', 'g', 'g#', 'a', 'a#', 'h', 'c', 'c#', 'd', 'd#', 'e']]
    default_tuning = ['e', 'h', 'g', 'd', 'a', 'e']
    size = 100
    return size, 6, tones, default_tuning

def paintTones(input_tones):
    size, iterate, tones, tuning = getGuitarAttributes()
    image = createImage('tones.svg', 1060, 300 + size)

    color = "black"

    paintVerticalLine(image, 250 + size, -1)
    for i in range(12):
        paintVerticalLine(image, 250 + size, i)
        writeBarNumber(image, i)

    paintHorizontalLine(image, -1)
    for string in range(iterate):
        color = "black"
        paintHorizontalLine(image, string)
        if tuning[string] in input_tones:
            color = "red"
        writeBaseTone(image, string, tuning[string], color)

        for bar in range(12):
            color = "red"
            if tones[string][bar] in input_tones:
                paintTone(image, bar, string, tones[string][bar])

    writeTextUnderPicture(image, 280 + size, input_tones)
    saveImage(image)