import sys
from ReadInput import *

inputFile = sys.argv[-1]

Image = prepareOutputPicture(5)
paintText(Image, 10, 10, 'a')
saveImage(Image)