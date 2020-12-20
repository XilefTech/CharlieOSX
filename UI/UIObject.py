from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

# from UI.tools import Box


class UIObject:
    def __init__(self, name: str, brick: EV3Brick, bounds: Box, contentType, padding, content):
        # self.logger = logger
        self.name = name
        self.brick = brick
        self.bounds = bounds
        self.padding = padding
        self.contentType = contentType
        self.content = content
        self.radius = 0
        self.selected = False

        self.bounds.y *= self.bounds.height + self.padding[1]

    def update(self):
        pass

    def draw(self):
        if self.padding[2]:
            x = self.padding[0]
            y = self.padding[1]
        else:
            x = self.bounds.x + self.padding[0]
            y = self.bounds.x + self.padding[1]
            
        if self.contentType == 'img':
            if self.selected:
                self.radius = 5
            else:
                self.radius = 0

            self.brick.screen.draw_image(x, y, self.content, transparent=Color.RED)
            # self.brick.screen.draw_box(
            #     self.bounds.x, self.bounds.y, self.bounds.width + self.padding[0], self.bounds.height+self.padding[1], r=self.radius, fill=False, color=Color.BLACK)
            


    def drawInfoBox(self):
        self.brick.screen.draw_box(
            self.bounds.width + self.padding[0] + 3, 0, self.brick.screen.width-1, self.brick.screen.height-1, r=5, fill=False, color=Color.BLACK)

        self.brick.screen.set_font(Font(size=14))

        self.brick.screen.draw_text(
            self.bounds.width + 5, 0, self.name, text_color=Color.BLACK, background_color=None)
