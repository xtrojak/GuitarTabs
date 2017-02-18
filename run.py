import sys
from ReadInput import *

inputFile = sys.argv[-1]

data, num = parseInput(inputFile)
Image = prepareOutputPicture(num)
paintTabs(Image, data)
saveImage(Image)