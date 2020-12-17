import _thread, time

from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI.UIObject import UIObject
from UI.tools import Menu, Box


class UIManager(CharlieOSX):
    """
        Basicly a Menu
    """

    def __init__(self, config, settings, brick, logger, settingsPath):
        # general variable setup
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
        self.__settingsPath = settingsPath
        self.brick = brick
        self.logger = logger
        #self.profileHelper = ProfileHelper(self.logger, self.__config)
        self.__sound_lock = _thread.allocate_lock()

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
            self.mainMenu.addObject(UIObject(name, self.brick, Box(0, i, 30, 25), 'img', (0, 0, True), mainPages[i]))

        # Programming Menu
        self.programming = Menu('list', self.brick)
        self.programming.setList(self.__config['profileNames'])
        # self.programming.draw([0, 0, False])

        # Testing Menu
        self.testing = Menu('list', self.brick)
        self.testing.setList(self.__config['profileNames'])

        # Remote-Control Menu
        self.remote = Menu('canvas')

        # Competition-Mode Menu
        self.competition = Menu('canvas')

        # Settings Menu
        self.settingsMenu = Menu('dict')

        # menu Variables
        self.loop = True        
        self.currentMenu = self.mainMenu
        self.position = [0, 0, False]
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
        return "UI Manager"

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

        while self.loop:
            if any(self.brick.buttons.pressed()):
                if Button.UP in self.brick.buttons.pressed():
                    self.position[1] = self.position[1] - 1 if self.position[1] > 0 else self.currentMenu.maxY
                elif Button.DOWN in self.brick.buttons.pressed():
                    self.position[1] = self.position[1] + 1 if self.position[1] < self.currentMenu.maxY else 0
                elif Button.LEFT in self.brick.buttons.pressed() and len(self.position) > 3:
                    # self.position[0] = self.position[0] - 1 if self.position[0] > 0 else self.currentMenu.maxX
                    self.position.pop(0)
                    self.position.pop(0)
                    self.position.pop(0)
                    if len(self.position) == 3:
                        self.animate(self.position[1], False)
                        self.currentMenu = self.mainMenu
                elif Button.RIGHT in self.brick.buttons.pressed():
                    # self.position[0] = self.position[0] + 1 if self.position[0] < self.currentMenu.maxX else 0
                    if len(self.position) == 3:
                        self.animate(self.position[1], True)
                        self.currentMenu = self.subMenus[self.position[1]]
                    self.position.insert(0, False)
                    self.position.insert(0, 0)
                    self.position.insert(0, 0)
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
            except Exception as exception:
                self.logger.error(
                    self, "Could not animate menu: ", str(exception))
        else:
            try:
                for i in reversed(range(1, 11)):
                    self.brick.screen.draw_image(
                        0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent=Color.RED)
            except Exception as exception:
                self.logger.error(
                    self, "Could not animate menu: ", str(exception))