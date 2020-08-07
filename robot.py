from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Direction)

class Charlie():
    '''This is the main class of the robot. It contains all the functions CharlieOSX has to offer'''
    def __init__(self, config, settings, brick, logger):
        logger.info(self, 'Starting initialisation of Charlie')
        self.__config = config
        self.__settings = settings

        self.brick = brick
        self.logger = logger

        self.__conf2port = {1: Port.S1, 2: Port.S2, 3: Port.S3, 4: Port.S4}

        self.logger.debug(self, "Starting sensor initialisation...")
        try:
            self.__gyro = GyroSensor(self.__conf2port[self.__config['gyroSensorPort']]) if self.__config['gyroSensorPort'] != 0 else 0
            self.logger.debug(self, 'Gyrosensor initialized sucessfully on port %s' % self.__config['gyroSensorPort'])
        except Exception as exception:
            self.__gyro = 0
            self.logger.error(self, "Failed to initialize the Gyro-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        try:
            self.__rLight = ColorSensor(self.__conf2port[self.__config['rightLightSensorPort']]) if self.__config['rightLightSensorPort'] != 0 else 0
            self.logger.debug(self, 'Colorsensor initialized sucessfully on port %s' % self.__config['rightLightSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the right Color-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        try:
            self.__lLight = ColorSensor(self.__conf2port[self.__config['leftLightSensorPort']]) if self.__config['leftLightSensorPort'] != 0 else 0  
            self.logger.debug(self, 'Colorsensor initialized sucessfully on port %s' % self.__config['leftLightSensorPort'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the left Color-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        try:
            self.__touch = TouchSensor(self.__conf2port[self.__config['backTouchSensor']]) if self.__config['backTouchSensor'] != 0 else 0
            self.logger.debug(self, 'Touchsensor initialized sucessfully on port %s' % self.__config['backTouchSensor'])
        except Exception as exception:
            self.logger.error(self, "Failed to initialize the Touch-Sensor - Are u sure it's connected to Port %s?" % exception, exception)
        self.logger.debug(self, "Sensor initialisation done")
        self.logger.debug(self, "Starting motor initialisation...")
        if self.__config['robotType'] == 'NORMAL':
            try:
                self.__lMotor = Motor(self.__conf2port[self.__config['leftMotorPort']], Direction.CLOCKWISE if (not self.__config['leftMotorInverted']) else Direction.COUNTERCLOCKWISE)
                self.__rMotor = Motor(self.__conf2port[self.__config['rightMotorPort']], Direction.CLOCKWISE if (not self.__config['rightMotorInverted']) else Direction.COUNTERCLOCKWISE)
            except Exception as exception:
                self.logger.error(self, "Failed to initialize movement motors for robot type NORMAL - Are u sure they\'re all connected?", exception)
            if self.__config['useGearing']:
                try:
                    self.__gearingPortMotor = Motor(self.__conf2port[self.__config['gearingSelectMotorPort']], Direction.CLOCKWISE if (not self.__config['gearingSelectMotorPortInverted']) else Direction.COUNTERCLOCKWISE)
                    self.__gearingTurnMotor = Motor(self.__conf2port[self.__config['gearingTurnMotorPort']], Direction.CLOCKWISE if (not self.__config['gearingTurnMotorPortInverted']) else Direction.COUNTERCLOCKWISE)
                except Exception as exception:
                    self.logger.error(self, "Failed to initialize action motors for the gearing - Are u sure they\'re all connected?", exception)
            else:
                try:
                    self.__aMotor1 = Motor(self.__conf2port[self.__config['firstActionMotorPort']], Direction.CLOCKWISE if (not self.__config['firstActionMotorInverted']) else Direction.COUNTERCLOCKWISE) if (self.__config['firstActionMotorPort'] != 0) else 0
                    self.__aMotor2 = Motor(self.__conf2port[self.__config['secondActionMotorPort']], Direction.CLOCKWISE if (not self.__config['secondActionMotorInverted']) else Direction.COUNTERCLOCKWISE) if (self.__config['secondActionMotorPort'] != 0) else 0
                except Exception as exception:
                    self.logger.error(self, "Failed to initialize action motors - Are u sure they\'re all connected?", exception)
        else:
            try:
                self.__fRMotor = Motor(self.__conf2port[self.__config['frontRightMotorPort']], Direction.CLOCKWISE if (not self.__config['frontRightMotorInverted']) else Direction.COUNTERCLOCKWISE) if (self.__config['frontRightMotorPort'] != 0) else 0
                self.__bRMotor = Motor(self.__conf2port[self.__config['backRightMotorPort']], Direction.CLOCKWISE if (not self.__config['backRightMotorInverted']) else Direction.COUNTERCLOCKWISE) if (self.__config['backRightMotorPort'] != 0) else 0
                self.__fLMotor = Motor(self.__conf2port[self.__config['frontLeftMotorPort']], Direction.CLOCKWISE if (not self.__config['frontLeftMotorInverted']) else Direction.COUNTERCLOCKWISE) if (self.__config['frontLeftMotorPort'] != 0) else 0
                self.__bLMotor = Motor(self.__conf2port[self.__config['backLeftMotorPort']], Direction.CLOCKWISE if (not self.__config['backLeftMotorInverted']) else Direction.COUNTERCLOCKWISE) if (self.__config['backLeftMotorPort'] != 0) else 0
            except Exception as exception:
                self.logger.error(self, "Failed to initialize movement motors for robot type %s - Are u sure they\'re all connected? Errored at Port" % config['robotType'], exception)
        self.logger.debug(self, "Motor initialisation done")
        self.logger.info(self, 'Charlie initialized')
    #TODO
    def __repr__(self):
        return "TODO"
    #TODO
    def __str__(self):
        return "Charlie"   

    def execute(self, params):
        '''Starts the different Driving modules according to the given parameters'''

        if self.__brick.battery.voltage()() <= 7500:
            self.logger.warn("Please charge the battery. Only %sV left. We recommend least 7.5 Volts for accurate and repeatable results." % self.brick.battery.voltage() * 0.001)
            return
        if self.__gyro == 0:
            self.logger.error(self, "Cannot drive without gyro", '')
            return

        __gyro.reset_angle(0)
        while params != [] and not any(self.brick.buttons()):
            pparams = params.pop(0)
            mode, arg1, arg2, arg3 = pparams.pop(0), pparams.pop(0), pparams.pop(0), pparams.pop(0)

            methods = { 4: turn(),
                        5: action(),
                        7: straight(),
                        9: intervall(),
                        11: curve(),
                        12: toColor(),
                        15: toWall()}
            
            methods[mode](arg1, arg2, arg3)
            
        breakMotors()
        if self.__config['useGearing']:
            gearingPortMotor.run_target(300, 0, Stop.HOLD, True)    #reset gearing

        time.sleep(0.3)

    def breakMotors(self):
        if self.__config['robotType'] == 'NORMAL':
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
                    if self.__config['robotType'] == 'NORMAL':
                        __lMotor.dc(speed)
                    else:
                        __fLMotor.dc(speed)
                        __bLMotor.dc(speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - _map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(self.brick.buttons()):
                        return
            else:
                while self.__gyro.angle() - startValue > deg:
                    if self.__config['robotType'] == 'NORMAL':
                        __lMotor.dc(-speed)
                    else:
                        __fLMotor.dc(-speed)
                        __bLMotor.dc(-speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - _map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(self.brick.buttons()):
                        return

        #turn only with right motor
        elif port == 3:
            #left motor off
            __lMotor.dc(0)
            #turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    if self.__config['robotType'] == 'NORMAL':
                        __rMotor.dc(-speed)
                    else:
                        __fRMotor.dc(-speed)
                        __bRMotor.dc(-speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - _map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(self.brick.buttons()):
                        return                 
            else:
                while self.__gyro.angle() - startValue > deg:
                    if self.__config['robotType'] == 'NORMAL':
                        __rMotor.dc(speed)
                    else:
                        __fRMotor.dc(speed)
                        __bRMotor.dc(speed)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - _map(deg, 1, 360, 10, 0.1) if speed > 20 else speed
                    
                    #cancel if button pressed
                    if any(self.brick.buttons()):
                        return

        #turn with both motors
        elif port == 23:
            #turn the angle
            if deg > 0:
                while self.__gyro.angle() - startValue < deg:
                    if self.__config['robotType'] == 'NORMAL':
                        __rMotor.dc(-speed / 2)
                        __lMotor.dc(speed / 2)
                    else:
                        __fRMotor.dc(-speed / 2)
                        __bRMotor.dc(-speed / 2)
                        __fLMotor.dc(speed / 2)
                        __bLMotor.dc(speed / 2)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue < deg * 0.6:
                        speed = speed - _map(deg, 1, 360, 10, 0.01) if speed > 40 else speed

                    #cancel if button pressed
                    if any(self.brick.buttons()):
                        return    
                    
            else:
                while self.__gyro.angle() - startValue > deg:
                    if self.__config['robotType'] == 'NORMAL':
                        __rMotor.dc(speed / 2)
                        __lMotor.dc(-speed / 2)
                    else:
                        __fRMotor.dc(speed / 2)
                        __bRMotor.dc(speed / 2)
                        __fLMotor.dc(-speed / 2)
                        __bLMotor.dc(-speed / 2)
                    #slow down to not overshoot
                    if not self.__gyro.angle() - startValue > deg * 0.6:
                        speed = speed - _map(deg, 1, 360, 10, 0.01) if speed > 40 else speed
                    
                    #cancel if button pressed
                    if any(self.brick.buttons()):
                        return

    def straight(self, speed, dist, *args):
        """drives forward with speed in a straight line, corrected by the self.__gyro when in normal or allwheel mode"""
        if self.__config['robotType'] != 'MECANUM':
            correctionStrength = 2 # how strongly the self will correct. 2 = default, 0 = nothing
            startValue = self.__gyro.angle()
            
            revs = dist / (self.__config['wheelDiameter'] * math.pi) # convert the input (cm) to revs
            revs = revs / 2

            #drive
            if self.__config['robotType'] == 'NORMAL':
                self.__rMotor.reset_angle(0)
                if revs > 0:
                    while revs > self.__rMotor.angle() / 360:
                        #if not driving staright correct it
                        if self.__gyro.angle() - startValue > 0:
                            lSpeed = speed - abs(self.__gyro.angle() - startValue) * correctionStrength
                            rSpeed = speed
                        elif self.__gyro.angle() - startValue < 0:
                            rSpeed = speed - abs(self.__gyro.angle() - startValue) * correctionStrength
                            lSpeed = speed
                        else:
                            lSpeed = speed
                            rSpeed = speed

                        self.__rMotor.dc(rSpeed)
                        self.__lMotor.dc(lSpeed)
                        #cancel if button pressed
                        if any(self.brick.buttons()):
                                return
                else:
                    while revs < __rMotor.angle() / 360:
                        #if not driving staright correct it
                        if self.__gyro.angle() - startValue < 0:
                            rSpeed = speed + abs(self.__gyro.angle() - startValue) * correctionStrength
                            lSpeed = speed
                        elif self.__gyro.angle() - startValue > 0:
                            lSpeed = speed + abs(self.__gyro.angle() - startValue) * correctionStrength
                            rSpeed = speed
                        else:
                            lSpeed = speed
                            rSpeed = speed

                        self.__rMotor.dc(-rSpeed)
                        self.__lMotor.dc(-lSpeed)
                        #cancel if button pressed
                        if any(self.brick.buttons()):
                                return

            elif self.__config['robotType'] == 'ALLWHEEL':
                self.__fRMotor.reset_angle(0)
                if revs > 0:
                    while revs > self.__fRMotor.angle() / 360:
                        #if not driving staright correct it
                        if self.__gyro.angle() - startValue > 0:
                            lSpeed = speed - abs(self.__gyro.angle() - startValue) * correctionStrength
                            rSpeed = speed
                        elif self.__gyro.angle() - startValue < 0:
                            rSpeed = speed - abs(self.__gyro.angle() - startValue) * correctionStrength
                            lSpeed = speed
                        else:
                            lSpeed = speed
                            rSpeed = speed

                        self.__fRMotor.dc(rSpeed)
                        self.__bRMotor.dc(rSpeed)
                        self.__fLMotor.dc(lSpeed)
                        self.__bLMotor.dc(lSpeed)
                        #cancel if button pressed
                        if any(self.brick.buttons()):
                                return
                else:
                    while revs < self.__fRMotor.angle() / 360:
                        #if not driving staright correct it
                        if self.__gyro.angle() - startValue < 0:
                            rSpeed = speed + abs(self.__gyro.angle() - startValue) * correctionStrength
                            lSpeed = speed
                        elif self.__gyro.angle() - startValue > 0:
                            lSpeed = speed + abs(self.__gyro.angle() - startValue) * correctionStrength
                            rSpeed = speed
                        else:
                            lSpeed = speed
                            rSpeed = speed

                        self.__fRMotor.dc(rSpeed)
                        self.__bRMotor.dc(rSpeed)
                        self.__fLMotor.dc(lSpeed)
                        self.__bLMotor.dc(lSpeed)
                        #cancel if button pressed
                        if any(self.brick.buttons()):
                                return
        else:
            self.__fRMotor.reset_angle(0)
            revs = dist / (self.__config['wheelDiameter'] * math.pi) # convert the input (cm) to revs
            speed = speed * 1.7 * 6 # convert speed form % to deg/min

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

    def intervall(self, speed, revs, count):
        """drives revs forward and backward with speed count times"""
        i = 0
        speed = speed * 1.7 * 6 # speed in deg/s to %
        # move count times forwards and backwards
        while i < count:
            if self.__config['robotType'] == 'NORMAL':
                ang = self.__lMotor.angle()
                # drive backwards
                self.__rMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                self.__lMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__lMotor.angle() > revs * -360:
                    if any(self.brick.buttons()):
                        return
                #drive forwards
                self.__lMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__rMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__rMotor.angle() <= ang:
                    if any(self.brick.buttons()):
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
                    if any(self.brick.buttons()):
                        return
                #drive forwards
                self.__fRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__bRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__fLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                self.__bLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while self.__rMotor.angle() <= ang:
                    if any(self.brick.buttons()):
                        return
            i += 1

    def curve(self, speed, revs1, deg):
        """Drives in a curve deg over revs with speed"""
        speed = speed * 1.7 * 6 #speed to deg/s from %

        #gyro starting point
        startValue = self.__gyro.angle()
        
        #claculate revs for the second wheel
        pathOutside = self.__config['wheelDiameter'] * 2 * math.pi * revs1
        rad1 = pathOutside / (math.pi * (deg / 180))
        rad2 = rad1 - self.__config['wheelDistance']
        pathInside = rad2 * math.pi * (deg/180)
        revs2 = pathInside / (self.__config['wheelDiameter'] * 2 * math.pi)

        #claculate the speed for the second wheel
        relation = revs1 / revs2
        speedSlow = speed / relation

        if deg > 0:
            #asign higher speed to outer wheel
            lSpeed = speed
            rSpeed = speedSlow
            self.__rMotor.run_angle(rSpeed, revs2 * 360, Stop.COAST, False)
            self.__lMotor.run_angle(lSpeed, revs1 * 360 + 5, Stop.COAST, False)
            #turn
            while self.__gyro.angle() - startValue < deg and not any(self.brick.buttons()):
                pass

        else:
            #asign higher speed to outer wheel
            rSpeed = speed
            lSpeed = speedSlow
            self.__rMotor.run_angle(rSpeed, revs1 * 360 + 5, Stop.COAST, False)
            self.__lMotor.run_angle(lSpeed, revs2 * 360, Stop.COAST, False)
            #turn
            while self.__gyro.angle() + startValue > deg and not any(self.brick.buttons()):
                pass

    def toColor(self, speed, color, side):
        """Drives until the self drives to a color line with speed"""
        # sets color to a value that the colorSensor can work with
        if color == 0:
            color = Color.BLACK
        else:
            color = Color.WHITE

        #only drive till left colorSensor 
        if side == 2:
            #if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while lLight.color() != Color.WHITE and not any(self.brick.buttons()):
                    if robotType == 'NORMAL':
                        self.__rMotor.dc(speed)
                        self.__lMotor.dc(speed)
                    else: 
                        self.__fRMotor.dc(speed)
                        self.__bRMotor.dc(speed)
                        self.__fLMotor.dc(speed)
                        self.__bLMotor.dc(speed)

            while lLight.color() != color and not any(self.brick.buttons()):
                if robotType == 'NORMAL':
                    self.__rMotor.dc(speed)
                    self.__lMotor.dc(speed)
                else: 
                    self.__fRMotor.dc(speed)
                    self.__bRMotor.dc(speed)
                    self.__fLMotor.dc(speed)
                    self.__bLMotor.dc(speed)
            
        #only drive till right colorSensor 
        elif side == 3:
            #if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while rLight.color() != Color.WHITE and not any(self.brick.buttons()):
                    if robotType == 'NORMAL':
                        self.__rMotor.dc(speed)
                        self.__lMotor.dc(speed)
                    else: 
                        self.__fRMotor.dc(speed)
                        self.__bRMotor.dc(speed)
                        self.__fLMotor.dc(speed)
                        self.__bLMotor.dc(speed)

            while rLight.color() != color and not any(self.brick.buttons()):
                if robotType == 'NORMAL':
                    self.__rMotor.dc(speed)
                    self.__lMotor.dc(speed)
                else: 
                    self.__fRMotor.dc(speed)
                    self.__bRMotor.dc(speed)
                    self.__fLMotor.dc(speed)
                    self.__bLMotor.dc(speed)
            
        #drive untill both colorSensors
        elif side == 23:
            rSpeed = speed
            lSpeed = speed
            rWhite = False
            lWhite = False
            
            while (rLight.color() != color or lLight.color() != color) and not any(self.brick.buttons()):
                #if drive to color black drive until back after white to not recognize colors on the field as lines
                if color == Color.BLACK:
                    if rLight.color() == Color.WHITE:
                        rWhite = True
                    if lLight.color() == Color.WHITE:
                        lWhite = True

                self.__rMotor.dc(rSpeed)
                self.__lMotor.dc(lSpeed)
                #if right at color stop right Motor
                if rLight.color() == color and rWhite:
                    rSpeed = 0
                #if left at color stop left Motor
                if lLight.color() == color and lWhite:
                    lSpeed = 0

    def toWall(self, speed, *args):
        """drives backwards with speed until it reaches a wall"""
        while not touch.pressed():
            if self.__config['robotType'] == 'NORMAL':
                self.__rMotor.dc(- abs(speed))
                self.__lMotor.dc(- abs(speed))
            else:
                self.__fRMotor.dc(- abs(speed))
                self.__bRMotor.dc(- abs(speed))
                self.__fLMotor.dc(- abs(speed))
                self.__bLMotor.dc(- abs(speed))

            if any(self.brick.buttons()):
                break
        
        self.__lMotor.dc(0)
        self.__rMotor.dc(0)

    def action(self, speed, revs, port):
        """rotates the port for revs revulutions with a speed of speed"""
        if self.__config['useGearing']:
            speed = speed * 1.7 * 6 #speed to deg/s from %
            self.__gearingPortMotor.run_target(300, port * 90, Stop.HOLD, True) #select gearing Port
            ang = self.__gearingTurnMotor.angle()
            self.__gearingTurnMotor.run_angle(speed, revs * 360, Stop.BRAKE, False) #start turning the port
            #cancel, if any brick button is pressed
            if revs > 0:
                while self.__gearingTurnMotor.angle() < revs * 360 - ang:
                    if any(self.brick.buttons()):
                        self.__gearingTurnMotor.dc(0)
                        return
            else:
                while self.__gearingTurnMotor.angle() > revs * 360 + ang:
                    if any(self.brick.buttons()):
                        self.__gearingTurnMotor.dc(0)
                        return
        else:
            # turn motor 1
            if port == 1:
                self.__aMotor1.run_angle(speed, revs * 360, Stop.BRAKE, False)
                if revs > 0:
                    while self.__aMotor1.angle() < revs * 360 - ang:
                        if any(self.brick.buttons()):
                            self.__aMotor1.dc(0)
                            return
                else:
                    while self.__aMotor1.angle() > revs * 360 + ang:
                        if any(self.brick.buttons()):
                            self.__aMotor1.dc(0)
                            return
            # turm motor 2
            elif port == 2:
                self.__aMotor2.run_angle(speed, revs * 360, Stop.BRAKE, False)
                if revs > 0:
                    while self.__aMotor2.angle() < revs * 360 - ang:
                        if any(self.brick.buttons()):
                            self.__aMotor2.dc(0)
                            return
                else:
                    while self.__aMotor2.angle() > revs * 360 + ang:
                        if any(self.brick.buttons()):
                            self.__aMotor2.dc(0)
                            return

    def _map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    
