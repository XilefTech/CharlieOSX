import _thread, time, os

from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI.UIObject import UIObject
from UI.tools import Menu, Box, ProgrammingWindow


class UIManager:
    """
        Basicly a Menu
    """

    def __init__(self, config, settings, brick, logger, settingsPath, charlieOSX):
        # general variable setup
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
        self.__settingsPath = settingsPath
        self.brick = brick
        self.logger = logger
        self.os = charlieOSX
        self.profileHelper = ProfileHelper(self.logger, self.__config)
        self.__sound_lock = _thread.allocate_lock()
        self.__almostBigFont = Font(family='Arial', size=12, bold=False)
        self.__bigFont = Font(family='Arial', size=15, bold=True)
        self.position = [0, 0, False]

        # Main Menu
        self.mainMenu = Menu('sidebar')
        mainPages = [
            "assets/graphics/menus/programming.png",
            "assets/graphics/menus/testing.png",
            "assets/graphics/menus/remote.png",
            "assets/graphics/menus/competition.png",
            "assets/graphics/menus/settings.png",
        ]
        for i in range(len(mainPages)):
            name = mainPages[i].split('/')[3].split('.')[0]
            self.mainMenu.addObject(UIObject(name, self.brick, Box(0, i, 30, 25), 'img', mainPages[i], padding=(0, 0, True)))

        # Programming Menu
        self.programming = Menu('list', self.brick)
        self.programming.setList(self.__config['profileNames'])
        self.programming.setClickAction(self.runProgramming)

        # Testing Menu
        self.testing = Menu('list', self.brick)
        self.testing.setList(self.__config['profileNames'])
        self.testing.setClickAction(self.runTesting)

        # Remote-Control Menu
        self.remote = Menu('canvas')
        self.remote.addObject(UIObject('startButton', self.brick, Box(58, 80, 82, 14), 'textBox', 'Start Webremote', padding=(-1, -1, False)))
        self.remote.addObject(UIObject('endButton', self.brick, Box(59, 80, 81, 14), 'textBox', 'Stop Webremote', padding=(-1, -1, False), visible=False))
        self.remote.getObjectByName('startButton').setClickAction(self.runWebremote)

        # Competition-Mode Menu
        self.competition = Menu('canvas')
        self.competition.addObject(UIObject('startButton', self.brick, Box(55, 80, 88, 14), 'textBox', 'Start Competition', padding=(-1, -1, False)))
        self.competition.addObject(UIObject('runButton', self.brick, Box(74, 90, 48, 14), 'textBox', 'Start Run', padding=(-1, -1, False), visible=False))
        self.competition.addObject(UIObject('nextButton', self.brick, Box(72, 90, 53, 14), 'textBox', 'Start Next', padding=(-1, -1, False), visible=False))
        self.competition.getObjectByName('startButton').setClickAction(self.runCompetition)

        # Settings Menu
        self.settingsMenu = Menu('dict', self.brick)
        self.settingsMenu.setDict(self.__settings)

        # menu Variables
        self.loop = True        
        self.currentMenu = self.mainMenu
        self.subMenus = [
            self.programming,
            self.testing,
            self.remote,
            self.competition,
            self.settingsMenu
        ]
        self.types = {
            4: 'Turn',
            5: 'Action' if not self.__config['useGearing'] else 'Gearing',
            7: 'Straight',
            9: 'Intervall',
            11: 'Curve',
            12: 'to Color',
            15: 'to Wall'
        }
        self.secondParam = {
            4: 'Angle',
            5: 'Revs',
            7: 'Distance',
            9: 'Distance',
            11: 'Distance',
            12: 'Color',
            15: 'none'
        }
        self.thirdParam = {
            4: 'Port',
            5: 'Port',
            7: 'none' if self.__config['robotType'] != 'MECANUM' else 'Angle',
            9: 'Amount',
            11: 'Angle',
            12: 'Side',
            15: 'none'
        }
        self.valueTypes = {
            1: {
                4: 'percentage',
                5: 'percentage',
                7: 'percentage',
                9: 'percentage',
                11: 'percentage',
                12: 'percentage',
                15: 'percentage'
            },
            2: {
                4: 'largeInt',
                5: 'largeInt',
                7: 'largeInt',
                9: 'largeInt',
                11: 'largeInt',
                12: 'bool',
                15: 'none'
            },
            3: {
                4: 'side',
                5: 'port',
                7: 'none',
                9: 'largeInt',
                11: 'largeInt',
                12: 'side',
                15: 'none'
            }
        }
        self.valueRanges = {
            'percentage': range(0, 101),
            'type': [4, 5, 7, 9, 11, 12, 15],
            'largeInt': range(0, 10000),
            'side': [2, 3, 23],
            'bool': [0, 1],
            'port': range(0, 4),
            'none': [0]
        }

        #self.logger.info(self, 'UI initialized')

    def __str__(self):
        return "UIManager"

    def __sound(self, file):
        '''
        This private method is used for playing a sound in a separate thread so that other code can be executed simultaneously.

        Args:
            file (str / SoundFile): The path to the soundfile to play
        '''
        def __playSoundFile(soundFile):
            with self.__sound_lock:
                self.brick.speaker.play_file(soundFile)
        _thread.start_new_thread(__playSoundFile, (file, ))

    def mainLoop(self):
        # Welcome screen
        self.brick.screen.draw_image(0, 0, 'assets/graphics/menus/mainMenu.png', transparent=Color.RED)
        while not any(self.brick.buttons.pressed()): pass
        if Button.UP in self.brick.buttons.pressed():
            self.position[1] = self.currentMenu.maxY
        elif Button.DOWN in self.brick.buttons.pressed():
            self.position[1] = 0
        self.currentMenu.draw(self.position)
        print(self.position)
        time.sleep(0.3)
        self.menuLocations = [
            "assets/graphics/animations/mainProgram/10.png",
            "assets/graphics/animations/mainTest/10.png",
            "assets/graphics/animations/mainRemote/10.png",
            "assets/graphics/animations/mainCompetition/10.png",
            "assets/graphics/animations/mainSettings/10.png",
        ]

        while self.loop:
            if any(self.brick.buttons.pressed()):
                if Button.UP in self.brick.buttons.pressed() and not self.position[2]:
                    self.position[1] = self.position[1] - 1 if self.position[1] > 0 else self.currentMenu.maxY
                elif Button.DOWN in self.brick.buttons.pressed() and not self.position[2]:
                    self.position[1] = self.position[1] + 1 if self.position[1] < self.currentMenu.maxY else 0
                elif Button.LEFT in self.brick.buttons.pressed() and len(self.position) > 3 and not self.position[2]:
                    if self.currentMenu.getType() == 'canvas' and self.position[0] > 0:
                        self.position[0] = self.position[0] - 1 if self.position[0] > 0 else self.currentMenu.maxX
                    else:
                        self.position.pop(0)
                        self.position.pop(0)
                        self.position.pop(0)
                        if len(self.position) == 3:
                            self.animate(self.position[1], False)
                            self.currentMenu = self.mainMenu
                elif Button.RIGHT in self.brick.buttons.pressed() and not self.position[2]:
                    # self.position[0] = self.position[0] + 1 if self.position[0] < self.currentMenu.maxX else 0
                    if self.currentMenu.getType() == 'canvas':
                        self.position[0] = self.position[0] + 1 if self.position[0] < self.currentMenu.maxX else 0
                    else:
                        if len(self.position) == 3:
                            self.animate(self.position[1], True)
                            self.currentMenu = self.subMenus[self.position[1]]
                        self.position.insert(0, False)
                        self.position.insert(0, 0)
                        self.position.insert(0, 0)
                elif Button.RIGHT in self.brick.buttons.pressed() and self.position[2]:
                    self.position[0] = self.position[0] + 1 if self.position[0] < self.currentMenu.maxX else 0
                    self.__settings['options'][list(self.__settings['options'].keys())[self.position[1]]] = self.position[0]
                elif Button.LEFT in self.brick.buttons.pressed() and self.position[2]:
                    self.position[0] = self.position[0] - 1 if self.position[0] > 0 else self.currentMenu.maxX
                    self.__settings['options'][list(self.__settings['options'].keys())[self.position[1]]] = self.position[0]
                elif Button.CENTER in self.brick.buttons.pressed():
                    if self.currentMenu.getType() == 'list':
                        self.currentMenu.click(self.position)
                    elif self.currentMenu.getType() == 'dict':
                        if self.position[2]:
                            self.position.pop(0)
                            self.position.pop(0)
                            self.position.pop(0)
                            self.position[2] = not self.position[2]
                            self.os.storeSettings(self.__settings, 'default')
                            self.os.applySettings(self.__settings)
                        else:
                            self.position[2] = not self.position[2]
                            self.position.insert(0, True)
                            self.position.insert(0, self.position[2])
                            self.position.insert(0, self.__settings['options'][list(self.__settings['options'].keys())[self.position[0]]])
                    elif len(self.position[1]) != 3:
                        self.position[2] = not self.position[2]
                        self.currentMenu.getObjectByPostion(self.position).click()
                        if self.currentMenu.getType() not in ['canvas']:
                            self.position.insert(0, False)
                            self.position.insert(0, 0)
                            self.position.insert(0, 0)
                if self.position[0] == -1:
                    self.position.pop(0)
                    self.brick.screen.draw_image(0, 0, self.menuLocations[self.position[len(self.position) - 4]], transparent=Color.RED)
                self.currentMenu.draw(self.position)
                print(self.position)
                time.sleep(0.3)
            
    def animate(self, state, direction):
        '''
        Animates the transition between the main-menu-pages and the submenu-pages
        Args:
            state (int): The menu-transition to animate
            direction (bool): wether it should play the animation forwards or backwards
        '''
        menus = ['mainProgram',
                 'mainTest',
                 'mainRemote',
                 'mainCompetition',
                 'mainSettings']
        if direction:
            try:
                for i in range(1, 11):
                    self.brick.screen.draw_image(
                        0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent=Color.RED)
                    time.sleep(0.05)
            except Exception as exception:
                self.logger.error(
                    self, "Could not animate menu: ", str(exception))
        else:
            try:
                for i in reversed(range(1, 11)):
                    self.brick.screen.draw_image(
                        0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent=Color.RED)
                    time.sleep(0.05)
            except Exception as exception:
                self.logger.error(
                    self, "Could not animate menu: ", str(exception))

    def runProgramming(self, position):
        index = position[1]
        content = self.profileHelper.getProfileData(self.__config['profileNames'][index])

        self.runList = Menu('progList', self.brick)
        self.runList.setList(content)
        self.runList.setClickAction(self.runEditing)
        self.runList.draw(self.position)

        # sideloop for interactive sub submenu
        while not Button.LEFT in self.brick.buttons.pressed():
            if any(self.brick.buttons.pressed()):
                if Button.UP in self.brick.buttons.pressed() and not self.position[2]:
                    self.position[1] = self.position[1] - 1 if self.position[1] > 0 else self.runList.maxY
                elif Button.DOWN in self.brick.buttons.pressed() and not self.position[2]:
                    self.position[1] = self.position[1] + 1 if self.position[1] < self.runList.maxY else 0
                elif Button.CENTER in self.brick.buttons.pressed():
                    if self.position[1] != len(content) - 1:
                        self.runList.click(self.position)
                    else:
                        content.pop()
                        content.append([7, 100, 10, 0])
                        self.runList.setList(content)
                        self.profileHelper.setProfileData(self.__config['profileNames'][index], content)
                if self.position[0] == -1:
                    self.position.pop(0)
                    self.brick.screen.draw_image(0, 0, self.menuLocations[self.position[len(self.position) - 4]], transparent=Color.RED)
                self.runList.draw(self.position)
                print(self.position)
                time.sleep(0.3)
        
    def runEditing(self, position):
        def formatScreenContent():
            screenContent[0] = 'Type: %s' % self.types[content[index][0]]
            screenContent[1] = 'Speed: %s' % content[index][1]
            screenContent[2] = '%s: %s' % (self.secondParam[content[index][0]], content[index][2]) if self.secondParam[content[index][0]] != 'none' else ''
            screenContent[3] = '%s: %s' % (self.thirdParam[content[index][0]], content[index][3]) if self.thirdParam[content[index][0]] != 'none' else ''

        smallStep = 1
        bigStep = 5
        index = position[1]
        screenContent = ['', '', '', '']
        content = self.profileHelper.getProfileData(self.__config['profileNames'][position[4]])

        formatScreenContent()

        menu = ProgrammingWindow(self.brick, 'Edit Step', 'list', screenContent)
        self.position.insert(0, False)
        self.position.insert(0, 0)
        self.position.insert(0, 0)
        mmax = 3
        menu.open(position)
        while not (Button.LEFT in self.brick.buttons.pressed() and not position[2]):
            if any(self.brick.buttons.pressed()):
                valueType = self.valueTypes[position[1]][content[index][0]] if position[1] != 0 else 'type'
                valueRange = self.valueRanges[valueType]
                if Button.UP in self.brick.buttons.pressed():
                    if self.position[2]:
                        if valueType != 'type':
                            content[index][position[1]] = content[index][position[1]] + smallStep if content[index][position[1]] + smallStep in valueRange else valueRange[0]
                        else:
                            content[index][position[1]] = valueRange[valueRange.index(content[index][position[1]]) - 1 if valueRange.index(content[index][position[1]]) - 1 >= 0 else len(valueRange) - 1]
                    else:
                        self.position[1] = self.position[1] - 1 if self.position[1] > 0 else mmax
                elif Button.DOWN in self.brick.buttons.pressed():
                    if self.position[2]:
                        if valueType != 'type':
                            content[index][position[1]] = content[index][position[1]] - smallStep if content[index][position[1]] - smallStep in valueRange else valueRange[len(valueRange) - 1]
                        else:
                            content[index][position[1]] = valueRange[valueRange.index(content[index][position[1]]) + 1 if valueRange.index(content[index][position[1]]) + 1 < len(valueRange) else 0]
                    else:
                        self.position[1] = self.position[1] + 1 if self.position[1] < mmax else 0
                elif Button.RIGHT in self.brick.buttons.pressed():
                    if self.position[2]:
                        if valueType != 'type':
                            content[index][position[1]] = content[index][position[1]] + bigStep if content[index][position[1]] + bigStep in valueRange else valueRange[0]
                elif Button.LEFT in self.brick.buttons.pressed():
                    if self.position[2]:
                        if valueType != 'type':
                            content[index][position[1]] = content[index][position[1]] - bigStep if content[index][position[1]] - bigStep in valueRange else valueRange[len(valueRange) - 1]
                elif Button.CENTER in self.brick.buttons.pressed():
                    position[2] = not position[2]
                formatScreenContent()
                menu.updateContent(screenContent)
                menu.draw(position=position)
                if not (Button.LEFT in self.brick.buttons.pressed() and not position[2]):
                    time.sleep(0.3)

        self.position.pop(0)
        self.position.pop(0)
        self.position.pop(0)
        self.profileHelper.setProfileData(self.__config['profileNames'][position[4]], content)
        menu.close(position)
        time.sleep(0.3)

        

    def runTesting(self, position):
        index = position[1]
        profileData = self.profileHelper.getProfileData(self.__config['profileNames'][index])
        time.sleep(0.3)
        self.os.robot.execute(profileData)

    def runWebremote(self):
        self.currentMenu.getObjectByName('startButton').setVisibility(False)
        self.currentMenu.getObjectByName('endButton').setVisibility(True)
        self.position[1] += 1
        self.currentMenu.draw(self.position)
        time.sleep(0.3)
        self.os.webremote.run()
        self.currentMenu.getObjectByName('startButton').setVisibility(True)
        self.currentMenu.getObjectByName('endButton').setVisibility(False)
        self.position[2] = False
        self.position[1] -= 1
        self.currentMenu.draw(self.position)
        time.sleep(0.3)

    def runCompetition(self):
        dataArray = []
        self.wireless(False)   # uncomment to not loose connectivity for console-logging and effective development through wifi
        self.currentMenu.getObjectByName('startButton').setVisibility(False)
        self.currentMenu.getObjectByName('runButton').setVisibility(True)
        self.position[0], self.position[1] = 1, 1
        self.currentMenu.draw(self.position)
        for i in self.__config['profileNames']:
            dataArray.append(self.profileHelper.getProfileData(i))
        self.currentMenu.getObjectByName('runButton').setVisibility(False)
        self.currentMenu.getObjectByName('nextButton').setVisibility(True)
        time.sleep(0.3)
        for index in range(0, len(dataArray)):
            self.brick.screen.draw_box(30, 30, 200, 80, fill=True, color=Color.WHITE)
            self.brick.screen.set_font(self.__almostBigFont)
            self.brick.screen.draw_text(74, 36, "Run %s/%s:" % (index, len(dataArray) - 1), background_color=Color.WHITE)
            self.brick.screen.set_font(self.__bigFont)
            self.brick.screen.draw_text(98 - self.__bigFont.text_width(self.__config['profileNames'][index]) / 2, 60, self.__config['profileNames'][index], background_color=Color.WHITE)
            while Button.CENTER not in self.brick.buttons.pressed(): pass
            self.position[0], self.position[1] = 1, 1
            self.currentMenu.draw(self.position)
            time.sleep(0.3)
            self.os.robot.execute(dataArray[index])
            time.sleep(0.3)
            self.position[0], self.position[1] = 1, 0
            self.currentMenu.draw(self.position)

        self.wireless(True)
        self.brick.screen.draw_box(30, 30, 200, 80, fill=True, color=Color.WHITE)
        self.position[0], self.position[1], self.position[2] = 0, 0, False
        self.currentMenu.getObjectByName('startButton').setVisibility(True)
        self.currentMenu.getObjectByName('runButton').setVisibility(False)
        self.currentMenu.getObjectByName('nextButton').setVisibility(False)
        self.currentMenu.draw(self.position)
    
    def wireless(self, enable):
        cmd = 'enable' if not enable else 'disable'
        os.system('connmanctl {} offline'.format(cmd))


