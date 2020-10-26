#!/usr/bin/env pybricks-micropython

import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, StopWatch
from charlieosx import CharlieOSX
     
os = CharlieOSX('config.cfg', 'settings.json', '')

brick = EV3Brick()

import webremote

webremote = webremote.Webremote()

webremote.startServerThread()


while not any(brick.buttons.pressed()):
    if webremote.newDataAvailable():
        data = webremote.getResponseData()
        os.robot.setRemoteValues(data)
        #print(data)
    time.sleep(0.05)

