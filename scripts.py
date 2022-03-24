
from robot import Charlie
from driving.robot import Robot
from math import pi
from pybricks.parameters import (Stop, Color)
import time

class Scripts():
    '''runs'''

    def __init__(self, robot: Robot, config: dict, legacyRobot: Charlie):
        '''init'''
        print('init scripts')
        self.robot = robot
        self.legacyRobot = legacyRobot
        self.config = config

        self.scriptList = [
            self.runOne,
            self.runTwo,
            self.runThree,
            self.runFour
        ]

    def runOne(self):
        '''the first script (FLL-Run 2021/22: Wing, Packet, Bridge, helicoper and wagon cargo)'''
        driving = self.robot.driving

        ## drive to doorstep
        self.robot.__rMotor.run_angle(500, self.cmToDeg(130), then=Stop.BRAKE, wait=False)
        self.robot.__lMotor.run_angle(500, self.cmToDeg(130), then=Stop.BRAKE, wait=True)
        #self.robot.action(20, 7/8, 1)
        driving.breakMotors()
        self.robot.brick.speaker.beep()

        ## manuver out of the corner
        driving.straight(10, -3, 0)
        driving.breakMotors()
        driving.turn(30, 5, 23)
        driving.breakMotors()
        driving.straight(20, -22, 0)
        driving.turn(10, -1, 23)
        driving.breakMotors()
        driving.straight(15, 10, 0)

        ## to the helicopter and wagon
        driving.absTurn(2, -57, 3)
        driving.breakMotors()
        time.sleep(0.5)
        driving.straight(40, 60, 0)

        while self.robot.rLight.color() != Color.WHITE:
            pass

        driving.breakMotors()
        time.sleep(0.2)
        driving.straight(10, -2, 0)
        driving.breakMotors()
        driving.absTurn(10, 15, 2)
        driving.straight(10, 2, 0)
        driving.breakMotors()
        driving.absTurn(10, 0, 2)


        driving.breakMotors()
        time.sleep(1)

    def runTwo(self):
        '''the second script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-45)
        time.sleep(0.5)

        ## to the crane
        driving.straight(45, 65, 0)
        driving.absTurn(20, -5, 23)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.5)

        # push crane over
        driving.straight(40, 58, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()

        ## manuver around crane
        driving.straight(20, -10, 0)
        driving.absTurn(40, 45, 23)
        driving.breakMotors()
        time.sleep(0.3)
        driving.straight(35, 10, 0)
        driving.absTurn(50, 0, 23)
        driving.breakMotors()
        time.sleep(0.3)
        driving.straight(35, 16, 0)

        ## backwards to wall
        driving.absTurn(50, 110, 23)
        driving.breakMotors()
        time.sleep(0.3)
        driving.straight(20, -20, 0)
        driving.absTurn(20, 90, 23)
        driving.breakMotors()

        self.robot.aMotor2.run_angle(300, 0.9 * 360, then=Stop.COAST, wait=False) # extend side arm

        ## go to work
        self.robot.aMotor1.run_angle(800, 600 * 3, then=Stop.HOLD, wait=True) # put down fork
        time.sleep(0.3)
        driving.straight(30, 22, 0)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(300, -0.8 * 360, then=Stop.COAST, wait=False) # flip rail-piece
        self.robot.aMotor1.run_angle(700, -500 * 3, then=Stop.HOLD, wait=True) # lift up containers
        time.sleep(0.3)

        driving.straight(40, -50, 0)
        driving.absTurn(30, 180, 23)
        driving.breakMotors()

    def runThree(self):
        '''the third script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-90)

        ## to the container station
        driving.straight(20, 12, 0)
        driving.absTurn(20, -45, 3)
        driving.breakMotors()
        driving.straight(40, 73, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()

        driving.absTurn(20, 0, 2)
        driving.breakMotors()
        driving.straight(20, 5, 0) # 29? 19?
        self.legacyRobot.toColor(20, 0, 2) 
        driving.breakMotors()
        driving.absTurn(20, -90, 3)
        driving.breakMotors()
        driving.straight(20, 7, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.3)

        ## to the train line
        driving.straight(30, -20, 0)
        driving.absTurn(30, -10, 23)
        driving.breakMotors()
        driving.straight(35, 15, 0)
        driving.absTurn(40, 105, 23)
        driving.breakMotors()
        driving.straight(35, -35, 0)
        driving.absTurn(20, 91, 23)
        driving.breakMotors()
        time.sleep(1)
        driving.straight(50, 40, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.5)

        ## back to home
        driving.straight(50, -20, 0)
        driving.breakMotors()
        driving.absTurn(40, 180, 23)
        driving.breakMotors()
        driving.straight(65, 55, 0)
        self.legacyRobot.curve(65, 40, -40)
        self.legacyRobot.curve(65, 40, 30)
        driving.straight(65, 40, 0)
        driving.breakMotors()

    def runFour(self):
        '''the fourth script'''
        pass

    def cmToDeg(self, dist: float) -> float:
        '''converts a measurement from centimeters to degrees the moevement motors have to turn'''
        return dist / (self.config['wheelDiameter'] * pi) * 360