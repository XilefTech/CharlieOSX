'''This method is for outsourcing mathematical and other essential functions that don't interact directly with sensors or motors'''

from pybricks.parameters import Align, Color, Button
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile
from robotError import *
import time, _thread


charlie = EV3Brick()
logMsg = 0




# method for animating transitions between menus
def animate(state, direction, *args):
    menus = {10: 'mainProgram',
             20: 'mainTest',
             30: 'mainRemote',
             40: 'mainCompetition',
             50: 'mainSettings'}

    
    if direction:
        i = 1
        try:
            while i <= 10: 
                charlie.screen.draw_image(0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                i += 1
        except Exception as exception:
            log.error("Could not animate menu: ", str(exception))
            return(RobotError.Display.Animation.generalError)
  
    else:
        i = 10
        try:
            while i >= 1:
                charlie.screen.draw_image(0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                i -= 1
        except Exception as exception:
            log.error("Could not animate menu: ", str(exception))
            return(RobotError.Display.Animation.generalError) 

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

def getBatteryVoltage(human = False):
    """Gets the battery voltage, has 'human' argument."""
    global charlie
    if (not human):
        return(charlie.battery.voltage())
    else:
        return(float(str(charlie.battery.voltage())[:1] + "." + str(charlie.battery.voltage())[1:]))
  