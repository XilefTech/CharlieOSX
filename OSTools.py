'''This method is for outsourcing mathematical and other essential functions that don't interact directly with sensors or motors'''
from pybricks import ev3brick as charlie
from pybricks.parameters import Align
import time

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
        imgPath = 'graphics/menus/programingMainMenu.jpg'
    elif menuState == 0.2:
        imgPath = 'graphics/menus/testingMainMenu.jpg'
    elif menuState == 0.3:
        imgPath = 'graphics/menus/remoteMainMenu.jpg'
    elif menuState == 0.4:
        imgPath = 'graphics/menus/competitionMainMenu.jpg'
    elif menuState == 0.5:
        imgPath = 'graphics/menus/settingsMainMenu.jpg'

    try:
        charlie.display.image(imgPath, Align.TOP_RIGHT, clear = True)
        print("Menu drawn ", menuState)
    except:
        print("could not draw menu ", menuState)

# method for animating transitions between menus
def animate(state, *args):
    print(state)
    if state == 5:
        # in Germany we would call it "Pfusch vor dem Herrn" It's as bad as it could get, but it is only to display something and test if the concept works
        charlie.display.image('graphics/animations/mainSettings/1.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/2.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/3.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/4.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/5.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/6.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/7.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/8.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/9.jpg', Align.TOP_RIGHT, clear = True)
        charlie.display.image('graphics/animations/mainSettings/10.jpg', Align.TOP_RIGHT, clear = True)
        

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
