from robot import Charlie
from driving.robot import Robot
from math import pi
from pybricks.parameters import (Stop, Color)
from pybricks.hubs import EV3Brick
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
            self.runTwo,
            self.runThree,
            self.runOne,
            self.runFour
        ]

    def runOne(self):
        '''the first script (FLL-Run 2021/22: Wing, Packet, Bridge and wagon cargo)'''
        driving = self.robot.driving

        ## drive to doorstep
        driving.setAccel(5)
        driving.straight(45, 107, 0)
        driving.breakMotors()
        #self.robot.rMotor.run_angle(500, self.cmToDeg(108), then=Stop.Coast, wait=False)
        #self.robot.lMotor.run_angle(500, self.cmToDeg(108), then=Stop.Coast, wait=True)
        self.robot.aMotor1.run_angle(800, 90, wait=False)
        driving.straight(12, 20, 0)
        driving.breakMotors(coast=True)
        time.sleep(0.2)
        driving.setAccel(self.config["acceleration"]-5)
        EV3Brick().speaker.beep()

        driving.straight(35, -8, 0)
        print("turning")
        driving.absTurn(10, -45, 3, min_speed=100)
        driving.breakMotors()
        driving.straight(80, 52, 0)
        driving.absTurn(10, 0, 23, min_speed=100)
        driving.breakMotors()
        driving.breakMotors()
        self.robot.aMotor2.run_angle(90, 160)
        EV3Brick().speaker.beep()
        EV3Brick().speaker.beep()
        driving.straight(50, -8, 0)
        self.robot.aMotor2.run_angle(120, -90, wait=False)
        driving.absTurn(30, 130, 23, min_speed=100)
        driving.breakMotors()
        time.sleep(0.2)
        driving.straight(60, 20, 0)
        driving.absTurn(30, 148, 23, min_speed=80)
        driving.breakMotors()
        time.sleep(0.2)
        driving.straight(70, 39, 0)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(300, -90)
        driving.straight(50, -20, 0)
        driving.absTurn(20, 175, 23, min_speed=50)
        driving.breakMotors()
        time.sleep(0.2)
        driving.straight(100, 100, 0)



        driving.breakMotors()
        time.sleep(1)

    def runTwo(self):
        '''the second script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-45)
        time.sleep(0.5)

        

        time.sleep(100)
        ## to the crane
        driving.straight(90, 75, 0)
        driving.absTurn(10, -15, 23, min_speed=40)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        time.sleep(0.5)

        # push crane over
        driving.straight(90, 50, 0)
        driving.absTurn(10, 8, 23, min_speed=40)
        driving.straight(10, 15, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()

        ## manuver around crane
        driving.straight(70, -15, 0)
        driving.absTurn(10, 45, 23, min_speed=40)
        driving.breakMotors()
        time.sleep(0.3)
        driving.straight(80, 15, 0)
        driving.absTurn(10, 0, 23, min_speed=40)
        driving.breakMotors()
        time.sleep(0.3)
        driving.straight(35, 25, 0)

        ## backwards to wall
        driving.absTurn(10, 130, 23, min_speed=40)
        driving.breakMotors()
        time.sleep(0.3)
        driving.straight(50, -20, 0)
        driving.absTurn(20, 90, 23, min_speed=40)
        driving.breakMotors()

        self.robot.aMotor2.run_angle(400, -180, then=Stop.COAST, wait=False) # extend side arm

        ## go to work
        self.robot.aMotor1.run_angle(900, -90 * (20/12), then=Stop.HOLD, wait=True) # put down fork
        time.sleep(0.3)
        driving.straight(30, 32, 0)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(300, 180, then=Stop.COAST, wait=False) # flip rail-piece
        self.robot.aMotor1.run_angle(700, 100, then=Stop.HOLD, wait=True) # lift up containers
        time.sleep(0.3)

        driving.straight(40, -50, 0)
        driving.absTurn(30, 180, 23)
        driving.breakMotors()

    def runThree(self):
        '''the third script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-90)
        self.robot.aMotor1.run_angle(50, -17, then=Stop.BRAKE)

        ## to the container station
        driving.straight(80, 67, 0)
        driving.absTurn(20, -59, 3, min_speed=70)
        driving.breakMotors()
        driving.straight(50, 32, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        driving.straight(50, -4, 0)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(200, -90)

        ## cargo plane
        driving.straight(80, -17, 0)
        driving.absTurn(30, -133, 2, min_speed=80)
        driving.breakMotors()
        driving.straight(30, 4, 0)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(200, 110, then=Stop.HOLD, wait=False)
        driving.straight(30, -14, 0)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(400, -60)
        driving.turn(10, 30, 23, min_speed=70)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(200, 60)
        driving.absTurn(20, -135, 3, min_speed=60)
        self.robot.aMotor1.run_angle(800, -100)

        ## go do the plane
        driving.absTurn(10, -330, 23, min_speed=100)
        driving.breakMotors()
        driving.straight(50, 6.5, 0)
        driving.turn(30, 25, 2, min_speed=50)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(2000, 180)
        driving.straight(90, -20, 0)
        driving.breakMotors()

        ## homee
        driving.absTurn(40, -270, 2, min_speed=100)
        driving.straight(100, 50, 0)
        driving.breakMotors()

        

    def runFour(self):
        '''the fourth script'''
        pass

    def cmToDeg(self, dist: float) -> float:
        '''converts a measurement from centimeters to degrees the moevement motors have to turn'''
        return dist / (self.config['wheelDiameter'] * pi) * 360