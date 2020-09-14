from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI import UIObject

from UI import UIIcon


class UIManager:
    def __init__(self, config, settings, brick, logger, settingsPath):

        # needed Stuff
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__settingsPath = settingsPath
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
        self.brick = brick
        self.logger = logger
        self.profileHelper = ProfileHelper(self.logger, self.__config)
        self.__sound_lock = _thread.allocate_lock()
        self.logger.info(self, 'UI initialized')

        # UI Stuff

        self.UIObjects = []
        self.UIIcons = [
            "./icons/1.png",
            "./icons/2.png",
            "./icons/3.png",
            "./icons/4.png",
            "./icons/5.png",
        ]

        for i in range(len(self.UIIcons)):
            self.addObject(UIIcon(self.brick, self.logger, i, self.UIIcons[i]))

    def addObject(self, UIObject):
        self.UIObjects.append(UIObject)

    def draw(self):
        for UIObject in self.UIObjects:
            UIObject.draw()
