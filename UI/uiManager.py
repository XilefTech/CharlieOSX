import _thread

from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI.UIObject import UIObject
#from UI import UIIcon
from UI.tools import Menu, Box


class UIManager:
    """
        Basicly a Menu
    """

    def __init__(self, config, settings, brick, logger, settingsPath):
        # needed Stuff
        #logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
        self.__settingsPath = settingsPath
        self.brick = brick
        self.logger = logger
        #self.profileHelper = ProfileHelper(self.logger, self.__config)
        self.__sound_lock = _thread.allocate_lock()
        #self.logger.info(self, 'UI initialized')

        self.loop = True

        self.currentObject = 0

        # UI Stuff
        self.UIObjects = []
        self.UIIcons = [
            "UI/icons/Programming.png",
            "UI/icons/Testing.png",
            "UI/icons/Remote-Control.png",
            "UI/icons/Competition-Mode.png",
            "UI/icons/Settings.png",
        ]

        for i in range(len(self.UIIcons)):
            name = self.UIIcons[i].split('/')[2].split('.')[0]
            self.addObject(UIObject(name, 'img', self.brick, Box(
                0, i, 30, 25), (2, 1), self.UIIcons[i]))

        self.UIObjects[self.currentObject].selected = True

        self.draw()

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

    def addObject(self, UIObject):
        self.UIObjects.append(UIObject)

    def draw(self):
        for UIObject in self.UIObjects:
            UIObject.draw()

    def mainLoop(self):
        while self.loop:
            self.update()

    def update(self):
        # for UIObject in self.UIObjects:
        #     UIObject.update()

        if self.brick.buttons.pressed():
            self.brick.screen.clear()
            self.checkButtons()
            self.draw()

    def checkButtons(self):
        # print("Current Icon: " + str(self.currentObject))

        if Button.DOWN in self.brick.buttons.pressed():
            if not self.currentObject == len(self.UIObjects) - 1:
                self.changeCurrentObj(1)
        elif Button.UP in self.brick.buttons.pressed():
            if not self.currentObject == 0:
                self.changeCurrentObj(-1)

    def changeCurrentObj(self, num):
        self.UIObjects[self.currentObject].selected = False
        self.currentObject += num
        self.UIObjects[self.currentObject].selected = True
