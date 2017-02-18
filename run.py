import sys
from ReadInput import *

inputFile = sys.argv[-1]

data, num = parseInput(inputFile)
Image = prepareOutputPicture(num)
paintText(Image, 10, 10, 'a')
saveImage(Image)