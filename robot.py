import config
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Direction)

# sensor initialisation
if config.gyroSensorPort != 0:
    try:
        gyro = GyroSensor(config.gyroSensorPort)
    except:
        gyro = 0
        print("Gyro-Sensor not connected to given port ")
else:
    print('You need a gyro sensor in order to be able to drive properly with your robot')

try:
    rLight = ColorSensor(config.rightLightSensorPort) if (config.rightLightSensorPort != 0) else 0
except:
    print("Color-Sensor not connected to given port ")

try:
    lLight = ColorSensor(config.leftLightSensorPort) if (config.leftLightSensorPort != 0) else 0  
except:
    print("Color-Sensor not connected to given port ")

try:
    touch = TouchSensor(config.touchSensorPort) if (config.touchSensorPort != 0) else 0
except:
    print("Touch-Sensor not connected to given port ")


# motor initialisation
try:
    if config.robotType == 'NORMAL':
        lMotor = Motor(config.leftMotorPort, Direction.CLOCKWISE if (not config.leftMotorInverted) else Direction.COUNTERCLOCKWISE)
        rMotor = Motor(config.rightMotorPort, Direction.CLOCKWISE if (not config.rightMotorInverted) else Direction.COUNTERCLOCKWISE)

        if config.useGearing:
            gearingPortMotor = Motor(config.gearingSelectMotorPort, Direction.CLOCKWISE if (not config.gearingSelectMotorPortInverted) else Direction.COUNTERCLOCKWISE)
            gearingTurnMotor = Motor(config.gearingTurnMotorPort, Direction.CLOCKWISE if (not config.gearingTurnMotorPortInverted) else Direction.COUNTERCLOCKWISE)

        else:
            aMotor1 = Motor(config.firstActionMotorPort, Direction.CLOCKWISE if (not config.firstActionMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.firstActionMotorPort != 0) else 0
            aMotor2 = Motor(config.secondActionMotorPort, Direction.CLOCKWISE if (not config.secondActionMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.secondActionMotorPort != 0) else 0

    else:
        fRMotor = Motor(config.frontRightMotorPort, Direction.CLOCKWISE if (not config.frontRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.frontRightMotorPort != 0) else 0
        bRMotor = Motor(config.backRightMotorPort, Direction.CLOCKWISE if (not config.backRightMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.backRightMotorPort != 0) else 0
        fLMotor = Motor(config.frontLeftMotorPort, Direction.CLOCKWISE if (not config.frontLeftMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.frontLeftMotorPort != 0) else 0
        bLMotor = Motor(config.backLeftMotorPort, Direction.CLOCKWISE if (not config.backLeftMotorInverted) else Direction.COUNTERCLOCKWISE) if (config.backLeftMotorPort != 0) else 0
except:
    print("Some of the motors are not connected or connected to the wrong port. Please fix it either in config or on your Robot.")