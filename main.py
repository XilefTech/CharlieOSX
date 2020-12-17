#!/usr/bin/env pybricks-micropython

from UI.uiManager import UIManager
from charlieosx import CharlieOSX
from pybricks.tools import print, StopWatch
from pybricks.parameters import (
    Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.hubs import EV3Brick
import time



# example code to start CharlieOSX and it's menu-system
os = CharlieOSX('config.cfg', 'settings.json', '')
os.ui.mainLoop()

# example for driving straight
#os.robot.straight(100, 20, 0)

# x = UIManager('', '', EV3Brick(), '')
# print(x)
# time.sleep(10)

