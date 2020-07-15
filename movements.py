import self, OSTools
from robotError import *

# TODO?: gearing homing?

if self.__gyro != 0:
    self.__gyro.reset_angle(0)
    
    
            

    def straightMecanum(speed, dist, ang, *args):
        """Driving a straight line of dist cm with speed in ang direction. Only working with MECANUM Type"""
        __fRMotor.reset_angle(0)

        revs = dist / (config.wheelDiameter * math.pi) # convert the input (cm) to revs
        speed = speed * 1.7 * 6 # convert speed form % to deg/min

        # driving the self into the desired direction
        if ang >= 0 and ang <= 45:
            multiplier = tools.map(ang, 0, 45, 1, 0)
            __fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            __bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang >= -45 and ang < 0:
            multiplier = tools.map(ang, -45, 0, 0, 1)
            __fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            __bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang > 45 and ang <= 90:
            multiplier = tools.map(ang, 45, 90, 0, 1)
            __fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            __bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang < -45 and ang >= -90:
            multiplier = tools.map(ang, -45, -90, 0, 1)
            __fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            __bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang > 90 and ang <= 135:
            multiplier = tools.map(ang, 90, 135, 1, 0)
            __fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            __bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang < -90 and ang >= -135:
            multiplier = tools.map(ang, -90, -135, 1, 0)
            __fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            __bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            __bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang > 135 and ang <= 180:
            multiplier = tools.map(ang, 135, 180, 0, 1)
            __fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            __bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang < -135 and ang >= -180:
            multiplier = tools.map(ang, -135, -180, 0, 1)
            __fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            __bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            __bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
            

        '''while __fRMotor.angle() < revs * 360:
            if any(self.brick.buttons()):
                break'''

    def intervall(speed, revs, count, *args):
        """drives revs forward and backward with speed count times"""
        i = 0
        speed = speed * 1.7 * 6 # speed in deg/s to %
        # move count times for- and backwards
        while i < count:
            if config.robotType == 'NORMAL':
                ang = __lMotor.angle()
                # drive backwards
                __rMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                __lMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while __lMotor.angle() > revs * -360:
                    if any(self.brick.buttons()):
                        return

                #drive forwards
                __lMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                __rMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while __rMotor.angle() <= ang:
                    if any(self.brick.buttons()):
                        return
            
            elif config.robotType == 'ALLWHEEL' or config.robotType == 'MECANUM':
                ang = __lMotor.angle()
                # drive backwards
                __fRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                __bRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                __fLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                __bLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while __lMotor.angle() > revs * -360:
                    if any(self.brick.buttons()):
                        return

                #drive forwards
                __fRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                __bRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                __fLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                __bLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while __rMotor.angle() <= ang:
                    if any(self.brick.buttons()):
                        return

            i += 1

    def curveShape(speed, revs1, deg, *args):
        """Drives in a curve deg over revs with speed"""
        speed = speed * 1.7 * 6 #speed to deg/s from %

        #self.__gyro starting point
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
            print(rSpeed, lSpeed, revs1, revs2)
            __rMotor.run_angle(rSpeed, revs2 * 360, Stop.COAST, False)
            __lMotor.run_angle(lSpeed, revs1 * 360 + 5, Stop.COAST, False)
            #turn
            while self.__gyro.angle() - startValue < deg and not any(self.brick.buttons()):
                pass

        else:
            #asign higher speed to outer wheel
            rSpeed = speed
            lSpeed = speedSlow
            
            __rMotor.run_angle(rSpeed, revs1 * 360 + 5, Stop.COAST, False)
            __lMotor.run_angle(lSpeed, revs2 * 360, Stop.COAST, False)

            #turn
            while self.__gyro.angle() + startValue > deg and not any(self.brick.buttons()):
                pass
                
    def toColor(speed, color, side, *args):
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
                        __rMotor.dc(speed)
                        __lMotor.dc(speed)
                    else: 
                        __fRMotor.dc(speed)
                        __bRMotor.dc(speed)
                        __fLMotor.dc(speed)
                        __bLMotor.dc(speed)

            while lLight.color() != color and not any(self.brick.buttons()):
                if robotType == 'NORMAL':
                    __rMotor.dc(speed)
                    __lMotor.dc(speed)
                else: 
                    __fRMotor.dc(speed)
                    __bRMotor.dc(speed)
                    __fLMotor.dc(speed)
                    __bLMotor.dc(speed)
            
        #only drive till right colorSensor 
        elif side == 3:
            #if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while rLight.color() != Color.WHITE and not any(self.brick.buttons()):
                    if robotType == 'NORMAL':
                        __rMotor.dc(speed)
                        __lMotor.dc(speed)
                    else: 
                        __fRMotor.dc(speed)
                        __bRMotor.dc(speed)
                        __fLMotor.dc(speed)
                        __bLMotor.dc(speed)
                
            while rLight.color() != color and not any(self.brick.buttons()):
                if robotType == 'NORMAL':
                    __rMotor.dc(speed)
                    __lMotor.dc(speed)
                else: 
                    __fRMotor.dc(speed)
                    __bRMotor.dc(speed)
                    __fLMotor.dc(speed)
                    __bLMotor.dc(speed)
            
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

                __rMotor.dc(rSpeed)
                __lMotor.dc(lSpeed)
                #if right at color stop right Motor
                if rLight.color() == color and rWhite:
                    rSpeed = 0
                #if left at color stop left Motor
                if lLight.color() == color and lWhite:
                    lSpeed = 0

    def toWall(speed, *args):
        """drives backwards with speed until it reaches a wall"""
        while not touch.pressed():
            if config.robotType == 'NORMAL':
                __rMotor.dc(- abs(speed))
                __lMotor.dc(- abs(speed))
            else:
                __fRMotor.dc(- abs(speed))
                __bRMotor.dc(- abs(speed))
                __fLMotor.dc(- abs(speed))
                __bLMotor.dc(- abs(speed))

            if any(self.brick.buttons()):
                break
        
        __lMotor.dc(0)
        __rMotor.dc(0)

    def gearing(speed, revs, port, *args):
        """rotates the port for revs revulutions with a speed of speed"""
        speed = speed * 1.7 * 6 #speed to deg/s from %
        gearingPortMotor.run_target(300, port * 90, Stop.HOLD, True) #select gearing Port
        ang = gearingTurnMotor.angle()
        gearingTurnMotor.run_angle(speed, revs * 360, Stop.BRAKE, False) #start turning the port
        #cancel, if any brick button is pressed
        if revs > 0:
            while gearingTurnMotor.angle() < revs * 360 - ang:
                if any(self.brick.buttons()):
                    gearingTurnMotor.dc(0)
                    return
        else:
            while gearingTurnMotor.angle() > revs * 360 + ang:
                if any(self.brick.buttons()):
                    gearingTurnMotor.dc(0)
                    return

    def actionMotors(speed, revs, port, *args):
        # turn motor 1
        if port == 1:
            aMotor1.run_angle(speed, revs * 360, Stop.BRAKE, False)

            if revs > 0:
                while aMotor1.angle() < revs * 360 - ang:
                    if any(self.brick.buttons()):
                        aMotor1.dc(0)
                        return
            else:
                while aMotor1.angle() > revs * 360 + ang:
                    if any(self.brick.buttons()):
                        aMotor1.dc(0)
                        return
        # turm motor 2
        elif port == 2:
            aMotor2.run_angle(speed, revs * 360, Stop.BRAKE, False)

            if revs > 0:
                while aMotor2.angle() < revs * 360 - ang:
                    if any(self.brick.buttons()):
                        aMotor2.dc(0)
                        return
            else:
                while aMotor2.angle() > revs * 360 + ang:
                    if any(self.brick.buttons()):
                        aMotor2.dc(0)
                        return
    
