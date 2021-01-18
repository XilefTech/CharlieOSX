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
        # testSubmenu = Menu('normal')
        # testSubmenu.addObject(UIObject('testObject1', self.brick, Box(0, 85, 20, 20), 'img', (0, 0), 'assets/graphics/menus/settingsMainMenu.png'))
        # testSubmenu.addObject(UIObject('testObject2', self.brick, Box(0, 5, 20, 20), 'img', (0, 0), 'assets/graphics/menus/programmingMainMenu.png'))
        # testSubmenu.addObject(UIObject('testObject3', self.brick, Box(40, 5, 20, 20), 'img', (0, 0), 'assets/graphics/menus/programmingMainMenu.png'))
        # print(testSubmenu.rasterize())

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
                    else:
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
        menu = ProgrammingWindow(self.brick, self.__config['profileNames'][index], 'list', content)
        menu.open()
        #do stuff
        time.sleep(5)
        menu.close(position)

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


