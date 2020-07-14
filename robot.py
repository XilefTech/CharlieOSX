import config
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Direction)


class Charlie():
    '''This is the main class of the robot. It contains all the functions CharlieOSX has to offer'''

    def __init__(self, configPath, settingsPath, logFileLocation):
        self.__configPath = configPath
        self.__logFileLocation = logFileLocation
        self.__configPath = configPath

        self.logger = Logger(self.__configPath, self.__logFileLocation)

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
