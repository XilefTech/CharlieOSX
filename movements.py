import robot, OSTools
from robotError import *

# TODO?: gearing homing?

if self.__gyro != 0:
    self.__gyro.reset_angle(0)
    

    

                


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
    
