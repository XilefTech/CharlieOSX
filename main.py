#!/usr/bin/env pybricks-micropython

#from UI.uiManager import UIManager
from charlieosx import CharlieOSX
from pybricks.tools import print, StopWatch
from pybricks.parameters import (
    Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.hubs import EV3Brick
import time



# example code to start CharlieOSX and it's menu-system
#os = CharlieOSX('config.cfg', 'settings.json', '')
#os.ui.mainLoop()

# example for driving straight
#os.robot.straight(100, -50, 0)

# x = UIManager('', '', EV3Brick(), '')
# print(x)
# time.sleep(10)

import lineFollow

lf = lineFollow.LineFollower(Port.D, Port.A, Port.S4, rDir=Direction.COUNTERCLOCKWISE, lDir=Direction.COUNTERCLOCKWISE)

print ('running app')
lf.app.run(host='192.168.178.60')