import robot, OSTools, robotError

if robot.gyro != 0:
    robot.gyro.reset_angle(0)

# TODO?: gearing homing?

def execute(params, *args):
    """Starts the different Driving modules according to the given parameters"""

    if (OSTools.getBatteryVoltage() <= 7500):
        log.warn("Please charge the battery. Only " + str(OSTools.getBatteryVoltage(human=True)) + " V left. You need at least 7.5 Volts.")
        return RobotErrors.Battery.tooLow

    
    while params != [] and not any(charlie.buttons()):

        mode = params.pop(0)
        arg1 = params.pop(0)
        arg2 = params.pop(0)
        arg3 = params.pop(0)

        #turn
        if mode == 4:
            turn(arg1, arg2, arg3)
    
        #gearing
        elif mode == 5:
            if config.useGearing():
                gearing(arg1, arg2, arg3)
            else:
                actionMotors(arg1, arg2, arg3)
    
        #straight
        elif mode == 7:
            if config.robotType != 'MECANUM':
                straight(arg1, arg2, arg3)
            else:
                straightMecanum(arg1, arg2, arg3)
        
        #intervall
        elif mode == 9:
            intervall(arg1, arg2, arg3)
        
        #curve shaped
        elif mode == 11:
            curveShape(arg1, arg2, arg3)
        
        #to color 
        elif mode == 12:
            toColor(arg1, arg2, arg3)
        
        #until back wall
        elif mode == 15:
            toWall(arg1, arg2, arg3)
        

    if config.robotType == 'NORMAL':
        lMotor.dc(0)
        rMotor.dc(0)
    else:
        fRMotor.dc(0)
        bRMotor.dc(0)
        fLMotor.dc(0)
        bLMotor.dc(0)

    if config.useGearing:
        gearingPortMotor.run_target(300, 0, Stop.HOLD, True)    #reset gearing

    time.sleep(0.3)

