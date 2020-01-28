from pybricks import ev3brick as charlie
from pybricks.parameters import Align


def drawRectangle(x, y, width, height, *args):
    xIndex = 0
    yIndex = 0

    #Top Line
    while(xIndex < width):
        xIndex += 1
        charlie.display.image('graphics/pixel.png', (x + xIndex, y + yIndex), False)

    #Left Line
    while(yIndex < height):
        yIndex += 1
        charlie.display.image('graphics/pixel.png', (x + xIndex, y + yIndex), False)
    
    #Bottom Line
    while(xIndex > 0):
        xIndex -= 1
        charlie.display.image('graphics/pixel.png', (x + xIndex, y + yIndex), False)
    
    #Right Line
    while(yIndex > 0):
        yIndex -= 1
        charlie.display.image('graphics/pixel.png', (x + xIndex, y + yIndex), False)    


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
