import math, _thread, time, math, copy
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Direction, Color, Stop)
from pybricks.media.ev3dev import Font


class Charlie():
    '''
    Charlie is the class responsible for driving,
    Robot-Movement and general Real-world interaction of the robot with Sensors and motors.

    Args:
        config (dict): The parsed config
        brick (EV3Brick): EV3Brick for getting button input
        logger (Logger): Logger for logging
    '''

    def __init__(self, config, brick, logger):
        logger.info(self, 'Starting initialisation of Charlie')
        self.__config = config

        self.brick = brick
        self.logger = logger

        self.__conf2port = {1: Port.S1, 2: Port.S2, 3: Port.S3, 4: Port.S4, 'A': Port.A, 'B': Port.B, 'C': Port.C, 'D': Port.D}

        self.__initSensors()
        self.__initMotors()

        self.min_speed = 35 # lage motor 20, medium motor 30
        
        self.__gyro.reset_angle(0)

        self.__screenRoutine = False
        self.showDetails()

        
        self.logger.info(self, 'Driving for Charlie initialized')
    ##TODO
    def __repr__(self):
        outputString = "(TODO)\n Config: " + self.__config + "\n Brick: " + self.brick + "\n Logger: " + self.logger
        outputString += "\n--Debug--\n Minimum Speed: "+ str(self.min_speed) + "\n "
        return "TODO"

    def __str__(self):
        return "Charlie"   

    def __initSensors(self):
        '''Sub-method for initializing Sensors.'''
        self.logger.debug(self, "Starting sensor initialisation...")
        try:
            self.__gyro = GyroSensor(self.__conf2port[self.__config['gyroSensorPort']], Direction.CLOCKWISE if not self.__config['gyroInverted'] else Direction.COUNTERCLOCKWISE) if self.__config['gyroSensorPort'] != 0 else 0
            self.logger.debug(self, 'Gyrosensor initialized sucessfully on port %s' % self.__config['gyroSensorPort'])
        except Exception as exception:
            self.__gyro = 0
            self.logger.error(self, "Failed to initialize the Gyro-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        try:
            self.__rLight = ColorSensor(
                self.__conf2port[self.__config['rightLightSensorPort']]) if self.__config['rightLightSensorPort'] != 0 else 0
            self.logger.debug(self, 'Colorsensor initialized sucessfully on port %s' % self.__config['rightLightSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the right Color-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        try:
            self.__lLight = ColorSensor(
                self.__conf2port[self.__config['leftLightSensorPort']]) if self.__config['leftLightSensorPort'] != 0 else 0
            self.logger.debug(self, 'Colorsensor initialized sucessfully on port %s' % self.__config['leftLightSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the left Color-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        try:
            self.__touch = TouchSensor(self.__conf2port[self.__config['backTouchSensor']]) if self.__config['backTouchSensor'] != 0 else 0
            self.logger.debug(self, 'Touchsensor initialized sucessfully on port %s' % self.__config['backTouchSensor'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the Touch-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        self.logger.debug(self, "Sensor initialisation done")

    def __initMotors(self):
        '''Sub-method for initializing Motors.'''
        self.logger.debug(self, "Starting motor initialisation...")
        if self.__config['robotType'] == 'NORMAL':
            try:
                self.__lMotor = Motor(self.__conf2port[self.__config['leftMotorPort']],
                    Direction.CLOCKWISE if (not self.__config['leftMotorInverted']) else Direction.COUNTERCLOCKWISE,
                    gears = self.__config['leftMotorGears'])
                self.__rMotor = Motor(self.__conf2port[self.__config['rightMotorPort']],
                    Direction.CLOCKWISE if (not self.__config['rightMotorInverted']) else Direction.COUNTERCLOCKWISE,
                    gears = self.__config['rightMotorGears'])
            except Exception as exception:
                self.logger.error(
                    self, "Failed to initialize movement motors for robot type NORMAL - Are u sure they\'re all connected?", exception)
            if self.__config['useGearing']:
                try:
                    self.__gearingPortMotor = Motor(self.__conf2port[self.__config['gearingSelectMotorPort']],
                        Direction.CLOCKWISE if (not self.__config['gearingSelectMotorInverted']) else Direction.COUNTERCLOCKWISE,
                        gears = self.__config['gearingSelectMotorGears'])
                    self.__gearingTurnMotor = Motor(self.__conf2port[self.__config['gearingTurnMotorPort']],
                        Direction.CLOCKWISE if (not self.__config['gearingTurnMotorInverted']) else Direction.COUNTERCLOCKWISE,
                        gears = self.__config['gearingTurnMotorGears'])
                except Exception as exception:
                    self.logger.error(
                        self, "Failed to initialize action motors for the gearing - Are u sure they\'re all connected?", exception)
            else:
                try:
                    self.__aMotor1 = Motor(self.__conf2port[self.__config['firstActionMotorPort']],
                        Direction.CLOCKWISE if (not self.__config['firstActionMotorInverted']) else Direction.COUNTERCLOCKWISE,
                        gears = self.__config['firstActionMotorGears']) if (self.__config['firstActionMotorPort'] != 0) else 0
                    self.__aMotor2 = Motor(self.__conf2port[self.__config['secondActionMotorPort']],
                        Direction.CLOCKWISE if (not self.__config['secondActionMotorInverted']) else Direction.COUNTERCLOCKWISE,
                        gears = self.__config['secondActionMotorGears']) if (self.__config['secondActionMotorPort'] != 0) else 0
                except Exception as exception:
                    self.logger.error(
                        self, "Failed to initialize action motors - Are u sure they\'re all connected?", exception)
        else:
            try:
                self.__fRMotor = Motor(self.__conf2port[self.__config['frontRightMotorPort']],
                Direction.CLOCKWISE if (not self.__config['frontRightMotorInverted']) else Direction.COUNTERCLOCKWISE,
                gears = self.__config['frontRightMotorGears']) if (self.__config['frontRightMotorPort'] != 0) else 0
                self.__bRMotor = Motor(self.__conf2port[self.__config['backRightMotorPort']],
                Direction.CLOCKWISE if (not self.__config['backRightMotorInverted']) else Direction.COUNTERCLOCKWISE,
                gears = self.__config['backRightMotorGears']) if (self.__config['backRightMotorPort'] != 0) else 0
                self.__fLMotor = Motor(self.__conf2port[self.__config['frontLeftMotorPort']],
                Direction.CLOCKWISE if (not self.__config['frontLeftMotorInverted']) else Direction.COUNTERCLOCKWISE,
                gears = self.__config['frontLeftMotorGears']) if (self.__config['frontLeftMotorPort'] != 0) else 0
                self.__bLMotor = Motor(self.__conf2port[self.__config['backLeftMotorPort']],
                Direction.CLOCKWISE if (not self.__config['backLeftMotorInverted']) else Direction.COUNTERCLOCKWISE,
                gears = self.__config['backLeftMotorGears']) if (self.__config['backLeftMotorPort'] != 0) else 0
            except Exception as exception:
                self.logger.error(
                    self, "Failed to initialize movement motors for robot type %s - Are u sure they\'re all connected? Errored at Port" % self.__config['robotType'], exception)
        self.logger.debug(self, "Motor initialisation done")
        self.logger.info(self, 'Charlie initialized')

    def showDetails(self):
        '''
        Processes sensor data in a separate thread and shows 
        '''
        threadLock = _thread.allocate_lock()
        def __screenPrintRoutine():
            while True:
                if self.__gyro.angle() > 360:
                    ang = self.__gyro.angle() - 360
                else:
                    ang = self.__gyro.angle()
                speedRight = self.__rMotor.speed() if self.__config['robotType'] == 'NORMAL' else self.__fRMotor.speed()
                speedRight = speedRight / 360   # from deg/s to revs/sec
                speedRight = speedRight * (self.__config['wheelDiameter'] * math.pi)    # from revs/sec to cm/sec
                speedLeft = self.__lMotor.speed() if self.__config['robotType'] == 'NORMAL' else self.__fLMotor.speed()
                speedLeft = speedLeft / 360   # from deg/s to revs/sec
                speedLeft = speedLeft * (self.__config['wheelDiameter'] * math.pi)    # from revs/sec to cm/sec
                
                #self.brick.screen.set_font(Font(family = 'arial', size = 16))
                if self.__screenRoutine:
                    print(self.__gyro.angle())
                    self.brick.screen.draw_text(5, 10, 'Robot-Angle: %s' % ang, text_color=Color.BLACK, background_color=Color.WHITE)
                    self.brick.screen.draw_text(5, 40, 'Right Motor Speed: %s' % ang, text_color=Color.BLACK, background_color=Color.WHITE)
                    self.brick.screen.draw_text(5, 70, 'Left Motor Speed: %s' % ang, text_color=Color.BLACK, background_color=Color.WHITE)
                time.sleep(0.1)


        with threadLock:
            _thread.start_new_thread(__screenPrintRoutine, ())

    def execute(self, params):
        '''
        This function interprets the number codes from the given array and executes the driving methods accordingly

        Args:
            params (array): The array of number code arrays to be executed
        '''

        if self.brick.battery.voltage() <= 7600:
            self.logger.warn("Please charge the battery. Only %sV left. We recommend least 7.6 Volts for accurate and repeatable results." %
                             self.brick.battery.voltage() * 0.001)
            return
        if self.__gyro == 0:
            self.logger.error(self, "Cannot drive without gyro", '')
            return

        methods = {
            3: self.absTurn,
            4: self.turn,
            5: self.action,
            7: self.straight,
            9: self.intervall,
            11: self.curve,
            12: self.toColor,
            15: self.toWall
        }

        self.__gyro.reset_angle(0)
        self.__gyro.reset_angle(0)
        time.sleep(0.1)
        self.__screenRoutine = True
        while params != [] and not any(self.brick.buttons.pressed()):
            pparams = params.pop(0)
            mode, arg1, arg2, arg3 = pparams.pop(0), pparams.pop(
                0), pparams.pop(0), pparams.pop(0)

            methods[mode](arg1, arg2, arg3)

        self.breakMotors()
        if self.__config['useGearing']:
            self.__gearingPortMotor.run_target(300, 0, Stop.HOLD, True)  # reset gearing

        time.sleep(0.3)
        self.__screenRoutine = False

    def turn(self, speed, deg, port):
        '''
        Used to turn the motor on the spot using either one or both Motors for turning (2 or 4 in case of ALLWHEEL and MECANUM)

        Args:
            speed (int): the speed to drive at
            deg (int): the angle to turn
            port (int): the motor(s) to turn with
        '''

        startValue = self.__gyro.angle()
        speed = self.min_speed if speed < self.min_speed else speed

        # turn only with left motor
        if port == 2:
            # right motor off
            self.__rMotor.dc(0)
            # turn the angle
            if deg > 0:     
                while self.__gyro.angle() - startValue < deg:
                    self.turnLeftMotor(speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed

                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return
            else:
                while self.__gyro.angle() - startValue > deg:
                    self.turnLeftMotor(-speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed
                        
                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

        # turn only with right motor
        elif port == 3:
            # left motor off
            self.__lMotor.dc(0)
            # turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    self.turnRightMotor(-speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed 

                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return
            else:
                while self.__gyro.angle() - startValue > deg:
                    self.turnRightMotor(speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed + 5
                    
                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

        # turn with both motors
        elif port == 23:
            dualMotorbonus = 19
            speed = speed * 2
            # turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    self.turnLeftMotor(speed / 2)
                    self.turnRightMotor(-speed / 2)
                    # slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.01) if speed - self._map(deg, 1, 360, 10, 0.01) > self.min_speed * 2 - dualMotorbonus else self.min_speed * 2 - dualMotorbonus

                    # cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

            else:
                while self.__gyro.angle() - startValue > deg:
                    self.turnLeftMotor(-speed / 2)
                    self.turnRightMotor(speed / 2)
                    # slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.01) if speed - self._map(deg, 1, 360, 10, 0.01) > self.min_speed * 2 - dualMotorbonus else self.min_speed * 2 - dualMotorbonus

                    # cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

    def absTurn(self, speed, deg, port):
        '''
        Used to turn the motor on the spot using either one or both Motors for turning (2 or 4 in case of ALLWHEEL and MECANUM)
        This method turns in contrast to the normal turn() method to an absolute ange (compared to starting point)

        Args:
            speed (int): the speed to drive at
            deg (int): the angle to turn to
            port (int): the motor(s) to turn with
        '''

        speed = self.min_speed if speed < self.min_speed else speed

        # turn only with left motor
        if port == 2:
            # right motor off
            self.__rMotor.dc(0)
            # turn the angle
            if deg > 0:     
                while self.__gyro.angle() < deg:
                    self.turnLeftMotor(speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() < deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed

                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return
            else:
                while self.__gyro.angle() > deg:
                    self.turnLeftMotor(-speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() > deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed
                        
                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

        # turn only with right motor
        elif port == 3:
            # left motor off
            self.__lMotor.dc(0)
            # turn the angle
            if deg > 0:
                while self.__gyro.angle() < deg:
                    self.turnRightMotor(-speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() < deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed 

                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return
            else:
                while self.__gyro.angle() > deg:
                    self.turnRightMotor(speed)
                    # slow down to not overshoot
                    if not self.__gyro.angle() > deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.1) if speed > self.min_speed else self.min_speed + 5
                    
                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

        # turn with both motors
        elif port == 23:
            dualMotorbonus = 19
            speed = speed * 2
            # turn the angle
            if deg > 0:
                while self.__gyro.angle() < deg:
                    self.turnLeftMotor(speed / 2)
                    self.turnRightMotor(-speed / 2)
                    # slow down to not overshoot
                    if not self.__gyro.angle() < deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.01) if speed - self._map(deg, 1, 360, 10, 0.01) > self.min_speed * 2 - dualMotorbonus else self.min_speed * 2 - dualMotorbonus

                    # cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

            else:
                while self.__gyro.angle() > deg:
                    self.turnLeftMotor(-speed / 2)
                    self.turnRightMotor(speed / 2)
                    # slow down to not overshoot
                    if not self.__gyro.angle() > deg * 0.6:
                        speed = speed - self._map(deg, 1, 360, 10, 0.01) if speed - self._map(deg, 1, 360, 10, 0.01) > self.min_speed * 2 - dualMotorbonus else self.min_speed * 2 - dualMotorbonus

                    # cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

    def straight(self, speed, dist, ang):
        '''
        Drives the Robot in a straight line.
        Also it self-corrects while driving with the help of a gyro-sensor. This is used to make the Robot more accurate

        Args:
            speed (int): the speed to drive at
            dist (int): the distance in cm to drive
        '''
        if self.__config['robotType'] != 'MECANUM':
            correctionStrength = 2.5  # how strongly the self will correct. 2 = default, 0 = nothing
            startValue = self.__gyro.angle()

            # convert the input (cm) to revs
            revs = dist / (self.__config['wheelDiameter'] * math.pi)

            motor = self.__rMotor if self.__config['robotType'] == 'NORMAL' else self.__fRMotor

            # drive
            motor.reset_angle(0)
            if revs > 0:
                while revs > (motor.angle() / 360):
                    # if not driving staright correct it
                    if self.__gyro.angle() - startValue > 0:
                        lSpeed = speed - abs(self.__gyro.angle() - startValue) * correctionStrength
                        rSpeed = speed
                    elif self.__gyro.angle() - startValue < 0:
                        rSpeed = speed - abs(self.__gyro.angle() - startValue) * correctionStrength
                        lSpeed = speed
                    else:
                        lSpeed = speed
                        rSpeed = speed

                    self.turnLeftMotor(lSpeed)
                    self.turnRightMotor(rSpeed)
                    
                    #cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return
            else:
                while revs < motor.angle() / 360:
                    # if not driving staright correct it
                    if self.__gyro.angle() - startValue < 0:
                        rSpeed = speed + abs(self.__gyro.angle() - startValue) * correctionStrength
                        lSpeed = speed
                    elif self.__gyro.angle() - startValue > 0:
                        lSpeed = speed + abs(self.__gyro.angle() - startValue) * correctionStrength
                        rSpeed = speed
                    else:
                        lSpeed = speed
                        rSpeed = speed

                    self.turnLeftMotor(-lSpeed)
                    self.turnRightMotor(-rSpeed)
                    # cancel if button pressed
                    if any(self.brick.buttons.pressed()):
                        return

        else:
            self.__fRMotor.reset_angle(0)
            # convert the input (cm) to revs
            revs = dist / (self.__config['wheelDiameter'] * math.pi)
            speed = speed * 1.7 * 6  # convert speed form % to deg/min

            # driving the robot into the desired direction
            if ang >= 0 and ang <= 45:
                multiplier = _map(ang, 0, 45, 1, 0)
                self.__fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
                self.__bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
            elif ang >= -45 and ang < 0:
                multiplier = _map(ang, -45, 0, 0, 1)
                self.__fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
                self.__bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
            elif ang > 45 and ang <= 90:
                multiplier = _map(ang, 45, 90, 0, 1)
                self.__fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
                self.__bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
            elif ang < -45 and ang >= -90:
                multiplier = _map(ang, -45, -90, 0, 1)
                self.__fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
                self.__bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
            elif ang > 90 and ang <= 135:
                multiplier = _map(ang, 90, 135, 1, 0)
                self.__fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
                self.__bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
            elif ang < -90 and ang >= -135:
                multiplier = _map(ang, -90, -135, 1, 0)
                self.__fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
                self.__bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
                self.__bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
            elif ang > 135 and ang <= 180:
                multiplier = _map(ang, 135, 180, 0, 1)
                self.__fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
                self.__bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
            elif ang < -135 and ang >= -180:
                multiplier = _map(ang, -135, -180, 0, 1)
                self.__fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
                self.__bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
                self.__bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)

    def intervall(self, speed, dist, count):
        '''
        Drives forwads and backwards x times.

        Args:
            speed (int): the speed to drive at
            revs (int): the distance (in cm) to drive
            count (int): how many times it should repeat the driving
        '''
        # convert the input (cm) to revs
        revs = dist / (self.__config['wheelDiameter'] * math.pi) / 2

        speed = speed * 1.7 * 6  # speed in deg/s to %
        # move count times forwards and backwards
        for i in range(count + 1):
            if self.__config['robotType'] == 'NORMAL':
                ang = self.__lMotor.angle()
                # drive backwards
                self.__rMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                self.__lMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__lMotor.angle() > revs * -360:
                    if any(self.brick.buttons.pressed()):
                        return
                # drive forwards
                self.__lMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__rMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__rMotor.angle() <= ang:
                    if any(self.brick.buttons.pressed()):
                        return

            elif self.__config['robotType'] == 'ALLWHEEL' or self.__config['robotType'] == 'MECANUM':
                ang = self.__lMotor.angle()
                # drive backwards
                self.__fRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                self.__bRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                self.__fLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                self.__bLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__lMotor.angle() > revs * -360:
                    if any(self.brick.buttons.pressed()):
                        return
                # drive forwards
                self.__fRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__bRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__fLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__bLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__rMotor.angle() <= ang:
                    if any(self.brick.buttons.pressed()):
                        return

    def curve(self, speed, dist, deg):
        '''
        Drives forwads and backwards x times.

        Args:
            speed (int): the speed to drive at
            revs1 (int): the distance (in motor revolutions) for the outer wheel to drive
            deg (int): how much of a circle it should drive
        '''
        speed = speed * 1.7 * 6  # speed to deg/s from %

        # gyro starting point
        startValue = self.__gyro.angle()

        revs1 = dist / (self.__config['wheelDiameter'] * math.pi)


        # claculate revs for the second wheel
        pathOutside = self.__config['wheelDiameter'] * math.pi * revs1
        rad1 = pathOutside / (math.pi * (deg / 180))
        rad2 = rad1 - self.__config['wheelDistance']
        pathInside = rad2 * math.pi * (deg/180)
        revs2 = pathInside / (self.__config['wheelDiameter'] * math.pi)

        # claculate the speed for the second wheel
        relation = revs1 / revs2
        speedSlow = speed / relation

        if deg > 0:
            # asign higher speed to outer wheel
            lSpeed = speed
            rSpeed = speedSlow
            self.__rMotor.run_angle(rSpeed, revs2 * 360, Stop.COAST, False)
            self.__lMotor.run_angle(lSpeed, revs1 * 360 + 5, Stop.COAST, False)
            #turn
            while self.__gyro.angle() - startValue < deg and not any(self.brick.buttons.pressed()):
                pass

        else:
            # asign higher speed to outer wheel
            lSpeed = speed
            rSpeed = speedSlow
            self.__rMotor.run_angle(rSpeed, revs2 * 360 + 15, Stop.COAST, False)
            self.__lMotor.run_angle(lSpeed, revs1 * 360, Stop.COAST, False)
            #turn
            while self.__gyro.angle() - startValue > deg and not any(self.brick.buttons.pressed()):
                pass

    def toColor(self, speed, color, side):
        '''
        Drives forward until the given colorSensor sees a given color.

        Args:
            speed (int): the speed to drive at
            color (int): the color to look for (0 = Black, 1 = White)
            side (int): which side's color sensor should be used
        '''
        # sets color to a value that the colorSensor can work with
        if color == 0:
            color = Color.BLACK
        else:
            color = Color.WHITE

        # Refactor code

        # only drive till left colorSensor
        if side == 2:
            # if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while lLight.color() != Color.WHITE and not any(self.brick.buttons.pressed()):
                    self.turnBothMotors(speed)

            while lLight.color() != color and not any(self.brick.buttons.pressed()):
                self.turnBothMotors(speed)

        # only drive till right colorSensor
        elif side == 3:
            # if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while rLight.color() != Color.WHITE and not any(self.brick.buttons.pressed()):
                    self.turnBothMotors(speed)

            while rLight.color() != color and not any(self.brick.buttons.pressed()):
                self.turnBothMotors(speed)

        # drive untill both colorSensors
        elif side == 23:
            rSpeed = speed
            lSpeed = speed
            rWhite = False
            lWhite = False 
            while (rLight.color() != color or lLight.color() != color) and not any(self.brick.buttons.pressed()):
                #if drive to color black drive until back after white to not recognize colors on the field as lines
                if color == Color.BLACK:
                    if rLight.color() == Color.WHITE:
                        rWhite = True
                    if lLight.color() == Color.WHITE:
                        lWhite = True

                self.__rMotor.dc(rSpeed)
                self.__lMotor.dc(lSpeed)
                # if right at color stop right Motor
                if rLight.color() == color and rWhite:
                    rSpeed = 0
                # if left at color stop left Motor
                if lLight.color() == color and lWhite:
                    lSpeed = 0

    def toWall(self, speed, *args):
        '''
        Drives until a pressure sensor is pressed

        Args:
            speed (int): the speed to drive at
        '''
        while not touch.pressed():
            self.turnBothMotors(- abs(speed))

            if any(self.brick.buttons()):
                break

        self.turnBothMotors(0)

    def action(self, speed, revs, port):
        '''
        Doesn't drive the robot, but drives the action motors

        Args:
            speed (int): the speed to turn the motor at
            revs (int): how long to turn the motor for
            port (int): which one of the motors should be used
        '''
        speed = abs(speed) * 1.7 * 6  # speed to deg/s from %
        if self.__config['useGearing']:
            self.__gearingPortMotor.run_target(300, port * 90, Stop.HOLD, True)  # select gearing Port
            ang = self.__gearingTurnMotor.angle()
            self.__gearingTurnMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)  # start turning the port
            # cancel, if any brick button is pressed
            if revs > 0:
                while self.__gearingTurnMotor.angle() < revs * 360 - ang:
                    if any(self.brick.buttons.pressed()):
                        self.__gearingTurnMotor.dc(0)
                        return
            else:
                while self.__gearingTurnMotor.angle() > revs * 360 + ang:
                    if any(self.brick.buttons.pressed()):
                        self.__gearingTurnMotor.dc(0)
                        return
        else:
            # turn motor 1
            if port == 1:
                ang = self.__aMotor1.angle()
                self.__aMotor1.run_angle(speed, revs * 360, Stop.HOLD, False)
                if revs > 0:
                    while self.__aMotor1.angle() < revs * 360 - ang:
                        if any(self.brick.buttons.pressed()):
                            self.__aMotor1.dc(0)
                            return
                else:
                    while self.__aMotor1.angle() > revs * 360 + ang:
                        if any(self.brick.buttons.pressed()):
                            self.__aMotor1.dc(0)
                            return
            # turm motor 2
            elif port == 2:
                ang = self.__aMotor2.angle()
                self.__aMotor2.run_angle(speed, revs * 360, Stop.HOLD, False)
                if revs > 0:
                    while self.__aMotor2.angle() < revs * 360 - ang:
                        if any(self.brick.buttons.pressed()):
                            self.__aMotor2.dc(0)
                            return
                else:
                    while self.__aMotor2.angle() > revs * 360 + ang:
                        if any(self.brick.buttons.pressed()):
                            self.__aMotor2.dc(0)
                            return

    def turnLeftMotor(self, speed):
        '''
        Sub-method for driving the left Motor(s)

        Args:
            speed (int): the speed to drive the motor at
        '''

        if self.__config['robotType'] == 'NORMAL':
            self.__lMotor.dc(speed)
        else:
            self.__fLMotor.dc(speed)
            self.__bLMotor.dc(speed)

    def turnRightMotor(self, speed):
        '''
        Sub-method for driving the right Motor(s)

        Args:
            speed (int): the speed to drive the motor at
        '''

        if self.__config['robotType'] == 'NORMAL':
            self.__rMotor.dc(speed)
        else:
            self.__fRMotor.dc(speed)
            self.__bRMotor.dc(speed)

    def turnBothMotors(self, speed):
        '''
        Submethod for setting a motor.dc() to all motors
        
        Args:
            speed (int): the speed (in percent) to set the motors to
        '''
        if self.__config['robotType'] == 'NORMAL':
            self.__rMotor.dc(speed)
            self.__lMotor.dc(speed)
        else:
            self.__fRMotor.dc(speed)
            self.__bRMotor.dc(speed)
            self.__fLMotor.dc(speed)
            self.__bLMotor.dc(speed)

    def breakMotors(self):
        '''Sub-method for breaking all the motors'''
        if self.__config['robotType'] == 'NORMAL':
            self.__lMotor.hold()
            self.__rMotor.hold()
        else:
            self.__fRMotor.hold()
            self.__bRMotor.hold()
            self.__fLMotor.hold()
            self.__bLMotor.hold()
        time.sleep(0.2)

    def _map(self, x, in_min, in_max, out_min, out_max):
        '''
        Converts a given number in the range of two numbers to a number in the range of two other numbers

        Args:
            x (int): the input number that should be converted
            in_min (int): The minimal point of the range of input number
            in_max (int): The maximal point of the range of input number
            out_min (int): The minimal point of the range of output number
            out_max (int): The maximal point of the range of output number

        Returns:
        int: a number between out_min and out_max, de
        '''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def getGyroAngle(self):
        return self.__gyro.angle()

    def setRemoteValues(self, data):
        x = data['x']
        y = data['y']
        if x == 0:
            x = 0.0001
        if data['y'] == 0 and data['x'] == 0:
            self.breakMotors()
        else:
            radius = int(math.sqrt(x**2 + y**2)) # distance from center
            ang = math.atan(y / x) # angle in radians

            a = int(self._map(radius, 0, 180, 0, 100))
            b = int(-1 * math.cos(2 * ang) * self._map(radius, 0, 180, 0, 100))

            if x < 0:
                temp = a
                a = b
                b = temp

            if y < 0:
                temp = a
                a = -b
                b = -temp

            self.turnLeftMotor(int(self._map(a, 0, 100, 0, data['maxSpeed'])))
            self.turnRightMotor(int(self._map(b, 0, 100, 0, data['maxSpeed'])))

        if data['a1'] == 0:
            self.__aMotor1.hold()
        else:
            a1Speed = data['a1']
            self.__aMotor1.dc(a1Speed)

