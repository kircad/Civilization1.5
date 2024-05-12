import random 
import curses

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]

    def generate_terrain(self, mode):
        if mode == "random":
            terrain_types = ['P', 'M', 'R', 'F']  # 'P' for plains, 'M' for mountains, 'R' for rivers, 'F' for forests
            
            for y in range(self.height):
                for x in range(self.width):
                    # Assign random terrain type to each cell
                    terrain_type = random.choice(terrain_types)
                    self.grid[y][x] = terrain_type
        elif mode == "preset":
            terrain_layout = [
                ['F', 'F', 'F', 'M', 'M', 'M', 'P', 'P', 'P', 'P'],
                ['F', 'F', 'F', 'F', 'M', 'M', 'M', 'P', 'P', 'P'],
                ['F', 'F', 'F', 'F', 'F', 'M', 'M', 'M', 'P', 'P'],
                ['F', 'F', 'F', 'F', 'F', 'M', 'M', 'M', 'R', 'R'],
                ['F', 'F', 'F', 'F', 'F', 'M', 'M', 'M', 'R', 'R'],
                ['F', 'F', 'F', 'F', 'M', 'M', 'M', 'P', 'R', 'P'],
                ['F', 'F', 'F', 'M', 'M', 'M', 'P', 'P', 'P', 'P'],
                ['F', 'F', 'F', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['F', 'F', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['F', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
            ]

            for y in range(self.height):
                for x in range(self.width):
                    self.grid[y][x] = terrain_layout[y][x]

    def print_map_opponent(self):
        out = ""
        for row in self.grid:
            out += ' | '.join(row) + '\n'
        return out
    
    def print_map_player(self, stdscr, units, cities):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Dark green (F)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Grey (M)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Blue (R)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # Yellow (P)

        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == 'F':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(1))
                elif char == 'M':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(2))
                elif char == 'R':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(3))
                elif char == 'P':
                    stdscr.addstr(y+1, x, ' ', curses.color_pair(4))
        for unit in units:
            color_pair = stdscr.inch(unit.coordinates[1]+1, unit.coordinates[0]) & curses.A_COLOR
            stdscr.addstr(unit.coordinates[1]+1, unit.coordinates[0], unit.symbol, color_pair)
        for city in cities:
            pass