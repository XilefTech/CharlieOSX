#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port, Direction, Color
from lib.simple_pid import PID
import lib.picoweb as picoweb
import math, time

class LineFollower():
    '''Linefollower Class Contains functionality for PID-Controlled line following, as well as Web-Panel-Aided PID-Tuning'''

    def __init__(self, rPort: Port, lPort: Port, csPort: Port, rDir=Direction.CLOCKWISE, lDir=Direction.CLOCKWISE, debug=0) -> None:
        '''init'''
        self.debug = debug

        self.brick = EV3Brick()
        self.brick.speaker.beep(200, 500)
        self.brick.speaker.beep(300, 500)
        self.brick.speaker.beep(400, 500)

        self.lm = Motor(lPort, lDir)
        self.rm = Motor(rPort, rDir)

        self.cSensor = ColorSensor(csPort)

        self.pid = PID(Kp = 3.5, Ki = 0, Kd = 5, setpoint = 28) #define the parameters for the 
        self.pid.sample_time = 0.01         #times the pid refreshes the output value
        self.pid.setpoint = 25              #the reflection value of the line - the sensor should rest above the middle of the line

        self.app = picoweb.WebApp("PID-Tuning-Server")

        @self.app.route("/")
        def index(req, resp):
            if req.method == "GET":
                with open('site/lineFollowing/index.html') as file:
                    yield from picoweb.start_response(resp, content_type = "text/html")

                    for line in file:
                        yield from resp.awrite(line)
            
            elif req.method == "POST":
                yield from req.read_form_data()
                Kp = float(req.form["Kp"])
                Kd = float(req.form["Kd"])
                Ki = float(req.form["Ki"])
                speed = float(req.form["speed"])
                dist = float(req.form["dist"])

                yield from picoweb.start_response(resp)
                with open('site/lineFollowing/index.html') as file:
                    yield from picoweb.start_response(resp, content_type = "text/html")

                    for line in file:
                        yield from resp.awrite(line)
                
                self.pid.tunings = (Kp, Ki, Kd)
                self.run_distance(speed, dist)
                yield from resp.awrite("<br><br>finished driving")

        @self.app.route("/colorValues")
        def getColorValues(req, resp):
            yield from picoweb.start_response(resp, content_type = "text/html")

            yield from resp.awrite("RGB: " + str(self.cSensor.rgb()))
            yield from resp.awrite("<br>RGB-Middle: " + str(round(sum(self.cSensor.rgb()) / 3, 1)))
            yield from resp.awrite("<br>Reflection: " + str(self.cSensor.reflection()))


    def run(self, speed, displayDebug=False):
        '''
        Drives along a line as long as no brick-button is pressed.
        
        Args:
            speed (int): the speed to drive at
            displayDebug (bool): wether Debug information should be displayed on the screen and in console
        '''

        Limit = speed - 50 #the maximal/minimal output of the pid
        self.pid.output_limits = (-Limit, Limit)

        while not any(self.brick.buttons.pressed()):
            self.brick.screen.clear()

            control = self.pid(self.cSensor.reflection())
            
            self.lm.run(speed - control)
            self.rm.run(speed + control)

            if displayDebug:
                print(speed - control)
                print(speed + control)

                self.brick.screen.draw_text(20, 20, speed - control, text_color=Color.BLACK, background_color=None)
                self.brick.screen.draw_text(20, 40, speed + control, text_color=Color.BLACK, background_color=None)

    def run_distance(self, speed, distance):
        '''
        Drives along a line as long as no brick-button is pressed.
        
        Args:
            speed (int): the speed to drive at
            displayDebug (bool): wether Debug information should be displayed on the screen and in console
        '''
        print('runDistance called')
        Limit = speed / 2 #- 50 #the maximal/minimal output of the pid
        self.pid.output_limits = (-Limit, Limit)

        revs = distance / (8.8 * math.pi) # convert distance from cm to revs for driving TODO: use config/parameter for this

        self.lm.reset_angle(0)
        while not abs(self.lm.angle() / 360) > abs(revs):
            now = time.time()
            self.brick.screen.clear()

            control = self.pid(sum(self.cSensor.rgb()) / 3)
            
            self.lm.run(speed - control)
            self.rm.run(speed + control)

            if self.debug == 0:
                #print(speed, round(sum(self.cSensor.rgb()) / 3, 2), round(control, 1), round(speed - control, 1), round(speed + control, 1))

                if control == 0:
                    self.brick.speaker.beep(200, 100)
                elif control > 0:
                    self.brick.speaker.beep(300, -1)
                    print(speed, round(sum(self.cSensor.rgb()) / 3, 2), round(control, 1), round(speed - control, 1), round(speed + control, 1))
                elif control < 0:
                    self.brick.speaker.beep(400, -1)

                #self.brick.screen.draw_text(20, 20, speed - control, text_color=Color.BLACK, background_color=None)
                #self.brick.screen.draw_text(20, 40, speed + control, text_color=Color.BLACK, background_color=None)
            #print(time.time() - now)
            
            #cancel if button pressed
            if any(self.brick.buttons.pressed()):
                break

            while time.time() < (now + 0.05):
                pass
            #print(time.time() - now)
        self.lm.stop()
        self.rm.stop()
        self.brick.speaker.beep(500, 100)
        print('runDistance done')