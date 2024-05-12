from collections import defaultdict
from city import *
from unit import *

class Civ:
    def __init__(self, name, traits=[]):
        self.name = name
        self.cities = defaultdict(City)
        self.units = defaultdict(Unit)
        self.traits = traits
