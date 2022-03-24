from pybricks.ev3devices import GyroSensor, ColorSensor, TouchSensor, Motor
from pybricks.parameters import Port, Direction
from pybricks.hubs import EV3Brick

from lib.logging import Logger


class Robot():
    '''
    Robot holds all data of your robot.
    You can access all Motors & Sensors from variables in this class

    Args:
        config (dict): The parsed config
        brick (EV3Brick): EV3Brick for getting button input
        logger (Logger): Logger for logging
    '''

    def __init__(self, config: dict, brick, logger: Logger):
        logger.info(self, 'Starting initialisation of Charlie')
        self.config = config

        self.brick = EV3Brick()
        self.logger = logger

        self.__conf2port = {1: Port.S1, 2: Port.S2, 3: Port.S3, 4: Port.S4, 'A': Port.A, 'B': Port.B, 'C': Port.C, 'D': Port.D}

        ## general robot information
        self.type = self.config['robotType']
        self.hasGearing = self.config['useGearing']


        if self.type == "NORMAL":
            self.__initSensors()
            self.__initNormalMotors()
        else:
            print("Other Robot Types other than NORMAL are curently not supported by the new driving system.")
            print("Please use the old robot.py")

        ### TODO: Find something better than this
        self.gyro.reset_angle(0) if self.gyro != 0 else self.logger.error(self, "No gyro attached, robot movement will probably not work and you likely will receive crashes", None)
        
        if self.type == "NORMAL":
            from driving.normal import NormalDriving
            self.driving = NormalDriving(self, logger, config)

        self.logger.info(self, 'Robot initialized')

    def __repr__(self):
        ### TODO: get all device-connections, put them together in a program-readable form (and maybe also a readout of the device-values?)
        return "TODO"

    def __str__(self):
        ### TODO: collect stats of what is connected, and add them to this string (-> give full port layout in form of ascii-table)
        # + device-readout?
        return "Robot object"  

    def __initSensors(self):
        '''Sub-method for initializing Sensors.'''
        ### TODO: stop making this so oddly specific, open up more possibilities for color sensors
        self.logger.debug(self, "Starting sensor init...")

        ## gyro
        try:
            if self.config['gyroSensorPort'] != 0: 
                self.gyro = GyroSensor(self.__conf2port[self.config['gyroSensorPort']], self.getDirection("gyroInverted"))
                self.logger.debug(self, 'Gyrosensor initialized sucessfully on port %s' % self.config['gyroSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the Gyro-Sensor - Are u sure it's connected to Port %s?" % exception, exception)

        ## color sensor
        try:
            if self.config['rightLightSensorPort'] != 0: 
                self.rLight = ColorSensor(self.__conf2port[self.config['rightLightSensorPort']])
                self.logger.debug(self, 'Colorsensor initialized sucessfully on port %s' % self.config['rightLightSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the right Color-Sensor - Are u sure it's connected to Port %s?" % exception, exception)

        ## color sensor
        try:
            if self.config['leftLightSensorPort'] != 0: 
                self.lLight = ColorSensor(self.__conf2port[self.config['leftLightSensorPort']])
                self.logger.debug(self, 'Colorsensor initialized sucessfully on port %s' % self.config['leftLightSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the left Color-Sensor - Are u sure it's connected to Port %s?" % exception, exception)

        ## touch sensor
        try:
            if self.config['backTouchSensor'] != 0: 
                self.touch = TouchSensor(self.__conf2port[self.config['backTouchSensor']])
                self.logger.debug(self, 'Touchsensor initialized sucessfully on port %s' % self.config['backTouchSensor'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the Touch-Sensor - Are u sure it's connected to Port %s?" % exception, exception)

        self.logger.debug(self, "Sensor init done")

    def __initNormalMotors(self):
        '''Sub-method for initializing Motors.'''
        self.logger.debug(self, "Starting motor init...")
        
        ## movement motors
        try:
            self.lMotor = Motor(port=self.__conf2port[self.config['leftMotorPort']],
                                positive_direction=self.getDirection("leftMotorInverted"),
                                gears = self.config['leftMotorGears'])

            self.rMotor = Motor(port=self.__conf2port[self.config['rightMotorPort']],
                                positive_direction=self.getDirection("rightMotorInverted"),
                                gears = self.config['rightMotorGears'])

        except Exception as exception:
            self.logger.error(self, "Failed to initialize movement motors for robot type NORMAL - Are u sure they're all connected?", exception)
        

        ## gearing motors
        if self.hasGearing:
            try:
                self.gearingPortMotor = Motor(port=self.__conf2port[self.config['gearingSelectMotorPort']],
                                            positive_direction=self.getDirection("gearingSelectMotorInverted"),
                                            gears = self.config['gearingSelectMotorGears'])

                self.gearingTurnMotor = Motor(port=self.__conf2port[self.config['gearingTurnMotorPort']],
                                            positive_direction=self.getDirection("gearingTurnMotorInverted"),
                                            gears = self.config['gearingTurnMotorGears'])

            except Exception as exception:
                self.logger.error(self, "Failed to initialize action motors as gearing - Are u sure they're all connected?", exception)

        ## no gearing
        else:
            try:
                if self.config['firstActionMotorPort'] != 0:
                    self.aMotor1 = Motor(port=self.__conf2port[self.config['firstActionMotorPort']],
                                        positive_direction=self.getDirection("firstActionMotorInverted"),
                                        gears=self.config['firstActionMotorGears'])

                if self.config['secondActionMotorPort'] != 0:
                    self.aMotor2 = Motor(port=self.__conf2port[self.config['secondActionMotorPort']],
                                        positive_direction=self.getDirection("secondActionMotorInverted"),
                                        gears = self.config['secondActionMotorGears'])

            except Exception as exception:
                self.logger.error(self, "Failed to initialize action motors - Are u sure they're all connected?", exception)

        self.logger.debug(self, "Motor init done")

    def getDirection(self, key: str):
        '''Returns Direction.CLOCKWISE or COUNTERCLOCKWISE, based on the config entry at the given key'''
        return Direction.CLOCKWISE if (not self.config[key]) else Direction.COUNTERCLOCKWISE