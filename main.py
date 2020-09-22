#!/usr/bin/env pybricks-micropython

import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, StopWatch
from charlieosx import CharlieOSX
from UI.uiManager import UIManager
     
### things, I'm sometimes using to test things - can be ignored
"""
lineMap = {'height' : 300, 'width' : 1000,
            'from' : (1, 1), 'to' : (1, 4), 
            'obstacles' : [((2, 1), (4, 1))]}

tools.doIntersect(lineMap)"""


### example code to start CharlieOSX and it's menu-system
#os = CharlieOSX('config.cfg', 'settings.json', '')
#os.ui.mainLoop()

### example for driving straight
#os.robot.straight(100, 20, 0)

from UI.uiManager import UIManager
x = UIManager('','',EV3Brick(),'')
print(x)
time.sleep(10)