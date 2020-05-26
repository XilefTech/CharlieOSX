#!/usr/bin/env pybricks-micropython

import time
import math
import OSTools as tools
from pybricks import ev3brick as charlie
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import config

# initialize the Sensors and Motors
import robot

import movements


def mainLoop():
    menuState = 0.0
    oldMenuState = 0.1
    loop = True
    while loop:
        #print(charlie.buttons())
        if menuState == 0.0:
            if charlie.buttons() == [256]:
                menuState = 0.5
                time.sleep(0.2)
            elif charlie.buttons() == [4]:
                menuState = 0.1
                time.sleep(0.2)
        elif menuState > 0.0 and menuState < 0.6:
            if charlie.buttons() == [256] and menuState > 0.1:
                menuState = menuState - 0.1
                time.sleep(0.2)
            elif charlie.buttons() == [256] and menuState == 0.1:
                menuState = 0.5
                time.sleep(0.2)
            if charlie.buttons() == [4] and menuState < 0.5:
                menuState = menuState + 0.1
                time.sleep(0.2)
            elif charlie.buttons() == [4] and menuState == 0.5:
                menuState = 0.1
                time.sleep(0.2)
        
        if charlie.buttons() == [32]:
            menuState = menuState * 10
            oldMenuState = menuState

            tools.animate(menuState)
            time.sleep(2)

        if oldMenuState != menuState:
            tools.drawMenu(menuState)
            oldMenuState = menuState



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