if robot.gyro != 0:
    def turn(speed, deg, port, *args):
        """turns deg with speed. port indicates with wich motor(s)"""
        startValue = robot.gyro.angle()

        #turn only with left motor
        if port == 2:
            #right motor off
            rMotor.dc(0)
            #turn the angle
            if deg > 0:
                while robot.gyro.angle() - startValue < deg:
                    if config.robotType == 'NORMAL':
                        lMotor.dc(speed)
                    else:
                        fLMotor.dc(speed)
                        bLMotor.dc(speed)
                    #slow down to not overshoot
                    if not robot.gyro.angle() - startValue < deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return
            else:
                while robot.gyro.angle() - startValue > deg:
                    if config.robotType == 'NORMAL':
                        lMotor.dc(-speed)
                    else:
                        fLMotor.dc(-speed)
                        bLMotor.dc(-speed)
                    #slow down to not overshoot
                    if not robot.gyro.angle() - startValue > deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return

        #turn only with right motor
        elif port == 3:
            #left motor off
            lMotor.dc(0)
            #turn the angle
            if deg > 0:
                while robot.gyro.angle() - startValue < deg:
                    if config.robotType == 'NORMAL':
                        rMotor.dc(-speed)
                    else:
                        fRMotor.dc(-speed)
                        bRMotor.dc(-speed)
                    #slow down to not overshoot
                    if not robot.gyro.angle() - startValue < deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return                 
            else:
                while robot.gyro.angle() - startValue > deg:
                    if config.robotType == 'NORMAL':
                        rMotor.dc(speed)
                    else:
                        fRMotor.dc(speed)
                        bRMotor.dc(speed)
                    #slow down to not overshoot
                    if not robot.gyro.angle() - startValue > deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.1) if speed > 20 else speed
                    
                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return

        #turn with both motors
        elif port == 23:
            #turn the angle
            if deg > 0:
                while robot.gyro.angle() - startValue < deg:
                    if config.robotType == 'NORMAL':
                        rMotor.dc(-speed / 2)
                        lMotor.dc(speed / 2)
                    else:
                        fRMotor.dc(-speed / 2)
                        bRMotor.dc(-speed / 2)
                        fLMotor.dc(speed / 2)
                        bLMotor.dc(speed / 2)
                    #slow down to not overshoot
                    if not robot.gyro.angle() - startValue < deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.01) if speed > 40 else speed

                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return    
                    
            else:
                while robot.gyro.angle() - startValue > deg:
                    if config.robotType == 'NORMAL':
                        rMotor.dc(speed / 2)
                        lMotor.dc(-speed / 2)
                    else:
                        fRMotor.dc(speed / 2)
                        bRMotor.dc(speed / 2)
                        fLMotor.dc(-speed / 2)
                        bLMotor.dc(-speed / 2)
                    #slow down to not overshoot
                    if not robot.gyro.angle() - startValue > deg * 0.6:
                        speed = speed - tools.map(deg, 1, 360, 10, 0.01) if speed > 40 else speed
                    
                    #cancel if button pressed
                    if any(charlie.buttons()):
                        return

    def straight(speed, dist, *args):
        """drives forward with speed in a straight line, corrected by the robot.gyro. Only working for NORMAL and ALLWHEEL Type"""
        correctionStrength = 2 # how strongly the robot will correct. 2 = default, 0 = nothing
        startValue = robot.gyro.angle()
        
        
        revs = dist / (config.wheelDiameter * math.pi) # convert the input (cm) to revs
        revs = revs / 2

        #drive
        if config.robotType == 'NORMAL':
            rMotor.reset_angle(0)
            if revs > 0:
                while revs > rMotor.angle() / 360:
                    #if not driving staright correct it
                    if robot.gyro.angle() - startValue > 0:
                        lSpeed = speed - abs(robot.gyro.angle() - startValue) * correctionStrength
                        rSpeed = speed
                    elif robot.gyro.angle() - startValue < 0:
                        rSpeed = speed - abs(robot.gyro.angle() - startValue) * correctionStrength
                        lSpeed = speed
                    else:
                        lSpeed = speed
                        rSpeed = speed

                    rMotor.dc(rSpeed)
                    lMotor.dc(lSpeed)
                    
                    #cancel if button pressed
                    if any(charlie.buttons()):
                            return
            else:
                while revs < rMotor.angle() / 360:
                    
                    #if not driving staright correct it
                    if robot.gyro.angle() - startValue < 0:
                        rSpeed = speed + abs(robot.gyro.angle() - startValue) * correctionStrength
                        lSpeed = speed
                    elif robot.gyro.angle() - startValue > 0:
                        lSpeed = speed + abs(robot.gyro.angle() - startValue) * correctionStrength
                        rSpeed = speed
                    else:
                        lSpeed = speed
                        rSpeed = speed

                    rMotor.dc(-rSpeed)
                    lMotor.dc(-lSpeed)

                    #cancel if button pressed
                    if any(charlie.buttons()):
                            return
        
        elif config.robotType == 'ALLWHEEL':
            fRMotor.reset_angle(0)
            if revs > 0:
                while revs > fRMotor.angle() / 360:
                    #if not driving staright correct it
                    if robot.gyro.angle() - startValue > 0:
                        lSpeed = speed - abs(robot.gyro.angle() - startValue) * correctionStrength
                        rSpeed = speed
                    elif robot.gyro.angle() - startValue < 0:
                        rSpeed = speed - abs(robot.gyro.angle() - startValue) * correctionStrength
                        lSpeed = speed
                    else:
                        lSpeed = speed
                        rSpeed = speed

                    fRMotor.dc(rSpeed)
                    bRMotor.dc(rSpeed)
                    fLMotor.dc(lSpeed)
                    bLMotor.dc(lSpeed)
                    
                    #cancel if button pressed
                    if any(charlie.buttons()):
                            return
            else:
                while revs < fRMotor.angle() / 360:
                    #if not driving staright correct it
                    if robot.gyro.angle() - startValue < 0:
                        rSpeed = speed + abs(robot.gyro.angle() - startValue) * correctionStrength
                        lSpeed = speed
                    elif robot.gyro.angle() - startValue > 0:
                        lSpeed = speed + abs(robot.gyro.angle() - startValue) * correctionStrength
                        rSpeed = speed
                    else:
                        lSpeed = speed
                        rSpeed = speed

                    fRMotor.dc(rSpeed)
                    bRMotor.dc(rSpeed)
                    fLMotor.dc(lSpeed)
                    bLMotor.dc(lSpeed)

                    #cancel if button pressed
                    if any(charlie.buttons()):
                            return

    def straightMecanum(speed, dist, ang, *args):
        """Driving a straight line of dist cm with speed in ang direction. Only working with MECANUM Type"""
        fRMotor.reset_angle(0)

        revs = dist / (config.wheelDiameter * math.pi) # convert the input (cm) to revs
        speed = speed * 1.7 * 6 # convert speed form % to deg/min

        # driving the robot into the desired direction
        if ang >= 0 and ang <= 45:
            multiplier = tools.map(ang, 0, 45, 1, 0)
            fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang >= -45 and ang < 0:
            multiplier = tools.map(ang, -45, 0, 0, 1)
            fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang > 45 and ang <= 90:
            multiplier = tools.map(ang, 45, 90, 0, 1)
            fRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            bLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang < -45 and ang >= -90:
            multiplier = tools.map(ang, -45, -90, 0, 1)
            fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            bRMotor.run_angle(speed, revs * 360, Stop.COAST, False)
            bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed, revs * 360, Stop.COAST, True)
        elif ang > 90 and ang <= 135:
            multiplier = tools.map(ang, 90, 135, 1, 0)
            fRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            bLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang < -90 and ang >= -135:
            multiplier = tools.map(ang, -90, -135, 1, 0)
            fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            bRMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed * multiplier + 1, revs * 360 * multiplier, Stop.COAST, False)
            bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang > 135 and ang <= 180:
            multiplier = tools.map(ang, 135, 180, 0, 1)
            fRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            bRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            bLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
        elif ang < -135 and ang >= -180:
            multiplier = tools.map(ang, -135, -180, 0, 1)
            fRMotor.run_angle(speed, revs * -360, Stop.COAST, False)
            bRMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            fLMotor.run_angle(speed * multiplier + 1, revs * -360 * multiplier, Stop.COAST, False)
            bLMotor.run_angle(speed, revs * -360, Stop.COAST, True)
            

        '''while fRMotor.angle() < revs * 360:
            if any(charlie.buttons()):
                break'''

    def intervall(speed, revs, count, *args):
        """drives revs forward and backward with speed count times"""
        i = 0
        speed = speed * 1.7 * 6 # speed in deg/s to %
        # move count times for- and backwards
        while i < count:
            if config.robotType == 'NORMAL':
                ang = lMotor.angle()
                # drive backwards
                rMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                lMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while lMotor.angle() > revs * -360:
                    if any(charlie.buttons()):
                        return

                #drive forwards
                lMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                rMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while rMotor.angle() <= ang:
                    if any(charlie.buttons()):
                        return
            
            elif config.robotType == 'ALLWHEEL' or config.robotType == 'MECANUM':
                ang = lMotor.angle()
                # drive backwards
                fRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                bRMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                fLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                bLMotor.run_angle(speed, revs * -360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while lMotor.angle() > revs * -360:
                    if any(charlie.buttons()):
                        return

                #drive forwards
                fRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                bRMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                fLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                bLMotor.run_angle(speed, revs * 360, Stop.BRAKE, False)
                # return to cancel if any button is pressed
                while rMotor.angle() <= ang:
                    if any(charlie.buttons()):
                        return

            i += 1

    def curveShape(speed, revs1, deg, *args):
        """Drives in a curve deg over revs with speed"""
        speed = speed * 1.7 * 6 #speed to deg/s from %

        #robot.gyro starting point
        startValue = robot.gyro.angle()
        
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
            rMotor.run_angle(rSpeed, revs2 * 360, Stop.COAST, False)
            lMotor.run_angle(lSpeed, revs1 * 360 + 5, Stop.COAST, False)
            #turn
            while robot.gyro.angle() - startValue < deg and not any(charlie.buttons()):
                pass

        else:
            #asign higher speed to outer wheel
            rSpeed = speed
            lSpeed = speedSlow
            
            rMotor.run_angle(rSpeed, revs1 * 360 + 5, Stop.COAST, False)
            lMotor.run_angle(lSpeed, revs2 * 360, Stop.COAST, False)

            #turn
            while robot.gyro.angle() + startValue > deg and not any(charlie.buttons()):
                pass
                
    def toColor(speed, color, side, *args):
        """Drives until the robot drives to a color line with speed"""
        # sets color to a value that the colorSensor can work with
        if color == 0:
            color = Color.BLACK
        else:
            color = Color.WHITE

        #only drive till left colorSensor 
        if side == 2:
            #if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while lLight.color() != Color.WHITE and not any(charlie.buttons()):
                    if robotType == 'NORMAL':
                        rMotor.dc(speed)
                        lMotor.dc(speed)
                    else: 
                        fRMotor.dc(speed)
                        bRMotor.dc(speed)
                        fLMotor.dc(speed)
                        bLMotor.dc(speed)

            while lLight.color() != color and not any(charlie.buttons()):
                if robotType == 'NORMAL':
                    rMotor.dc(speed)
                    lMotor.dc(speed)
                else: 
                    fRMotor.dc(speed)
                    bRMotor.dc(speed)
                    fLMotor.dc(speed)
                    bLMotor.dc(speed)
            
        #only drive till right colorSensor 
        elif side == 3:
            #if drive to color black drive until back after white to not recognize colors on the field as lines
            if color == Color.BLACK:
                while rLight.color() != Color.WHITE and not any(charlie.buttons()):
                    if robotType == 'NORMAL':
                        rMotor.dc(speed)
                        lMotor.dc(speed)
                    else: 
                        fRMotor.dc(speed)
                        bRMotor.dc(speed)
                        fLMotor.dc(speed)
                        bLMotor.dc(speed)
                
            while rLight.color() != color and not any(charlie.buttons()):
                if robotType == 'NORMAL':
                    rMotor.dc(speed)
                    lMotor.dc(speed)
                else: 
                    fRMotor.dc(speed)
                    bRMotor.dc(speed)
                    fLMotor.dc(speed)
                    bLMotor.dc(speed)
            
        #drive untill both colorSensors
        elif side == 23:
            rSpeed = speed
            lSpeed = speed
            rWhite = False
            lWhite = False
            
            while (rLight.color() != color or lLight.color() != color) and not any(charlie.buttons()):
                #if drive to color black drive until back after white to not recognize colors on the field as lines
                if color == Color.BLACK:
                    if rLight.color() == Color.WHITE:
                        rWhite = True
                    if lLight.color() == Color.WHITE:
                        lWhite = True

                rMotor.dc(rSpeed)
                lMotor.dc(lSpeed)
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
                rMotor.dc(- abs(speed))
                lMotor.dc(- abs(speed))
            else:
                fRMotor.dc(- abs(speed))
                bRMotor.dc(- abs(speed))
                fLMotor.dc(- abs(speed))
                bLMotor.dc(- abs(speed))

            if any(charlie.buttons()):
                break
        
        lMotor.dc(0)
        rMotor.dc(0)

    def gearing(speed, revs, port, *args):
        """rotates the port for revs revulutions with a speed of speed"""
        speed = speed * 1.7 * 6 #speed to deg/s from %
        gearingPortMotor.run_target(300, port * 90, Stop.HOLD, True) #select gearing Port
        ang = gearingTurnMotor.angle()
        gearingTurnMotor.run_angle(speed, revs * 360, Stop.BRAKE, False) #start turning the port
        #cancel, if any brick button is pressed
        if revs > 0:
            while gearingTurnMotor.angle() < revs * 360 - ang:
                if any(charlie.buttons()):
                    gearingTurnMotor.dc(0)
                    return
        else:
            while gearingTurnMotor.angle() > revs * 360 + ang:
                if any(charlie.buttons()):
                    gearingTurnMotor.dc(0)
                    return

    def actionMotors(speed, revs, port, *args):
        # turn motor 1
        if port == 1:
            aMotor1.run_angle(speed, revs * 360, Stop.BRAKE, False)

            if revs > 0:
                while aMotor1.angle() < revs * 360 - ang:
                    if any(charlie.buttons()):
                        aMotor1.dc(0)
                        return
            else:
                while aMotor1.angle() > revs * 360 + ang:
                    if any(charlie.buttons()):
                        aMotor1.dc(0)
                        return
        # turm motor 2
        elif port == 2:
            aMotor2.run_angle(speed, revs * 360, Stop.BRAKE, False)

            if revs > 0:
                while aMotor2.angle() < revs * 360 - ang:
                    if any(charlie.buttons()):
                        aMotor2.dc(0)
                        return
            else:
                while aMotor2.angle() > revs * 360 + ang:
                    if any(charlie.buttons()):
                        aMotor2.dc(0)
                        return
    
