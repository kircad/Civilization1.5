import random 
import curses
import city
import unit
from collections import defaultdict

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.features = defaultdict(dict) 
        # cities, resources, and units -- ex. features[0][0] would give {'resources': [], 'units': [], 'cities': []} for that tile

    def generate_terrain(self, mode):
        if mode == "random":
            terrain_types = ['P', 'M', 'R', 'F']  # 'P' for plains, 'M' for mountains, 'R' for rivers, 'F' for forests
            for y in range(self.height):
                for x in range(self.width):
                    terrain_type = random.choice(terrain_types)
                    self.grid[y][x] = terrain_type

        elif mode == "preset":
            terrain_layout = [ #TODO MAKE BIGGER
                ['F', 'F', 'F', 'F', 'F', 'F', 'P', 'P', 'P', 'P'],
                ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'P', 'P', 'P'],
                ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'P', 'P'],
                ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'R', 'R'],
                ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'R', 'R'],
                ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'P', 'R', 'P'],
                ['F', 'F', 'F', 'F', 'F', 'F', 'P', 'P', 'P', 'P'],
                ['F', 'F', 'F', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['F', 'F', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['F', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
            ]


            for y in range(self.height):
                for x in range(self.width):
                    self.grid[y][x] = terrain_layout[y][x]

    def print_map_opponent(self): #TODO FIND BETTER WAY TO PASS MAP INTO LLM (JSON? FEATURE-BASED?)
        out = ""
        count = 0
        for row in self.grid:
            print("ROW " + str(count) + ":")
            out += ' | '.join(row) + '\n'
            count += 1
        return out
    
    def print_map_player(self, stdscr, units, cities): #TODO add knowntiles mechanic TODO FIX COLORS NOT SHOWING UP ACCORDING TO UNIT CIV
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Dark green (F) (PLAYER UNITS)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Blue (R)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # Yellow (P)
        
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Dark green (F) (PLAYER UNITS)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)   # Blue (R)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Yellow (P)

        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == 'F':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(1))
                elif char == 'R':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(2))
                elif char == 'P':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(3))
        for coords, feature in self.features.items(): #resources, landmarks, etc.
                color_pair = stdscr.inch(coords[1]+1, coords[0]) & curses.A_COLOR
                stdscr.addstr(coords[1]+1, coords[0], feature.symbol, color_pair)
        
        for unit in units:
            y = unit.coordinates[1]+1
            x = unit.coordinates[0]
            char = self.grid[y-1][x]
            if unit.civ == "player":
                if char == 'F':
                    stdscr.addstr(y, x, unit.symbol, curses.color_pair(1))
                elif char == 'R':
                    stdscr.addstr(y, x, unit.symbol, curses.color_pair(2))
                elif char == 'P':
                    stdscr.addstr(y, x, unit.symbol, curses.color_pair(3))
            else:
                if char == 'F':
                    stdscr.addstr(y, x, unit.symbol, curses.color_pair(4))
                elif char == 'R':
                    stdscr.addstr(y, x, unit.symbol, curses.color_pair(5))
                elif char == 'P':
                    stdscr.addstr(y, x, unit.symbol, curses.color_pair(6))
        for city in cities:
            pass