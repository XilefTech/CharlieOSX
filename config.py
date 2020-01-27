from pybricks.parameters import Port
#----------------------------------------------------------------------------------
#
#                               Config file for 
#
#
#                                 CharlieOSX
#
#                    the OS with more control of your Robot
#
#----------------------------------------------------------------------------------
# Fill in everything about your robot that is required.
# Ports all start with 'Port.' and for sensors there is 'S1', 'S2', 'S3', 'S4', motor ports are 'A', 'B', 'C', 'D', e.g Port.S1
# Each motor has a Inverted variable that can either be True or False.
# It can be set if you built your robot so that the motors are inversed.


# Robot type:
# NORMAL = 2 powered normal wheels
# MECANUM = 4 powered mecanum wheels
# ALLWHEEL = 4 powered normal wheels
robotType = "MECANUM"

# Robot wheels
# (currently only affects driving in curve shaped mode)
wheelDistance = 12 # cm
wheelDiameter = 7.5  # cm

# Robot Sensor Conection:
# (if not used 0)

# touchSensor in the back of the Robot
touchSensorPort = Port.S1

# bottom viewing light sensors
leftLightSensorPort = Port.S2
rightLightSensorPort = Port.S3

# gyro sensor used for driving
gyroSensorPort = Port.S4

# motors:
if robotType == "NORMAL":
    # settings only for 'NORMAL' type

    # driving motors:
    rightMotorPort = Port.C
    rightMotorInverted = True
    leftMotorPort = Port.B
    leftMotorInverted = True

    # robot uses a 4-way hardware gearing
    useGearing = True

    if useGearing:
        # lightsensor that senses RED when gearing is in port 0 position
        gearingHomeLightSensorPort = 0

        # gearing motor for selecting the port
        gearingSelectMotorPort = Port.A
        gearingSelectMotorPortInverted = False

        # gearing motor for turning the port
        gearingTurnMotorPort = Port.D
        gearingTurnMotorPortInverted = False

    else:
        firstActionMotorPort = Port.A
        firstActionMotorInverted = False

        secondActionMotorPort = Port.D
        secondActionMotorInverted = False

else:
    useGearing = False

    # settings for ALLWHEEL and MECANUM type
    frontRightMotorPort = Port.B
    frontRightMotorInverted = False

    frontLeftMotorPort = Port.A
    frontLeftMotorInverted = False

    backRightMotorPort = Port.D
    backRightMotorInverted = True

    backLeftMotorPort = Port.C
    backLeftMotorInverted = True




# FLL:
# Activates different saving slots for programs according to the names given in runNames
# Also activates an option for the competition to run all the programs after each other in the same order as in runNames
FLLMode = True

# names of the different runs that you want to complete at FLL
# please note that names over x characters will appear shortened on the screen  TODO: insert max characters number
runNames = ['Crane', 'Elevator', 'Treehouse', 'ConstructRed', 'ConstructBrown', 'Architecture']
