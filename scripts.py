
from robot import Charlie
from math import pi
from pybricks.parameters import Stop

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
        '''the first script (Wing, Packet, Bridge and ...)'''
        self.robot.__rMotor.run_angle(250, self.cmToDeg(115), then=Stop.BRAKE, wait=False)
        self.robot.__rMotor.run_angle(250, self.cmToDeg(115), then=Stop.BRAKE)

        self.robot.straight(20, -5, 0)
        self.robot.turn(20, -45, 23)
        self.robot.straight(50, 20, 0)

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
        return dist / (self.config['wheelDiameter'] * pi)