from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI.rect import Box


class UIObject:
    def __init__(self, brick, logger, bounds: Box):

        # Needed stuf

        self.brick = brick
        self.logger = logger

        # UI Stuff
        self.bounds = bounds

    def draw(self):
        pass
