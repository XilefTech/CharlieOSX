'''This method is for outsourcing mathematical and other essential functions that don't interact directly with sensors or motors'''
from pybricks.hubs import EV3Brick
from pybricks.parameters import Align, Color
from pybricks.media.ev3dev import Image, ImageFile, Font
import time
import sys as sys

charlie = EV3Brick()

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

# method for animating transitions between menus
def animate(state, direction, *args):
    menus = {10: 'mainProgram',
             20: 'mainTest',
             30: 'mainRemote',
             40: 'mainCompetition',
             50: 'mainSettings'}

    
    if direction:
        i = 1
        while i <= 10:
            try:
                charlie.screen.draw_image(0, 0, 'graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
            except Exception as exception:
                log.error("Could not animate menu: ", str(exception))

            i += 1
    else:
        i = 10
        while i >= 1:
            try:
                charlie.screen.draw_image(0, 0, 'graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
            except Exception as exception:
                log.error("Could not animate menu: ", str(exception))

            i -= 1
        

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


# error, notification an logging
class log:
    ### if-statements are placeholders to toggle console and display logging on/off
    def __init__ (self):
        pass

    def error(msg, exception, *args):
        if True:
            print("[Error]", msg, exception, *args)
        
        if True:
            charlie.screen.draw_image(26, 24, 'graphics/notifications/error.png', transparent = Color.RED)
            charlie.screen.set_font(Font(family = 'arial', size = 7))
            if Font.text_width(Font(family = 'arial', size = 7), exception) <= 90:
                charlie.screen.draw_text(32, 47, exception, text_color = Color.BLACK)
            elif len(exception) <= 30 * 2:
                exception1, exception2 = exception[:27], exception[27:]
                charlie.screen.draw_text(32, 47, exception1, text_color = Color.BLACK)
                charlie.screen.draw_text(32, 57, exception2, text_color = Color.BLACK)
            else:
                exception1, exception2, exception3 = exception[:27], exception[27:53], exception[53:]
                charlie.screen.draw_text(32, 47, exception1, text_color = Color.BLACK)
                charlie.screen.draw_text(32, 57, exception2, text_color = Color.BLACK)
                charlie.screen.draw_text(32, 67, exception3, text_color = Color.BLACK)

    def warn(msg):
        if True:
            print("[Warning]", exception, msg)
        
        if True:
            charlie.screen.draw_image(26, 24, 'graphics/notifications/warn.png', transparent = Color.RED)
            charlie.screen.draw_text(31, 34, exception, text_color = Color.BLACK)