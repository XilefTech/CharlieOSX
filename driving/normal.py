from lib.logging import Logger
from driving.robot import Robot
import time
from math import pi
from lib.simple_pid import PID


class NormalDriving():
    '''docstring'''

    def __init__(self, robot: Robot, logger: Logger, config: dict, sensorAssist=True, doAccel=True, doDecel=True):
        if config['robotType'] != "NORMAL":
            raise TypeError("Wrong robot type configured for use of this class")

        self.robot = robot
        self.logger = logger
        self.sensorAssist = sensorAssist
        self.doAccel = doAccel
        self.doDecel = doDecel
        self.maxSpeed = self.robot.lMotor.control.limits()[0]

        self.wheelDiameter = config["wheelDiameter"]
        self.wheelDistance = config["wheelDistance"]

        self.acceleration = config["acceleration"]
        self.deceleration = config["deceleration"]
        self.setAccel(self.acceleration)

        if sensorAssist:
            try:
                robot.gyro
            except NameError:
                robot.gyro = None
                self.sensorAssist = False
                self.logger.warn(self, "No Gyro Connected, Sensor-Assisted Driving unavailiable.")
                self.logger.warn(self, "\tPlease note: some functions are currently not availiable, since they rlie on a gyro sensor")
                self.logger.warn(self, "\tTherefore, some functions might return without doing anything")

        self.pid = PID(Kp=0.88, Ki=0.11, Kd=0.3, setpoint=0)
        self.pid.sample_time = 0.01
        

    def turnLeftMotor(self, relativeSpeed):
        '''
        converts the relative speed into absolute measurement in °/s for the motor to rotate at

        Args:
            speed (float): the speed to drive the motor at (in percent)
        '''
        ## calculate speed in deg/s
        speed = self.map(relativeSpeed, 0, 100, 0, self.maxSpeed)

        self.robot.lMotor.run(speed)

    def turnRightMotor(self, relativeSpeed):
        '''
        converts the relative speed into absolute measurement in °/s for the motor to rotate at

        Args:
            speed (float): the speed to drive the motor at (in percent)
        '''
        ## calculate speed in deg/s
        speed = self.map(relativeSpeed, 0, 100, 0, self.maxSpeed)

        self.robot.rMotor.run(speed)

    def map(self, x, in_min, in_max, out_min, out_max) -> float:
        '''
        Converts a given number in the range of two numbers to a number in the range of two other numbers

        Args:
            x (int): the input number that should be converted
            in_min (int): The minimal point of the range of input number
            in_max (int): The maximal point of the range of input number
            out_min (int): The minimal point of the range of output number
            out_max (int): The maximal point of the range of output number

        Returns:
        float: a number between out_min and out_max
        '''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min