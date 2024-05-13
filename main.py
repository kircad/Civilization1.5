from map import *
from globals import *
from civ import *
from unit import *
from APIcalls import *
from time import sleep
import json
import google.generativeai as genai
import google.api_core
import curses
import sys

debug_file = open("debug.log", "a")
log_file = open("output.log", "a")
sys.stdout = log_file
sys.stderr = debug_file

responses = []
context = [
{"role": "system", "content": init_prompt }
]

def main(stdscr):
    # Initializing game
    cities = []
    units = []
    player_civ = Civ("player")
    ai_civ = Civ("opponent")
    terrainMap = Map(10, 10)
    terrainMap.generate_terrain("preset")
    units.append(Unit('warrior', 0, 'player', [0, 0]))
    units.append(Unit('warrior', 1, 'opponent', [9, 9]))

    #Initializing model
    GOOGLE_API_KEY='AIzaSyD3CTe6s7RIWeQKVfrUaaGVEkteYOa7eKU'
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest") #TODO TRY 1.0?
    currTurn = 1

    curses.curs_set(0)  # Hide cursor
    curses.start_color()  # Enable color
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "Welcome to Civilization!", curses.A_BOLD)
    stdscr.addstr(2, 0, "Press any key to continue...", curses.A_NORMAL)
    stdscr.getch()
    while currTurn < maxTurns:
        stdscr.clear()
        stdscr.addstr("YEAR " + str(currTurn) + "\n")
        terrainMap.print_map_player(stdscr, units, cities)
        stdscr.refresh()
        for unit in units:
            if (unit.civ == "player"):
                key = stdscr.getch()
                if (key == ord('w')): # TODO BOUND CHECKING
                    unit.coordinates[1] -= 1
                if (key == ord('s')):
                    unit.coordinates[1] += 1
                if (key == ord('d')):
                    unit.coordinates[0] += 1
                if (key == ord('a')):
                    unit.coordinates[0] -= 1
                else:
                    continue #TODO INVALID INPUT THING
        for city in cities:
            pass
        request = make_request(context, terrainMap, units, cities, currTurn)
        out = get_response(model, request)
        if out is not None:
           json_string = out.strip("```")[4:]
           parsed_dict = json.loads(json_string)
           print(json_string)
           responses.append(parsed_dict)
           for unit in parsed_dict['UnitMoves']:
                move = unit['MOVE']
                unit = units[unit['UNIT_ID']]
                if (move == ('w')): # TODO BOUND CHECKING
                    unit.coordinates[1] -= 1
                if (move == ('s')):
                    unit.coordinates[1] += 1
                if (move == ('d')):
                    unit.coordinates[0] += 1
                if (move == ('a')):
                    unit.coordinates[0] -= 1
                else:
                    continue #TODO INVALID INPUT THING
        else:
           print("Gemini Error!")
        currTurn += 1



if __name__ == "__main__":
    curses.wrapper(main)