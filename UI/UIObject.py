from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

# from UI.tools import Box


class UIObject:
    def __init__(self, name: str, brick: EV3Brick, bounds: Box, contentType, content, padding=(0, 0, False), font=Font(family='arial', size=11)):
        # self.logger = logger
        self.name = name
        self.brick = brick
        self.bounds = bounds
        self.padding = padding
        self.contentType = contentType
        self.content = content
        self.font = font
        self.radius = 0
        self.selected = False

    def getName(self):
        return self.name

    def update(self):
        pass

    def draw(self):
        if self.padding[2]:
            x = self.padding[0]
            y = self.padding[1]
        else:
            x = self.bounds.x + self.padding[0]
            y = self.bounds.y + self.padding[1]

        if self.contentType == 'img':
            if self.selected:
                self.radius = 5
            else:
                self.radius = 0
            self.brick.screen.draw_image(x, y, self.content, transparent=Color.RED)
        elif self.contentType == 'textBox':
            self.brick.screen.set_font(self.font)
            self.brick.screen.draw_text(self.bounds.x + 1, self.bounds.y + 1, self.content)
            self.brick.screen.draw_box(x, y, x + self.bounds.width, y + self.bounds.height, r=2, fill=False, color=Color.BLACK)

    def setClickAction(self, action: Function):
        self.clickAction = action