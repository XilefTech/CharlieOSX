class Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, other):
        return ((self.x > othder.x and self.x < (other.x+other.width)) and (self.y > othder.y and self.y < (other.y+other.height)))
