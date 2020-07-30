'''This method is for outsourcing mathematical and other essential functions that don't interact directly with sensors or motors'''

from pybricks.parameters import Align, Color, Button
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile
from robotError import *
import time, _thread

# method for Linemap calculations and pathfinding, currently not in use
def doIntersect(lineMap):
    x1 = lineMap['from'][0]
    x2 = lineMap['to'][0]
    x3 = lineMap['obstacles'][0][0][0]
    x4 = lineMap['obstacles'][0][1][0]
    
    y3 = lineMap['obstacles'][0][0][1]
    y4 = lineMap['obstacles'][0][1][1]
    print((x1+x2*y3-x3)/(x4+x2*y4))
