from UI.uiObject import UIObject


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

class Box():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getMidHeight(self):
        return self.y + self.height / 2
    
    def getMidWidth(self):
        return self.x + self.width / 2

    def contains(self, other):
        return ((self.x > other.x and self.x < (other.x+other.width)) and (self.y > other.y and self.y < (other.y+other.height)))
