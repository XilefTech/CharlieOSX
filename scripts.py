
from robot import Charlie
from math import pi
from pybricks.parameters import (Stop, Color)
import time

class Scripts():
    '''runs'''

    def __init__(self, robot: Charlie, config: dict):
        '''init'''
        print('init scripts')
        self.robot = robot
        self.config = config

        self.scriptList = [
            self.runOne,
            self.runTwo,
            self.runThree,
            self.runFour
        ]

    def runOne(self):
        '''the first script (FLL-Run 2021/22: Wing, Packet, Bridge, helicoper and wagon cargo)'''
        #self.robot.action(20, -7/8, 1)

        ## drive to doorstep
        self.robot.__rMotor.run_angle(500, self.cmToDeg(130), then=Stop.BRAKE, wait=False)
        self.robot.__lMotor.run_angle(500, self.cmToDeg(130), then=Stop.BRAKE, wait=True)
        #self.robot.action(20, 7/8, 1)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()

        ## manuver out of the corner
        self.robot.straight(10, -3, 0)
        self.robot.breakMotors()
        self.robot.turn(30, 5, 23)
        self.robot.breakMotors()
        self.robot.straight(20, -22, 0)
        self.robot.turn(10, -1, 23)
        self.robot.breakMotors()
        self.robot.straight(15, 10, 0)

        ## to the helicopter and wagon
        self.robot.absTurn(2, -57, 3)
        self.robot.breakMotors()
        time.sleep(0.5)
        self.robot.straight(40, 60, 0)

        while self.robot.__rLight.color() != Color.WHITE:
            pass

        self.robot.breakMotors()
        time.sleep(0.2)
        self.robot.straight(10, -2, 0)
        self.robot.breakMotors()
        self.robot.absTurn(10, 15, 2)
        self.robot.straight(10, 2, 0)
        self.robot.breakMotors()
        self.robot.absTurn(10, 0, 2)


        self.robot.breakMotors()
        time.sleep(1)

    def runTwo(self):
        '''the second script'''
        self.robot.__gyro.reset_angle(-45)
        time.sleep(0.5)

        ## to the crane
        self.robot.straight(45, 65, 0)
        self.robot.absTurn(20, -5, 23)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.5)

        # push crane over
        self.robot.straight(40, 58, 0)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()

        ## manuver around crane
        self.robot.straight(20, -10, 0)
        self.robot.absTurn(40, 45, 23)
        self.robot.breakMotors()
        time.sleep(0.3)
        self.robot.straight(35, 10, 0)
        self.robot.absTurn(50, 0, 23)
        self.robot.breakMotors()
        time.sleep(0.3)
        self.robot.straight(35, 16, 0)

        ## backwards to wall
        self.robot.absTurn(50, 110, 23)
        self.robot.breakMotors()
        time.sleep(0.3)
        self.robot.straight(20, -20, 0)
        self.robot.absTurn(20, 90, 23)
        self.robot.breakMotors()

        self.robot.__aMotor2.run_angle(300, 0.9 * 360, then=Stop.COAST, wait=False) # extend side arm
        '''self.robot.turnBothMotors(-50)
        time.sleep(3)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(1)
        self.robot.__gyro.reset_angle(90)
        time.sleep(1)'''

        ## go to work
        self.robot.__aMotor1.run_angle(800, 600 * 3, then=Stop.HOLD, wait=True) # put down fork
        time.sleep(0.3)
        self.robot.straight(30, 22, 0)
        self.robot.breakMotors()
        self.robot.__aMotor2.run_angle(300, -0.8 * 360, then=Stop.COAST, wait=False) # flip rail-piece
        self.robot.__aMotor1.run_angle(700, -500 * 3, then=Stop.HOLD, wait=True) # lift up containers
        time.sleep(0.3)

        self.robot.straight(40, -50, 0)
        self.robot.absTurn(30, 180, 23)
        self.robot.breakMotors()

    def runThree(self):
        '''the third script'''
        self.robot.__gyro.reset_angle(-90)

        ## to the container station
        self.robot.straight(20, 12, 0)
        self.robot.absTurn(20, -45, 3)
        self.robot.breakMotors()
        self.robot.straight(40, 73, 0)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()

        self.robot.absTurn(20, 0, 2)
        self.robot.breakMotors()
        self.robot.straight(20, 5, 0) # 29? 19?
        self.robot.toColor(20, 0, 2) 
        self.robot.breakMotors()
        self.robot.absTurn(20, -90, 3)
        self.robot.breakMotors()
        self.robot.straight(20, 7, 0)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.3)

        ## to the train line
        self.robot.straight(30, -20, 0)
        self.robot.absTurn(30, -10, 23)
        self.robot.breakMotors()
        self.robot.straight(35, 15, 0)
        self.robot.absTurn(40, 105, 23)
        self.robot.breakMotors()
        self.robot.straight(35, -35, 0)
        self.robot.absTurn(20, 91, 23)
        self.robot.breakMotors()
        time.sleep(1)
        self.robot.straight(50, 40, 0)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.5)

        ## back to home
        self.robot.straight(50, -20, 0)
        self.robot.breakMotors()
        self.robot.absTurn(40, 180, 23)
        self.robot.breakMotors()
        self.robot.straight(65, 55, 0)
        self.robot.curve(65, 40, -40)
        self.robot.curve(65, 40, 30)
        self.robot.straight(65, 40, 0)
        self.robot.breakMotors()

    def runFour(self):
        '''the fourth script'''
        pass

    def cmToDeg(self, dist: float) -> float:
        '''converts a measurement from centimeters to degrees the moevement motors have to turn'''
        return dist / (self.config['wheelDiameter'] * pi) * 360