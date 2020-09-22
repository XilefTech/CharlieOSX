from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

#from UI.tools import Box


class UIObject:
    def __init__(self, name: str, brick, bounds: Box, contentType, contentPosition: tuple, content):
        #self.logger = logger
        self.name = name
        self.brick = brick
        self.bounds = bounds
        self.contentType = contentType
        self.contentPosition = contentPosition
        self.content = content

    def draw(self):
        if self.contentType == 'img':
            self.brick.screen.draw_image(self.contentPosition[0], self.contentPosition[1], self.content, transparent = Color.RED)
