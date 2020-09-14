from UI.UIObject import UIObject
from UI.rect import Box


class UIIcon(UIObject):
    def __init__(self, brick, logger, y, icon):
        UIObject.__init__(brick, logger, Rectangle(0, y, 10, 10))
        self.icon = icon

        self.container = Rectangle(
            self.bounds.width, 0, self.brick.screen.width, self.brick.screen.height)

    def drawIcon(self):
        self.brick.screen.draw_box(self.bounds.x, self.bounds.y, self.bounds.width, self.bounds.height, r=0,
                                   fill=true, color=Color.RED)

    def drawContainer(self):
        # Draw Border
        pass
