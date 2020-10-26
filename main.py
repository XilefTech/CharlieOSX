#!/usr/bin/env pybricks-micropython

import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, StopWatch
from charlieosx import CharlieOSX
     
# os = CharlieOSX('config.cfg', 'settings.json', '')



import webremote

webremote = webremote.Webremote()

webremote.startServerThread()

while True:
    print(webremote.getResponseData())
    time.sleep(0.1)

