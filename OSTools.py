'''This method is for outsourcing mathematical and other essential functions that don't interact directly with sensors or motors'''
from pybricks import ev3brick as charlie
from pybricks.parameters import Align

# tested drwaing objects on screen out of single pixels, but very slow.
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

# method for displaying the right contents of the menu on the Display
def drawMenu(menuState, *args):
    if menuState == 0.0:
        imgPath = 'graphics/menus/mainMenu.jpg'
    elif menuState == 0.1:
        pass

    charlie.display.image(imgPath, Align.TOP_RIGHT, clear = True)


# method for Linemap calculations and pathfinding, currently not in use
def doIntersect(lineMap):
    x1 = lineMap['from'][0]
    x2 = lineMap['to'][0]
    x3 = lineMap['obstacles'][0][0][0]
    x4 = lineMap['obstacles'][0][1][0]
    
    y3 = lineMap['obstacles'][0][0][1]
    y4 = lineMap['obstacles'][0][1][1]
    print((x1+x2*y3-x3)/(x4+x2*y4))


# maps a number x as a number in range in_min - in_max to a number in range out_min - out_max
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
