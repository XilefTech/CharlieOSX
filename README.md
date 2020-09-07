*Disclaimer: Everything in this Repository is still experimental and WIP. Nothing is expected to fully work.
I'm still far away from a final version.*

# CharlieOSX
*By XilefTech from the "Lego Spirits"*

CharlieOSX is the best choice as a program for your specific robot.
Just fill in your robot Parameters in the config.py file and everything else like driving and robot handling is set up automatically.


### How to use CharlieOSX with your robot:
1. Download and open this project in VS code
2. Open the config.py file and fill in everything that is needed about your robot
3. You can now add as many execute() functions as you like to the end of the main.py file with an array with the number codes. *Note: you can add multiple commands directly after each other in the array and the robot will drive them all*
4. Just download and the robot will execute your instructions

#### Features
|Feature       | Status     |
|-------|----------|
| Steering any of the three Robot types with the Help of the [number codes](https://docs.google.com/spreadsheets/d/1DmdYeWCkykAH5O6e8qv4fGR5aR4e66AjW1zxPTqASJo/edit?usp=sharing) | Done |
| insert/edit the number codes on the brick itself | WIP |
| create a map with barriers and let the robot navigate on it's own   | NYI |
| steer the robot with a remote control of some kind (actually not sure what), save the steered path and let it repeat it   | NYI |
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
CharlieOSX.robot.straight(100, 20) # drives in a straight line 20cm with 100% speed
CharlieOSX.robot.turn(75, 90, 23)  # turns 90 deg using both motors with 75% speed
```

### More Information
You will always be able to find more (detailed) information about the project in the [wiki](https://github.com/XilefTech/CharlieOSX/wiki).
If there are still questions left, after visiting our wiki, feel free to ask in an issue!

## Contributors
- XilefTech
- GerhardBenkovsky
- TheGreydiamond
