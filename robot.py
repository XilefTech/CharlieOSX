import config
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Direction)


class Charlie():
    '''This is the main class of the robot. It contains all the functions CharlieOSX has to offer'''

    def __init__(self, configPath, settingsPath, logFileLocation):
        self.__configPath = configPath
        self.__logFileLocation = logFileLocation
        self.__configPath = configPath

        self.brick = EV3Brick()
        self.logger = Logger(self.__configPath, self.__logFileLocation, self.brick)

        __initSensors()
        __initMotors()
    
    def __repr__(self):
        return "TODO"
  
    def __str__(self):
        return "TODO"

    def __initMotors(self):
        self.logger.debug("Starting motor initialisation...")
        if config.robotType == 'NORMAL':
            try:
                self.__lMotor = Motor(config.leftMotorPort, Direction.CLOCKWISE if (not config.leftMotorInverted) else Direction.COUNTERCLOCKWISE)
                self.__rMotor = Motor(config.rightMotorPort, Direction.CLOCKWISE if (not config.rightMotorInverted) else Direction.COUNTERCLOCKWISE)
            except as Exception:
                self.logger.error("Failed to initialize movement motors for robot type NORMAL - Are u sure they\'re all connected?")
                self.logger.error(Exception)

            if config.useGearing:
                try:
                    self.__gearingPortMotor = Motor(config.gearingSelectMotorPort, Direction.CLOCKWISE if (not config.gearingSelectMotorPortInverted) else Direction.COUNTERCLOCKWISE)
                    self.__gearingTurnMotor = Motor(config.gearingTurnMotorPort, Direction.CLOCKWISE if (not config.gearingTurnMotorPortInverted) else Direction.COUNTERCLOCKWISE)
                except as Exception:
                    self.logger.error("Failed to initialize action motors for the gearing - Are u sure they\'re all connected?")
                    self.logger.error(Exception)
            else:
                try:
                    self.__aMotor1 = Motor(config.firstActionMotorPort, Direction.CLOCKWISE if (not config.firstActionMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.firstActionMotorPort != 0) else 0
                    self.__aMotor2 = Motor(config.secondActionMotorPort, Direction.CLOCKWISE if (not config.secondActionMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.secondActionMotorPort != 0) else 0
                except as Exception:
                    self.logger.error("Failed to initialize action motors - Are u sure they\'re all connected?")
                    self.logger.error(Exception)

        else:
            try:
                self.__fRMotor = Motor(config.frontRightMotorPort, Direction.CLOCKWISE if (not config.frontRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.frontRightMotorPort != 0) else 0
                self.__bRMotor = Motor(config.backRightMotorPort, Direction.CLOCKWISE if (not config.backRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.backRightMotorPort != 0) else 0
                self.__fLMotor = Motor(config.frontLeftMotorPort, Direction.CLOCKWISE if (not config.frontLeftMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.frontLeftMotorPort != 0) else 0
                self.__bLMotor = Motor(config.backLeftMotorPort, Direction.CLOCKWISE if (not config.backLeftMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.backLeftMotorPort != 0) else 0
            except as Exception:
                self.logger.error("Failed to initialize movement motors for robot type %s - Are u sure they\'re all connected?" % config.robotType)
                self.logger.error(Exception)
        self.logger.debug("Motor initialisation done")

    def __initSensors(self):
        self.logger.debug("Starting sensor initialisation...")
        try:
            self.__gyro = GyroSensor(config.gyroSensorPort) if config.gyroSensorPort != 0 else 0
        except as Exception:
            self.__gyro = 0
            self.logger.error("Failed to initialize the Gyro-Sensor - Are u sure it's connected (to the right port)?")
            self.logger.error(Exception)

        try:
            self.__rLight = ColorSensor(config.rightLightSensorPort) if (config.rightLightSensorPort != 0) else 0
        except as Exception:
            self.logger.error("Failed to initialize the right Color-Sensor - Are u sure it's connected (to the right port)?")
            self.logger.error(Exception)

        try:
            self.__lLight = ColorSensor(config.leftLightSensorPort) if (config.leftLightSensorPort != 0) else 0  
        except as Exception:
            self.logger.error("Failed to initialize the left Color-Sensor - Are u sure it's connected (to the right port)?")
            self.logger.error(Exception)

        try:
            self.__touch = TouchSensor(config.touchSensorPort) if (config.touchSensorPort != 0) else 0
        except as Exception:
            self.logger.error("Failed to initialize the Touch-Sensor - Are u sure it's connected (to the right port)?")
            self.logger.error(Exception)

        self.logger.debug("Sensor initialisation done")

    def execute(self, params):
        """Starts the different Driving modules according to the given parameters"""

        if self.brick.battery.voltage()() <= 7500:
            self.logger.warn("Please charge the battery. Only %sV left. We recommend least 7.5 Volts for accurate and repeatable results." % self.brick.battery.voltage() * 0.001)
            return 'failed to execute: Battery to low'

        if self.__gyro == 0:
            self.logger.error("Cannot drive without gyro")
            return 'error: no gyro'

        __gyro.reset_angle(0)
        while params != [] and not any(charlie.buttons()):
            mode, arg1, arg2, arg3 = params.pop(0), params.pop(0), params.pop(0), params.pop(0)

            methods = { 4: turn(),
                        5: gearing(), if config.useGearing else actionMotors(),
                        7: straight(), if config.robotType != 'MECANUM' else straightMecanum(),
                        9: intervall(),
                        11: curveShape(),
                        12: toColor(),
                        15: toWall()}
            
            methods[mode](arg1, arg2, arg3)
            
        breakMotors()

        if config.useGearing:
            gearingPortMotor.run_target(300, 0, Stop.HOLD, True)    #reset gearing

    def breakMotors(self):
        if config.robotType == 'NORMAL':
            lMotor.run_angle(100, 0, Stop.HOLD, False)
            rMotor.run_angle(100, 0, Stop.HOLD, False)
        else:
            fRMotor.run_angle(100, 0, Stop.HOLD, False)
            bRMotor.run_angle(100, 0, Stop.HOLD, False)
            fLMotor.run_angle(100, 0, Stop.HOLD, False)
            bLMotor.run_angle(100, 0, Stop.HOLD, False)

    def turn(self, speed, deg, port):
        """turns deg with speed. port indicates with wich motor(s)"""
        startValue = self.__gyro.angle()

        #turn only with left motor
        if port == 2:
            #right motor off
            __rMotor.dc(0)
            #turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    if config.robotType == 'NORMAL':
                        __lMotor.dc(speed)
                    else:
                        __fLMotor.dc(speed)
                        __bLMotor.dc(speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return
            else:
                while self.__gyro.angle() - startValue > deg:
                    if config.robotType == 'NORMAL':
                        __lMotor.dc(-speed)
                    else:
                        __fLMotor.dc(-speed)
                        __bLMotor.dc(-speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return

        #turn only with right motor
        elif port == 3:
            #left motor off
            __lMotor.dc(0)
            #turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    if config.robotType == 'NORMAL':
                        __rMotor.dc(-speed)
                    else:
                        __fRMotor.dc(-speed)
                        __bRMotor.dc(-speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return                 
            else:
                while self.__gyro.angle() - startValue > deg:
                    if config.robotType == 'NORMAL':
                        __rMotor.dc(speed)
                    else:
                        __fRMotor.dc(speed)
                        __bRMotor.dc(speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed
                    
                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return

        #turn with both motors
        elif port == 23:
            #turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    if config.robotType == 'NORMAL':
                        __rMotor.dc(-speed / 2)
                        __lMotor.dc(speed / 2)
                    else:
                        __fRMotor.dc(-speed / 2)
                        __bRMotor.dc(-speed / 2)
                        __fLMotor.dc(speed / 2)
                        __bLMotor.dc(speed / 2)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.01) if speed > 40 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return    
                    
            else:
                while self.__gyro.angle() - startValue > deg:
                    if config.robotType == 'NORMAL':
                        __rMotor.dc(speed / 2)
                        __lMotor.dc(-speed / 2)
                    else:
                        __fRMotor.dc(speed / 2)
                        __bRMotor.dc(speed / 2)
                        __fLMotor.dc(-speed / 2)
                        __bLMotor.dc(-speed / 2)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.01) if speed > 40 else speed
                    
                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return