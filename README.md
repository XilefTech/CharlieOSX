*Disclaimer: Everything in this Repository is still experimental and WIP. Nothing is expected to fully work.
I'm still far away from a final version. If you should experience any issues or bugs, please open an issue in this repository.*

# CharlieOSX
*By XilefTech from the "Lego Spirits"*

![Image of the Main Menu](https://i.pinimg.com/474x/38/bf/b9/38bfb9bd54bc9f610f0fcf08225d95ac.jpg)

#### Summary
CharlieOSX is a Project, meant to be used in all kinds of driving Lego Mindstorms EV3 Robots, with support for other types of robots maybe coming in the future.
CharlieOSX offers a wide feature set with the two main things being:
1. Highly accurate and self-correcting driving methods based on gyro-sensor data
2. An on-Brick GUI for Programing, testing and using of programs without the need of a computer at all.

It will be FLL-Ready (as soon as the basic feature set is fully implemented and tested).

Also it will help you to improve your movements through showing important data in the screen while driving. (Not implemented yet)

### How to use CharlieOSX with your robot:
1. Install [Ev3dev](ev3dev.org/docs/getting-started) or [Pybricks](https://docs.pybricks.com/en/latest/start_ev3.html) on your brick.

2. Download and open this project in VS code
3. Open the config.py file and fill in everything that is needed about your robot
4. You can now add as many execute() functions as you like to the end of the main.py file with an array with the number codes. *Note: you can add multiple commands directly after each other in the array and the robot will drive them all*
5. Just download and the robot will execute your instructions

#### Features
|Feature       | Status     |
|-------|----------|
| Steering any of the three Robot types with the Help of the [number codes](https://docs.google.com/spreadsheets/d/1DmdYeWCkykAH5O6e8qv4fGR5aR4e66AjW1zxPTqASJo/edit?usp=sharing) | Done |
| insert/edit the number codes on the brick itself | WIP |
| create a map with barriers and let the robot navigate on it's own   | NYI |
| steer the robot with a remote control in your browser | Done |
| save the Remote-controlled path and let it repeat it   | NYI |
| use a FLL mode with separate program slots according to the Tasks on the Field and an extra mode for executing them in a specific order at the competition itself   | NYI |


### Usage examples:
To use CharlieOSX you always have to initialize it at the beginning of your program:
```Python
CharlieOSX = CharlieOSX('config.cfg', 'settings.json', '')
```
If you then just want to start the Menu-Interface on the brick and use it, you have to call the UI-Mainloop:
```Python
CharlieOSX.ui.mainLoop()
```
Alternatively, if you want to write your own code inbetween lines and don't need the UI, you can use the drivin methods directly:
```Python
CharlieOSX.robot.straight(100, 20, 0) # drives in a straight line 20cm with 100% speed
CharlieOSX.robot.turn(75, 90, 23)  # turns 90 deg using both motors with 75% speed
```
#### Webremote:
If you want to use the browser-based Webremote of CharlieOSX, you'll need a USB-WIFI adapter. When your robot is connected to your local WIFI network, make sure the robots local IP-adress and the localIP in the config match.

To then start the webremote call the run() function:
```Python
CharlieOSX = CharlieOSX('config.cfg', 'settings.json', '')
CharlieOSX.webremote.run()
```
Now the webserver will start and you can acess the webremote with any webbrowser at < yourBrickIP >:8081 so for example 192.168.178.52:8081

![Webremote-Image](https://user-images.githubusercontent.com/52332196/98609202-0ddb4700-22ed-11eb-9de7-c34cd266c071.png)

The interface is pretty simple:
1. A joystick for moving the robot
2. A slider to control the velocity of an action motor
3. A slider to set the maximum speed for the robot

### More Information
You will always be able to find more (detailed) information about the project in the [wiki](https://github.com/XilefTech/CharlieOSX/wiki).
If there are still questions left, after visiting our wiki, feel free to ask in an issue!

## Contributors
- XilefTech
- GerhardBenkovsky
- TheGreydiamond
