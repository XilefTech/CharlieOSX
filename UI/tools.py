from UI.UIObject import UIObject
from copy import copy
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color
from pybricks.media.ev3dev import Font


class Menu():
    '''This Method defines a Menu for a given Page'''

    def __init__(self, type, brick=None):
        self.brick = brick
        self.type = type
        self.objects, self.llist = [], []
        self.maxX = 0
        self.maxY = 0
        self.font = Font(family='arial', size=13)
        self.raster = self.rasterize()

    def getType(self):
        return self.type

    def addObject(self, object: UIObject):
        self.objects.append(object)
        self.raster = self.rasterize()

    def setList(self, arrList: Array):
        self.llist = arrList
        self.maxX = 0
        self.maxY = len(self.llist) - 1

    def setDict(self, ddict: dict):
        self.dict = ddict
        self.maxX = 0
        self.maxY = len(self.dict['options']) - 1

    def setClickAction(self, clickAction):
        if self.type == 'list':
            self.clickAction = clickAction
        else:
            raise AttributeError

    def getObjectByName(self, name):
        for i in self.objects:
            if i.getName() == name:
                return i

    def getObjectByPostion(self, position):
        return self.raster[position[0]][position[1]]

    def updateSettings(self, settings):
        self.settings = settings

    def draw(self, selector):
        # Sidebar-Menu
        if self.type == 'sidebar':
            self.objects[selector[1]].draw()
        # list-Menu
        elif self.type == 'list':
            self.brick.screen.set_font(self.font)

            if selector[1] in range(0, 3):
                offset = 0
            elif selector[1] in range(len(self.llist) - 2, len(self.llist)):
                offset = len(self.llist) - 5
            else:
                offset = selector[1] - 2

            self.drawScrollBar(len(self.llist), selector[1])
            for i in range(5):
                if offset + i == selector[1]:
                    if selector[2]:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r=3, fill=True, color=Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, self.llist[i + offset])
                    else:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r=3, fill=True, color=Color.WHITE)
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r=3, fill=False, color=Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, self.llist[i + offset])
                else:
                    self.brick.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill=True, color=Color.WHITE)
                    self.brick.screen.draw_text(29, 30 + i * 20, self.llist[i + offset])
        # dict-Menu
        elif self.type == 'dict':
            self.brick.screen.set_font(self.font)

            if selector[1] in range(0, 3):
                offset = 0
            elif selector[1] in range(len(self.dict['options']) - 2, len(self.dict['options'])):
                offset = len(self.dict['options']) - 5
            else:
                offset = selector[1] - 2

            self.drawScrollBar(len(self.dict['options']), selector[1])
            for i in range(5):
                if offset + i == selector[1]:
                    if selector[2]:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r=3, fill=True, color=Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, "%s: %s" % list(self.dict['options'].items())[i + offset], text_color=Color.WHITE)
                    else:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r=3, fill=True, color=Color.WHITE)
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r=3, fill=False, color=Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, "%s: %s" % list(self.dict['options'].items())[i + offset])
                else:
                    self.brick.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill=True, color=Color.WHITE)
                    self.brick.screen.draw_text(29, 30 + i * 20, "%s: %s" % list(self.dict['options'].items())[i + offset])

            if selector[2]:
                keys = list(self.dict['options'].keys())
                index = selector[1]
                print(keys[index])
                if self.dict['types'][keys[index]] == 'bool':
                    self.maxX = 1
                elif self.dict['types'][keys[index]] == 'int':
                    self.maxX = abs(self.dict['values']['min'][keys[index]]) + abs(self.dict['values']['max'][keys[index]])
            else:
                self.maxX = 0
        # something else
        else:
            for i in self.objects:
                if not i.getVisibility():
                    i.draw() if i != self.raster[selector[0]][selector[1]] else i.draw(selected=True)
            for i in self.objects:
                if i.getVisibility():
                    i.draw() if i != self.raster[selector[0]][selector[1]] else i.draw(selected=True)

    def drawScrollBar(self, totalLength, pos):
        '''
        Draws a scroll bar on the side of the screen
        Args:
            totalLength (int): The total amount of positions for the scroll bar to be in
            pos (int): the current position of the scroll bar
        '''
        self.brick.screen.draw_box(171, 25, 177, 127, r=2, fill=False, color=Color.BLACK)
        self.brick.screen.draw_box(172, 26, 176, 126, r=2, fill=True, color=Color.WHITE)
        self.brick.screen.draw_box(173, 27 + 102 / totalLength * pos, 175, 23 + 102 / totalLength * (pos + 1), r=1, fill=True, color=Color.BLACK)

    def rasterize(self):
        array = []
        todo = copy(self.objects)
        # group the UIObjects in their y ranges
        while todo != []:
            x = todo.pop(0)
            array.append([])
            array[len(array) - 1].append(x)
            for i in todo:
                if i.bounds.getMidHeight() in range(x.bounds.y, x.bounds.y + x.bounds.height + 1):
                    array[len(array) - 1].append(i)
                    todo.pop(0)
        # sort objects in the subarrays by x value
        for i in array:
            i.sort(key=lambda x: x.bounds.x, reverse=False)

        # get maximum x and y values
        self.maxY = len(array) - 1
        for i in array:
            if len(i) - 1 > self.maxX:
                self.maxX = len(i) - 1
        return array
   
    def click(self, position):
        if self.type == 'list':
            self.clickAction(position)
        else:
            pass

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
