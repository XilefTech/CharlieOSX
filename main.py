#!/usr/bin/env pybricks-micropython

import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, StopWatch
from charlieosx import CharlieOSX
     
# os = CharlieOSX('config.cfg', 'settings.json', '')



import picoweb, _thread

app = picoweb.WebApp("app")

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/html")
  
    htmlFile = open('site.html', 'r')
  
    for line in htmlFile:
        yield from resp.awrite(line)
 

weblock = _thread.allocate_lock()

def runWebserver():
    with weblock:
        app.run(debug=True, host = "192.168.178.52")
_thread.start_new_thread(runWebserver, ())


while True:
    time.sleep(5)