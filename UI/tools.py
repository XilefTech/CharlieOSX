from UI.UIObject import UIObject
from copy import copy


class Menu():
    '''This Method defines a Menu for a given Page'''

    def __init__(self, type):
        self.type = type
        self.objects = []
        self.raster = self.rasterize()

    def addObject(self, object: UIObject):
        self.objects.append(object)
        self.raster = self.rasterize()

    def draw(self):
        if self.type != 'sidebar':
            for i in self.objects:
                i.draw()
        else:
            self.objects[0].draw()

    def rasterize(self):
        array = []
        todo = copy(self.objects)
        while todo != []:
            x = todo.pop(0)
            array.append([])
            array[len(array) - 1].append(x)
            for i in todo:
                if i.bounds.getMidHeight() in range(x.bounds.y, x.bounds.y + x.bounds.height + 1):
                    array[len(array) - 1].append(i)
                    todo.pop(0)
        
        return array

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
