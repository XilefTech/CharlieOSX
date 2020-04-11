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


# just some example code
charlie.sound.beep()
movements.execute([7, 75, 10, 0])




#things, I'm currently using to test things
"""
lineMap = {'height' : 300, 'width' : 1000,
            'from' : (1, 1), 'to' : (1, 4), 
            'obstacles' : [((2, 1), (4, 1))]}

tools.doIntersect(lineMap)"""

#tools.drawMenu(0.0)
#time.sleep(20)
