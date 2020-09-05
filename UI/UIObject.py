from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from rect.py import Rectangle

class UIObject:
    def __init__(self,brick,logger,rect):

        # Needed stuf

        self.brick = brick
        self.logger = logger


        # UI Stuff
        self.rect = rect

    def draw(self):
        self.brick.screen.draw_box(self.x, self.y, self.width, self.height, r=3, fill=True, color=Color.RED)