from UI.box import Box
from UI.UIObject import UIObject


class Menu():
    '''This Method defines a Menu for a given Page'''

    def __init__(self, type):
        self.type = type
        self.objects = []

    def addObject(self, object: UIObject):
        self.objects.append(object)

    def draw(self):
        for i in self.objects:
            i.draw()

    def rasterize(self):
        return 'WIP'