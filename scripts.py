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
        self.robot.rMotor.run_angle(550, self.cmToDeg(107), then=Stop.COAST, wait=False)
        self.robot.lMotor.run_angle(500, self.cmToDeg(107), then=Stop.COAST, wait=True)
        #driving.straight(45, 107, 0)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(800, 90, wait=False)
        driving.straight(12, 20, 0)
        driving.breakMotors(coast=True)
        time.sleep(0.2)
        driving.setAccel(self.config["acceleration"])
        EV3Brick().speaker.beep()

        ## go deliver chicken
        driving.straight(35, -4, 0)
        driving.breakMotors()
        driving.turn(30, 18, 23, min_speed=90)
        driving.breakMotors()
        driving.straight(50, -12, 0)
        driving.breakMotors()
        driving.absTurn(20, 0, 23, min_speed=90)
        driving.breakMotors()
        driving.straight(70, -38, 0)
        driving.breakMotors()
        driving.absTurn(30, 33, 23, min_speed=100)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(800, -90)

        ## home sweet home
        driving.straight(10, -12, 0)
        driving.absTurn(50, 17, 2, min_speed=120)
        driving.breakMotors()
        driving.straight(95, -100, 0)

    def runTwo(self):
        '''the second script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-45)
        time.sleep(0.5)

        ## go out of base 
        driving.straight(50, 10, 0)
        driving.absTurn(30, -50, 23, min_speed=50)
        driving.breakMotors()
        driving.straight(60, 59, 0)

        ## to crane (west dock)
        driving.breakMotors()
        driving.absTurn(30, -5, 23, min_speed=60)
        driving.breakMotors()
        time.sleep(0.3)
        self.legacyRobot.toColor(40, 0, 2)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        driving.straight(90, 23, 0)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(600, 260, then=Stop.COAST, wait=True) # extend side arm
        driving.absTurn(10, 10, 2)
        driving.breakMotors()
        driving.straight(12, 15, 0)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(600, -260, then=Stop.COAST, wait=True) # retract side arm

        
        ## off we go further into the depths of the field
        driving.straight(70, 32, 0)
        driving.absTurn(30, 86, 2, min_speed=60)
        driving.breakMotors()
        
        self.robot.aMotor2.run_angle(800, 360, then=Stop.COAST, wait=False) # extend side arm
        self.robot.aMotor1.run_angle(900, -90 * (20/12), then=Stop.HOLD, wait=True) # put down fork
        time.sleep(0.3)

        driving.straight(50, 13, 0)
        driving.breakMotors()

        self.robot.aMotor2.run_angle(400, -360, then=Stop.COAST, wait=False) # retract side arm
        self.robot.aMotor1.run_angle(900, 60 * (20/12), then=Stop.HOLD, wait=True) # put down fork

        driving.straight(90, -15, 0, connect=True)
        driving.breakMotors(coast=True)

    def runThree(self):
        '''the third script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-90)
        self.robot.aMotor1.run_angle(50, -17, then=Stop.BRAKE)

        ## to the engine
        driving.straight(80, 50, 0)
        driving.turn(20, -50, 3, min_speed=100)
        driving.breakMotors()
        driving.straight(40, 10, 0)
        driving.breakMotors()
        driving.straight(40, -10, 0)
        driving.turn(20, 50, 3, min_speed=100)
        driving.breakMotors()
        driving.straight(70, 17, 0)
        driving.absTurn(20, -58, 3, min_speed=70)
        driving.breakMotors()
        self.legacyRobot.toColor(35, 0, 2)
        driving.breakMotors()
        driving.straight(50, 17, 0)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        driving.straight(50, -5, 0)
        driving.breakMotors()
        self.robot.aMotor1.run_angle(200, -90)

        ## cargo plane
        driving.straight(80, -16, 0)
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
        driving.straight(50, 10, 0)
        driving.turn(30, 20, 2, min_speed=60)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(2000, 180)
        driving.straight(90, -23, 0)
        driving.breakMotors()

        ## homee
        driving.absTurn(40, -250, 2, min_speed=100)
        driving.breakMotors()
        driving.straight(80, 70, 0)
        driving.breakMotors()

    def runFour(self):
        '''the fourth script'''
        driving = self.robot.driving

        self.robot.gyro.reset_angle(-45)
        driving.setAccel(30)
        
        ## go out of base 
        driving.straight(50, 10, 0)
        driving.absTurn(30, -46, 23, min_speed=50)
        driving.breakMotors()
        driving.straight(60, 60, 0)
        driving.breakMotors()

        ## to blue ciiircle
        driving.absTurn(30, -5, 23, min_speed=80)
        driving.breakMotors()
        time.sleep(0.3)
        self.legacyRobot.toColor(30, 0, 2)
        driving.breakMotors()
        self.robot.brick.speaker.beep()
        driving.turn(10, 3, 2, min_speed=80)
        driving.breakMotors()
        driving.straight(40, 20, 0)
        self.legacyRobot.toColor(30, 0, 2)
        driving.breakMotors()
        driving.straight(50, 25, 0, connect=True)
        driving.absTurn(30, -45, 3, min_speed=70)
        driving.breakMotors()
        driving.straight(60, 22, 0)
        driving.breakMotors()
        self.robot.aMotor2.run_angle(140, 80)
        time.sleep(0.2)
        self.robot.aMotor2.run_angle(100, -40)
        time.sleep(0.5)

        ## chooo chooooooo
        driving.absTurn(30, 20, 2, min_speed=80)
        driving.absTurn(30, 60, 23, min_speed=60)
        driving.breakMotors()
        driving.straight(30, 4, 0)
        driving.absTurn(30, 89, 2, min_speed=40)
        driving.breakMotors()
        driving.straight(50, 20, 0)
        driving.breakMotors()


    def cmToDeg(self, dist: float) -> float:
        '''converts a measurement from centimeters to degrees the moevement motors have to turn'''
        return dist / (self.config['wheelDiameter'] * pi) * 360