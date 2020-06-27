#!/usr/bin/env pybricks-micropython

import time, math, json
import OSTools as tools
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from collections import OrderedDict

import config

# initialize the Sensors and Motors
import robot

import movements

def loadSettings():
    order = ['Debug Driving', 'Audio-Volume', 'EFX-Volume', 'Console-Log', 'Show Warnings', 'Show Errors']
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        sorted_settings = OrderedDict()
        sorted_settings['options'] = OrderedDict()
        for i in range(len(order)):
            sorted_settings['options'][order[i]] = settings['options'][order[i]]
        sorted_settings['values'] = settings['values']
        return sorted_settings

def storeSettings(data):
    with open('settings.json', 'w') as f:
        f.write(json.dumps(data, sort_keys = False))

settings = OrderedDict({'options': OrderedDict({'Debug Driving': 2, 'Audio-Volume': 100, 'EFX-Volume': 100, 'Console-Log': True, 'Show Warnings': True, 'Show Errors': True}),
            'values': {
                'min': {'Debug Driving': 0, 'Audio-Volume': 0, 'EFX-Volume': 0, 'Console-Log': False, 'Show Warnings': False, 'Show Errors': False},
                'max': {'Debug Driving': 2, 'Audio-Volume': 100, 'EFX-Volume': 100, 'Console-Log': True, 'Show Warnings': True, 'Show Errors': True}
            }})


#storeSettings(settings) # temporary for storing changes in keys of the dictionary, created above, to the file

charlie = EV3Brick()

def mainLoop():
    global menuState
    menuState, oldMenuState, position = 0, 0, 0
    oldPos = 1
    loop, selected = True, False
    tools.drawMenu(int(menuState))
    keys = list(settings['options'].keys())
    while loop:
        # navigation inbetween main pages
        if menuState == 0:
            if Button.UP in charlie.buttons.pressed():
                menuState = 5
            elif Button.DOWN in charlie.buttons.pressed():
                menuState = 1
        elif menuState > 0 and menuState < 6:
            if Button.UP in charlie.buttons.pressed() and menuState > 1:
                menuState -= 1
            elif Button.UP in charlie.buttons.pressed() and menuState == 1:
                menuState = 5
            if Button.DOWN in charlie.buttons.pressed() and menuState < 5:
                menuState += 1
            elif Button.DOWN in charlie.buttons.pressed() and menuState == 5:
                menuState = 1
        
        # subMenus
        elif menuState == 50: #settings Menu

            if Button.UP in charlie.buttons.pressed():
                if not selected:
                    if position > 0:
                        position -= 1
                    elif position == 0:
                        position = len(settings['options']) - 1
                else:
                    if settings['options'][keys[position]] > settings['values']['min'][keys[position]]:
                        settings['options'][keys[position]] -= 1
                    elif settings['options'][keys[position]] == settings['values']['min'][keys[position]]:
                        settings['options'][keys[position]] = settings['values']['max'][keys[position]]
                    tools.sound('media/click.wav')
                    tools.drawSettings(position, settings, selected)
            if Button.DOWN in charlie.buttons.pressed():
                if not selected:
                    if position < len(settings['options']) - 1:
                        position += 1
                    elif position == len(settings['options']) - 1:
                        position = 0
                else:
                    if settings['options'][keys[position]] < settings['values']['max'][keys[position]]:
                        settings['options'][keys[position]] += 1
                    elif settings['options'][keys[position]] == settings['values']['max'][keys[position]]:
                        settings['options'][keys[position]] = settings['values']['min'][keys[position]]
                    tools.sound('media/click.wav')
                    tools.drawSettings(position, settings, selected)
                        


            if Button.CENTER in charlie.buttons.pressed():
                if selected:
                    storeSettings(settings)
                selected = not selected
                oldPos += 1

            if position != oldPos:
                tools.sound('media/click.wav')
                time.sleep(0.08)
                tools.drawSettings(position, settings, selected)
                oldPos = position
                time.sleep(0.15)

        # selection of pages
        if Button.RIGHT in charlie.buttons.pressed() and menuState > 0 and menuState <= 5 and not selected:
            menuState = menuState * 10
            position, oldPos = 0, 1
            oldMenuState = menuState
            tools.sound('media/confirm.wav')
            time.sleep(0.08)
            tools.animate(menuState, True)
            time.sleep(0.4)

        if Button.LEFT in charlie.buttons.pressed() and menuState >= 10 and not selected:
            tools.sound('media/confirm.wav')
            time.sleep(0.08)
            tools.animate(menuState, False)
            menuState = menuState / 10
            oldMenuState = menuState
            time.sleep(0.4)


        if oldMenuState != menuState:
            tools.sound('media/click.wav')
            time.sleep(0.08)
            tools.drawMenu(menuState)
            oldMenuState = menuState
            time.sleep(0.3)

        if tools.logMsg == 1:
            tools.logMsg = 0
            menuState = menuState / 10

        




# just some example code
#charlie.sound.beep()
#movements.execute([7, 75, 10, 0])


### things, I'm sometimes using to test things - can be ignored
"""
lineMap = {'height' : 300, 'width' : 1000,
            'from' : (1, 1), 'to' : (1, 4), 
            'obstacles' : [((2, 1), (4, 1))]}

tools.doIntersect(lineMap)"""

settings = loadSettings()
#runs menu
mainLoop()

