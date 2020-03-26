import random

MAXTILE = 15

class Tile(object):
    def __init__(self):
        self.value = random.choice([2,2,4])
        self.image_index = 0
        self.scale = 1  # Relevant for scaling new tiles during transitions
        self.speed = (0,0) # Only relevant for transitions
        self.set_display()
    
    def __str__(self):
        return str(self.value)
    
    def isEmpty(self):
        return False
    
    def __eq__(self, other):
        return self.value == other.value
    
    def set_display(self):
        for i in range(MAXTILE):
            if self.value == 2**(i+1):
                self.image_index = i
        

class EmptyTile(Tile):
    def __init__(self):
        self.value = 0
        self.image_index = 0
        self.colour = "grey"
        self.speed = (0,0)
    def __str__(self):
        return " "
    def isEmpty(self):
        return True  

