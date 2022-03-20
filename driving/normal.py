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
        
    def setAccel(self, acceleration):
        '''
        set the acceleration rate

        Args:
            acceleration (float): the acceleration value
        '''
        circ = self.wheelDiameter * pi
        cmPerDeg = 360 / circ
        acceleration = acceleration * cmPerDeg

        self.robot.lMotor.control.limits(self.maxSpeed, acceleration, 100)
        self.robot.rMotor.control.limits(self.maxSpeed, acceleration, 100)
    
    def enableAccel(self, doAccel: bool):
        '''
        Enable/Disable Acceleration for all Driving operations

        Args:
            doAccel (bool): the current state of acceleration
        '''
        self.doAccel = doAccel

        # set motor acceleration accordingly
        if doAccel:
            self.setAccel(self.acceleration)
        else:
            self.robot.lMotor.control.limits(self.maxSpeed, 3000, 100)
            self.robot.rMotor.control.limits(self.maxSpeed, 3000, 100)
    
    def enableDecel(self, doDecel: bool):
        '''
        Enable/Disable Deceleration for all Driving operations

        Args:
            doDecel (bool): the current state of deceleration
        '''
        self.doDecel = doDecel

    def straight(self, speed, dist, ang, connect=False):
        '''
        Steers the Robot in a straight line forwards/backwards.
        Optional Acceletation & Deceleration (Enable/Disable with setAccel() & setDecel())

        Args:
            speed (int): the speed to drive at (in percent)
            dist (int): the distance (in cm) to drive
        kwArgs:
            connect (bool): used for smooth connection to following driving actions, disables deceleration
        '''
        ## a bit of variable setup & math
        speed = 100 if speed > 100 else abs(speed)   # cap the max speed at 100% and ensure it's positive
        speed = self.map(speed, 0, 100, 0, self.maxSpeed) # convert speed to deg/s
        rSpeed, lSpeed = speed, speed

        revs = dist / (self.wheelDiameter * pi) # convert the input (cm) to revs

        steer = 0
        direction = 1 if revs > 0 else -1

        ## deceleration
        trueSpeed, decelTime, decelDistance = self.getDecelValues(speed)
        #trueSpeed = (self.wheelDiameter * pi) / 360 * speed
        #decelTime = trueSpeed / self.deceleration
        #decelDistance = 0.5 * self.deceleration * decelTime**2
        #print(speed, "\t", trueSpeed, "\t", decelTime, "\t", decelDistance)


        ## robot sensor readout & setup
        self.pid.setpoint = self.robot.gyro.angle()
        self.robot.rMotor.reset_angle(0)

        # drive
        while abs(revs) > abs(self.robot.rMotor.angle() / 360):
            timer = time.perf_counter() # get time for accurate loop-timing

            ## line-correction
            pidValue = int(self.pid(self.robot.gyro.angle()) * 0.125)
            steer += pidValue

            rSpeed = speed - steer if steer > 0 else speed
            lSpeed = speed + steer if steer < 0 else speed

            self.robot.lMotor.run(direction * lSpeed if lSpeed > 0 else 0)
            self.robot.rMotor.run(direction * rSpeed if rSpeed > 0 else 0)
            
            ## deceleration
            drivenDistance = abs(self.robot.rMotor.angle() / 360) * (self.wheelDiameter * pi)
            if self.doDecel and drivenDistance >= dist - decelDistance and not connect:
                decelDist = drivenDistance - (dist - decelDistance)
                robotSpeed = trueSpeed - (2 * self.deceleration * decelDist)**0.5
                speed = robotSpeed / (self.wheelDiameter * pi / 360) if robotSpeed / (self.wheelDiameter * pi / 360) > 20 else 20

            ## cancel if button pressed
            if any(EV3Brick().buttons.pressed()):
                return
            
            ## ensure consistent loop timing
            while time.perf_counter() - timer < 0.05:
                pass

    def turn(self, speed, deg, port, absolute=False):
        '''
        Used to turn the robot on the spot using either one or both Motors for turning

        Args:
            speed (int): the speed to drive at
            deg (int): the angle to turn
            port (int): the motor(s) to turn with
        '''
        startValue = self.robot.gyro.angle() if not absolute else 0
        speed = self.speedClean(speed)

        # turn only with one motor
        if port is 2 or port is 3:
            # stop non-turning motor
            self.robot.rMotor.hold() if port is 2 else self.robot.lMotor.hold()

            dist = pi * self.wheelDistance * 2 * (deg/360)
            trueSpeed, decelTime, decelDistance = self.getDecelValues(speed)
            #print(speed, "\t", trueSpeed, "\t", decelTime, "\t", decelDistance)

            turningMotor = self.robot.lMotor if port is 2 else self.robot.rMotor
            direction = 1 if port is 2 else -1

            # turn the angle
            if deg > 0:     
                while self.robot.gyro.angle() - startValue < deg:
                    timer = time.perf_counter() # get time for accurate loop-timing

                    turningMotor.run(speed * direction)

                    ## deceleration
                    drivenDistance = abs(turningMotor.angle() / 360) * (self.wheelDiameter * pi)
                    if self.doDecel and drivenDistance >= dist - decelDistance:
                        decelDist = drivenDistance - (dist - decelDistance)
                        robotSpeed = trueSpeed - (2 * self.deceleration * decelDist)**0.5
                        speed = robotSpeed / (self.wheelDiameter * pi / 360) if robotSpeed / (self.wheelDiameter * pi / 360) > 20 else 20

                    ## cancel if button pressed
                    if any(EV3Brick().buttons.pressed()):
                        return

                    ## ensure consistent loop timing
                    while time.perf_counter() - timer < 0.05:
                        pass
            else:
                while self.robot.gyro.angle() - startValue > deg:
                    timer = time.perf_counter() # get time for accurate loop-timing

                    turningMotor.run(-speed * direction)

                    ## deceleration
                    drivenDistance = abs(turningMotor.angle() / 360) * (self.wheelDiameter * pi)
                    if self.doDecel and drivenDistance >= dist - decelDistance:
                        decelDist = drivenDistance - (dist - decelDistance)
                        robotSpeed = trueSpeed - (2 * self.deceleration * decelDist)**0.5
                        speed = robotSpeed / (self.wheelDiameter * pi / 360) if robotSpeed / (self.wheelDiameter * pi / 360) > 20 else 20
                        
                    ## cancel if button pressed
                    if any(EV3Brick().buttons.pressed()):
                        return

                    ## ensure consistent loop timing
                    while time.perf_counter() - timer < 0.05:
                        pass

        # turn with both motors
        elif port is 23:
            dualMotorbonus = 4
            speed = speed * 2

            dist = pi * self.wheelDistance * (deg/360)
            trueSpeed, decelTime, decelDistance = self.getDecelValues(speed)
            #print(speed, "\t", trueSpeed, "\t", decelTime, "\t", decelDistance)

            # turn the angle
            if deg > 0:
                while self.robot.gyro.angle() - startValue < deg:
                    timer = time.perf_counter() # get time for accurate loop-timing

                    self.robot.lMotor.run(speed / 1.5)
                    self.robot.rMotor.run(-speed / 1.5)

                    ## deceleration
                    drivenDistance = abs(self.robot.rMotor.angle() / 360) * (self.wheelDiameter * pi)
                    if self.doDecel and drivenDistance >= dist - decelDistance:
                        decelDist = drivenDistance - (dist - decelDistance)
                        robotSpeed = trueSpeed - (2 * self.deceleration * decelDist)**0.5
                        speed = robotSpeed / (self.wheelDiameter * pi / 360) if robotSpeed / (self.wheelDiameter * pi / 360) > 20 else 20

                    # cancel if button pressed
                    if any(EV3Brick().buttons.pressed()):
                        return

                    ## ensure consistent loop timing
                    while time.perf_counter() - timer < 0.05:
                        pass

            else:
                while self.robot.gyro.angle() - startValue > deg:
                    timer = time.perf_counter() # get time for accurate loop-timing

                    self.robot.lMotor.run(speed / 1.5)
                    self.robot.rMotor.run(-speed / 1.5)
                    
                    ## deceleration
                    drivenDistance = abs(self.robot.rMotor.angle() / 360) * (self.wheelDiameter * pi)
                    if self.doDecel and drivenDistance >= dist - decelDistance:
                        decelDist = drivenDistance - (dist - decelDistance)
                        robotSpeed = trueSpeed - (2 * self.deceleration * decelDist)**0.5
                        speed = robotSpeed / (self.wheelDiameter * pi / 360) if robotSpeed / (self.wheelDiameter * pi / 360) > 20 else 20

                    # cancel if button pressed
                    if any(EV3Brick().buttons.pressed()):
                        return

                    ## ensure consistent loop timing
                    while time.perf_counter() - timer < 0.05:
                        pass

    def absTurn(self, speed, deg, port):
        '''
        Used to turn the motor on the spot using either one
        This method turns (in contrast to the normal turn() method) to an absolute ange (compared to starting point)

        Args:
            speed (int): the speed to drive at
            deg (int): the angle to turn to
            port (int): the motor(s) to turn with
        '''
        self.turn(speed, deg, port, absolute=True)

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

    def breakMotors(self, coast=False):
        '''Sub-method for breaking all the motors'''
        if not coast:
            self.__lMotor.hold()
            self.__rMotor.hold()

            if self.__aMotor1:
                self.__aMotor1.hold()
            if self.__aMotor2:
                self.__aMotor2.hold()

            time.sleep(0.1)
        else:
            self.__lMotor.stop()
            self.__rMotor.stop()

            if self.__aMotor1:
                self.__aMotor1.stop()
            if self.__aMotor2:
                self.__aMotor2.stop()

    def getDecelValues(self, speed):
        '''calculates trueSpeed, decelTime and decelDistance from given speed'''
        trueSpeed = (self.wheelDiameter * pi) / 360 * speed
        decelTime = trueSpeed / self.deceleration
        decelDistance = 0.5 * self.deceleration * decelTime**2
        return trueSpeed, decelTime, decelDistance

    def speedClean(self, speed):
        '''converts the speed from percent to deg/s'''
        speed = 100 if speed > 100 else abs(speed)   # cap the max speed at 100% and ensure it's positive
        speed = self.map(speed, 0, 100, 0, self.maxSpeed) # convert speed to deg/s
        return speed

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