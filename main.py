#!/usr/bin/env pybricks-micropython

import time
import math
import _thread
import OSTools as tools
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import config

# initialize the Sensors and Motors
import robot

import movements

charlie = EV3Brick()

def mainLoop():
    global menuState
    menuState = 0
    oldMenuState = 0
    loop = True
    tools.drawMenu(int(menuState))
    while loop:
        if menuState == 0:
            if Button.UP in charlie.buttons.pressed():
                menuState = 5
            elif Button.DOWN in charlie.buttons.pressed():
                menuState = 1
        elif menuState > 0 and menuState < 6:
            if Button.UP in charlie.buttons.pressed() and menuState > 1:
                menuState -= 1
            elif Button.UP in charlie.buttons.pressed() and menuState == 1:
                menuState = 5
            if Button.DOWN in charlie.buttons.pressed() and menuState < 5:
                menuState += 1
            elif Button.DOWN in charlie.buttons.pressed() and menuState == 5:
                menuState = 1
        

        if Button.RIGHT in charlie.buttons.pressed() and menuState > 0:
            menuState = menuState * 10
            oldMenuState = menuState
            tools.sound('media/confirm.wav')
            time.sleep(0.08)
            tools.animate(menuState, True)
            time.sleep(0.4)

        if Button.LEFT in charlie.buttons.pressed() and menuState >= 10:
            tools.sound('media/confirm.wav')
            time.sleep(0.08)
            tools.animate(menuState, False)
            menuState = menuState / 10
            oldMenuState = menuState
            time.sleep(0.4)


        if oldMenuState != menuState:
            tools.sound(SoundFile.CLICK)
            time.sleep(0.08)
            tools.drawMenu(menuState)
            oldMenuState = menuState
            time.sleep(0.31)

        if tools.logMsg == 1:
            tools.logMsg = 0
            menuState = menuState / 10

        




# just some example code
#charlie.sound.beep()
#movements.execute([7, 75, 10, 0])




### things, I'm currently using to test things
"""
lineMap = {'height' : 300, 'width' : 1000,
            'from' : (1, 1), 'to' : (1, 4), 
            'obstacles' : [((2, 1), (4, 1))]}

tools.doIntersect(lineMap)"""


mainLoop()

#tools.drawMenu(0.0)
#time.sleep(20)
