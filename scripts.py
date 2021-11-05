
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
        ## drive to doorstep
        self.robot.__rMotor.run_angle(700, self.cmToDeg(123), then=Stop.BRAKE, wait=False)
        self.robot.__lMotor.run_angle(700, self.cmToDeg(123), then=Stop.BRAKE, wait=True)
        
        ## manuver out of the corner
        self.robot.straight(10, -3, 0)
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
        self.robot.straight(25, 12, 0)
        self.robot.turn(25, 45, 2)
        self.robot.breakMotors()
        self.robot.straight(25, 45, 0)
        self.robot.turn(30, 45, 2)
        self.robot.breakMotors()
        self.robot.__aMotor1.run_ang(300, 200, then=Stop.COAST, wait=True)

    def runThree(self):
        '''the third script'''
        pass

    def runFour(self):
        '''the fourth script'''
        pass

    def cmToDeg(self, dist: float) -> float:
        '''converts a measurement from centimeters to degrees the moevement motors have to turn'''
        return dist / (self.config['wheelDiameter'] * pi) * 360