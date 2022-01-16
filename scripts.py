
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

        ## push LKW to bridge
        self.robot.straight(40, 38, 0)
        self.robot.turn(30, 45, 23)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        self.robot.straight(30, 10, 0)
        self.robot.breakMotors()
        time.sleep(0.2)

        ## to the crane
        self.robot.straight(40, -35, 2)
        self.robot.breakMotors()
        self.robot.absTurn(30, -10, 23)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        self.robot.straight(40, 72, 0)
        self.robot.absTurn(30, 0, 23)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()

        ## push crane over
        self.robot.straight(30, 25, 0)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()

        ## to the ladevorrichtung
        self.robot.absTurn(30, 45, 3)
        self.robot.breakMotors()
        self.robot.straight(30, 16, 0)
        self.robot.absTurn(25, 0, 23)
        self.robot.breakMotors()
        self.robot.straight(30, 50, 0)

        ## backwards to wall
        self.robot.absTurn(25, 90, 23)
        self.robot.__aMotor2.run_angle(360, -4 * 360, then=Stop.COAST, wait=False)
        self.robot.straight(40, -55, 0)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.2)

        ## go to work
        self.robot.__aMotor1.run_angle(360, -270, then=Stop.COAST, wait=False)
        self.robot.straight(30, 60, 0)
        self.robot.breakMotors()
        self.robot.__aMotor2.run_angle(960, -4 * 360, then=Stop.COAST, wait=False)
        self.robot.__aMotor1.run_angle(270, 270, then=Stop.HOLD, wait=True)
        time.sleep(0.3)

        self.robot.straight(40, -50, 0)
        self.robot.absTurn(30, 180, 23)
        self.robot.breakMotors()

    def runThree(self):
        '''the third script'''
        self.robot.__gyro.reset_angle(-45)

        ## blue container knockout
        self.robot.straight(50, 40, 0)
        self.robot.absTurn(30, 0, 23)
        self.robot.breakMotors()
        self.robot.brick.speaker.beep()

        ## drive away and to wall
        self.robot.straight(50, -70, 0)
        self.robot.absTurn(40, -90, 23)
        self.robot.breakMotors()
        self.robot.straight(50, -40, 0)
        self.robot.breakMotors()

        ## from wall to container station on ship
        self.robot.straight(50, 55, 0)
        self.robot.breakMotors()
        self.robot.absTurn(50, 0, 2)
        self.robot.breakMotors()
        self.robot.straight(50, 40, 0)
        self.robot.breakMotors()
        self.robot.absTurn(40, -90, 23)
        self.robot.straight(40, 40, 0)
        self.robot.breakMotors()
        time.sleep(1)
        self.robot.brick.speaker.beep()

        ## from crane to platform
        self.robot.straight(50, -20, 0)
        self.robot.breakMotors()
        self.robot.turn(40, -120, 23)
        self.robot.breakMotors()
        self.robot.straight(50, -10, 0)
        self.robot.breakMotors()
        self.robot.absTurn(30, -90, 23)
        self.robot.breakMotors()
        self.robot.straight(50, 20, 0)
        self.robot.breakMotors()



        self.robot.breakMotors()
        time.sleep(2)
        # self.robot.absTurn(15, 0, 23)
        # self.robot.breakMotors()
        # time.sleep(0.3)
        # self.robot.brick.speaker.beep()
        # self.robot.straight(40, 95, 0)
        # self.robot.breakMotors()
        # self.robot.brick.speaker.beep()
        # self.robot.absTurn(20, -90, 23)
        # self.robot.straight(40, 22, 0)
        # self.robot.breakMotors()
        # time.sleep(0.3)

        ## push over the crane
        self.robot.straight(20, -20, 0)
        self.robot.absTurn(20, -40, 23)
        self.robot.breakMotors()
        self.robot.straight(20, 22, 0)
        self.robot.absTurn(20, 0, 2)
        self.robot.straight(20, 15, 0)

        ## train wagon push
        self.robot.absTurn(20, 140, 3)
        self.robot.straight(20, -20, 0)
        self.robot.absTurn(20, 90, 20)
        self.robot.straight(40, 20, 0)

        ## way home
        # TODO

    def runFour(self):
        '''the fourth script'''
        pass

    def cmToDeg(self, dist: float) -> float:
        '''converts a measurement from centimeters to degrees the moevement motors have to turn'''
        return dist / (self.config['wheelDiameter'] * pi) * 360