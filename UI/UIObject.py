from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

# from UI.tools import Box


class UIObject:
    def __init__(self, name: str, brick, bounds: Box, contentType, content):
        # self.logger = logger
        self.name = name
        self.brick = brick
        self.bounds = bounds
        self.contentType = contentType
        self.content = content
        self.radius = 0
        self.selected = False

        self.bounds.y *= self.bounds.height

    def update(self):
        if self.selected:
            self.radius = 10
        else:
            self.radius = 0

    def draw(self):
        if self.contentType == 'img':
            self.brick.screen.draw_image(
                self.bounds.x + 5, self.bounds.y + 4, self.content, transparent=Color.RED)
            self.brick.screen.draw_box(
                self.bounds.x, self.bounds.y, self.bounds.width+1, self.bounds.height, r=self.radius, fill=False, color=Color.BLACK)
            if self.selected:
                self.drawInfoBox()

    def drawInfoBox(self):

        self.brick.screen.draw_box(
            self.bounds.width + 2, 0, self.brick.screen.width-1, self.brick.screen.height-1, r=5, fill=False, color=Color.BLACK)

        self.brick.screen.set_font(Font(size=14))

        self.brick.screen.draw_text(
            self.bounds.width + 5, 0, self.name, text_color=Color.BLACK, background_color=None)

    def clear(self):
        self.brick.screen.draw_box(
            self.bounds.x, self.bounds.y, self.bounds.width+1, self.bounds.height, r=0, fill=True, color=Color.WHITE)

        self.brick.screen.draw_box(
            self.bounds.width, 0, self.brick.screen.width, self.brick.screen.height-1, r=0, fill=True, color=Color.WHITE)
