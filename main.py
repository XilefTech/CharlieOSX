#!/usr/bin/env pybricks-micropython

from charlieosx import CharlieOSX
from pybricks.tools import print, StopWatch
from pybricks.parameters import (
    Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.hubs import EV3Brick



# example code to start CharlieOSX
os = CharlieOSX('config.cfg', 'settings.json', '')
#os.robot.__aMotor2.run_angle(1000000, -360 * 15)
#os.scripts.runThree()
#os.robot.straight(50, 70, 0)
#os.robot.action(50, 1/8, 1)
#os.robot.straight(30, 30, 0)
os.scripts.scriptList[1]()



#os.ui.mainLoop()
# example for driving straight
#os.robot.straight(100, -50, 0)



#import lineFollow

#lf = lineFollow.LineFollower(Port.D, Port.A, Port.S4, rDir=Direction.COUNTERCLOCKWISE, lDir=Direction.COUNTERCLOCKWISE)

#print ('running app')
#lf.app.run(host='192.168.178.60')