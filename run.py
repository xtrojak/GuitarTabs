import sys
from ReadInput import *

inputFile = sys.argv[-1]

data, num = parseInput(inputFile)
Image = prepareOutputPicture(num)
paintTabs(Image, data)
drawBarNumbers(Image, num)
writeTitle(Image, 'This is a long title which should be centered')
saveImage(Image)