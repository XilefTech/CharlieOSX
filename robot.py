import config
from logging import Logger
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
    #TODO
    def __repr__(self):
        return "TODO"
    #TODO
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
        while params != [] and not any(self.brick.buttons()):
            mode, arg1, arg2, arg3 = params.pop(0), params.pop(0), params.pop(0), params.pop(0)

            methods = { 4: turn(),
                        5: gearing(), if config.useGearing else actionMotors(),
                        7: straight(), if config.robotType != 'MECANUM' else straightMecanum(),
                        9: intervall(),
                        11: curve(),
                        12: toColor(),
                        15: toWall()}
            
            methods[mode](arg1, arg2, arg3)
            
        breakMotors()
        if config.useGearing:
            gearingPortMotor.run_target(300, 0, Stop.HOLD, True)    #reset gearing

        time.sleep(0.3)

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
                    if any(self.brick.buttons()):
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
                    if any(self.brick.buttons()):
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
                    if any(self.brick.buttons()):
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
                    if any(self.brick.buttons()):
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
                    if any(self.brick.buttons()):
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
                    if any(self.brick.buttons()):
                        return

    def straight(self, speed, dist, *args):
        """drives forward with speed in a straight line, corrected by the self.__gyro. Only working for NORMAL and ALLWHEEL Type"""
        correctionStrength = 2 # how strongly the self will correct. 2 = default, 0 = nothing
        startValue = self.__gyro.angle()
        
        revs = dist / (config.wheelDiameter * math.pi) # convert the input (cm) to revs
        revs = revs / 2

        #drive
        if config.robotType == 'NORMAL':
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

        elif config.robotType == 'ALLWHEEL':
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

    def straightMecanum(self, speed, dist, ang):
        """Driving a straight line of dist cm with speed in ang direction. Only working with MECANUM Type"""
        self.__fRMotor.reset_angle(0)
        revs = dist / (config.wheelDiameter * math.pi) # convert the input (cm) to revs
        speed = speed * 1.7 * 6 # convert speed form % to deg/min

        # driving the robot into the desired direction
        if ang >= 0 and ang <= 45:
            multiplier = tools.map(ang, 0, 45, 1, 0)
            self.__fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            self.__bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang >= -45 and ang < 0:
            multiplier = tools.map(ang, -45, 0, 0, 1)
            self.__fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            self.__bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang > 45 and ang <= 90:
            multiplier = tools.map(ang, 45, 90, 0, 1)
            self.__fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            self.__bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            self.__bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang < -45 and ang >= -90:
            multiplier = tools.map(ang, -45, -90, 0, 1)
            self.__fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            self.__bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            self.__bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang > 90 and ang <= 135:
            multiplier = tools.map(ang, 90, 135, 1, 0)
            self.__fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            self.__bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang < -90 and ang >= -135:
            multiplier = tools.map(ang, -90, -135, 1, 0)
            self.__fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            self.__bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            self.__bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang > 135 and ang <= 180:
            multiplier = tools.map(ang, 135, 180, 0, 1)
            self.__fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            self.__bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            self.__bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            self.__fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang < -135 and ang >= -180:
            multiplier = tools.map(ang, -135, -180, 0, 1)
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
            if config.robotType == 'NORMAL':
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
            
            elif config.robotType == 'ALLWHEEL' or config.robotType == 'MECANUM':
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
        pathOutside = config.wheelDiameter * 2 * math.pi * revs1
        rad1 = pathOutside / (math.pi * (deg / 180))
        rad2 = rad1 - config.wheelDistance
        pathInside = rad2 * math.pi * (deg/180)
        revs2 = pathInside / (config.wheelDiameter * 2 * math.pi)

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
            if config.robotType == 'NORMAL':
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

    def gearing(self, speed, revs, port):
        """rotates the port for revs revulutions with a speed of speed"""
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

    def actionMotors(self, speed, revs, port):
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



