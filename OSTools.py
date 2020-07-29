'''This method is for outsourcing mathematical and other essential functions that don't interact directly with sensors or motors'''
from pybricks.hubs import EV3Brick
from pybricks.parameters import Align, Color, Button
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile
from robotError import *
import time, _thread


charlie = EV3Brick()
logMsg = 0

# playing soundfiles without waiting for the end


# method for displaying the right contents of the menu on the Display
def drawMenu(menuState, *args):
    menus = {0: 'graphics/menus/mainMenu.png',
             1: 'graphics/menus/programmingMainMenu.png',
             2: 'graphics/menus/testingMainMenu.png',
             3: 'graphics/menus/remoteMainMenu.png',
             4: 'graphics/menus/competitionMainMenu.png',
             5: 'graphics/menus/settingsMainMenu.png'
             }

    
    try:
        charlie.screen.draw_image(0, 0, menus[menuState], transparent = Color.RED)
    except Exception as exception:
        log.error("Could not draw menu: ", str(exception))

# method for the settings selection menu
def drawSettings(pos, settings, selected, *args):

    def drawOptions(value, *args):
        '''Function that draws the 5 current options on the screen'''
        i = 0
        while i <= 4:
            if value + i == pos:
                if selected:
                    charlie.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.BLACK)
                    charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.WHITE, background_color = None) if settings['types'][keys[value + i]] == 'int' else charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.WHITE, background_color = None)
                else:
                    charlie.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.WHITE)
                    charlie.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = False, color = Color.BLACK)
                    charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.BLACK, background_color = None) if settings['types'][keys[value + i]] == 'int' else charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.BLACK, background_color = None)
            else:
                charlie.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill = True, color = Color.WHITE)
                charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.BLACK, background_color = Color.WHITE) if settings['types'][keys[value + i]] == 'int' else charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.BLACK, background_color = Color.WHITE)
            i += 1

    keys = list(settings['options'].keys())
    charlie.screen.set_font(Font(family = 'arial', size = 13))

    # the slider bar indicator
    charlie.screen.draw_box(171, 25, 177, 127, r = 2, fill = False, color = Color.BLACK)
    charlie.screen.draw_box(172, 26, 176, 126, r = 2, fill = True, color = Color.WHITE)
    charlie.screen.draw_box(173, 27 + 102 / len(settings['options']) * pos, 175, 23 + 102 / len(settings['options']) * (pos + 1), r = 1, fill = True, color = Color.BLACK)

    if pos > 1 and pos < (len(settings['options']) - 2):
        drawOptions(pos - 2)
    elif pos == 0:
        drawOptions(pos)
    elif pos == 1:
        drawOptions(pos - 1)
    elif pos == len(settings['options']) - 2:
        drawOptions(pos - 3)
    elif pos == len(settings['options']) - 1:
        drawOptions(pos - 4)

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
                charlie.screen.draw_image(0, 0, 'graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                i += 1
        except Exception as exception:
            log.error("Could not animate menu: ", str(exception))
            return(RobotError.Display.Animation.generalError)
  
    else:
        i = 10
        try:
            while i >= 1:
                charlie.screen.draw_image(0, 0, 'graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
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

# error, notification an logging

    