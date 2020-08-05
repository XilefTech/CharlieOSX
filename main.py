#!/usr/bin/env pybricks-micropython

import time, math, json
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from charlieosx import CharlieOSX
#import config, ui

      
### things, I'm sometimes using to test things - can be ignored
"""
lineMap = {'height' : 300, 'width' : 1000,
            'from' : (1, 1), 'to' : (1, 4), 
            'obstacles' : [((2, 1), (4, 1))]}

tools.doIntersect(lineMap)"""
os = CharlieOSX('config.cfg', 'settings.json', '')

#runs menu
#ui.mainLoop()

