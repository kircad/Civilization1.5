from collections import defaultdict
from city import *
from unit import *

class Civ:
    def __init__(self, name, traits=[]):
        self.name = name
        self.traits = traits
