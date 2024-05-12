from globals import *

class Unit:
    def __init__(self, name, id, civ, coordinates):
        self.name = name
        self.civ = civ
        self.id = id
        self.health = 4
        self.attack = 2
        self.defense = 1
        self.symbol = 'W'
        self.coordinates = coordinates